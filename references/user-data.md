# Public plugin, private overlay

The plugin ships no personal data. Anything of yours (names, signatures, brands,
house styles) lives in a data directory outside the plugin, which survives plugin
updates and can be a private git repo. Skills read both layers, and yours wins.

Find it with `${CLAUDE_PLUGIN_ROOT}/scripts/paths.sh`. Don't guess. It checks, in
order: `$RTL_SKILLS_HOME`, `$CLAUDE_USER_DATA/rtl-skills`,
`~/.claude-user-data/rtl-skills` if that root exists,
`${XDG_DATA_HOME:-~/.local/share}/claude-plugins/rtl-skills` if that root exists,
then `~/.claude-user-data/rtl-skills`. Never write under `~/.claude/`.

```
<data dir>/
├── config.json        # email profiles and signatures (setup-rtl writes it)
├── brands/<name>.json # newsletter brands: name, logo, colour, address, opt-out
├── templates/         # same file name as a built-in = replaces it
├── typst/             # sender.typ for letters, document-base.typ for a house style
├── assets/            # logos and images
└── notes.md           # your own rules; skills read it when present
```

- `paths.sh file templates/newsletter.html` gives the winning path.
- `paths.sh list brands` lists brands; `paths.sh list templates` lists templates.
- `paths.sh stage-typst <dir>` copies the built-in `.typ` files into a working
  directory, then yours on top.

Built-ins are read from the plugin, not copied into the data dir, so they keep
getting fixes. Never commit a filled-in `sender.typ`, `config.json` or brand file
to a public repository.
