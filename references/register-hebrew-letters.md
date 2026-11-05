# Register in Hebrew correspondence

## The rule

**Formality follows the recipient, not the language.** Writing in Hebrew does not
make a message formal, and a Hebrew message to a friend should not carry `לכבוד`.

| Recipient | Register |
| --- | --- |
| Friend, family, colleague | Informal. First name, plain opening and closing. |
| Vendor, shop, tradesperson | Neutral. Polite, no honorifics, no identifiers. |
| Bank, insurer, utility, HMO | Formal. `לכבוד`, `בכבוד רב`, account/reference in the sign-off. |
| Municipality, ministry, regulator, ombudsman | Formal, with filing identifiers repeated in the sign-off. |

## Formal openings

```
לכבוד
<שם הגוף>
<מחלקה>

הנדון: <נושא הפנייה>
```

`הנדון:` is the subject line inside the letter body — keep it short and factual;
it is what gets quoted back in a file reference.

## Formal closings

```
בכבוד רב,
<שם>
<תפקיד, אם רלוונטי>
<עוסק מורשה / ח.פ. — for business correspondence>
<טלפון> | <דוא״ל>
```

For business correspondence the `עוסק מורשה` number belongs in the sign-off, not
the letterhead.

## Reference numbers

Repeat every identifier the recipient will need to route the message — account
number, claim number, complaint reference, previous letter's date — in the
sign-off as well as the body. A formal Hebrew letter that arrives without them
gets filed rather than actioned.

Wrap bare identifiers in `<bdi>` in HTML, or rely on the isolate handling in
`eml_toolkit`, so they do not reorder inside RTL text.

## Dating

Formal letters carry both Hebrew and Gregorian dates. The Typst template does
this; for the Hebrew date alone use `https://www.hebcal.com/converter?cfg=json&date=YYYY-MM-DD&g2h=1&strict=1`
(public, no key).
