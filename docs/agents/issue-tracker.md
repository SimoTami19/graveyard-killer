# Issue tracker: GitHub Issues

Issues live in GitHub Issues on `andreadorizza/graveyard-killer`. Work with them through the `gh` CLI, always passing `--repo andreadorizza/graveyard-killer`.

The repo and its issues are public, so write nothing private there.

## Conventions

- One issue per problem, question or feature.
- A spec is an issue labelled `spec`. Its implementation tickets are separate issues whose body starts with `Part of #<spec>`.
- Triage state is a label (see `triage-labels.md` for the role strings). Add `bug` or `enhancement` too when it fits.
- Discussion goes in the issue's comments.
- The specs of features that have shipped are kept as records in `docs/specs/`.

## When a skill says "publish to the issue tracker"

Write the body to a file, then:

```
gh issue create --repo andreadorizza/graveyard-killer --title "<title>" --body-file <file> --label needs-triage
```

## When a skill says "fetch the relevant ticket"

```
gh issue view <number> --repo andreadorizza/graveyard-killer --comments
```

The user will normally pass the issue number or its link.

## Wayfinding operations

Used by `/wayfinder`. The **map** is an issue with one **child** issue per ticket.

- **Map**: an issue labelled `map`, whose body holds the Notes, Decisions-so-far and Fog.
- **Child ticket**: an issue whose body starts with `Part of #<map>`, then a `Type:` line (`research`/`prototype`/`grilling`/`task`), then the question.
- **Blocking**: a `Blocked by: #N, #N` line near the top. A ticket is unblocked when every issue it lists is closed.
- **Frontier**: the open, unblocked child issues of the map with no `claimed` label; the lowest number wins.
- **Claim**: add the `claimed` label before any work.
- **Resolve**: comment the answer under an `## Answer` heading, close the issue, then add a context pointer (gist + issue link) to the map's Decisions-so-far by editing the map issue's body.
