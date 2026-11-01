// Data-driven document: CSV → table, computed columns, JSON metadata, CLI inputs.
// typst compile data-report.typ --input client="ACME Corp"
#let client = sys.inputs.at("client", default: "Example Client")
#let rows = csv("data.csv", row-type: dictionary)
#let growth(r) = (float(r.q3) - float(r.q2)) / float(r.q2)
#let pct(x) = str(calc.round(x * 100, digits: 1)) + " %"

#set page(paper: "a4", margin: 2cm)
#set text(lang: "en", size: 10.5pt)
#set table(inset: 6pt, stroke: (x, y) => (bottom: if y == 0 { 0.8pt } else { 0.3pt + gray }))

= Sales report for #client

#table(
  columns: (1fr, auto, auto, auto),
  align: (left, right, right, right),
  table.header[*Region*][*Q2*][*Q3*][*Growth*],
  ..for r in rows {
    (r.region, r.q2, r.q3, text(fill: if growth(r) < 0 { red } else { green.darken(30%) }, pct(growth(r))))
  },
  table.hline(),
  [*Total*],
  [*#rows.map(r => int(r.q2)).sum()*],
  [*#rows.map(r => int(r.q3)).sum()*],
  [],
)

Best region: #rows.sorted(key: r => -growth(r)).first().region.

// Generated bar chart with plain shapes
#let maxv = calc.max(..rows.map(r => int(r.q3)))
#stack(dir: ttb, spacing: 4pt, ..rows.map(r => grid(
  columns: (3cm, 1fr), gutter: 6pt,
  align(right + horizon, r.region),
  rect(width: int(r.q3) / maxv * 100%, height: 10pt, fill: blue.lighten(30%)),
)))
