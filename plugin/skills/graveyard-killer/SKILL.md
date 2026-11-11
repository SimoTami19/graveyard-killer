---
name: graveyard-killer
description: Capture a shared post into the user's Graveyard Killer Library, and recall what the user saved there. Use whenever a message is a link (Instagram, TikTok, YouTube or any web page) with no request, such as a bare link, a link inside an app's share text, or a link with a short "save this"; whenever the user asks about a post they saved; and whenever the user names Graveyard Killer, for example to set it up, import old saves or get its Digest.
---

# Graveyard Killer

Graveyard Killer files the posts a user sends you into their own **Library**, a Notion page they own. Each post becomes one **Entry**. You do the work through the user's own connectors: there is no server and no API key.

Talk to the user in the language set in their Library's **Settings**. Keep this skill's own words (field and Status names) for your thinking, and write the Library's names into the Library.

With the user, use plain words in their language instead of this skill's terms, and recognise those words when they write them:

| This skill says | Say | In Italian |
| --- | --- | --- |
| Library | your Library | la tua Libreria |
| Entry | card | scheda |
| Inbox Entry | a placeholder | un segnaposto |
| Worker run | the tidy-up | il riordino |
| Digest | the recap | il riepilogo |
| Proposal | an offer | una proposta |
| Graveyard | old saves | vecchi salvataggi |
| dig up | bring back | ripescare |
| Amnesty | set aside old saves | scartare i vecchi salvataggi |

## 1. Choose the job

A **Capture** is the user sending you one post's URL to keep it. It arrives as a link on its own, a link inside an app's share text ("Check out this reel!"), or a link with a short "save this". The user is usually on their phone and wants to send the next post in seconds. So finish a Capture in one turn and ask nothing.

A link that comes with a question or a task ("summarise this", "is this true?") is a request, and a message with no link is ordinary chat. Answer those as usual, without this skill, unless they ask about the user's saves.

Done when you know the job:

- **Capture**: follow the steps below, then [references/capture.md](references/capture.md).
- **Recall**: the user asks about something they saved ("that carbonara recipe I saved?", "what did I save this week?"). Follow the steps below, then [references/recall.md](references/recall.md).
- **Worker run**: the user asks to run the Graveyard Killer worker or its tidy-up. Use the `graveyard-killer-worker` skill, which runs it on the model it needs. If you have no shell, as in a phone app, tell the user the Worker runs on their computer, in the Claude Desktop Code tab, and stop.
- **Schedule the Worker**: the user asks Graveyard Killer to run its Worker on a schedule, or to change its time, for example "schedule the Graveyard Killer worker". Follow the steps below, then [references/schedule.md](references/schedule.md).
- **Setup**: the user asks to set up Graveyard Killer, or has no Library yet. On a phone, tell them Setup runs on their computer, in the Claude Desktop Code tab, and stop. Otherwise go straight to [references/setup.md](references/setup.md), which creates the Library.
- **Graveyard**: the user asks Graveyard Killer to import their old saves, to dig up a Category next, or for an Amnesty. Follow the steps below, then [references/graveyard.md](references/graveyard.md).
- **Digest**: the user asks for their Graveyard Killer Digest, or what is new in their Library. Follow the steps below, then [references/digest.md](references/digest.md).
- **Preference**: the user tells Graveyard Killer to always, never, or ask before making a kind of offer, such as "stop offering grocery lists". Follow the steps below, then [references/ping.md](references/ping.md#when-the-user-answers).

## 2. Find the Library

Look in your instructions and memory for the Library's location, one line: `Graveyard Killer Library: <link>`. Done when you hold the Library link.

- If the line is missing, ask the user once for the link to their Graveyard Killer Library page in Notion. If they have no Library yet: on a computer, offer Setup ([references/setup.md](references/setup.md)); on a phone, tell them Setup runs on their computer, in the Claude Desktop Code tab, and stop.
- When you had to ask for the link, give the user the pointer text from [setup.md](references/setup.md#the-pointer) once, ready to paste into the Instructions in their Claude settings, so that you need not ask again.

## 3. Read the Settings

Read the Settings page inside the Library through your Notion connector, as described in [references/library.md](references/library.md). Done when you know the language, every field name, every Status label, every Category and the fallback Category.

If the Library or its Settings cannot be read, tell the user which one failed and that the Notion connector may need reconnecting, and stop.
