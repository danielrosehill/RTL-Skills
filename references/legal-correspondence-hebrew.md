# Legal-style Hebrew correspondence (מכתב דרישה / מכתב התראה)

Formatting directions for a letter that reads like it came from a lawyer's office: a
demand for information or action, sent by registered mail, that may later be exhibited.
These are drafting conventions, not legal advice. Have a lawyer draft anything with a
limitation period, litigation threat or settlement offer.

Built from a real letter (demand to a contractor and developer over construction noise,
2026-11). The structure carries over to complaints against companies, landlords,
authorities and service providers.

## Furniture, top to bottom

1. **Sender block** (top right): name, ת"ז if the recipient needs to identify you,
   address with apartment and postcode, phone, email. Put the email on its own line
   (see bidi notes).
2. **Date and route** (top left): `23.11.2026`, then `בדואר רשום` (and `ובדואר אלקטרוני`
   only if you really do email a copy as well).
3. **Without-prejudice line**, bold, above the addressee:
   `מבלי לפגוע בכל זכות או טענה`. ("ללא פגיעה בזכויות" is also seen. Use one.)
4. **Addressee**: `לכבוד`, the **legal name** with its registry number (ח.פ. / מס' שותפות),
   `לידי: המנהל הכללי` (or `השותף הכללי` for a limited partnership), and the
   **registered office including the care-of (אצל) line** from the registrar. A
   marketing or directory address is not enough.
5. **העתקים** (copies), smaller type: other parties, the authority, named individuals
   you already corresponded with (with their email), and any open reference numbers.
6. **Subject (הנדון)**, bold and centred: site or matter, the identifiers (gush/helka,
   file number, permit number), and what the letter is ("דרישה למידע ולמענה בכתב").
7. `אדונים נכבדים,` (to a company) or `שלום רב,`.

## Body: sections (פרקים) and numbered paragraphs (סעיפים)

- Group the body under lettered section headings: `א. הצדדים והאתר`, `ב. העובדות`,
  `ג. פניות קודמות שלא נענו`, `ד. המסגרת הנורמטיבית`, `ה. הדרישה`.
- **Number every paragraph continuously across the whole letter (1, 2, 3 … 19).
  Never restart per section.** Each numbered paragraph is a **סעיף**. The reply, and
  any later letter or court filing, will cite them ("כאמור בסעיף 9 לעיל",
  "בהמשך לסעיף 13 למכתבי"). Restarting numbering breaks that.
- Sub-items inside one סעיף: `(א)`, `(ב)`, `(ג)`. The demand list is the usual place.
- Refer to yourself as **הח"מ** (the undersigned), in the third person, throughout the body.
- One fact per סעיף. Dates in `D.M.YYYY`. Count days explicitly where it helps
  ("141 ימים ממועד הפנייה הראשונה").

## Citing law (the seif/takana distinction)

- A section of a **statute (חוק / פקודה)** is a **סעיף**: `סעיף 2 לחוק למניעת מפגעים, התשכ"א-1961`;
  `סעיף 44 לפקודת הנזיקין [נוסח חדש]`.
- A section of **regulations (תקנות)** is a **תקנה**: `תקנה 5 לתקנות למניעת מפגעים (מניעת רעש), התשנ"ג-1992`.
  Never write "סעיף 5 לתקנות".
- Municipal by-laws (חוק עזר) use סעיף: `סעיף 4 לחוק העזר לירושלים (מניעת רעש), התשס"ז-2007`.
- Guidance documents and appendices: `סעיף 2.2 ל"נספח הנחיות …" (נוסח מיום 2.12.2025)`.
- Give the full official name with the Hebrew year the first time, and a short form after.
  Cite only what you have read. Mark anything inferred as such in your own notes, not in the letter.

## The demand and the close

- **Demand** (one סעיף with (א)…(ז) sub-items): closed, answerable questions, a written
  reply, and a deadline counted from receipt: `בכתב ותוך 14 ימים ממועד קבלת מכתב זה`.
- **Consequence, measured**: e.g. `היעדר מענה נוסף ייזקף לחובתכם, ומכתב זה והפניות
  הקודמות ישמשו, ככל שיידרש, ראיה …`. Don't threaten proceedings you haven't decided on.
- **Parallel steps**: say so, factually (`במקביל … מוגשת בקשה לפי חוק חופש המידע`).
- **Reservation of rights**, always last: `אין באמור במכתב זה, או במה שלא נאמר בו, כדי
  לגרוע מכל זכות, טענה או סעד העומדים לח"מ על פי כל דין, וכל זכויותיו שמורות.`
- Sign-off: `בכבוד רב,`, a signature line, the name, then the identity line again.

## Typst notes (what went wrong the first time)

- **Continuous numbering:** Typst `+` enums restart after every heading. Write explicit
  `1.`, `2.`, … at the start of each paragraph (or renumber with a script), and use
  `#set enum(numbering: "(א)")` only inside the demand list.
- **Ranges and figures:** `70%–80%` written as two LTR spans renders reversed. Wrap the
  whole range in one span: `#L[70–80%]`. Do the same for dates, phone numbers, file
  numbers and anything with separators (`#L[2019/0588.01]`, `#L[02-376-3631]`).
- **Phone and email on one line** get reordered by the bidi algorithm. Give each its own line.
- **Signature orphaned on its own page:** wrap `בכבוד רב` through the signature block in
  `#block(breakable: false)[…]`, and tighten size/leading if the letter runs one line over.
- Keep the sender's ID number in a git-ignored include (e.g. `sender.local.typ`), never
  in a committed source file.
- Run `verify_render.py` and look at every page before sending. Check the page count, an
  orphaned signature, and reversed ranges.

## Sending

Registered mail is the norm for this kind of letter (proof of posting and delivery).
`israel-post:israel-post-registered-letter` sends a PDF as registered mail online.
Record the tracking number in the covering email and in your own correspondence log.
