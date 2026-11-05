---
name: rtl-email
description: Send or draft email whose body is in Hebrew, Arabic, Farsi or Urdu so it renders right-to-left in every mail client (Gmail, Outlook, Apple Mail), through any email tool (Gmail, Resend or another provider). Use whenever an email body, or a substantial part of it, is in an RTL script, including short replies. Rules for any tool; to send signed mail use send-rtl-personal-email or send-rtl-business-email, and for mailings write-rtl-newsletter.
---

# RTL email

Apply the rules in the rtl-basics skill. This skill adds what is specific to email.

## The one rule

**Never send an RTL body as plain text. Always send HTML with an explicit
`dir="rtl"`.** Plain-text email has no direction metadata, so each client guesses.
Gmail usually guesses right for pure Hebrew. Outlook often doesn't. Any URL, email
address or account number in a paragraph can tip the guess the wrong way. No
message is too short for this; a one-line reply gets the same treatment.

## Building the body

Start from `references/template.html`. It has no wrapper table, no fixed width and
no card: one-to-one mail should look typed. A centred 600px card puts its gutter on
the wrong side of an RTL message.

- Wrapper: `<div dir="rtl" lang="he" style="direction:rtl;text-align:right;line-height:1.7;font-family:Arial,'Noto Sans Hebrew',sans-serif;">`.
  Set **both** the `dir` attribute and the CSS. Outlook on Windows (Word engine)
  respects the attribute; webmail clients respect the CSS.
- **Every** `<p>`, `<td>`, `<li>` and `<div>` holding RTL text gets its own
  `dir="rtl"`. Mail clients rewrite HTML before display, and an inherited direction
  does not reliably survive.
- Multi-part numbers in LTR spans: `<span dir="ltr">02-123-4567</span>`. In a
  table, put the value in its own cell: `<td dir="ltr" align="right">…</td>`.
- The signature goes in a separate `<div dir="ltr">` below the RTL body if it is in
  Latin script. A Hebrew signature stays inside the RTL wrapper.
- `lang`: `he`, `ar`, `fa` or `ur`.

## Pass raw HTML, never escaped HTML

The failure that has actually happened: the body was written as
`&lt;div dir="rtl"&gt;` instead of `<div dir="rtl">`. The tool sent it as HTML,
returned a message ID, and the recipient saw the tags as text. **If the body you are
about to pass contains `&lt;` or `&gt;`, it is wrong. The first character of an
HTML body is a literal `<`.**

## Per tool

**Route: the Gmail API first. Use Resend only if Gmail fails**, and say the route changed.

- **Gmail-style tools:** pass the HTML as the body and set the body format or
  content type to HTML (often a parameter like `body_format: "html"` or
  `mimeType: text/html`). Leaving it out sends your markup as plain text, which is
  the worst result of all.
- **Resend:** pass the HTML in the `html` field. If there is also a `text` field,
  fill it with the plain-text fallback below. Resend never adds a signature, so
  include one.
- **A tool that only accepts plain text:** tell the user it cannot send correctly
  laid-out Hebrew. Offer to save a draft for them to send from their mail app, or to
  use a different tool. If they still want plain text, use the fallback below.
- **Drafts:** the same rules apply. A Hebrew draft saved as plain text opens
  left-to-right in the composer.

## Plain-text fallback

Use it as the text alternative of the HTML message, or when nothing else is
possible. Begin every paragraph with the RIGHT-TO-LEFT MARK, U+200F (the actual
invisible character). Put phone, account and reference numbers on lines of their
own. This only improves the odds; it does not make a client render RTL.

## Subject line

A pure-Hebrew subject needs nothing. For a mixed subject, put the Hebrew first. If
it still displays the wrong way round, prefix U+200F.

## After sending

For anything formal (a bank, health fund, municipality, landlord, employer) or
anything quoting an identifier, read the sent message back through your email tool
and check it:

| The body you read back shows | Meaning |
|---|---|
| Rendered text, no tags | Correct |
| `<div`, `<p>` or `dir=` as visible text | Escaped-HTML bug: send it again, correctly |
| Your HTML source, not rendered | Sent as plain text: the HTML flag was dropped |

## A letter attached as a PDF

When the real letter travels as a PDF, keep the email body to a few plain lines
with RLM marks (or minimal HTML) and let the PDF carry the content. See the
rtl-generated-files skill for producing the PDF.
