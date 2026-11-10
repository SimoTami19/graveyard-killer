# Graveyard Killer

Your saved posts are a graveyard. Share a post from your phone to Claude, and Graveyard Killer files what it says in your own Notion Library. Once a week your computer reads the new posts and leaves you a Digest: what is coming up, what is new, and what you could do with it. It needs no server and no API keys.

**Status: early release (0.3.0).** Tested with Claude on Android and on a Mac. iPhone, Windows and Linux should work the same way but are untested. The Library is Notion only for now.

## What you need

- A paid Claude plan (Pro or above). Plugins and the Code tab, where setup and the weekly run happen, are not on the free plan.
- Claude Desktop on your computer and the Claude app on your phone.
- Notion, connected to Claude in *Customize → Connectors*.

## Install

1. In Claude Desktop, open *Customize → Plugins → Add marketplace* and paste `https://github.com/andreadorizza/graveyard-killer`.
2. Find **Graveyard Killer** under *Discover* and add it. Adding the marketplace alone is not enough.
3. In the Code tab, open a session in an empty folder and type `Set up Graveyard Killer`. Setup asks what you save, creates the Library in your Notion, schedules the weekly run and tests one post end to end.

To get a new version, open *Customize → Plugins* and choose *Check for updates* on this marketplace.

Other agents can install the skill with `npx skills add andreadorizza/graveyard-killer`, with the Notion MCP server and your own weekly scheduler. That route is untested.

## How it works

- **Capture.** Share a post from Instagram, TikTok or YouTube to the Claude app's chat, with no text. Claude files an Entry with a Category, a summary and a next action. From Instagram it gets only the link; the weekly run fills in the rest.
- **The weekly run.** A scheduled task in the Code tab, while the app is open and the computer is awake. It downloads each new post, transcribes it, reads its on-screen text, completes the Entry and deletes the video.
- **The Digest.** A page in your Library with what is coming up in the next 14 days, what is new and what waits for you. Ask "show me my Graveyard Killer Digest" from any chat: Claude offers up to three things to do, such as adding an event to your calendar, and does nothing until you say yes.

## Instagram account safety

Graveyard Killer reads posts without your login, so your account is not used. Instagram may still slow down or block reading from your connection if it reads many posts at once, so a weekly run reads only a few, and it stops reading Instagram at the first challenge.

## Docs

- [Design](docs/design.md): how v1 works
- [Glossary](GLOSSARY.md): the words this project uses
- [Decision records](docs/adr/)

## License

[MIT](LICENSE)
