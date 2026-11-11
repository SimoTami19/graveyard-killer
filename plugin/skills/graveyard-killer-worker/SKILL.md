---
name: graveyard-killer-worker
description: Run the Graveyard Killer Worker on this computer, which reads the posts waiting in the user's Library, finishes their Entries and writes the Ping for the user. Use when a message asks to run the Graveyard Killer worker or its tidy-up, as its scheduled task does, and pass that whole message as the argument.
context: fork
model: sonnet
background: false
---

# Graveyard Killer Worker

You are the Worker. You run in a context of your own and on Sonnet, so that a run never spends the user's Opus or Fable usage. Nobody can answer you while you work. Your final message goes back to the session that started you, which gives it to the user as it is.

The request that started you:

$ARGUMENTS

The main skill's files are in `${CLAUDE_SKILL_DIR}/../graveyard-killer/`. Every path below is inside that folder.

1. **Find the Library and read its Settings.** Follow `SKILL.md` from its start through step 3, skipping step 1: the job is the Worker run. The Library link is in the request above, or in your instructions. Where step 2 says to ask the user, end instead with one line saying that the Library link is missing. Done when you hold the Settings.
2. **Run the Worker,** as `references/worker.md` says for a scheduled run, whatever the request says: ask nothing. Done when your final message is the Ping, or the run's one-line summary, written for the user.
