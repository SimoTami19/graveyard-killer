# Agent instructions

## Agent skills

### Issue tracker

Issues and specs are GitHub Issues on this repo, worked with the `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

The five default triage roles, written as a `Status:` line in each issue file. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

## Releases

A push to `main` is a release. Installed copies get new files only when the plugin's `version` changes, so before every push to `main`, run `git diff --stat origin/main -- plugin/`. If it lists files, raise `version` in `plugin/.claude-plugin/plugin.json` in the same push: minor for a new job or a change in behaviour, patch for a fix or a change that keeps behaviour. Build each release on its own branch, `release-<version>`, and merge it to `main` only after its evals pass. Tag the commit on `main` as `v<version>` and push the tag with it.

## Library apps

Jobs read and write the Library only through the operations named in `plugin/skills/graveyard-killer/references/library.md`. How a Library app does each operation, and its own rules, go in `library-<app>.md`, and its Setup steps in `setup-<app>.md`. Never name an app's tools or quirks in a job file. See ADR-0005.
