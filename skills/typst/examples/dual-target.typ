// One source, PDF and HTML.
//   typst compile dual-target.typ                              (PDF)
//   typst compile dual-target.typ out.html --features html     (HTML, experimental)
#set document(title: "Dual target")
#set text(lang: "en")

= Hello
Regular *markup* works in both. Math becomes MathML in HTML (0.15): $a^2 + b^2 = c^2$.

#context if target() == "html" {
  html.div(class: "note")[This paragraph is HTML only. #html.span(style: "color: red")[styled]]
} else [
  This paragraph is only in paged output.
]

#figure(
  context if target() == "html" { html.frame(rect(width: 4cm, height: 1cm, fill: orange)) }
  else { rect(width: 4cm, height: 1cm, fill: orange) },
  caption: [Shapes rendered as inline SVG in HTML.],
)
