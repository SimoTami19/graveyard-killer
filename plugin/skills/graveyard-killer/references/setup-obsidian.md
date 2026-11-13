# Setup in Obsidian

The Obsidian steps of [setup.md](setup.md). Read [library-obsidian.md](library-obsidian.md) first.

An Obsidian Library lives on this computer, so only the agent on this computer can read it: the Claude app on the phone cannot. Capture, Recall and the Worker run in the Claude Desktop Code tab, and the phone saves posts as files into the vault, with no agent.

## Create the Library

1. **Find the vault.** Ask for the vault's folder, unless the session's folder is the vault or sits inside one: the nearest folder that holds `.obsidian`. A vault in iCloud sits under `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/<vault name>`. Done when you hold the vault's absolute path and have checked that it holds `.obsidian`.

2. **Name it and place it.** Ask in one question what to call the Library and where in the vault it goes, suggesting a folder "Graveyard Killer" at the vault's top, or inside the folder the user keeps resources in, if their vault has one. Done when you hold the Library folder's absolute path, which must not exist yet or must be empty.

3. **Write the Settings.** Create the folder and write `Settings.md` in it with your file-writing tool: every section of [library.md](library.md#the-settings) in order, then the Folders section of [library-obsidian.md](library-obsidian.md#layout), with the three folders named in the Settings language (in Italian: Schede, Condividi qui, Già letti). Done when the file exists.
   - The Fields table names Tags `tags`, and also names Captures, Transcript and On-screen text (in Italian: Catture, Trascrizione, Testo a schermo).
   - The Limits start at 20 per day and 100 per week.
   - The Schedule and "Ping by" stay empty until Setup's steps 3 and 9, and the Preferences table holds only its header row.

4. **Make the folders.** Run `python3 scripts/obsidian.py init "<Library folder>"`, then `python3 scripts/obsidian.py query "<Library folder>" --count`. Done when `init` prints `"ok": true` and `query` prints `{"count": 0}`.

The Library link, for the pointer, is the Library folder's absolute path.

**The pointer on this computer only.** Setup's step 6 puts the pointer in `~/.claude/CLAUDE.md`. In step 8, skip the pointer in the Claude app's Instructions and the "Save through Claude" route: a phone chat cannot reach a folder on this computer, and every chat that read the pointer would fail.

## Save from the phone

**Save through a Shortcut into the vault.** This is the only way to save from the phone, with no tokens and with the computer off. Walk the user through building it on the iPhone, one step at a time. On an iPhone the names of the actions may differ a little with the iOS version.

1. In the **Shortcuts** app, a new shortcut named "Salva nel Graveyard" (in the Settings language). In its details, turn on **Show in Share Sheet**, receiving **URLs** and **Text**.
2. Add **Format Date** on **Current Date**, with the custom format `yyyyMMdd-HHmmss`.
3. Add **Text**, holding **Shortcut Input**.
4. Add **Save File**: save the Text, turn off **Ask Where to Save**, choose as its folder the Library's "Share here" folder inside the vault, in iCloud Drive → Obsidian → the vault, and as its subpath the Formatted Date followed by `.md`. Turn off overwriting.
5. Test it: in Instagram, Share → More → "Salva nel Graveyard". Then check, on the computer, that a file arrived in "Share here": run `python3 scripts/obsidian.py shared "<Library folder>"`.

If **Save File** lets the shortcut save only inside the Shortcuts folder, save into a folder "Graveyard" there instead, and write that folder's absolute path on the computer, `~/Library/Mobile Documents/iCloud~is~workflow~my~workflows/Documents/Graveyard`, as the name of "Share here" in the Settings' Folders section: a name that starts with `/` or `~` is a path of its own.

On Android, a vault synced with another app works the same way if the share sheet can save text as a file into the "Share here" folder.

Tell the user that iCloud can keep a file only in the cloud until it is opened, and that keeping the vault's folder downloaded on the computer (Finder: right click → Keep Downloaded) makes the files arrive sooner. The script asks iCloud for any file that is missing.
