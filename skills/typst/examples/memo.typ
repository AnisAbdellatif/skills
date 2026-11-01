// Short note / memo. Compile: typst compile memo.typ
#set document(title: "Project memo", author: "Team")
#set page(paper: "a4", margin: (x: 2.5cm, y: 2.5cm), numbering: "1")
#set text(font: "Libertinus Serif", size: 11pt, lang: "en")
#set par(justify: true, leading: 0.65em)

#grid(
  columns: (auto, 1fr),
  column-gutter: 1em,
  row-gutter: 0.5em,
  [*To:*], [Project team],
  [*From:*], [Alex Example],
  [*Date:*], [#datetime.today().display("[month repr:long] [day], [year]")],
  [*Subject:*], [Status update],
)
#line(length: 100%, stroke: 0.5pt)

#show heading.where(level: 1): set text(13pt)
#set heading(numbering: none)

= Summary
#lorem(40)

= Action items
+ Review the draft by Friday.
+ Send comments to the editor.
+ Prepare the final version.

= Next meeting
#lorem(20)
