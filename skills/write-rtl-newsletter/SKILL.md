---
name: write-rtl-newsletter
description: Generate a Hebrew or other RTL marketing email or newsletter as HTML. Use for "Hebrew newsletter", "campaign email", "ניוזלטר".
---

# Write an RTL newsletter

Produces a mailing as HTML plus a plain-text part and a subject line. **It doesn't
send.** For one-to-one mail use `send-rtl-personal-email` or
`send-rtl-business-email`, because a centred card reads as a mailing.

## Build

1. Pick a brand: `${CLAUDE_PLUGIN_ROOT}/scripts/paths.sh list brands`. If there is
   none, run `setup-rtl`. Never invent an address or an opt-out route.
2. Write `content.json`. The shape is in `examples/newsletter/content.json` and the
   header of `scripts/build_newsletter.py`. Wrap multi-part runs in
   `<span dir="ltr">`. The builder adds `dir="rtl"` to your blocks.
3. Build and lint:
   ```bash
   T=$(${CLAUDE_PLUGIN_ROOT}/scripts/paths.sh file templates/newsletter.html)
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build_newsletter.py content.json \
     --brand "$(${CLAUDE_PLUGIN_ROOT}/scripts/paths.sh dir)/brands/<name>.json" \
     --out out --template "$T"
   ```
   Exit 1 means the lint failed. Fix the cause rather than editing the output.
4. Look at it at both widths, because RTL layout bugs show at narrow widths:
   ```bash
   google-chrome --headless --hide-scrollbars --window-size=700,900 --screenshot=wide.png out/newsletter.html
   google-chrome --headless --hide-scrollbars --window-size=420,900 --screenshot=narrow.png out/newsletter.html
   ```
   A browser render doesn't prove Outlook is fine. Send a test through the real
   platform before a real send. Untested in Outlook as of 2026-11-04.

## Sending platforms

- Paste the full HTML into the platform's custom-HTML mode. A block editor will
  rewrite the markup and can drop `dir`.
- Put the platform's unsubscribe merge tag in the brand's `unsubscribe_url`.
  Lower-case tags pass the lint.
- If a platform takes a body only, keep the `<table dir="rtl">` wrapper. Some strip
  `<html>` and `<body>`, which is why `dir` is on every table and cell.
- Sending to a list is outward-facing: confirm the recipients and the final render
  with the user first.

## Israeli rules for advertising mail

Read from Communications Law (Bezeq and Broadcasts) 1982, section 30A, on Hebrew
Wikisource, 2026-11-04. This is a checklist, not legal advice.

- **Consent:** explicit prior written consent (30A(b)), with narrow exceptions such
  as existing customers, who must be able to refuse.
- **Label:** the word פרסומת opens the subject line, or בקשת תרומה or תעמולה where
  that fits. The builder adds פרסומת for Hebrew. Set `"label"` to change it, or to
  `""` only if the user confirms the mailing isn't advertising.
- **Sender:** the advertiser's name, address and contact details. The lint enforces
  name and address.
- **Refusal:** state the right to refuse at any time, with a simple route and a valid
  internet address for it. Refusal must be free, in writing or the way the ad was
  sent, as the recipient chooses. Give a link and an email address: a Central
  District Court ruling reported by a law firm held a link alone insufficient.
- Senders abroad may be covered if they target Israelis.

Other countries have their own rules, so ask where the list is if it isn't Israel.
