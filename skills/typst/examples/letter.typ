// Formal letter (DIN-5008-ish, A4).
#set document(title: "Letter")
#set page(paper: "a4", margin: (left: 2.5cm, right: 2cm, top: 2.5cm, bottom: 2cm))
#set text(font: "Libertinus Serif", size: 11pt, lang: "en")
#set par(justify: true, spacing: 1em)

#align(right)[Alex Example \ 1 Sample Street \ 12345 Town \ alex\@example.org]
#v(1.5cm)
Dr. Pat Recipient \ Example Institute \ 2 Other Road \ 54321 City

#align(right)[#datetime.today().display("[month repr:long] [day], [year]")]
#v(1cm)
*Subject: Application for the advertised position*

Dear Dr. Recipient,

#lorem(60)

#lorem(40)

Kind regards,

#v(1.2cm)
Alex Example
