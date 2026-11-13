"""Read and write an Obsidian Library: one Markdown note per Entry, in a vault folder.

    obsidian.py init    <library>                       create the folders the Settings name
    obsidian.py query   <library> [filters] [--fields a,b] [--count]
    obsidian.py find    <library> --link <url> [--id <id>]
    obsidian.py search  <library> <word> [<word> ...] [--fields a,b]
    obsidian.py tags    <library>                       every Tag in use, with its count
    obsidian.py create  <library>                       JSON on stdin: one Entry or a list
    obsidian.py update  <library> <note>                JSON on stdin: the changes
    obsidian.py shared  <library>                       the shared saves waiting in "Share here"
    obsidian.py shared-done <library> <file> [...]      move shared saves to "Already read"
    obsidian.py remove  <library> <note>                move a duplicate to the vault's .trash

find, search, create and update also give each note's obsidian:// link, to show the user.

Filters for query: --where FIELD=VALUE, --not FIELD=VALUE, --since FIELD=YYYY-MM-DD,
--empty FIELD. Each one may repeat; all of them must hold.

<library> is the Library link from the pointer line: the Library folder, its Settings.md,
or a file:// link to either. Field names are the Library's own names, as the Settings
map them. Every result is one JSON object on stdout. Standard library only, no network.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote, unquote, urlparse

SETTINGS = "Settings.md"
FOLDER_KEYS = ("Entries", "Share here", "Already read")
TAGS_KEY = "tags"
COVER_KEY = "cover"
COVERS_FOLDER = "_covers"
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PLAIN_KEY = re.compile(r"^[^\s:#\"'{}\[\],&*!|>%@`-][^:#{}\[\],]*$")
# CommonMark lets a backslash escape any ASCII punctuation. These are the marks that
# would turn a creator's text into Obsidian tags, links, math, embeds or formatting.
ESCAPED = set("\\`*_[]#$<%~=|")


class LibraryError(Exception):
    pass


# ---------------------------------------------------------------- the Library


def library_folder(link: str) -> Path:
    if link.startswith("file://"):
        link = unquote(urlparse(link).path)
    path = Path(link).expanduser()
    if path.name == SETTINGS or path.suffix == ".md":
        path = path.parent
    if not (path / SETTINGS).is_file():
        raise LibraryError(f"no {SETTINGS} in {path}: this is not an Obsidian Library")
    return path


def settings_table(text: str, heading: str) -> list[list[str]]:
    """The body rows of the first table under '## <heading>'."""
    rows: list[list[str]] = []
    inside = False
    for line in text.splitlines():
        if line.startswith("## "):
            if inside:
                break
            inside = line[3:].strip().lower() == heading.lower()
            continue
        if inside and line.strip().startswith("|"):
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            rows.append(cells)
    return [row for row in rows[1:] if not all(set(cell) <= set("-: ") for cell in row)]


def folders(library: Path) -> dict[str, Path]:
    rows = settings_table((library / SETTINGS).read_text(encoding="utf-8"), "Folders")
    names = {row[0]: row[1] for row in rows if len(row) >= 2 and row[1]}
    missing = [key for key in FOLDER_KEYS if key not in names]
    if missing:
        raise LibraryError(f"the Settings' Folders section lacks {', '.join(missing)}")
    # A name may also be an absolute path, such as a "Share here" folder outside the vault
    # that the phone can write to.
    return {key: (Path(names[key]).expanduser() if names[key].startswith(("/", "~")) else library / names[key])
            for key in FOLDER_KEYS}


def shown(library: Path, path: Path) -> str:
    """A path to show and to pass back: relative to the Library when inside it."""
    try:
        return str(path.relative_to(library))
    except ValueError:
        return str(path)


def vault_root(library: Path) -> Path:
    for folder in (library, *library.parents):
        if (folder / ".obsidian").is_dir():
            return folder
    return library


# ---------------------------------------------------------------- frontmatter


def split_note(text: str) -> tuple[list[str], str]:
    """Frontmatter lines (without the --- fences) and the body."""
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[1:i], "\n".join(lines[i + 1:])
    return [], text


def unquote_key(key: str) -> str:
    key = key.strip()
    if len(key) >= 2 and key[0] == key[-1] and key[0] in "\"'":
        return json.loads(key) if key[0] == '"' else key[1:-1].replace("''", "'")
    return key


def key_split(line: str) -> tuple[str, str] | None:
    """'key: rest' for a top-level line, with a quoted key allowed."""
    if not line or line[0] in " \t-#":
        return None
    if line[0] in "\"'":
        quote = line[0]
        i = 1
        while i < len(line):
            if line[i] == "\\" and quote == '"':
                i += 2
                continue
            if line[i] == quote:
                if quote == "'" and line[i + 1:i + 2] == "'":
                    i += 2
                    continue
                break
            i += 1
        rest = line[i + 1:]
        if not rest.lstrip().startswith(":"):
            return None
        return unquote_key(line[:i + 1]), rest.lstrip()[1:].strip()
    if ":" not in line:
        return None
    key, rest = line.split(":", 1)
    if rest and not rest.startswith((" ", "\t")):
        return None
    return key.strip(), rest.strip()


def scalar(text: str) -> str | None:
    text = text.strip()
    if text in ("", "~", "null"):
        return None
    if text.startswith('"'):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return text.strip('"')
    if text.startswith("'") and text.endswith("'") and len(text) >= 2:
        return text[1:-1].replace("''", "'")
    return re.sub(r"\s+#.*$", "", text)


def flow_list(text: str) -> list[str]:
    inner = text.strip()[1:-1]
    items, current, quote = [], "", ""
    for char in inner:
        if quote:
            current += char
            if char == quote:
                quote = ""
        elif char in "\"'":
            quote = char
            current += char
        elif char == ",":
            items.append(current)
            current = ""
        else:
            current += char
    if current.strip():
        items.append(current)
    return [value for value in (scalar(item) for item in items) if value is not None]


def parse_value(rest: str, more: list[str]) -> Any:
    if rest.startswith(("|", ">")):
        lines = [line for line in more]
        indent = min((len(line) - len(line.lstrip()) for line in lines if line.strip()), default=0)
        body = [line[indent:] for line in lines]
        while body and not body[-1].strip():
            body.pop()
        if rest.startswith("|"):
            return "\n".join(body)
        folded, paragraph = [], []
        for line in body:
            if line.strip():
                paragraph.append(line.strip())
            else:
                folded.append(" ".join(paragraph))
                paragraph = []
        folded.append(" ".join(paragraph))
        return "\n".join(folded)
    if rest.startswith("["):
        return flow_list(rest)
    if not rest:
        items = [line.strip()[1:].strip() for line in more if line.strip().startswith("-")]
        if items:
            return [value for value in (scalar(item) for item in items) if value is not None]
        return None
    if more and not rest.startswith(("\"", "'")):
        rest = " ".join([rest, *(line.strip() for line in more if line.strip())])
    elif more and rest.startswith('"'):
        joined = rest + " " + " ".join(line.strip() for line in more)
        return scalar(joined)
    return scalar(rest)


def parse_frontmatter(lines: list[str]) -> list[tuple[str, list[str], Any]]:
    """Ordered (key, raw lines, value) items. Raw lines are kept for keys left unchanged."""
    items: list[tuple[str, list[str], Any]] = []
    i = 0
    while i < len(lines):
        split = key_split(lines[i])
        if split is None:
            if items:  # a stray line: keep it with the item before it
                key, raw, value = items[-1]
                items[-1] = (key, [*raw, lines[i]], value)
            i += 1
            continue
        key, rest = split
        j = i + 1
        while j < len(lines) and (lines[j].startswith((" ", "\t")) or not lines[j].strip()
                                  or (lines[j].startswith("-") and not rest)):
            j += 1
        more = lines[i + 1:j]
        items.append((key, lines[i:j], parse_value(rest, more)))
        i = j
    return items


def dump_key(key: str) -> str:
    return key if PLAIN_KEY.match(key) else json.dumps(key, ensure_ascii=False)


def dump_item(key: str, value: Any) -> list[str]:
    head = f"{dump_key(key)}:"
    if value is None or value == "" or value == []:
        return [head]
    if isinstance(value, list):
        return [head, *(f"  - {json.dumps(str(item), ensure_ascii=False)}" for item in value)]
    if isinstance(value, bool):
        return [f"{head} {'true' if value else 'false'}"]
    if isinstance(value, (int, float)):
        return [f"{head} {value}"]
    text = str(value)
    if DATE.match(text):
        return [f"{head} {text}"]
    return [f"{head} {json.dumps(text, ensure_ascii=False)}"]


def frontmatter_dict(items: list[tuple[str, list[str], Any]]) -> dict[str, Any]:
    return {key: value for key, _, value in items}


# ---------------------------------------------------------------- body


def escape(text: str) -> str:
    """Keep a creator's text as written: no tags, links, math or formatting in Obsidian."""
    return "".join("\\" + char if char in ESCAPED else char for char in text)


def add_to_section(body: str, heading: str, text: str) -> str:
    """Add text at the end of '## <heading>', creating the section at the end if missing."""
    lines = body.rstrip("\n").split("\n") if body.strip() else []
    target = f"## {heading}".strip().lower()
    start = next((i for i, line in enumerate(lines) if line.strip().lower() == target), None)
    if start is None:
        if lines:
            lines.append("")
        lines += [f"## {heading}", "", text]
        return "\n".join(lines) + "\n"
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    while end > start + 1 and not lines[end - 1].strip():
        end -= 1
    insert = ([""] if end > start + 1 else [""]) + [text]
    if end < len(lines):
        insert.append("")
    lines[end:end] = insert
    return "\n".join(lines) + "\n"


def sections(body: str) -> dict[str, str]:
    found: dict[str, list[str]] = {}
    current = None
    for line in body.split("\n"):
        if line.startswith("## "):
            current = line[3:].strip()
            found[current] = []
        elif current is not None:
            found[current].append(line)
    return {key: "\n".join(value).strip() for key, value in found.items()}


# ---------------------------------------------------------------- notes


def entry_notes(library: Path) -> list[Path]:
    entries = folders(library)["Entries"]
    if not entries.is_dir():
        return []
    return sorted(path for path in entries.glob("*.md") if not path.name.startswith("."))


def read_entry(path: Path) -> tuple[list[tuple[str, list[str], Any]], str]:
    lines, body = split_note(path.read_text(encoding="utf-8"))
    return parse_frontmatter(lines), body


def write_entry(path: Path, items: list[tuple[str, list[str], Any]], body: str) -> None:
    lines = ["---", *(line for _, raw, _ in items for line in raw), "---"]
    text = "\n".join(lines) + "\n" + (body if body.startswith("\n") or not body else "\n" + body)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def open_uri(library: Path, path: Path) -> str:
    """A link that opens the note in Obsidian, for replies to the user."""
    vault = vault_root(library)
    note = path.relative_to(vault).with_suffix("").as_posix()
    return f"obsidian://open?vault={quote(vault.name, safe='')}&file={quote(note, safe='')}"


def summary(library: Path, path: Path, fields: dict[str, Any], keep: list[str] | None,
            with_link: bool = False) -> dict[str, Any]:
    shown = fields if keep is None else {key: fields.get(key) for key in keep}
    head = {"note": str(path.relative_to(library))}
    if with_link:
        head["open"] = open_uri(library, path)
    return {**head, **shown}


def note_path(library: Path, note: str) -> Path:
    path = (library / note).resolve()
    if library.resolve() not in path.parents or path.suffix != ".md" or not path.is_file():
        raise LibraryError(f"no such Entry: {note}")
    return path


def slug(text: str) -> str:
    text = re.sub(r"[^\w-]+", "-", text, flags=re.UNICODE).strip("-")
    return text[:60] or "post"


def tag(text: str) -> str:
    """An Obsidian tag: no '#', no spaces, lowercase."""
    return re.sub(r"\s+", "-", text.strip().lstrip("#").strip()).lower()


def new_note_path(folder: Path, fields: dict[str, Any], link_key: str | None, platform_key: str | None,
                  day: str) -> Path:
    link = str(fields.get(link_key, "")) if link_key else ""
    platform = str(fields.get(platform_key, "")) if platform_key else ""
    post_id = ""
    if link:
        parsed = urlparse(link)
        parts = [part for part in parsed.path.split("/") if part]
        post_id = dict(item.split("=", 1) for item in parsed.query.split("&") if "=" in item).get("v", "") \
            or (parts[-1] if parts else parsed.netloc)
    stem = slug(" ".join(part for part in (day, platform.lower(), post_id) if part))
    path, n = folder / f"{stem}.md", 2
    while path.exists():
        path, n = folder / f"{stem}-{n}.md", n + 1
    return path


# ---------------------------------------------------------------- commands


def holds(fields: dict[str, Any], args: argparse.Namespace) -> bool:
    def value(key: str) -> str:
        found = fields.get(key)
        return "" if found is None else str(found)

    for rule in args.where or []:
        key, wanted = rule.split("=", 1)
        if value(key) != wanted:
            return False
    for rule in args.not_ or []:
        key, unwanted = rule.split("=", 1)
        if value(key) == unwanted:
            return False
    for rule in args.since or []:
        key, day = rule.split("=", 1)
        if not DATE.match(value(key)[:10]) or value(key)[:10] < day:
            return False
    for key in args.empty or []:
        if value(key):
            return False
    return True


def keep_fields(args: argparse.Namespace) -> list[str] | None:
    return [key.strip() for key in args.fields.split(",")] if getattr(args, "fields", None) else None


def cmd_init(library: Path, args: argparse.Namespace) -> dict[str, Any]:
    made = []
    for key, folder in folders(library).items():
        if not folder.exists():
            folder.mkdir(parents=True)
            made.append(shown(library, folder))
    return {"ok": True, "created": made, "vault": str(vault_root(library))}


def cmd_query(library: Path, args: argparse.Namespace) -> dict[str, Any]:
    found = []
    for path in entry_notes(library):
        fields = frontmatter_dict(read_entry(path)[0])
        if holds(fields, args):
            found.append(summary(library, path, fields, keep_fields(args)))
    if args.count:
        return {"count": len(found)}
    return {"count": len(found), "entries": found}


def cmd_find(library: Path, args: argparse.Namespace) -> dict[str, Any]:
    link_key = args.link_field
    exact, partial = [], []
    for path in entry_notes(library):
        fields = frontmatter_dict(read_entry(path)[0])
        link = str(fields.get(link_key) or "")
        if link == args.link:
            exact.append(summary(library, path, fields, None, True))
        elif args.id and args.id in link:
            partial.append(summary(library, path, fields, None, True))
    return {"exact": exact, "by_id": partial}


def cmd_search(library: Path, args: argparse.Namespace) -> dict[str, Any]:
    words = [word.lower() for word in args.words]
    found = []
    for path in entry_notes(library):
        items, body = read_entry(path)
        fields = frontmatter_dict(items)
        haystack = " ".join([json.dumps(fields, ensure_ascii=False), body.replace("\\", "")]).lower()
        hits = sum(word in haystack for word in words)
        if hits:
            found.append((hits, summary(library, path, fields, keep_fields(args), True)))
    found.sort(key=lambda pair: -pair[0])
    return {"count": len(found), "entries": [entry for _, entry in found[:args.limit]]}


def cmd_tags(library: Path, args: argparse.Namespace) -> dict[str, Any]:
    counts: dict[str, int] = {}
    for path in entry_notes(library):
        value = frontmatter_dict(read_entry(path)[0]).get(TAGS_KEY) or []
        for item in value if isinstance(value, list) else [value]:
            counts[str(item)] = counts.get(str(item), 0) + 1
    return {"tags": dict(sorted(counts.items(), key=lambda pair: (-pair[1], pair[0])))}


def apply_changes(library: Path, path: Path, items: list[tuple[str, list[str], Any]], body: str,
                  change: dict[str, Any]) -> tuple[list[tuple[str, list[str], Any]], str]:
    fields = dict(change.get("set") or {})
    for key in change.get("clear") or []:
        fields[key] = None
    if change.get("add_tags"):
        current = frontmatter_dict(items).get(TAGS_KEY) or []
        current = current if isinstance(current, list) else [current]
        merged = [*current, *(tag(item) for item in change["add_tags"] if tag(item) not in current)]
        fields[TAGS_KEY] = merged
    if TAGS_KEY in (change.get("set") or {}):
        value = change["set"][TAGS_KEY] or []
        fields[TAGS_KEY] = [tag(item) for item in (value if isinstance(value, list) else [value])]
    if change.get("cover_file"):
        source = Path(change["cover_file"])
        if source.is_file():
            covers = path.parent / COVERS_FOLDER
            covers.mkdir(exist_ok=True)
            target = covers / f"{path.stem}{source.suffix.lower() or '.jpg'}"
            shutil.copyfile(source, target)
            fields[COVER_KEY] = f"[[{target.relative_to(vault_root(library)).as_posix()}]]"
    by_key = {key: i for i, (key, _, _) in enumerate(items)}
    for key, value in fields.items():
        item = (key, dump_item(key, value), value)
        if key in by_key:
            items[by_key[key]] = item
        else:
            by_key[key] = len(items)
            items.append(item)
    for heading, text in (change.get("append") or {}).items():
        if text and str(text).strip():
            body = add_to_section(body, heading, escape(str(text)) if change.get("escape", True) else str(text))
    for heading, text in (change.get("append_raw") or {}).items():
        if text and str(text).strip():
            body = add_to_section(body, heading, str(text))
    return items, body


def cmd_create(library: Path, args: argparse.Namespace) -> dict[str, Any]:
    data = json.load(sys.stdin)
    entries = data if isinstance(data, list) else [data]
    folder = folders(library)["Entries"]
    folder.mkdir(parents=True, exist_ok=True)
    made = []
    for entry in entries:
        fields = dict(entry.get("set") or entry.get("fields") or {})
        day = str(entry.get("day") or date.today().isoformat())
        path = new_note_path(folder, fields, entry.get("link_field"), entry.get("platform_field"), day)
        items, body = apply_changes(library, path, [], "", {**entry, "set": fields})
        write_entry(path, items, body)
        made.append({"note": str(path.relative_to(library)), "open": open_uri(library, path)})
    return {"created": made}


def cmd_update(library: Path, args: argparse.Namespace) -> dict[str, Any]:
    path = note_path(library, args.note)
    items, body = read_entry(path)
    items, body = apply_changes(library, path, items, body, json.load(sys.stdin))
    write_entry(path, items, body)
    return {"updated": str(path.relative_to(library)), "open": open_uri(library, path)}


def icloud_pending(folder: Path) -> list[Path]:
    """Files iCloud has not downloaded yet show up on a Mac as '.<name>.icloud'.
    Ask iCloud to fetch them; they are read by the next call."""
    pending = [path for path in folder.glob(".*.icloud")] if folder.is_dir() else []
    brctl = shutil.which("brctl")
    for path in pending:
        if brctl:
            import subprocess
            subprocess.run([brctl, "download", str(path)], capture_output=True)
    return pending


def cmd_shared(library: Path, args: argparse.Namespace) -> dict[str, Any]:
    share = folders(library)["Share here"]
    pending = icloud_pending(share)
    if pending:
        import time
        time.sleep(3)
    found = []
    for path in sorted(share.glob("*")) if share.is_dir() else []:
        if not path.is_file() or path.name.startswith(".") or path.suffix.lower() not in (".md", ".txt", ""):
            continue
        text = path.read_text(encoding="utf-8", errors="replace").strip()
        shared = datetime.fromtimestamp(path.stat().st_mtime).date().isoformat()
        found.append({"file": shown(library, path), "name": path.stem, "text": text, "shared": shared})
    waiting = len([path for path in share.glob(".*.icloud")]) if share.is_dir() else 0
    return {"count": len(found), "shared": found, "waiting_for_icloud": waiting}


def cmd_shared_done(library: Path, args: argparse.Namespace) -> dict[str, Any]:
    places = folders(library)
    places["Already read"].mkdir(parents=True, exist_ok=True)
    moved = []
    for name in args.files:
        source = (library / Path(name).expanduser()).resolve()
        if source.parent != places["Share here"].resolve() or not source.is_file():
            raise LibraryError(f"not a shared save: {name}")
        target, n = places["Already read"] / source.name, 2
        while target.exists():
            target, n = places["Already read"] / f"{source.stem}-{n}{source.suffix}", n + 1
        source.replace(target)
        moved.append(shown(library, target))
    return {"moved": moved}


def cmd_remove(library: Path, args: argparse.Namespace) -> dict[str, Any]:
    path = note_path(library, args.note)
    trash = vault_root(library) / ".trash"
    trash.mkdir(exist_ok=True)
    target, n = trash / path.name, 2
    while target.exists():
        target, n = trash / f"{path.stem}-{n}.md", n + 1
    path.replace(target)
    return {"removed": str(path.relative_to(library)), "trash": str(target)}


def parser() -> argparse.ArgumentParser:
    main = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = main.add_subparsers(dest="command", required=True)

    def command(name: str, function: Any) -> argparse.ArgumentParser:
        part = sub.add_parser(name)
        part.add_argument("library")
        part.set_defaults(function=function)
        return part

    command("init", cmd_init)
    query = command("query", cmd_query)
    query.add_argument("--where", action="append")
    query.add_argument("--not", dest="not_", action="append")
    query.add_argument("--since", action="append")
    query.add_argument("--empty", action="append")
    query.add_argument("--fields")
    query.add_argument("--count", action="store_true")
    find = command("find", cmd_find)
    find.add_argument("--link", required=True)
    find.add_argument("--id")
    find.add_argument("--link-field", default="Link")
    search = command("search", cmd_search)
    search.add_argument("words", nargs="+")
    search.add_argument("--fields")
    search.add_argument("--limit", type=int, default=20)
    command("tags", cmd_tags)
    command("create", cmd_create)
    update = command("update", cmd_update)
    update.add_argument("note")
    command("shared", cmd_shared)
    done = command("shared-done", cmd_shared_done)
    done.add_argument("files", nargs="+")
    remove = command("remove", cmd_remove)
    remove.add_argument("note")
    return main


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        result = args.function(library_folder(args.library), args)
    except (LibraryError, json.JSONDecodeError, ValueError) as error:
        print(json.dumps({"error": str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
