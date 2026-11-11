---
name: graveyard-killer-worker
description: Run the Graveyard Killer Worker on this computer, which reads the posts waiting in the user's Library, finishes their Entries and pings the user with what needs them. Use when a message asks to run the Graveyard Killer worker or its tidy-up, as its scheduled task does.
model: sonnet
---

# Graveyard Killer Worker

This skill exists so that the Worker runs on Sonnet: a run never spends the user's Opus or Fable usage. Its instructions live in the main skill's folder, `../graveyard-killer/`, next to this one. Every path below is inside that folder.

1. **Find the Library and read its Settings.** Follow `SKILL.md` from its start through step 3, skipping step 1: the job is the Worker run. Done when you hold the Settings.
2. **Run the Worker,** as `references/worker.md` says. Done when it says the run is over.
