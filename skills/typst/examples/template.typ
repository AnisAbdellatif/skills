// Reusable template: import and apply with `#show: article.with(...)`.
#let article(
  title: none,
  authors: (),
  date: auto,
  abstract: none,
  lang: "en",
  accent: rgb("#8a1c1c"),
  body,
) = {
  set document(title: title, author: authors)
  set page(paper: "a4", margin: (x: 2.5cm, y: 2.5cm), numbering: "1")
  set text(font: "Libertinus Serif", size: 11pt, lang: lang)
  set par(justify: true)
  set heading(numbering: "1.1")
  show heading: set text(fill: accent)
  show heading.where(level: 1): set block(above: 1.6em, below: 0.9em)

  align(center)[
    #text(20pt, weight: "bold", fill: accent, title)
    #v(0.3em)
    #authors.join(", ", last: " and ")
    #if date != none [\ #if date == auto { datetime.today().display() } else { date }]
  ]
  if abstract != none {
    pad(x: 1.5cm, y: 1em, block(fill: luma(245), inset: 10pt, radius: 3pt)[*Abstract.* #abstract])
  }
  body
}

// A reusable component
#let callout(body, kind: "Note") = block(
  fill: rgb("#fff4e5"), stroke: (left: 2pt + orange), inset: 8pt, width: 100%,
)[*#kind.* #body]
