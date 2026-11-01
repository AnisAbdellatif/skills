// typst compile template-usage.typ
#import "template.typ": article, callout

#show: article.with(
  title: "Using a template",
  authors: ("Ada Lovelace", "Alan Turing"),
  abstract: [A template is just a function whose last argument is the document body.],
)

= Introduction
#lorem(40)

#callout[Templates keep content free of formatting.]

== Details
#lorem(30)
#callout(kind: "Warning")[Put `#show: ...` before any content.]
