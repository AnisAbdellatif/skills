// Accessible, archival PDF. Compile:
//   typst compile accessible.typ --pdf-standard a-2a,ua-1
// Checks: title set, language set, alt text on every image/figure, semantic table header,
// decorative content marked as artifact.
#set document(title: [Accessible report], author: "Accessibility Team", keywords: ("a11y", "pdf"))
#set text(lang: "en", size: 11pt)
#set page(paper: "a4", numbering: "1")
#set heading(numbering: "1.")

#title()

= Overview
This document passes Typst's PDF/UA-1 checks. Headings, lists and tables are *semantic* elements, not visual tricks.

= Data
#figure(
  table(
    columns: 3,
    table.header[Region][Q2][Q3],
    [North], [120], [135],
    [South], [98], [104],
  ),
  caption: [Revenue per region. North grew by 12.5%; South by 6.1%.],
)

#figure(
  rect(width: 60%, height: 3cm, fill: gradient.linear(blue, teal)),
  alt: "Decorative gradient bar standing in for a chart; the data is in the table above.",
  caption: [Placeholder graphic.],
)

Inline math needs a text alternative for PDF/UA:
#math.equation(block: true, alt: "E equals m c squared", $ E = m c^2 $)

#pdf.artifact(line(length: 100%, stroke: 0.4pt + gray))   // purely decorative rule
