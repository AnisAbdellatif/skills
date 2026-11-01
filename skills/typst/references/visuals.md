# Visuals: images, shapes, curves, colors, gradients, tilings

## Images

```typ-x
#image("figure.png", width: 60%)                 // png jpg gif webp svg pdf (0.14+: first/`page:` page of a PDF)
#image("logo.svg", height: 1cm, alt: "Company logo")
#image("photo.jpg", width: 5cm, height: 3cm, fit: "cover")   // fit: "cover" (default) | "contain" | "stretch"
#image("scan.png", scaling: "pixelated")      // viewer/PNG scaling for pixel art
#image("doc.pdf", page: 2, width: 100%)       // embed a PDF page (0.14)
#image(read("a.png", encoding: none), format: "png")   // from bytes (read(..., encoding: none) or generated)
#image(bytes(range(256).map(i => i)), format: (encoding: "luma8", width: 16, height: 16))  // raw pixels (0.13)
```

```typ
#image("a.png", width: 60%)
#box(image("a.png", height: 1em), baseline: 20%)
```

- Paths relative to the current file, `/x.png` project-root-relative; remote URLs are **not** supported (download first).
- `width`/`height` accept relative lengths; with only one given the aspect ratio is kept. In a `block(width: 5cm, height: 3cm, clip: true)` use `fit:`.
- Always add `alt:` (or put the image in a `figure(alt:)`) for accessible output; mark decorative images with `#pdf.artifact(image(...))`.
- Inline image in text: `#box(image("x.png", height: 1em))` (`baseline: 20%` to lower it).
- SVG: fonts in SVGs need to be installed; `<text>` is rendered via the installed fonts. Prefer converting text-heavy SVGs to paths.
- Image from plots: generate PNG/SVG with other tools; native alternatives are `cetz`, `lilaq`, `fletcher`.
- Image-as-background: `#set page(background: image("bg.jpg", width: 100%, height: 100%))`.
- `image(icc: ...)` to override/provide ICC profile; CMYK images work in PDF since 0.14.

## Shapes

```typ
#rect(width: 4cm, height: 1.5cm, fill: rgb("#e8f0fe"), stroke: 1pt + blue, radius: 4pt, inset: 8pt)[Label]
#square(size: 2cm, fill: red) #circle(radius: 1cm, fill: green.lighten(40%)) #ellipse(width: 3cm, height: 1cm)
#line(length: 100%, stroke: (paint: gray, thickness: 0.5pt, dash: "dashed"))
#line(start: (0pt, 0pt), end: (2cm, 1cm), stroke: 2pt + red)
#polygon(fill: yellow, stroke: 1pt, (0pt, 0pt), (2cm, 0pt), (1cm, 1.5cm))
#polygon.regular(vertices: 6, size: 2cm, fill: orange)
```

- Shapes with body content size to the content (`inset` default 5pt) unless `width`/`height` are set.
- `radius` can be per-corner: `(top-left: 4pt, rest: 0pt)`. `stroke` per side on rect: `(left: 2pt, rest: none)`.
- Place drawings absolutely: `#place(dx: 1cm, dy: 2cm, circle(radius: 5pt))` within a `box(width: 5cm, height: 3cm)`; or use `cetz` for full drawing.

## Curves (0.13+; replaces `path`)

```typ
#curve(
  fill: blue.lighten(80%), stroke: 1pt + blue,
  curve.move((0pt, 50pt)),
  curve.line((50pt, 0pt)),
  curve.cubic((60pt, 20pt), (80pt, 60pt), (100pt, 50pt)),   // control1, control2, end (use none/auto for smooth joins)
  curve.quad((120pt, 0pt), (150pt, 50pt)),
  curve.close(),
)
```

`relative: true` makes coordinates relative; `fill-rule: "even-odd"`; `curve.close(mode: "smooth"/"straight")`. `path()` was removed in 0.15.

## Colors

```typ
// named: red blue green yellow orange purple navy eastern aqua teal olive maroon fuchsia lime gray silver black white
#let palette = (luma(30%), rgb("#1e90ff"), rgb(30, 144, 255), rgb(30%, 56%, 100%, 80%), oklch(70%, 0.15, 250deg),
  cmyk(0%, 50%, 100%, 0%), color.hsl(120deg, 60%, 40%), color.linear-rgb(10%, 20%, 30%))
#let c = rgb("#d33")
#c.lighten(30%) #c.darken(20%) #c.saturate(20%) #c.desaturate(20%) #c.negate() #c.rotate(30deg) #c.transparentize(50%) #c.opacify(50%)
#c.to-hex() #c.components() #c.space() #color.mix(red, blue, space: oklab) #color.mix((red, 70%), (blue, 30%))
```

`rgb`, `luma`, `oklab`, `oklch`, `cmyk` are global; `hsl`, `hsv`, `linear-rgb` are namespaced: `color.hsl(...)`. Operations work in a perceptual color space (oklab) by default. Use `luma`/gray for text hierarchy (`luma(90)`); keep contrast high for accessibility (≥ 4.5:1). `color.map.viridis`, `inferno`, `magma`, `plasma`, `turbo`, `rocket`, `mako`, `vlag`, `icefire`, `coolwarm` (0.15), `spectral`, `rainbow`, `cividis`, `crest`, `flare` are arrays of colors for gradients.

Spot colors / separation colors (0.15) for print: see the `color` docs (`color.separation`).

## Gradients and tilings

```typ
#rect(width: 100%, height: 1cm, fill: gradient.linear(red, blue, angle: 45deg))
#rect(fill: gradient.linear(..color.map.viridis), width: 4cm, height: 1cm)
#circle(fill: gradient.radial(white, blue, center: (30%, 30%), radius: 70%))
#circle(fill: gradient.conic(red, yellow, green, red))
#text(fill: gradient.linear(red, blue), size: 24pt, weight: "bold")[Gradient text]
#gradient.linear((red, 0%), (blue, 100%), space: oklab, relative: "parent", dir: ltr)
#let g = gradient.linear(red, blue); #g.sample(30%) #g.stops() #g.repeat(3, mirror: true) #g.sharp(4)
#rect(width: 3cm, height: 1cm, fill: tiling(size: (10pt, 10pt))[#place(line(start: (0%, 100%), end: (100%, 0%)))])
```

`relative: "self"` (default for shapes) or `"parent"`; `gradient.sharp(n)` makes hard bands; `gradient.repeat`. Tilings (`tiling`, formerly `pattern`) repeat content as fill; `spacing:`, `relative:`, `offset:` (0.15).

## Strokes

```typ
#set line(stroke: 1pt + blue)
#rect(stroke: (paint: red, thickness: 2pt, cap: "round", join: "round", dash: "dotted", miter-limit: 4.0))
#rect(stroke: (top: 1pt, bottom: 2pt + red, rest: none))
// dash: "solid" "dotted" "densely-dotted" "loosely-dotted" "dashed" "densely-dashed" "loosely-dashed" "dash-dotted" ... or array/dict (array: (3pt, 2pt), phase:)
```

`stroke` can be a length, color, `length + color`, gradient/tiling paint, or dict. `stroke: auto` = default.

## Blend, clip, opacity

- Clip: `box(clip: true, ...)`, `block(clip: true)`; rounded clip with `radius`.
- Opacity: use colors with alpha (`rgb(0, 0, 0, 40%)`, `red.transparentize(50%)`); no `opacity()` function.
- Rotating/scaling content: `rotate`, `scale`, `skew` (see `styling-and-layout.md`).

## Drawing with packages

`cetz` (TikZ-like canvas), `fletcher` (flow/commutative diagrams), `lilaq` (scientific plots), `cetz-plot`, `diagraph` (Graphviz via WASM), `syntree`, `treet`, `pintorita`/`oxdraw` (UML/Mermaid-like), `timeliney`/`gantty` (Gantt). See `packages-and-ecosystem.md`. Minimal cetz:

```typ-x
#import "@preview/cetz:0.5.3": canvas, draw
#canvas(length: 1cm, {
  import draw: *
  circle((0, 0), radius: 1, fill: aqua)
  line((0, 0), (2, 1), mark: (end: ">"))
  content((2, 1), [point], anchor: "south-west")
})
```

(API changed between 0.1/0.2/0.3/0.4/0.5; check the package manual for the version you import.)

## Accessibility of visuals

- Provide `alt:` on images and `figure`s. Mark decorative shapes `#pdf.artifact(...)`. Do not rely on color alone; keep contrast. Avoid text inside images.
