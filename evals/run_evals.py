"""Run the Graveyard Killer evals headless, one fresh `claude -p` session each.

Usage:
    python3 evals/run_evals.py <app> <capture|worker|drive> <id> [<id> ...]
    python3 evals/run_evals.py <app> resume <run> "<reply>"
    python3 evals/run_evals.py <app> prompt <run> "<prompt>"

<app> is `notion` or `google-drive`. `resume` answers a finished run in its own
session. `prompt` runs any message against the test Library, for example to seed it.

Each run writes <temp folder>/gk-evals/<app>/<run>/: out.jsonl (the session's stream),
result.txt (its final message), session.txt and expectations.md (what to grade).
evals/local.json, which is not committed, holds each app's test Library link and
the placeholders' values; see evals/README.md.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
import tempfile
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
# Outside the repo, so the eval sessions load none of its CLAUDE.md or AGENTS.md.
RUNS = pathlib.Path(tempfile.gettempdir()) / "gk-evals"

APPS: dict[str, dict[str, Any]] = {
    "notion": {"name": "Notion", "tools": ["mcp__claude_ai_Notion"]},
    "google-drive": {
        "name": "Google Drive",
        "tools": ["mcp__claude_ai_Google_Drive", "mcp__claude_ai_Google_Sheets"],
    },
}
NO_MEMORY = {("capture", 12)}
SETTINGS = json.dumps(
    {"claudeMdExcludes": [str(pathlib.Path.home() / ".claude" / "CLAUDE.md"), str(pathlib.Path.home() / ".claude" / "projects") + "/**"]}
)
# Posts are untrusted input, so the sessions may run the skill's own scripts only, not any python3.
SCRIPTS = REPO / "plugin" / "skills" / "graveyard-killer" / "scripts"
ALLOWED = ["Skill", "ToolSearch", "Read", "Glob", "Grep", "WebFetch", "Bash(sleep:*)", "Bash(ls:*)",
           *(f"Bash(python3 {path}:*)" for name in ("link.py", "post.py", "graveyard.py")
             for path in (f"scripts/{name}", str(SCRIPTS / name)))]
# ~/.claude holds the user's own CLAUDE.md, with the pointer to their real Library. claudeMdExcludes keeps
# it out of the context, but an agent that finds no pointer will search for one, so it must not read there.
DISALLOWED = ["mcp__claude_ai_Gmail", "mcp__claude_ai_Google_Calendar", "PushNotification", "Write", "Edit",
              f"Read(/{pathlib.Path.home()}/.claude/**)"]  # A Read rule covers Grep and Glob too.


def load_local() -> dict[str, Any]:
    path = HERE / "local.json"
    if not path.exists():
        sys.exit(f"Missing {path}: see evals/README.md")
    data: dict[str, Any] = json.loads(path.read_text())
    return data


def fill(text: str, app: str, placeholders: dict[str, str]) -> str:
    text = text.replace("{{LIBRARY_APP}}", str(APPS[app]["name"]))
    for key, value in placeholders.items():
        text = text.replace(key, value)
    return text


def command(app: str, prompt: str) -> list[str]:
    allowed = [*ALLOWED, *APPS[app]["tools"]]
    disallowed = [*DISALLOWED, *(t for other, spec in APPS.items() if other != app for t in spec["tools"])]
    return ["claude", "-p", prompt, "--plugin-dir", str(REPO / "plugin"), "--settings", SETTINGS,
            "--output-format", "stream-json", "--verbose",
            "--allowedTools", *allowed, "--disallowedTools", *disallowed]


def run(folder: pathlib.Path, cmd: list[str], resume: bool = False) -> None:
    """Run one session. A resumed session adds to the run's stream; a new run starts it again."""
    cwd = folder / "cwd"
    with open(folder / "out.jsonl", "a" if resume else "w", encoding="utf-8") as out:
        try:
            subprocess.run(cmd, cwd=cwd, stdout=out, stderr=subprocess.STDOUT, timeout=3600)
        except subprocess.TimeoutExpired:
            print(f"=== {folder.name}: timed out after an hour", flush=True)
            return
    result, session = "", ""
    for line in (folder / "out.jsonl").read_text(encoding="utf-8").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        session = event.get("session_id", session)
        if event.get("type") == "result":
            result = event.get("result", "")
    (folder / "result.txt").write_text(result, encoding="utf-8")
    (folder / "session.txt").write_text(session, encoding="utf-8")
    print(f"=== {folder.name} (session {session})\n{result}\n", flush=True)


def prepare(app: str, name: str, library: str, memory: bool) -> pathlib.Path:
    folder = RUNS / app / name
    cwd = folder / "cwd"
    cwd.mkdir(parents=True, exist_ok=True)
    pointer = cwd / "CLAUDE.md"
    if memory:
        pointer.write_text(f"Graveyard Killer Library: {library}\n", encoding="utf-8")
    else:
        pointer.unlink(missing_ok=True)
    return folder


def main() -> None:
    if len(sys.argv) < 4 or sys.argv[1] not in APPS or (sys.argv[2] in ("resume", "prompt") and len(sys.argv) != 5):
        sys.exit(__doc__)
    app, kind = sys.argv[1], sys.argv[2]
    if kind == "drive" and app != "google-drive":
        sys.exit("drive.json runs against the Google Drive test Library only.")
    local = load_local()
    library: str = local["libraries"][app]
    placeholders: dict[str, str] = local.get("placeholders", {})

    if kind == "resume":
        folder = RUNS / app / sys.argv[3]
        session = (folder / "session.txt").read_text(encoding="utf-8").strip()
        run(folder, [*command(app, sys.argv[4]), "--resume", session], resume=True)
        return
    if kind == "prompt":
        folder = prepare(app, sys.argv[3], library, memory=True)
        run(folder, command(app, fill(sys.argv[4], app, placeholders)))
        return

    evals = {e["id"]: e for e in json.loads((HERE / f"{kind}.json").read_text(encoding="utf-8"))["evals"]}
    for eval_id in map(int, sys.argv[3:]):
        spec = evals[eval_id]
        folder = prepare(app, f"{kind}-{eval_id}", library, memory=(kind, eval_id) not in NO_MEMORY)
        lines = [f"# {kind} {eval_id} on {APPS[app]['name']}", "", fill(spec["expected_output"], app, placeholders), ""]
        lines += [f"- {fill(x, app, placeholders)}" for x in spec["expectations"]]
        (folder / "expectations.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        run(folder, command(app, fill(spec["prompt"], app, placeholders)))


if __name__ == "__main__":
    main()
