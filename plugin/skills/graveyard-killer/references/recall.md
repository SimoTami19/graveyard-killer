# Recall

The user's Library is a memory of what they saved. **Recall** is looking in it: when the user asks about a post they saved, or when a conversation touches a topic the Library may hold, such as a trip to Lisbon when they saved places there.

You have chosen Recall, found the Library and read its Settings (see SKILL.md).

## Steps

1. **Search every Entry,** whatever its Status. Done when you hold the matches, or know there are none.
   - For a topic, [search the Entries](library.md#search-the-entries) for its words.
   - For a time ("this week", "in June"), [query the Entries](library.md#query-the-entries) by Captured, Saved and Processed, and [list the shared saves](library.md#list-the-shared-saves). A shared save has no Captured date yet: use the day it was shared.

2. **Answer** in the Settings language, with a [link to each Entry](library.md#link-to-an-entry) you name. Done when you have sent it.
   - Say what each Entry is when it is not Processed or Used: a **placeholder** (Status Inbox, or a shared save, and its title usually starts with ⏳: the computer has not read the post yet, so you know only what came with it, often just the link), **Buried** (an old save not brought back yet), **Dismissed** (the user set it aside) or **Unavailable** (the post is gone).
   - A placeholder that holds only a link matches no topic. When the question is about a time, count the placeholders in it, such as "and 2 more I haven't read yet".
   - When a conversation only touches a topic, add the matches in one line at the end of your answer, and only when they help.
   - With no match, say so in one line. If recent placeholders hold only a link, add that one of them might be it: "I haven't read 3 recent posts yet".

3. **Offer to read the placeholders now,** when the search found nothing or only placeholders, and you have a shell with the Worker's tools, as in the Claude Desktop Code tab. On a yes, finish only those Entries, the most recent first, as [worker.md](worker.md#each-entry) says, then search again. Done when they are Processed and you have answered, or the user said no.

A request about an Entry, such as "make me the grocery list for it", is an ordinary request: do it as [ping.md](ping.md#on-a-yes) says.
