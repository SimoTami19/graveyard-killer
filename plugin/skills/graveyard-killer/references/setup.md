# Setup

Setup is a conversation on the user's computer, in the Claude Desktop Code tab, after the plugin is added. At the end the user has their own Library, the tools, the scheduled Worker, saving from the phone and a way to get Pings. The user is probably not technical, so do the work yourself. Explain each step in a line, and ask one thing at a time. Setup runs once, on whatever model the user picked; only the Worker is pinned to Sonnet.

Setup starts when the user asks to set up Graveyard Killer, or when a Graveyard Killer job finds no Library. It does not need an existing Library, so skip SKILL.md's steps 2 and 3.

**A user who already has a Library,** set up on another computer: ask for its link, read its Settings as SKILL.md's step 3 says, and do only steps 4, 6 and 7 here. Tell them to keep the scheduled Worker on one computer only, and to delete the task on the other one. Talk in the language the user writes in. It becomes the Settings language: say so in your first question, so the user can pick another.

## Steps

1. **What do they save?** Ask what kinds of posts the user saves, such as recipes, places, workouts or AI prompts. If the user mentions an Instagram export already on the computer, run `python3 scripts/graveyard.py "<path>"` and offer its `collections` as Categories. Done when you have 2 to 8 Categories, each with a line on what goes in it, and maybe its own fields (a recipe's ingredients, a place's location). Add one fallback Category for everything else.

2. **Create the Library.** Check that your Notion connector works, for example by reading the user's Notion profile or searching. If it does not, ask the user to connect Notion first. Ask in one question what to call the Library, suggesting "Graveyard Killer" as a private page. Then create it exactly as [library.md](library.md) describes:
   - the private page with that name;
   - the Entries database inside it, with every field in the user's language, the six Statuses and the Category options;
   - the `Settings` page, with every section. The Limits start at 20 per day and 100 per week. The Schedule and "Ping by" stay empty until steps 3 and 9.

   Done when you can read the Settings back.

3. **Pick the time.** Ask at what time the Worker should run every day. Suggest a time when the computer is usually on and awake, such as lunchtime, and say that it runs only while the Claude app is open and the computer is awake. Write the answer in the Settings' Schedule section. Done when the Settings hold it.

4. **Install the tools.** Follow step 1 of [worker.md](worker.md#steps). Done when `check` prints `"ok": true`.

5. **Test one link end to end.** Ask the user for the link of a public post they saved. Capture it as [capture.md](capture.md) says. Then finish only that Entry, as worker.md's [Each Entry](worker.md#each-entry) says, with no dig-up and no Ping. Show them the finished Entry. Done when it is Processed.

6. **Point this computer to the Library.** In the Code tab, the pointer goes in the user's Claude Code memory file, `~/.claude/CLAUDE.md`. Show the user [the pointer](#the-pointer). With their OK, add it at the end of that file. Done when it is saved.

7. **Schedule the Worker,** as [schedule.md](schedule.md) says. Done when the daily task exists and the user has set its model.

8. **Set up the phone.** Walk the user through it, one step at a time. Done when a shared post arrived in Entries, or the user says they will do it later.
   - **The pointer.** The Claude apps on the phone and the computer share one set of Instructions, in *Settings → Your Claude → Instructions*, which apply to every chat. Give them [the pointer](#the-pointer) to paste there. You cannot write it yourself.
   - **Save through Notion.** This is the main way to save, with no tokens and with the computer off. In Instagram, TikTok or YouTube, the user taps Share, picks Notion, chooses the Library's Entries database as the destination, and saves. On an iPhone they first turn Notion on under the share sheet's More. Then check that a row with the link arrived in Entries. Notion says its share sheet supports only browsers and the photo roll; if the app is missing or says the app is not supported, use the next route.
   - **Save through Claude.** The second way: share the post to the Claude app's Chat with no text. It costs a short chat, and for TikTok, YouTube and web links it writes a first summary at once. From Instagram it gets only the link.

9. **Pick how Pings arrive.** Explain that a run sends a Ping only when it has an offer for them or a problem only they can fix, and that they answer in that run's chat. Offer, and write the choice to "Ping by" in the Settings' Pings section. Then send a test Ping through it and ask whether it arrived. Done when the user confirms, or chose `none`.
   - `push`: a notification from Claude Desktop. It also reaches the phone when Remote Control is on for new sessions in Claude Desktop's settings.
   - `email`: an email to themselves, through their Gmail connector.
   - `notion`: a comment that mentions them on the Library page. Notion may not notify you about a mention you wrote through your own connector, so the test matters here.
   - `none`: no alert. They open the run's chat in the Claude app when they like.

10. **Offer the Graveyard.** Explain that their old saves can come in as Buried Entries, and how to request the exports (see [graveyard.md](graveyard.md#import-the-graveyard)). The exports take a few hours to about 2 days. Once they arrive, the user says "import my Graveyard Killer graveyard". Done when you have told them.

11. **Say how updates arrive.** To get the newest version, the user opens *Customize → Plugins* in the Claude app and selects *Check for updates* on the Graveyard Killer marketplace. Done when you have told them.

12. **Say the Instagram risk once.** Graveyard Killer reads posts without the user's login, so their account is not used. Instagram may still slow down or block reading from their connection if it reads many posts at once, so a run reads at most 20 posts a day and 100 a week, with a pause between Instagram posts, and stops reading Instagram at the first challenge. Done when you have told them.

## The pointer

Two lines in the user's language, with the Library link and no query string. The first line stays exactly as written; translate the second. In English:

```
Graveyard Killer Library: <link>
It holds the posts I saved. Look there when I ask about something I saved, or when we talk about a topic it may hold.
```

In Italian:

```
Graveyard Killer Library: <link>
Lì ci sono i post che ho salvato. Cercaci quando ti chiedo di qualcosa che ho salvato o quando parliamo di un argomento che potrebbe contenere.
```
