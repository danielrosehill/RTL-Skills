// Worked example — a formal letter to a fictional company, asking for a
// breakdown of charges under a service agreement.
//
// The content is invented and the addressee does not exist. It is here to
// exercise every part of the template at once and to show the shape a long
// formal letter takes: a head, a details block, a subject line, a notice the
// reader has to absorb first, numbered paragraphs under lettered sections, a
// quoted clause, an explicit list of what is being asked for, and enclosures.
//
// Copy this file, replace the content, and edit ../src/sender.typ once.

#import "profile.typ": *
#import "strings.typ" as strings

#let s = strings.he

#show: formal-doc.with(
  lang: "he",
  is-rtl: true,
  title: "בקשה לפירוט חיובים — חברת דוגמה בע\"מ",
  strings: s,
)

#doc-head(
  body: "חברת דוגמה בע\"מ · מחלקת שירות לקוחות",
  subtitle: "בקשה לפירוט חיובים ולקבלת מסמכי ההתקשרות",
  is-rtl: true,
)

#details(
  is-rtl: true,
  rows: (
    ("מאת", sender-block(labels: s, is-rtl: true)),
    ("אל", [חברת דוגמה בע\"מ — מחלקת שירות לקוחות \
      #text(size: 9.5pt, fill: muted)[רחוב העסקים 1, עיר הדוגמה ·
        service\@example.com]]),
    ("מספר לקוח", [00-000000]),
    ("אסמכתא", [XX/2026-08-05]),
    ("תאריך", [#dual-date(
        hebrew: "כ\"ב באב התשפ\"ו",
        gregorian: "5 באוגוסט 2026",
        is-rtl: true,
      )]),
  ),
)

#subject-line(
  text-body: "בקשה לפירוט חיובים בגין השנים 2024–2025 ולקבלת מסמכי ההתקשרות",
  is-rtl: true,
)

#notice(is-rtl: true)[
  #strong[מכתב זה הוא בקשה לקבלת מידע ואינו מכתב ביטול.] ההתקשרות עומדת בעינה,
  ואיני מבקש בשלב זה שינוי בתנאיה. ככל שחלק מן המבוקש אינו מצוי בידיכם, אבקש
  לקבל את יתרתו ולקבל הודעה בדבר החלק שאינו נמסר ומדוע.
]

= א. רקע

+ אני לקוח של החברה מאז שנת 2023, במסלול שירות חודשי מתחדש, ומספר הלקוח מופיע
  בראש מכתב זה.

+ בחשבוניות שהתקבלו במהלך השנים 2024 ו-2025 מופיעים סעיפי חיוב שאינם מפורטים
  לגופם, אלא תחת כותרת מרוכזת אחת. #strong[איני חולק על החיובים] — אני מבקש את
  פירוטם.

+ פניתי בעניין זה למוקד הטלפוני ב-15 ביולי 2026, ונמסר לי כי פירוט כאמור אינו
  זמין לנציגי המוקד וכי יש לפנות בכתב. #strong[מכתב זה הוא הפנייה בכתב.]

= ב. המבוקש

+ #strong[פירוט מלא של רכיבי החיוב החודשי] בכל אחד מחודשי השנים 2024 ו-2025, לפי
  רכיב ולפי סכום.

+ #strong[העתק של הסכם ההתקשרות התקף] ושל כל נספח או תיקון שנחתם לו מאז 2023.

+ פירוט של כל שינוי בתעריף שבוצע בתקופה זו, לרבות המועד שבו נכנס לתוקף והאופן
  שבו ניתנה עליו הודעה מוקדמת.

+ ככל שהמידע קיים בידיכם בקובץ ממוחשב, #strong[אבקש לקבלו כקובץ נתונים] — CSV או
  XLSX — ולא כמסמך סרוק. מסירת טבלה קיימת כסריקה מייקרת את הטיפול לשני הצדדים
  ללא תועלת לאיש.

= ג. לוח זמנים למענה

+ הסכם ההתקשרות קובע בעניין זה:

  #quote[החברה תמסור ללקוח, לבקשתו ובתוך 30 ימים ממועד הבקשה, פירוט של החיובים
  שנגבו ממנו בשנתיים שקדמו לבקשה. (סעיף 12.3 להסכם ההתקשרות)]

+ #strong[אבקש אישור קבלה למכתב זה] בתוך שבעה ימים, ובו מספר האסמכתא שתחתיה
  נרשמה הפנייה, כדי שניתן יהיה לעקוב אחריה.

= ד. אופן ההתקשרות

+ #strong[הדואר האלקטרוני הוא ערוץ הקשר המועדף] ואשיב בו במהירות. פרטי הקשר
  מופיעים בראש מכתב זה ובחתימתו.

+ מאחר שהפנייה נוגעת לנתונים ולסכומים, #strong[אבקש שכל תשובה מהותית תימסר לי
  בכתב] ולא בעל פה.

= ה. מסמכים מצורפים

#enum(
  numbering: "(1)",
  [העתקי החשבוניות שבמחלוקת הפרשנית, לשנים 2024–2025.],
  [תמצית ההתכתבות עם המוקד הטלפוני מיום 15 ביולי 2026.],
)

#v(8pt)

#signature(
  ref: "XX/2026-08-05",
  labels: s,
  is-rtl: true,
)
