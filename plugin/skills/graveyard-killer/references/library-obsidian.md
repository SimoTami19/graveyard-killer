# The Library in Obsidian

How an Obsidian Library does each operation in [library.md](library.md#operations), and Obsidian's own rules. An Obsidian Library is a folder of Markdown files in the user's vault, on this computer. There is no connector: you read and write it with `scripts/obsidian.py`, run with `python3` from this skill's folder, and with your file tools for `Settings.md` only.

## Layout

The Library is one folder inside an Obsidian vault, the vault being the nearest folder above it that holds `.obsidian`. The pointer gives the folder's absolute path, such as `/Users/simone/Library/Mobile Documents/iCloud~md~obsidian/Documents/SIMO BRAIN/Graveyard Killer`. The folder holds:

- `Settings.md`, with the sections of [library.md](library.md#the-settings) in their order. After library.md's sections comes a **Folders** section, for Obsidian only:

  | Folder | Name in this Library |
  | --- | --- |
  | Entries | Schede |
  | Share here | Condividi qui |
  | Already read | Già letti |

- the **Entries** folder, with one note per Entry;
- the **Share here** folder, where the phone saves one small file per shared post;
- the **Already read** folder, where shared files go once adopted.

**An Entry** is one note. Its file name is set once, at creation, from the date, the platform and the post's id, such as `2026-11-13-instagram-DQx1abc.md`, and never changes: the Title lives in a property, so a new title never breaks a link to the note. Its fields are the note's **properties** (the frontmatter), named as the Settings' Fields table says, except the four long ones, which are sections of the note's body, each under a `## ` heading with the Library's name for it, in this order: **Caption**, **Captures** (one line per extra Capture, and the "Shared as" line), **Transcript** and **On-screen text**. The Fields table names all four.

| Kind in library.md | In Obsidian |
| --- | --- |
| text | a text property (Caption: a body section) |
| link | a text property holding the link |
| one label | a text property holding the label |
| labels | the Tags field is always Obsidian's own `tags` property, a list, whatever the Library's language: the Fields table names it `tags` |
| date | a date property, `2026-11-12` |

Category fields are extra text properties. The cover is the `cover` property, a link to an image the script copies into the Entries folder's `_covers` subfolder.

The shared saves are the files in "Share here".

## Writing to Obsidian

- **Through the script only.** Create and change Entries only with `obsidian.py create` and `obsidian.py update`: it writes properties that Obsidian reads, keeps every property the user added or edited byte for byte, and escapes the creator's text. Never write an Entry note with your file tools. `Settings.md` is the exception: read it with your file-reading tool and change it with your editing tool, keeping its tables' layout.
- **JSON on stdin.** `create` and `update` read one JSON object from stdin. Pass it through a quoted heredoc, so no shell expands it:

  ```
  python3 scripts/obsidian.py update "<library>" "<note>" <<'JSON'
  {"set": {"Stato": "Elaborato", "Elaborato il": "2026-11-13"}, "clear": ["Nota"]}
  JSON
  ```

  The keys are:
  - `set`: properties to write, by the Library's names. A date is a `YYYY-MM-DD` string. `null` empties a property;
  - `clear`: properties to empty;
  - `add_tags`: Tags to add to `tags`, keeping the ones there;
  - `append`: body sections to add text to, by their Library names, such as `{"Trascrizione": "…"}`. The text goes at the end of the section, which the script creates when missing. It is escaped, so hashtags, `[[…]]`, `$` and Markdown in the creator's text stay as written and make no tags, links or math in the vault;
  - `cover_file`: an image file to copy in as the cover;
  - for `create` only: `link_field` and `platform_field`, the Library's names for Link and Platform, which name the file, and `day`, the date for its name (today when left out). `create` also takes a list of these objects, for many Entries at once.
- **Text values.** Write property values as plain text: the script quotes them. Leave out Markdown escapes.
- **Tags.** Lowercase, with words joined by `-` and no `#`, such as `cucina-italiana`: Obsidian tags hold no spaces. The script fixes the form; before a new Tag, reuse a Tag from `obsidian.py tags` that fits.
- **iCloud.** A vault in iCloud may hold files that iCloud has not downloaded to this computer yet. `obsidian.py shared` asks iCloud for them and reports `waiting_for_icloud`: when it is above 0, wait 10 seconds and run `shared` again, once.

Every command prints one JSON object. An `{"error": …}` result means the step failed: say what failed, as the job says.

## Operations

`<library>` is the Library link from the pointer, quoted.

### Read the Settings

Read `<library>/Settings.md` with your file-reading tool.

### Write the Settings

Edit `<library>/Settings.md` with your editing tool: change a value under its heading, or add a row at the end of a table. Add a missing section, with its heading, where library.md's order puts it.

### Find an Entry by its link

`python3 scripts/obsidian.py find "<library>" --link "<canonical link>" --link-field "<Library's name for Link>"`, adding `--id "<post id>"` when you know it and the job allows more than an exact match. `exact` holds the Entries whose Link equals it, `by_id` those whose Link contains the id.

### Query the Entries

`python3 scripts/obsidian.py query "<library>"` with filters, all of which must hold, each repeatable:

- `--where "<field>=<value>"`: equal, such as `--where "Stato=Da leggere"`;
- `--not "<field>=<value>"`: not equal, such as `--not "Piattaforma=Other"`;
- `--since "<date field>=<YYYY-MM-DD>"`: on or after that date;
- `--empty "<field>"`: empty;
- `--fields "<a>,<b>"`: return only these properties, which keeps the answer short. Always pass it when a job needs only a few fields, as for every Link in a Graveyard import;
- `--count`: return only how many match, as for the Worker's budget.

Each answer holds `note`, the path to pass to `update`, with the properties asked for.

### Search the Entries

`python3 scripts/obsidian.py search "<library>" <word> [<word> …] --fields "<Title>,<Summary>,<Status>,<Link>"`. It looks in every property and in the body, and ranks the Entries by how many words they hold.

### Create an Entry

`obsidian.py create` with the fields in `set`, and the Caption, a Captures line or a "Shared as" line in `append`.

### Update an Entry

`obsidian.py update` with its `note`. A "Captured again" line goes in `append` under Captures; the transcript under Transcript, one paragraph per block, with a blank line between paragraphs; the on-screen text under On-screen text. For the cover, pass the `thumbnail` path that `post.py read` printed as `cover_file`, before you run `post.py clean`: Instagram's image links expire, a copied file does not.

### Add a Category

Add a row for each new Category at the end of the Settings' Categories table. There is nothing else to change: a Category is a text property.

### Add a Tag

Nothing to add: a Tag is free text in `tags`. Reuse the spelling from `obsidian.py tags`.

### List the shared saves

`python3 scripts/obsidian.py shared "<library>"`. For each file: its link sits in its `text`, else in its `name`; it was shared on its `shared` day; and the text it was shared with is its `text`.

### Adopt a shared save

[Create an Entry](#create-an-entry) with the Worker's fields and the "Shared as" line under Captures. First [find an Entry by](#find-an-entry-by-its-link) the Worker's Link: if one exists, create the new one with its Note already set to "Duplicate of <[that Entry](#link-to-an-entry)>". Then `python3 scripts/obsidian.py shared-done "<library>" "<file>"`.

### Set a shared save aside

`obsidian.py shared-done` on its file, as for an adopted one. The Ping names it.

### Remove a duplicate

`python3 scripts/obsidian.py remove "<library>" "<note>"`, after checking its Note says "Duplicate of". It moves the note to the vault's `.trash` folder, Obsidian's own trash, from which the user can move it back.

### Link to an Entry

Give its Title as a Markdown link to the `open` link that `find`, `search`, `create` and `update` print, such as [Pasta alla Norma](obsidian://open?vault=SIMO%20BRAIN&file=Graveyard%20Killer%2FSchede%2F2026-11-13-instagram-DQx1abc). It opens the note in Obsidian on this computer.

### Create the Library

See [setup-obsidian.md](setup-obsidian.md#create-the-library).
