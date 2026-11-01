// Export structure with `typst eval`:
//   typst eval --in query-export.typ 'query(<doc-info>).first().value' --pretty
//   typst eval --in query-export.typ 'query(heading).map(h => (level: h.level, page: h.location().page()))' --pretty
//   typst eval --in query-export.typ 'query(<page-count>).first().value'   (counters need `context`, so the doc exports it)
#set page(width: 10cm, height: 8cm, numbering: "1")
#set heading(numbering: "1.")
#metadata((title: "Product spec", version: "2.1.0", status: "draft")) <doc-info>

= Scope
#lorem(30)
#pagebreak()
= Design
== Interfaces
#lorem(20)
#context [
  Pages: #counter(page).final().first(), headings: #query(heading).len()
]
#context [#metadata(counter(page).final().first()) <page-count>]
