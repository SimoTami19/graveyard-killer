# Run the Worker in Codex

Status: ready-for-human

People ask whether Graveyard Killer runs on ChatGPT or Codex. The public answer for now: "Claude only today; Codex support is being tested." Claim nothing more until the tests below pass.

Since [ADR-0004](../../docs/adr/0004-notion-share-sheet-captures.md), the phone saves through Notion's share sheet, so the phone needs no agent. Only the Worker needs a port: download, transcribe, read keyframes and write the Entries. ChatGPT on the phone matters only for the second Capture route.

## What the docs say (checked 2026-11-10)

**Codex**
- Skills use the same `SKILL.md` format. Codex reads them from `.agents/skills` in a repo or `$HOME/.agents/skills`.
- Codex reads a Claude plugin marketplace's `.claude-plugin/marketplace.json`, and `codex plugin marketplace add owner/repo` adds one.
- The Notion MCP server works after `codex mcp login notion`.
- Image viewing (`features.view_image`) is on by default, which keyframe reading needs.
- `codex exec -m <model>` picks the model. The ChatGPT desktop app's scheduled tasks run locally and can pick the model too.
- The sandbox has no network by default (`sandbox_workspace_write.network_access`). yt-dlp and gallery-dl need it.

**ChatGPT**
- Skills are documented for Business, Enterprise, Healthcare and Edu. Skills inside a plugin are documented on mobile.
- Its Notion connector writes "where supported".
- A custom MCP connector needs Business or Enterprise and works on the web only.
- Sharing from the Instagram app to the ChatGPT app is not documented.

## Tests

On a real Codex install with a ChatGPT Plus account, against a test Library (never a real one):

- [ ] The marketplace installs and Codex finds the `graveyard-killer-worker` skill.
- [ ] `post.py check` installs the tools, and `post.py read` downloads a public reel with network access on.
- [ ] The Worker finishes a shared row, a chat-captured Entry and a Buried Entry, reading keyframes.
- [ ] A scheduled task in the ChatGPT desktop app runs the Worker on a mid-tier model.
- [ ] The Ping reaches the user, and the user can answer in that task's chat.

Done when every box is ticked or a failed one has a note, and the README says what works.
