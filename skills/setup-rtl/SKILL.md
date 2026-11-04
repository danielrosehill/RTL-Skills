---
name: setup-rtl
description: First-run setup for RTL Skills. Checks Typst and poppler, and saves signatures, sender details and newsletter brands privately.
---

# Set up RTL Skills

Read `references/user-data.md` for the data directory. Find it with
`${CLAUDE_PLUGIN_ROOT}/scripts/paths.sh dir`. Do only the parts the user needs, and
if something exists, show it and ask what to change.

## 1. Toolchain (documents and letters)

```bash
for t in typst pdffonts pdftotext pdftoppm; do
  printf "%-10s " "$t"; command -v $t >/dev/null && echo ok || echo MISSING
done
```

`pdffonts`, `pdftotext` and `pdftoppm` come from `poppler-utils`. They are the only
way to check a render worked. Email previews need a Chromium-family browser.

David Libre is vendored in `${CLAUDE_PLUGIN_ROOT}/assets/fonts` (SIL OFL, licence
alongside). Typst finds it through `--font-path`, so no system install is needed.

## 2. Email profiles: `config.json`

Ask only for what's missing. `personal` and `business` are the two the send skills
expect, and more can be added.

| Field | Notes |
|---|---|
| `display_name` | Latin script, as it appears in the signature |
| `display_name_rtl` | The name in the RTL script. **Ask. Never transliterate it yourself.** |
| `lang` | `he`, `ar`, `fa`, `ur` |
| `register` | `informal` for personal, `formal` for business. Only a default: the recipient decides |
| `email`, `phone` | Phone as the user gives it out |
| `signature_html` | Rendered signature. Ask whether it should be Latin or RTL script. A Latin signature under an RTL body is normal, but it's the user's call |
| `identifiers` | Business, optional: label/value pairs such as company or VAT number |
| `org`, `org_rtl` | Business only |
| `ai_line` | Optional AI-assistance note in the profile's language, added after the signature |

```json
{
  "version": 1,
  "default_profile": "personal",
  "profiles": {
    "personal": {
      "lang": "he", "register": "informal",
      "display_name": "Ada Lovelace", "display_name_rtl": "עדה לאבלייס",
      "email": "ada@example.com", "phone": "02-000-0000",
      "signature_html": "<div>Ada Lovelace<br>ada@example.com</div>"
    }
  }
}
```

## 3. Letter sender: `typst/sender.typ`

Copy `${CLAUDE_PLUGIN_ROOT}/assets/typst/sender.typ` to `<data dir>/typst/sender.typ`
and fill it in. Keep the keys. Don't invent values, and leave `id` as `""` if the
user doesn't want one shown.

## 4. Newsletter brand: `brands/<name>.json`

Copy `${CLAUDE_PLUGIN_ROOT}/examples/newsletter/brand.json`. It needs `name`,
`address` and an opt-out route, and takes `logo_url` (a public URL, because mail
clients can't read local files), `accent` and `contact_email`.

## Report

Say which tools are missing and which files were written, and where.
