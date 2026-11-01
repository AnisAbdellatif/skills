// Paper with abstract, equations, theorem-style environments, citations.
// Needs refs.bib next to it.
#set document(title: "On Typst", author: ("A. Author", "B. Writer"))
#set page(paper: "a4", margin: 2.2cm, numbering: "1", columns: 1)
#set text(font: "New Computer Modern", size: 10.5pt, lang: "en")
#set par(justify: true, first-line-indent: (amount: 1.2em, all: false), spacing: 0.65em, leading: 0.6em)
#set heading(numbering: "1.1")
#set math.equation(numbering: "(1)")
#show heading: set block(above: 1.3em, below: 0.7em)
#show heading.where(level: 1): set text(12pt)

// Simple theorem environments built from figures (shared look, own counters).
#let thm-style(kind, name) = body => figure(
  kind: kind, supplement: name, numbering: "1",
  block(width: 100%, inset: (y: 0.4em), align(left)[
    *#name #context counter(figure.where(kind: kind)).display().* #emph(body)
  ]),
)
#let theorem = thm-style("theorem", "Theorem")
#let lemma = thm-style("lemma", "Lemma")
#show figure.where(kind: "theorem"): set block(breakable: true)
#show figure.where(kind: "lemma"): set block(breakable: true)

#align(center)[
  #title() \
  #v(0.4em)
  A. Author, B. Writer \
  #text(9pt)[University of Somewhere]
]

#pad(x: 2em)[
  *Abstract.* We illustrate how a short research paper can be typeset with Typst:
  numbered equations, theorem-like environments, cross references, and a bibliography.
]

= Introduction <sec:intro>
Typesetting mathematics has a long history @knuth. In @sec:method we describe our approach,
and @eq:main states the main result.

= Method <sec:method>
Let $f: RR -> RR$ be continuous. Then
$ integral_0^1 f(x) dif x = lim_(n -> oo) 1/n sum_(k=1)^n f(k/n). $ <eq:main>

#theorem[Every bounded monotone sequence converges.] <thm:mono>
#lemma[If $a_n -> a$ then $abs(a_n) -> abs(a)$.]

_Proof of_ @thm:mono. Take the supremum; the details follow @knuth[p. 12]. $square$

#figure(
  table(columns: 3, table.header[$n$][$n^2$][$2^n$], [1], [1], [2], [2], [4], [4], [3], [9], [8]),
  caption: [Small table with math in headers.],
) <tab:small>

= Conclusion
We refer to @tab:small and @sec:intro again. #lorem(30)

#bibliography("refs.bib", style: "ieee")
