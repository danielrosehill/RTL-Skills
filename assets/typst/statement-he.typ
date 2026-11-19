// Worked example: a signed personal statement for circulation, with an annex.
//
// Use this shape, rather than letter-he.typ, when the document is not a request
// to one addressee but "this is what I say about X, as of this date", meant to
// be passed on (to neighbours, a committee, a lawyer). It differs from the
// letter in four ways:
//   - the addressee row is "to whom it may concern" (לכל מאן דבעי);
//   - the footer carries the document title and a confidentiality line on every
//     page (`footer-title`, `confidential`), so a loose printed page still says
//     what it is and how to handle it;
//   - the signature is dated and timed (`dated`), because a statement speaks as
//     of a moment and may later be updated;
//   - supporting material goes in a numbered annex after a page break, inside
//     the same PDF, so page "N of M" counts the whole bundle.
//
// The content is invented. Copy this file, replace the content, and keep the
// sender's details in sender.typ. For a shareable copy, leave the ID out of
// sender.typ (id: "") rather than blanking it here.

#import "profile.typ": *
#import "strings.typ" as strings

#let s = strings.he
#let title = "הצהרה בעניין רעש מאולם אירועים סמוך – נוסח מעודכן"

#show: formal-doc.with(
  lang: "he",
  is-rtl: true,
  title: title,
  strings: s,
  footer-title: true,
  confidential: s.confidential,
)

#doc-head(
  body: "הצהרה אישית",
  subtitle: "בעניין רעש מאולם אירועים הסמוך לבניין, רחוב הדוגמה 1",
  is-rtl: true,
)

#details(
  is-rtl: true,
  rows: (
    ("מאת", sender-block(labels: s, is-rtl: true)),
    ("אל", [לכל מאן דבעי]),
    ("תאריך", [#dual-date(
        hebrew: "כ\"ב באב התשפ\"ו",
        gregorian: "5 באוגוסט 2026",
        is-rtl: true,
      )]),
  ),
)

#notice(is-rtl: true)[
  #strong[זהו הנוסח העדכני של הצהרתי בעניין, נכון למועד החתימה.] הוא מחליף נוסחים
  קודמים, ומותר להעבירו הלאה כפי שהוא.
]

= א. העובדות

+ אני מתגורר בבניין ברחוב הדוגמה 1 מאז 2025.

+ בלילות רבים נשמעת בדירה מוזיקה מאולם האירועים הסמוך, גם כשהחלונות סגורים.

= ב. התיעוד

+ תיעוד הלילות מצוין בטבלה. #strong[קבצי המקור שמורים אצלי ללא עריכה.]

#v(8pt)

#signature(
  labels: s,
  is-rtl: true,
  dated: [נחתם ביום #dual-date(hebrew: "כ\"ב באב התשפ\"ו", gregorian: "5 באוגוסט 2026", is-rtl: true), בשעה 10:00],
)

#pagebreak()

= #s.annex א' – שיטת התיעוד

+ #strong[הנתונים אינם מדידה מכוילת.] הם נקודת נתונים לדוגמה ולא בדיקה מכרעת.
