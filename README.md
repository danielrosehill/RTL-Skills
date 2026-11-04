# RTL Skills

Everything right-to-left for AI agents, in one plugin: email, PDFs, letters,
newsletters, Google Workspace, calendar and generated files, in Hebrew, Arabic, Farsi
and Urdu.

Wrong direction never raises an error. The tool call succeeds, the text is all there,
and it reads left-to-right with phone numbers and account references reordered. These
skills set the right switch on each surface and check that it took.

## Skills

| Skill | Does |
|---|---|
| `setup-rtl` | Checks the toolchain and saves your signatures, sender details and brands |
| `write-rtl-document` | Report, memo, brief or one-pager to PDF with Typst |
| `write-hebrew-letter` | Formal Hebrew letter to PDF: David Libre, dual dating, addressee and subject blocks |
| `write-rtl-newsletter` | Marketing email or newsletter as table-based RTL HTML, with a lint and Israeli advertising checklist |
| `send-rtl-personal-email` | Personal RTL email, signed from your profile |
| `send-rtl-business-email` | Formal RTL email, signed from your profile |
| `read-rtl-correspondence` | Incoming `.eml` or `.mbox` to a threaded PDF or Markdown |
| `verify-rtl-render` | Catches the silent font substitutions a Typst exit code hides |
| `rtl-basics` | Core rules: direction per block, isolating numbers, Israeli conventions |
| `rtl-email` | Email rules for any mail tool |
| `rtl-google-workspace` | Docs, Sheets, Slides and Drive |
| `rtl-calendar` | Calendar events |
| `rtl-generated-files` | Word, PDF, Excel, CSV and charts |

The `rtl-*` rule skills are instruction-only and also work in ChatGPT. The others need
a shell.

## Your private settings

The plugin ships no personal data. Signatures, letter sender details, newsletter brands
and house styles live in a folder of your own, by default
`~/.claude-user-data/rtl-skills/`, and override the built-ins by file name. It survives
updates and can be a private git repo. See
[`references/user-data.md`](references/user-data.md).

## Install

```
/plugin marketplace add danielrosehill/RTL-Skills
/plugin install rtl-skills@rtl-skills
```

Then run `setup-rtl`. Documents and letters need Typst and `poppler-utils`. Newsletter
and email previews need a Chromium-family browser.

## Why `verify-rtl-render` exists

Typst emits `warning: unknown font family: david libre` and compiles anyway, with a
Latin font that has no Hebrew. The exit code is 0 and the PDF still extracts every
Hebrew codepoint, so only the embedded font list shows it. See
[`references/fonts-and-rendering.md`](references/fonts-and-rendering.md).

## Credits

David Libre is included under the SIL Open Font License 1.1. The letter template comes
from [Typst-Hebrew-Letter](https://github.com/danielrosehill/Typst-Hebrew-Letter).

MIT licence.
