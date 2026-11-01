// Slides without packages: 16:9 pages, one heading per slide. (touying/polylux give animations.)
#set page(paper: "presentation-16-9", margin: (x: 2cm, y: 1.5cm),
  footer: context [#set text(12pt, fill: gray); #h(1fr) #counter(page).display()])
#set text(size: 24pt, font: "Libertinus Serif", lang: "en")
#show heading.where(level: 1): it => { pagebreak(weak: true); set text(36pt); it; v(0.4em) }

#align(horizon + center)[
  #text(48pt, weight: "bold")[Talk title] \
  #v(1em) Speaker · Event · #datetime.today().display("[year]")
]

= Motivation
- Typst compiles fast
- Scripts are first-class
- Output is PDF, HTML, PNG, SVG

= Equation
$ integral_0^oo e^(-x^2) dif x = sqrt(pi)/2 $

= Two columns
#grid(columns: (1fr, 1fr), gutter: 1cm,
  [Left text #lorem(10)],
  rect(width: 100%, height: 4cm, fill: gradient.linear(teal, blue)))
