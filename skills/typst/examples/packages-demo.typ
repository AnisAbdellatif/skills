// Verified against Typst 0.15.1 with these exact package versions (first compile downloads them).
// Re-check versions with: python3 ../scripts/search-packages.py --name cetz
#import "@preview/cetz:0.5.3": canvas, draw
#import "@preview/fletcher:0.5.8": diagram, node, edge
#import "@preview/codly:2.0.0" as codly           // 2.x API differs from 1.x (no codly-init)
#import "@preview/lilaq:0.6.0" as lq
#import "@preview/theorion:0.6.0": *
#import cosmos.clouds: *
#show: show-theorion
#show raw.where(block: true): codly.new

#set page(width: 14cm, height: auto, margin: 1cm)

== CeTZ drawing
#canvas(length: 1cm, {
  import draw: *
  circle((0, 0), radius: 0.8, fill: aqua)
  line((0, 0), (2, 1), mark: (end: ">"))
  content((2, 1), [point], anchor: "south-west")
})

== Fletcher diagram
#diagram(
  node((0, 0), [A]), edge("->", [f]), node((1, 0), [B]),
  edge((0, 0), (1, 1), "->", bend: 20deg), node((1, 1), [C]),
)

== Lilaq plot
#lq.diagram(width: 6cm, height: 4cm, lq.plot((1, 2, 3, 4), (2, 4, 3, 5)))

== Theorem (theorion)
#theorem(title: "Pythagoras")[$a^2 + b^2 = c^2$]
#proof[Trivial.]

== Codly code block
```python
def f(x):
    return x + 1
```
