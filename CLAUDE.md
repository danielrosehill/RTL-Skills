# RTL-Skills: agent notes

Public plugin `rtl-skills` (repo `danielrosehill/RTL-Skills`, renamed from
RTL-Conformity-Skills 2026-11-04). The one home for right-to-left output. It absorbed
`rtl-email` (Claude-RTL-Email) and `hebrew-correspondence`
(Claude-Hebrew-Correspondence-Plugin) on 2026-11-04.

## Consumers

- **Claude:** the repo is its own marketplace (`.claude-plugin/marketplace.json`,
  source `./`), and it is also listed in the main public marketplace.
- **ChatGPT workspaces:** a publish script may vendor the pushed `main` branch.
  Push first.

## Invariants

- **No `.mcp.json`:** ChatGPT would mark the plugin Desktop only.
- **Two kinds of skill.** The `rtl-*` rule skills are instruction-only and must work
  with no shell. The `write-*`, `verify-*` and `setup-*` skills may use `scripts/`.
- **Generic.** Name capabilities ("your email tool"), not vendor tool names. No
  personal identifiers, infra or private repo names anywhere in this repo.
- **Private data stays in the overlay** (`scripts/paths.sh`, `references/user-data.md`).
  Overlay first, built-in second, same relative path. Never a parallel private fork.
- **Say what is verified.** Date facts with absolute dates.
- **Fonts:** David Libre under SIL OFL, licence in `assets/fonts/`.
- Frontmatter `name` equals the folder name. `description` carries the search terms.
- Bump `version` in `plugin.json` and `marketplace.json` when skill content changes.
