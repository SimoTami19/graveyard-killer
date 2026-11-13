"""The Obsidian Library script: notes in, notes out, nothing lost."""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "plugin/skills/graveyard-killer/scripts"))
import obsidian  # noqa: E402

SETTINGS = """## Language
Italiano

## Statuses
| Status | Label in this Library |
| --- | --- |
| Inbox | Da leggere |

## Folders
| Folder | Name in this Library |
| --- | --- |
| Entries | Schede |
| Share here | Condividi qui |
| Already read | Già letti |
"""


@pytest.fixture
def library(tmp_path: Path) -> Path:
    vault = tmp_path / "SIMO BRAIN"
    (vault / ".obsidian").mkdir(parents=True)
    lib = vault / "Graveyard Killer"
    lib.mkdir()
    (lib / "Settings.md").write_text(SETTINGS, encoding="utf-8")
    return lib


def run(capsys, *argv: str, stdin: object | None = None, monkeypatch=None) -> dict:
    if stdin is not None:
        monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps(stdin)))
    code = obsidian.main(list(argv))
    out = json.loads(capsys.readouterr().out)
    assert code == 0, out
    return out


def test_init_makes_the_folders_and_finds_the_vault(library, capsys):
    out = run(capsys, "init", str(library / "Settings.md"))
    assert sorted(out["created"]) == ["Condividi qui", "Già letti", "Schede"]
    assert out["vault"].endswith("SIMO BRAIN")


def test_file_link_with_spaces(library, capsys):
    link = "file://" + str(library).replace(" ", "%20")
    assert run(capsys, "init", link)["vault"].endswith("SIMO BRAIN")


def test_not_a_library(tmp_path, capsys):
    assert obsidian.main(["query", str(tmp_path)]) == 1
    assert "not an Obsidian Library" in json.loads(capsys.readouterr().out)["error"]


def test_create_query_update_round_trip(library, capsys, monkeypatch):
    caption = 'Pasta "alla Norma": #ricetta #sicilia [[link]] $5\nseconda riga'
    entry = {
        "link_field": "Link", "platform_field": "Piattaforma", "day": "2026-11-13",
        "set": {"Titolo": "⏳ Post Instagram", "Link": "https://www.instagram.com/p/DQx1abc/",
                "Piattaforma": "Instagram", "Stato": "Da leggere", "Catturato il": "2026-11-13",
                "Riassunto": "Una frase: con due punti", "tags": ["Cucina Italiana", "#pasta"]},
        "append": {"Didascalia": caption},
    }
    created = run(capsys, "create", str(library), stdin=entry, monkeypatch=monkeypatch)["created"][0]
    note = created["note"]
    assert created["open"] == "obsidian://open?vault=SIMO%20BRAIN&file=Graveyard%20Killer%2FSchede%2F2026-11-13-instagram-DQx1abc"
    assert note == "Schede/2026-11-13-instagram-DQx1abc.md"
    text = (library / note).read_text(encoding="utf-8")
    assert "Catturato il: 2026-11-13" in text  # a bare date, so Obsidian sees a date
    assert "\\#ricetta" in text and "\\[\\[link\\]\\]" in text and "\\$5" in text

    inbox = run(capsys, "query", str(library), "--where", "Stato=Da leggere", "--fields", "Titolo,tags")
    assert inbox["entries"] == [{"note": note, "Titolo": "⏳ Post Instagram", "tags": ["cucina-italiana", "pasta"]}]

    change = {"set": {"Titolo": "Pasta alla Norma", "Stato": "Elaborato", "Elaborato il": "2026-11-14"},
              "clear": ["Nota"], "add_tags": ["pasta", "Ricette veloci"],
              "append": {"Trascrizione": "Primo blocco.\n\nSecondo blocco.", "Testo a schermo": "INGREDIENTI"}}
    run(capsys, "update", str(library), note, stdin=change, monkeypatch=monkeypatch)
    fields = run(capsys, "query", str(library))["entries"][0]
    assert fields["Titolo"] == "Pasta alla Norma"
    assert fields["Riassunto"] == "Una frase: con due punti"
    assert fields["tags"] == ["cucina-italiana", "pasta", "ricette-veloci"]
    assert fields["Nota"] is None
    body = obsidian.sections(obsidian.split_note((library / note).read_text(encoding="utf-8"))[1])
    assert list(body) == ["Didascalia", "Trascrizione", "Testo a schermo"]
    assert body["Trascrizione"] == "Primo blocco.\n\nSecondo blocco."

    assert run(capsys, "query", str(library), "--since", "Elaborato il=2026-11-14", "--count") == {"count": 1}
    assert run(capsys, "query", str(library), "--since", "Elaborato il=2026-11-15", "--count") == {"count": 0}
    assert run(capsys, "query", str(library), "--not", "Piattaforma=Instagram", "--count") == {"count": 0}


def test_obsidian_edits_survive(library, capsys, monkeypatch):
    """Obsidian rewrites properties in its own style; keys we do not touch stay byte for byte."""
    (library / "Schede").mkdir()
    note = library / "Schede" / "a.md"
    note.write_text(
        "---\n"
        "Titolo: Ricetta veloce\n"
        "Link: https://www.tiktok.com/@a/video/123\n"
        "tags:\n  - cucina\n  - veloce\n"
        "aliases: [uno, \"due, tre\"]\n"
        "letto: true\n"
        "Riassunto: |-\n  riga uno\n  riga due\n"
        "Nota: 'l''altra volta'\n"
        "---\n\nUna nota mia.\n",
        encoding="utf-8")
    fields = run(capsys, "query", str(library))["entries"][0]
    assert fields["tags"] == ["cucina", "veloce"]
    assert fields["aliases"] == ["uno", "due, tre"]
    assert fields["Riassunto"] == "riga uno\nriga due"
    assert fields["Nota"] == "l'altra volta"
    run(capsys, "update", str(library), "Schede/a.md", stdin={"add_tags": ["dolci"]}, monkeypatch=monkeypatch)
    text = note.read_text(encoding="utf-8")
    assert "letto: true\n" in text and "aliases: [uno, \"due, tre\"]\n" in text and "Riassunto: |-\n" in text
    assert text.endswith("\nUna nota mia.\n")
    assert run(capsys, "find", str(library), "--link", "https://www.tiktok.com/@a/video/123")["exact"]
    assert run(capsys, "find", str(library), "--link", "https://vm.tiktok.com/x", "--id", "123")["by_id"]
    assert run(capsys, "search", str(library), "veloce")["count"] == 1
    assert run(capsys, "tags", str(library))["tags"] == {"cucina": 1, "dolci": 1, "veloce": 1}


def test_shared_saves_and_remove(library, capsys):
    run(capsys, "init", str(library))
    (library / "Condividi qui" / "20261113-101500.md").write_text(
        "Guarda questo reel! https://www.instagram.com/reel/DQx1abc/?igsh=xyz", encoding="utf-8")
    shared = run(capsys, "shared", str(library))
    assert shared["count"] == 1 and "instagram.com/reel" in shared["shared"][0]["text"]
    moved = run(capsys, "shared-done", str(library), shared["shared"][0]["file"])["moved"]
    assert moved == ["Già letti/20261113-101500.md"]
    assert run(capsys, "shared", str(library))["count"] == 0

    (library / "Schede" / "dup.md").write_text("---\nTitolo: x\n---\n", encoding="utf-8")
    out = run(capsys, "remove", str(library), "Schede/dup.md")
    assert Path(out["trash"]).parent.name == ".trash" and Path(out["trash"]).parent.parent.name == "SIMO BRAIN"


def test_cover_copied_into_the_vault(library, capsys, monkeypatch, tmp_path):
    run(capsys, "init", str(library))
    (library / "Schede" / "b.md").write_text("---\nTitolo: x\n---\n", encoding="utf-8")
    thumb = tmp_path / "thumbnail.jpg"
    thumb.write_bytes(b"\xff\xd8jpeg")
    run(capsys, "update", str(library), "Schede/b.md", stdin={"cover_file": str(thumb)}, monkeypatch=monkeypatch)
    fields = run(capsys, "query", str(library))["entries"][0]
    assert fields["cover"] == "[[Graveyard Killer/Schede/_covers/b.jpg]]"
    assert (library / "Schede" / "_covers" / "b.jpg").read_bytes() == b"\xff\xd8jpeg"


def test_note_outside_the_library_is_refused(library, capsys):
    assert obsidian.main(["update", str(library), "../../etc/passwd.md"]) == 1


def test_share_folder_outside_the_vault(library, capsys, tmp_path):
    outside = tmp_path / "Shortcuts" / "Graveyard"
    settings = (library / "Settings.md").read_text(encoding="utf-8")
    (library / "Settings.md").write_text(settings.replace("| Share here | Condividi qui |", f"| Share here | {outside} |"),
                                         encoding="utf-8")
    run(capsys, "init", str(library))
    (outside / "x.md").write_text("https://youtu.be/abc", encoding="utf-8")
    shared = run(capsys, "shared", str(library))["shared"]
    assert shared[0]["file"] == str(outside / "x.md")
    assert run(capsys, "shared-done", str(library), shared[0]["file"])["moved"] == ["Già letti/x.md"]
