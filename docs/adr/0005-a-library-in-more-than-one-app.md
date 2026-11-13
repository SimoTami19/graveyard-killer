# A Library can live in more than one app

Some users keep their life in Google Drive and have no Notion account, and more apps may follow. So a Library lives in one **Library app** the user picks at Setup, Notion by default. [library.md](../../plugin/skills/graveyard-killer/references/library.md) holds what every Library app shares: the Entry fields, the Statuses, the Settings, duplicates, and a list of named operations such as "Find an Entry by its link". Each app has one file that says how it does each operation, with its own rules (`library-notion.md`), and one for its Setup steps (`setup-notion.md`). Jobs name operations only. An agent reads only its own app's files, so a Notion user's agent never loads the Drive rules, and a new app costs other users nothing. The host of the link in the pointer line tells which app a Library uses, so the pointer's format does not change. Google Drive is the second Library app, from the proposal and tests of `michelelupini-design` in issue #11.

## Considered Options

- **One column per app in `library.md`.** Fine for two apps, but every job would load every app's rules, and the Worker runs daily on the user's plan.
- **Settings in the plugin's `userConfig`,** as Claude Code plugins usually keep them. They live in one computer's `settings.json`, which the phone's chat and other agents cannot read. [ADR-0002](0002-settings-live-in-the-library.md) stands.
- **Drive as one Google Doc per Entry.** Listing the Inbox or finding a link would mean opening every Doc.
- **A Sheet with an Apps Script** to find rows and keep dropdowns. Scripts need the user's authorisation, and the connectors cannot install one.
- **Writing the Sheet with the connector's `update_values` and `append_values`.** They parse every value as if typed: `=1+1` runs, `3/4` becomes a date, `007` loses its zeros, and appended rows lose their dropdowns. Typed cells through `update_spreadsheet` (`appendCells`, `updateCells`) keep text exactly as written, write into empty rows and keep the dropdowns (tested 2026-11-12).

## Consequences

- A Drive Library is one Sheet, with an Entries tab and a Settings tab laid out like the Notion Settings page, and two folders named in the Settings language: "Share here", where the phone shares, and "Already read", where the Worker moves each shared file once read. The pointer links to the Sheet, and the Settings hold the folders' links.
- On Drive, users sort and move rows and columns, and a row has no address that survives a sort. So rows are found by their Link and columns by their header, every time, and an Entry is named by its Title and Link instead of a link to it.
- On Drive, dates are written as `=DATE(y,m,d)` in columns formatted `yyyy-mm-dd`, so they sort and filter like dates the user types and read back as `2026-11-12`. Long text, such as the transcript, goes in the last columns. One Sheets read returns about 40,000 characters (measured 2026-11-13), so a Drive Library is read one column at a time, in pages of 200 rows, and a Doc holds a value past 30,000 characters. Sheets shows no covers, so a Drive Entry has none.
- A duplicate row on Drive is deleted after the user's yes. Unlike Notion's trash, only the Sheet's version history brings it back.
- A shared save that holds no link is set aside: on Drive it moves to "Already read" and the next Ping names it; on Notion the row stays where it is.
- Saving from the phone into a Drive Library is Share, then Drive, then "Share here", as Notion's share sheet is for Notion ([ADR-0004](0004-notion-share-sheet-captures.md)). It was tested on Android; iOS is untested.
- Setup always asks which Library app, recommending Notion. A later release lets a user move a Library to another app by copying it; the old Library stays as it was.
- The evals stay one set with a Library-app placeholder, plus a few evals for Drive alone, each run against a test Library in that app.
