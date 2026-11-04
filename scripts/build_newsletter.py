#!/usr/bin/env python3
"""Build an RTL newsletter from a content file and a brand file, then lint it.

Usage:
    build_newsletter.py content.json --brand brand.json --out DIR [--template T]

Writes DIR/newsletter.html, DIR/newsletter.txt and DIR/subject.txt. Exit 1 if the
lint fails. Standard library only. Nothing is sent.

content.json:
    {"subject": "...", "preheader": "...", "lang": "he",
     "label": "פרסומת",          // omitted: "פרסומת" for he; "" means no label
     "sections": [{"heading": "...", "body_html": "<p>...</p>",
                   "image_url": "...", "image_alt": "...",
                   "cta_text": "...", "cta_url": "https://..."}]}

brand.json:
    {"name": "...", "logo_url": "...", "accent": "#1f3a5f", "address": "...",
     "contact_email": "...", "unsubscribe_url": "...", "unsubscribe_email": "..."}
    unsubscribe_url may be a sending platform's merge tag. Lower-case tags such
    as {{ unsubscribe_url }} pass the lint; upper-case {{THIS}} are ours.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PLUGIN_ROOT") or Path(__file__).resolve().parents[1])
FONTS = {
    "he": "Arial,'Segoe UI',-apple-system,sans-serif",
    "ar": "Tahoma,Arial,'Segoe UI',sans-serif",
    "fa": "Tahoma,Arial,'Segoe UI',sans-serif",
    "ur": "Tahoma,Arial,'Segoe UI',sans-serif",
}
FOOTER = {
    "he": ("נשלח על ידי", "להסרה מרשימת התפוצה", "או בכתובת", "ליצירת קשר"),
    "ar": ("أُرسل من", "لإلغاء الاشتراك", "أو عبر", "للتواصل"),
    "fa": ("ارسال از", "لغو اشتراک", "یا از طریق", "تماس"),
    "ur": ("بھیجنے والا", "رکنیت ختم کریں", "یا", "رابطہ"),
}
BLOCK = re.compile(r"<(p|h[1-6]|ul|ol|li|blockquote)(\s[^>]*)?>", re.I)


def add_dir(fragment: str) -> str:
    """Put dir="rtl" and right alignment on every block tag missing them."""
    def fix(m: re.Match) -> str:
        tag, attrs = m.group(1), m.group(2) or ""
        if "dir=" in attrs.lower():
            return m.group(0)
        return f'<{tag} dir="rtl" align="right"{attrs}>' if tag.lower() != "li" else f'<{tag} dir="rtl"{attrs}>'
    return BLOCK.sub(fix, fragment)


def keep_runs(fragment: str) -> str:
    """Stop an LTR run such as AUTUMN-2026 breaking at its hyphen."""
    return re.sub(r'<span dir="ltr">', '<span dir="ltr" style="white-space:nowrap;">', fragment)


def section(s: dict, font: str, accent: str) -> str:
    cell = (f'<tr><td dir="rtl" align="right" class="nl-pad" style="padding:12px 32px;'
            f'direction:rtl;text-align:right;font-family:{font};font-size:16px;'
            f'line-height:1.7;color:#1a1a2e;">')
    out = [cell]
    if s.get("image_url"):
        out.append(f'<img class="nl-img" src="{html.escape(s["image_url"], True)}" '
                   f'alt="{html.escape(s.get("image_alt", ""), True)}" width="536" '
                   f'style="display:block;width:536px;max-width:100%;height:auto;margin:0 0 14px;border:0;">')
    if s.get("heading"):
        out.append(f'<h2 dir="rtl" align="right" style="margin:0 0 8px;font-size:21px;'
                   f'line-height:1.35;color:{accent};">{html.escape(s["heading"])}</h2>')
    out.append(keep_runs(add_dir(s.get("body_html", ""))))
    if s.get("cta_url"):
        out.append(f'<table role="presentation" dir="rtl" cellpadding="0" cellspacing="0" '
                   f'border="0" align="right" style="margin:10px 0 6px;"><tr>'
                   f'<td dir="rtl" align="center" bgcolor="{accent}" style="background:{accent};'
                   f'border-radius:4px;"><a dir="rtl" href="{html.escape(s["cta_url"], True)}" '
                   f'style="display:inline-block;padding:11px 24px;font-family:{font};'
                   f'font-size:16px;font-weight:bold;color:#ffffff;text-decoration:none;">'
                   f'{html.escape(s.get("cta_text", ""))}</a></td></tr></table>')
    out.append("</td></tr>")
    return "".join(out)


def to_text(subject: str, c: dict, b: dict, words: tuple) -> str:
    def strip(x: str) -> str:
        x = re.sub(r"</(p|li|h\d)>|<br\s*/?>", "\n", x, flags=re.I)
        return html.unescape(re.sub(r"<[^>]+>", "", x)).strip()
    parts = [subject, ""]
    for s in c["sections"]:
        if s.get("heading"):
            parts.append(s["heading"])
        parts.append(strip(s.get("body_html", "")))
        if s.get("cta_url"):
            parts.append(f'{s.get("cta_text", "")}: {s["cta_url"]}')
        parts.append("")
    parts += [f'{words[0]} {b["name"]}, {b.get("address", "")}',
              f'{words[1]}: {b.get("unsubscribe_url", "")} {b.get("unsubscribe_email", "")}'.strip()]
    return "\n".join(parts) + "\n"


def lint(doc: str, subject: str, c: dict, b: dict, label: str) -> list[str]:
    bad = []
    left = sorted(set(re.findall(r"\{\{[A-Z_]+\}\}", doc)))
    if left:
        bad.append(f"unfilled placeholders: {', '.join(left)}")
    if re.search(r"&lt;(p|div|table|h\d)\b", doc):
        bad.append("entity-escaped HTML in the body: it would show as visible tags")
    body = doc[doc.find("<body"):]
    for m in re.finditer(r"<(table|td|p|h[1-6]|ul|ol)\b[^>]*>", body, re.I):
        if "dir=" not in m.group(0).lower():
            bad.append(f"block without dir: {m.group(0)[:70]}")
    for req in ("name", "address"):
        if not b.get(req):
            bad.append(f"brand.{req} is empty: the footer must identify the sender")
    if not (b.get("unsubscribe_url") or b.get("unsubscribe_email")):
        bad.append("no unsubscribe route in the brand file")
    if label and not subject.startswith(label):
        bad.append(f"subject does not start with the label {label!r}")
    for i, s in enumerate(c["sections"]):
        if s.get("image_url") and not s.get("image_alt"):
            bad.append(f"section {i}: image has no alt text")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("content")
    ap.add_argument("--brand", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--template", default=str(ROOT / "assets/templates/newsletter.html"))
    a = ap.parse_args()
    c = json.loads(Path(a.content).read_text(encoding="utf-8"))
    b = json.loads(Path(a.brand).read_text(encoding="utf-8"))
    lang = c.get("lang", "he")
    font = FONTS.get(lang, FONTS["he"])
    accent = b.get("accent", "#1f3a5f")
    words = FOOTER.get(lang, FOOTER["he"])
    label = c.get("label", "פרסומת" if lang == "he" else "")
    subject = c["subject"]
    if label and not subject.startswith(label):
        subject = f"{label}: {subject}"

    if b.get("logo_url"):
        mast = (f'<img src="{html.escape(b["logo_url"], True)}" alt="{html.escape(b.get("name", ""), True)}" '
                f'height="40" style="display:block;height:40px;width:auto;border:0;">')
    else:
        mast = f'<div dir="rtl" style="font-size:20px;font-weight:bold;color:{accent};">{html.escape(b.get("name", ""))}</div>'

    unsub = []
    if b.get("unsubscribe_url"):
        unsub.append(f'<a dir="rtl" href="{html.escape(b["unsubscribe_url"], True)}" style="color:#5a6270;">{words[1]}</a>')
    if b.get("unsubscribe_email"):
        e = html.escape(b["unsubscribe_email"], True)
        lead = words[2] if unsub else words[1] + ":"
        unsub.append(f'{lead} <span dir="ltr"><a href="mailto:{e}" style="color:#5a6270;">{e}</a></span>')
    contact = ""
    if b.get("contact_email"):
        e = html.escape(b["contact_email"], True)
        contact = f'<br>{words[3]}: <span dir="ltr"><a href="mailto:{e}" style="color:#5a6270;">{e}</a></span>'
    footer = (f'{words[0]} {html.escape(b.get("name", ""))}, {html.escape(b.get("address", ""))}'
              f'{contact}<br>{" ".join(unsub)}')

    doc = Path(a.template).read_text(encoding="utf-8")
    doc = re.sub(r"<!--.*?-->\n?", "", doc, flags=re.S)
    for k, v in {
        "LANG": lang, "SUBJECT": html.escape(subject), "PREHEADER": html.escape(c.get("preheader", "")),
        "ACCENT": accent, "FONT_STACK": font, "MASTHEAD_HTML": mast, "FOOTER_HTML": footer,
        "SECTIONS_HTML": "\n".join(section(s, font, accent) for s in c["sections"]),
    }.items():
        doc = doc.replace("{{" + k + "}}", v)

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "newsletter.html").write_text(doc, encoding="utf-8")
    (out / "newsletter.txt").write_text(to_text(subject, c, b, words), encoding="utf-8")
    (out / "subject.txt").write_text(subject + "\n", encoding="utf-8")
    bad = lint(doc, subject, c, b, label)
    for x in bad:
        print(f"LINT: {x}", file=sys.stderr)
    print(f"wrote {out}/newsletter.html, newsletter.txt, subject.txt; lint problems: {len(bad)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
