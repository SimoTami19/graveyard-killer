# Settings live in the Library; Instructions only point to it

The phone's chat agent and the Worker must agree on the exact Categories and field names, but they do not share memory. The Claude apps share one memory, Claude Code keeps its own, and other agents keep theirs separately. Memory is also rewritten by the model, so it cannot hold names that must match character for character. So the Settings, and the user's Preferences, live inside the Library, as a page, a tab or a file. Each agent surface holds one pointer: the Library's link and a one-line recall hint. In the Claude apps it sits in the account-wide Instructions, which apply to every chat and which only the user writes. In the Code tab it sits in `~/.claude/CLAUDE.md`. If the pointer is missing, the skill asks for the link once.

## Considered Options

- **The pointer in chat memory.** This was v1: Setup had the user send "Remember: Graveyard Killer Library: <link>". The model rewrites memory, and chat memory is not documented as read in every chat. Replaced by Instructions on 2026-11-11.
- **The Capture rule in the pointer.** Rejected: the instructions would live in two places that drift apart. The skill starts on its own when the user shares a link, through its description, so Capture needs the skill: an app that cannot run the skill cannot Capture.
- **A recall hint in the pointer.** Accepted. It copies no rule from the skill. It only tells the agent when to look in the Library: when the user asks about something they saved, or when a conversation touches a topic the Library may hold. The skill says how.

## Consequences

- Setup cannot write the Instructions. It gives the user the text to paste.
- Recall works in any chat, even when the skill does not load: the hint is enough to search the Library.
- Editing a Category or a Preference means editing the Library's Settings, not the skill or a local file.
- Not documented: whether Instructions reach Projects and the Code tab. The Code tab gets its own line.
