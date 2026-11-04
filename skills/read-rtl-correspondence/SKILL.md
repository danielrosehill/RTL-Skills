---
name: read-rtl-correspondence
description: Turn incoming Hebrew email — .eml exports, a folder of them, or an .mbox — into a readable threaded PDF or Markdown, with correct right-to-left rendering and optional redaction before sharing. Use when correspondence arrives as files rather than in a mailbox, or when a chain has to go to a lawyer, insurer or regulator. Triggers on "PDF of this Hebrew email chain", "read these .eml files", "prepare this correspondence for a complaint".
---

# Read and render incoming Hebrew correspondence

Uses the `eml_toolkit` library, which handles thread reconstruction and
per-block direction resolution. Installed as a dependency rather than copied, so
fixes land in one place.

## Install once

```bash
uv pip install "git+https://github.com/danielrosehill/Claude-Eml-Toolkit"
```

## Render a chain

```bash
python3 -m eml_toolkit.cli parse    <source> --out thread.json
python3 -m eml_toolkit.cli pdf      <source> --out chain.pdf
python3 -m eml_toolkit.cli markdown <source> --out thread.md
```

`<source>` is a single `.eml`, a directory searched recursively, or an `.mbox`.

Direction is resolved per paragraph, so a Hebrew thread containing an English
reply renders both correctly. There is no RTL flag to set and none is needed.

## Before sending a chain to a third party

```bash
python3 -m eml_toolkit.cli pdf <source> --out redacted.pdf \
  --redact --keep <your-address>,<reference-number>
```

`--keep` matters: without it the reference number the recipient needs in order to
act gets masked along with everything else, and a redacted complaint becomes
unactionable.

Then verify, and read the result yourself — the redaction patterns are
deliberately conservative and the failure that matters is the one they missed:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/verify_render.py redacted.pdf
pdftoppm -png -r 100 -f 1 -l 1 redacted.pdf /tmp/page   # then read /tmp/page-1.png
```

## For a complaint file

If the chain is going into a complaint or an evidence bundle, hash the source
`.eml` bytes rather than the rendered PDF — the PDF is a derivative. `thread.json`
already carries a SHA-256 per source file.
