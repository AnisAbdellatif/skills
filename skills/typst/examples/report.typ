// Multi-section report with title page, outline, figures, tables, footnotes.
#let accent = rgb("#0b6e99")

#set document(title: "Quarterly report", author: "Analytics Team")
#set page(paper: "a4", margin: (x: 2.5cm, top: 3cm, bottom: 2.5cm),
  header: context {
    if counter(page).get().first() > 1 [
      #set text(9pt, fill: luma(100))
      Quarterly report #h(1fr) #counter(page).display("1 / 1", both: true)
    ]
  })
#set text(font: "Libertinus Serif", size: 11pt, lang: "en")
#set par(justify: true, leading: 0.65em, spacing: 1.2em)
#set heading(numbering: "1.1")
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(1em)
  text(accent, 18pt, weight: "bold", it)
  v(0.5em)
}
#show heading.where(level: 2): set text(accent, 13pt)
#show link: set text(accent)
#show figure.caption: set text(9pt)
#set table(stroke: (x, y) => (
  top: if y <= 1 { 0.8pt } else { 0.3pt },
  bottom: 0.8pt,
))

// Title page (no header, no number)
#page(numbering: none, header: none)[
  #v(1fr)
  #align(left)[
    #text(28pt, weight: "bold", fill: accent)[Quarterly Report] \
    #v(0.5em)
    #text(14pt)[Q3 results and outlook] \
    #v(2em)
    #text(11pt)[Analytics Team · #datetime.today().display("[month repr:long] [year]")]
  ]
  #v(2fr)
]
#counter(page).update(1)

#outline(depth: 2)

= Introduction <intro>
#lorem(60) See @results for the numbers and @fig:trend for the trend.

= Results <results>
== Revenue
#figure(
  table(
    columns: (1fr, auto, auto),
    align: (left, right, right),
    table.header[*Region*][*Q2*][*Q3*],
    [North], [120], [135],
    [South], [98], [104],
    table.hline(),
    [*Total*], [*218*], [*239*],
  ),
  caption: [Revenue in thousands.],
) <tab:rev>

As @tab:rev shows, growth was steady#footnote[Figures are unaudited.].

== Trend
#figure(
  rect(width: 70%, height: 4cm, fill: gradient.linear(accent.lighten(70%), accent)),
  caption: [Placeholder for a chart.],
) <fig:trend>

= Outlook
#lorem(80)
