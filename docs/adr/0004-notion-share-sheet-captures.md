# Notion's share sheet is the main way to Capture

Capturing through the Claude chat spends a model turn to write one row, and the chat cannot watch the video: for Instagram it saves only the link anyway. People asked why an agent is needed for that. Notion's own share sheet writes a page with no agent and no tokens, and works with the computer off. So Setup teaches sharing into the Entries database first. The Worker adopts every row in Entries that has a link and no Status (the link in the Link field, the title or the page body) as an Inbox Entry. Capturing through the Claude chat stays as the second route, for a first summary right away of a TikTok, YouTube or web link.

## Considered Options

- **Chat Capture only.** This was v1. It costs tokens on every save and gives the "it cannot see the video" complaint.
- **An iOS Shortcut or an Android automation** that writes to Notion. It needs a Notion integration token, which [ADR-0001](0001-no-server-no-api-keys.md) rules out.
- **ChatGPT's app as a second phone agent.** Its skills are documented only for Business, Enterprise, Healthcare and Edu, and a custom connector works on the web only.

## Consequences

- Notion's help says the mobile share sheet works only from a browser or the photo roll and "doesn't support other apps yet" (checked 2026-11-11). A share from the Instagram app still worked on a Pixel on 2026-11-11. So Setup tests the share and falls back to chat Capture. On iOS the user first turns Notion on under the share sheet's More.
- That Pixel share filled the Link field with the reel's link (plus a `psln` query), kept the title the user typed, put an embed of the link in the page body and left Status empty. The Worker still looks for the link in the title and the body too, for rows added by hand.
- A shared row has no Category, summary or Next action until the Worker reads it.
- The launch video shows chat Capture. The README and the guide say the main route changed.
- The phone no longer needs the skill, so supporting another agent, such as Codex, needs only the Worker.
