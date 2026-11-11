# Graveyard Killer

Your saved posts are a graveyard. Graveyard Killer turns them into a Library in your own Notion. Share a post from your phone, and your computer later watches it, reads what it says and files it. When something you saved is worth doing this week, such as a concert date or a recipe for the weekend, Claude messages you with an offer, and does nothing until you say yes. It needs no server and no API keys.

**Status: early release (0.4.0).** Tested with Claude on Android and on a Mac. iPhone, Windows and Linux should work the same way but are untested. The Library is Notion only for now. Claude only: Codex support is being tested.

## What you need

- A paid Claude plan (Pro or above). Plugins and the Code tab, where setup and the daily run happen, are not on the free plan.
- Claude Desktop on your computer, and the Notion app on your phone.
- Notion, connected to Claude in *Customize → Connectors*.

## Install

1. In Claude Desktop, open *Customize → Plugins → Add marketplace* and paste `https://github.com/andreadorizza/graveyard-killer`.
2. Find **Graveyard Killer** under *Discover* and add it. Adding the marketplace alone is not enough.
3. In the Code tab, open a session in an empty folder and type `Set up Graveyard Killer`. Setup asks what you save, creates the Library in your Notion, schedules the daily run, tests one post end to end and shows you how to save from the phone.

To get a new version, open *Customize → Plugins* and choose *Check for updates* on this marketplace.

Other agents can install the skills with `npx skills add andreadorizza/graveyard-killer`, with the Notion MCP server and your own scheduler. That route is untested.

## How it works

- **Saving.** Share a post from Instagram, TikTok or YouTube to Notion, into your Library's Entries. It costs no tokens and works with your computer off. *This changed after the launch video*, which shows sharing to the Claude app; that still works, as a second way.
- **Placeholders.** Your phone cannot watch the video, and neither can Claude on your phone. Until your computer reads a post, its card is a placeholder, and its title starts with ⏳.
- **The daily run.** A scheduled task in the Code tab, while the app is open and the computer is awake. It downloads each new post, transcribes it, reads its on-screen text, completes the card and deletes the video. It runs on Sonnet, so it does not spend your Opus usage, and it skips old saves when your weekly usage is high.
- **Pings.** A run messages you only when it has something for you: an offer on a post it just read (a grocery list for a recipe, a concert in your calendar) or a problem only you can fix. You answer in that same chat. The first time an offer comes up, Claude asks whether you want it always, each time, or never, and remembers your answer in your Library.
- **Recall.** Setup gives you two lines for your Claude Instructions. With them, any chat can look in your Library when you ask about something you saved, or when you talk about a topic it holds.
- **Recap.** Ask "what's new in my Graveyard Killer?" in any chat. If a week passes with no message, the next run sends you the recap.

## Instagram account safety

Graveyard Killer reads posts without your login, so your account is not used. Instagram may still slow down or block reading from your connection if it reads many posts at once. So a run reads at most 20 posts a day and 100 a week, pauses between Instagram posts, and stops reading Instagram at the first challenge. You can change the limits in your Library's Settings.

## Docs

- [Design](docs/design.md): how v1 works, and what changed since
- [Glossary](GLOSSARY.md): the words this project uses
- [Decision records](docs/adr/)

## License

[MIT](LICENSE)
