# The Ping, Proposals and Preferences

A **Ping** is a message a Worker run sends the user on its own. It comes only when the run has something for the user: a **Proposal**, an action on an Entry it just read, or something only the user can fix. Otherwise the run stays silent, except that after 7 days with no Ping it brings the Digest. The user answers in the run's own chat, so the Ping always ends that chat.

A **Preference** is the user's standing answer to one kind of Proposal: always, ask me, or never. The agent asks for it the first time that kind comes up, and records it in the Settings' Preferences table ([library.md](library.md#the-settings-page)).

You came here from step 6 of [worker.md](worker.md#steps). Write everything in the Settings language and in plain words.

## Gather it

Done when you hold the three parts below, each of them possibly empty.

1. **Proposals.** For each Entry this run finished (Processed, from the Inbox or dug up), look for one action that uses its content in the coming days, in the post's own terms. For example: an event or a deadline goes in the calendar, a recipe becomes a grocery list, a workout starts on Monday, a tool gets tried on the user's own project. Offer only what helps this week, and only what you can do in the chat or with your own tools. Most Entries get none.
   - Its **kind** is the Entry's Category and the action, such as "Ricette · lista della spesa".
   - Look up the kind in the Preferences. **Never**: drop it. **Always**: do it now, as [On a yes](#on-a-yes) says, and list it as done. **Ask me**, or no Preference yet: offer it.
   - "Always" never covers an action that reaches other people or costs money: offer that one every time.
   - Order them by urgency, a date soonest first, then by how much each would help this week. Keep at most 5 offers. The rest are dropped: each Proposal is offered once, by the run that reads its Entry.
2. **Fixes:** what only the user can solve.
   - Missing tools, with their install commands.
   - Instagram asked for a login, and how many Instagram Entries wait for the next run.
   - Entries this run left with a new Note, in the Inbox or Buried. An Entry that fails again with the Note it already had is not news: it waits for the Digest's Needs you list, so that one dead link does not ping the user every day.
   - Duplicates this run found: Entries whose Note it set to "Duplicate of". Ask whether to move them to the Notion trash.
   - A scheduled run whose prompt is from before version 0.4.0 (it calls the run "unattended"): ask the user to say "update my Graveyard Killer schedule" in the Code tab, which also makes the run daily.
3. **The Digest,** when "Last Ping" in the Settings' Pings section is 7 or more days ago, or empty, and the Library has Entries Processed since "Last Digest". Gather it as [digest.md](digest.md#give-the-digest) says.

## Send it

1. **With nothing gathered,** end the run with one line: what it read, or that there was nothing to read. Alert nobody. Done.
2. **Alert the user** through "Ping by" in the Settings' Pings section, with one short line about the most urgent item, such as "Graveyard Killer: the Roma concert is on Saturday". Skip the alert when the run was not scheduled: the user is already in this chat. Done when the alert is sent, or failed and you noted why.
   - **push:** your push notification tool. In Claude Desktop it is `PushNotification`, which also reaches the phone when Remote Control is on. It may skip the alert while the user is active in the app, who then sees the chat anyway.
   - **email:** an email to the user's own address through their Gmail connector, saying to open the chat named after the scheduled task in the Claude app.
   - **notion:** a comment on the Library page that mentions the user.
   - **none**, or empty: no alert. The chat waits in the app's list of runs.
3. **Record it** in the Settings' Pings section: "Last Ping" is today, and "Last Digest" too when the Ping brings the Digest. Done when both are saved.
4. **End your turn with the Ping,** in this order. Done when it is sent:
   - one line on what the run did, such as "I read 4 new posts and brought back 2 old ones";
   - the Proposals, numbered so the user can answer "yes to 1 and 3", each one line with a link to its Entry. Add the Preference question to the first offer of each kind with no Preference yet, such as "For recipes: always, ask me each time, or never?" List the "always" ones you did, as done;
   - the fixes;
   - the Digest, when due. Number its Library Proposals after the Ping's own, in one sequence, and leave out its duplicates offer, which the fixes cover.

## When the user answers

The user answers in this chat, maybe hours later. Done when each answer is acted on.

- A yes to a Proposal: do it, as [On a yes](#on-a-yes) says.
- A Preference ("always", "never", "stop offering grocery lists"): add or update its row in the Settings' Preferences table, with the kind and the answer in the Settings language. A user can also change a Preference from any chat: "Graveyard Killer, stop offering grocery lists".
- A yes to the duplicates: move them to the Notion trash. The connector trashes a page only on the user's say-so, and this yes is it. On a no, they stay, and the Digest lists them under Needs you.
- "I did it" about an Entry: set its Status to the Library's label for Used. "I don't want it": set Dismissed. It stays in the Library.

## On a yes

Give the result in this chat: a grocery list from the recipe's ingredients, the steps of a workout. Put something in another app only on the user's yes or an "always", and only in the user's own apps through their connectors: a dated event goes in their calendar with the Entry's Title, the date and the Entry's link. With no tool for a step, say so and give the user what they need to do it themselves.
