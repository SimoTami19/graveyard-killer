# Digest

A **Digest** is a short review of the Library that you give the user in a chat: when they ask for it, or inside a Ping when a week has passed without one ([ping.md](ping.md#gather-it)). It is never written to a page.

You have chosen this job, found the Library and read its Settings (see SKILL.md), or a Worker run sent you here to gather its Ping.

## Give the Digest

1. **Find the period.** It runs from "Last Digest" in the Settings' Pings section, or from 7 days ago when it is empty, to today. Done when you hold both dates.

2. **Gather the lists** with [Query the Entries](library.md#query-the-entries). Each Entry goes in one list only: an Entry in Needs you appears nowhere else. Done when you hold all five:
   - **Coming up:** Entries whose Status is Processed and whose Next action names a calendar date (a day, or a day and a month) from today to 14 days after today. A date without a year is the next one to come. Words such as "this weekend" are not a date;
   - **New:** Entries whose Processed date is after the period's first day and whose Status is Processed or Used, grouped by Category, leaving out the Entries in Coming up or Dug up;
   - **Dug up:** Entries whose Processed date is after the period's first day, whose Status is Processed or Used, and that came from the Graveyard (they have a Saved date), leaving out the Entries in Coming up;
   - **Needs you:** every Entry in the Inbox with a Note, every Buried Entry with a Note, and every Entry whose Note says it is a duplicate;
   - **Re-import:** a reminder to export the Graveyard again and import it, only when "Last import" in the Settings' Graveyard section is more than 3 months ago, or empty while Buried Entries exist.

   If all five are empty, say there is nothing new since the last recap, and stop.

3. **Give it** in the Settings language, short enough to read on a phone. Done when you have sent it, or added it to the Ping.
   - One line per list that is not empty, in the order above, with its count. In Italian the lists are "In programma", "Nuovi", "Ripescati", "Ha bisogno di te" and "Da reimportare".
   - Name each Entry in Coming up with its date, and up to 3 Entries in New, the most useful first, each with a [link to its Entry](library.md#link-to-an-entry).

4. **Offer Library Proposals,** at most 3, the most useful first. Done when you have offered them, or none fits; then say nothing about them. These are about the Library itself; an Entry's own Proposal comes once, in the Ping of the run that read it:
   - **Move an Entry to another Category,** when it sits in the fallback Category and another fits. When three or more Entries in the fallback Category share a theme that no Category covers, offer a new Category named after it, for example after the Tags they share. On a yes, [add the Category](library.md#add-a-category). Then move the Entries.
   - **Remove the duplicates:** the Entries whose Note says they are duplicates. On a yes, [remove them](library.md#remove-a-duplicate).
   - **Dig up a Category next,** or **an Amnesty** when many Buried Entries are older than a year: follow [graveyard.md](graveyard.md).

5. **Record it.** [Write the Settings](library.md#write-the-settings): set "Last Digest" in the Pings section to today. Done when it is saved.

The user can answer about any Entry the Digest names, for example "I did it" or "make me the grocery list". Act as [ping.md](ping.md#when-the-user-answers) says.
