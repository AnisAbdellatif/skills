# API signatures (Typst 0.15.1)

Machine-extracted from the `typst-library` sources at tag `v0.15.1` (element fields = what `set` rules can configure unless marked positional/required). Notation: `name(param: type = default)`; `auto|X` = `auto` or X; `none|X`; `rel` = relative length (`50%`, `2cm + 10%`); `paint` = color, gradient or tiling; `stroke` = length / color / `length + color` / dictionary; `[]X` = array of X; `*` = also accepts an array (per column) or a function `(x, y) => value`; `..children` = variadic positional; `(body)` = trailing content argument. Types printed in CamelCase (e.g. `Margin`, `FigureKind`) are described in the docs/other references. **Verify uncertain items with a compile probe.**

## How to read this
- Positional parameters appear without defaults (`align(alignment, body)`); named parameters have `name: type`.
- Everything in "named" can appear in `#set elem(name: value)`. Parameters of functions that are not elements (e.g. methods) are in the second part.
- `context`-only reads: `text.size`, `par.leading`, … are readable inside `context` for every settable parameter: `#context par.leading`.

### Introspection

- `metadata(value)` — Exposes a value to the query system without producing visible content.

### Layout

- `align(alignment: alignment, body)` — Aligns content horizontally and vertically.
- `columns(count: int, gutter: rel = 4%, body)` — Separates a region into multiple equally sized columns.
- `colbreak(weak: bool = false)` — Forces a column break.
- `box(width: auto|rel|fr, height: auto|rel, baseline: BaselinePos, fill: none|paint, stroke: none|stroke, radius: none|rel, inset: none|rel, outset: none|rel, clip: bool = false, body: none|content)` — An inline-level container that sizes content.
- `block(width: auto|rel, height: auto|rel|fr, breakable: bool = true, fill: none|paint, stroke: none|stroke, radius: none|rel, inset: none|rel, outset: none|rel, spacing: auto|rel|fr, above: auto|rel|fr, below: auto|rel|fr, clip: bool = false, sticky: bool = false, body: none|BlockBody)` — A block-level container.
- `grid(columns: tracks, rows: tracks, gutter: tracks, column-gutter: tracks, row-gutter: tracks, inset: none|rel*, align: auto|alignment*, fill: none|paint*, stroke: none|stroke*, ..children)` — Arranges content in a grid.
- `grid.header(repeat: bool = true, level: int = 1, ..children)` — A repeatable grid header.
- `grid.footer(repeat: bool = true, ..children)` — A repeatable grid footer.
- `grid.hline(y: auto|int, start: int, end: none|int, stroke: none|stroke, position: OuterValignment)` — A horizontal line in the grid.
- `grid.vline(x: auto|int, start: int, end: none|int, stroke: none|stroke, position: OuterHalignment)` — A vertical line in the grid.
- `grid.cell(body, x: auto|int, y: auto|int, colspan: int = 1, rowspan: int = 1, inset: auto|none|rel, align: auto|alignment, fill: auto|none|paint, stroke: none|stroke, breakable: auto|bool)` — A cell in the grid. You can use this function in the argument list of a grid
- `hide(body)` — Hides content without affecting layout.
- `pad(left: rel, top: rel, right: rel, bottom: rel, x: rel, y: rel, rest: rel, body)` — Adds spacing around content.
- `page(paper: Paper, width: auto|length, height: auto|length, flipped: bool = false, margin: auto|Margin<Smart<rel>>, bleed: Margin<rel>, binding: auto|Binding, columns: int = 1, fill: auto|none|paint, numbering: none|numbering, supplement: auto|none|content, number-align: Specificalignment<Halignment, OuterValignment>, header: auto|none|content, header-ascent: rel = 30%, footer: auto|none|content, footer-descent: rel = 30%, background: none|content, foreground: none|content, body)` — Layouts its child onto one or multiple pages.
- `pagebreak(weak: bool = false, to: none|Parity)` — A manual page break.
- `place(alignment: auto|alignment, scope: PlacementScope, float: bool, clearance: length = 1.5em, dx: rel, dy: rel, body)` — Places content relatively to its parent container.
- `flush()` — Asks the layout algorithm to place pending floating elements before
- `repeat(body, gap: length, justify: bool = true)` — Repeats content to the available space.
- `h(amount, weak: bool = false)` — Inserts horizontal spacing into a paragraph.
- `v(amount, weak: bool)` — Inserts vertical spacing into a flow of blocks.
- `stack(dir: direction, spacing: none|rel|fr, ..children)` — Arranges content and spacing horizontally or vertically.
- `move(dx: rel, dy: rel, body)` — Moves content without affecting layout.
- `rotate(angle: angle, origin: alignment, reflow: bool = false, body)` — Rotates content without affecting layout.
- `scale(factor: auto|ScaleAmount, x: auto|ScaleAmount, y: auto|ScaleAmount, origin: alignment, reflow: bool = false, body)` — Scales content without affecting layout.
- `skew(ax: angle, ay: angle, origin: alignment, reflow: bool = false, body)` — Skews content.

### Math

- `math.accent(base, accent, size: rel, dotless: bool = true)` — Attaches an accent to a base.
- `math.attach(base, t: none|content, b: none|content, tl: none|content, bl: none|content, tr: none|content, br: none|content)` — A base with optional attachments.
- `math.primes(count)` — Grouped primes.
- `math.scripts(body)` — Forces a base to display attachments as scripts.
- `math.limits(body, inline: bool = true)` — Forces a base to display attachments as limits.
- `math.stretch(body, size: rel)` — Stretches a glyph.
- `math.cancel(body, length: rel, inverted: bool = false, cross: bool = false, angle: auto|Cancelangle, stroke: stroke)` — Displays a diagonal line over a part of an equation.
- `math.equation(block: bool = false, numbering: none|numbering, number-align: Specificalignment<OuterHalignment, Valignment>, supplement: auto|none|Supplement, alt: none|str, body)` — A mathematical equation.
- `math.frac(num, denom, style: FracStyle)` — A mathematical fraction.
- `math.binom(upper, lower: []content)` — A binomial expression.
- `math.lr(size: rel, body: content)` — Scales delimiters.
- `math.mid(body)` — Scales delimiters vertically to the nearest surrounding `{lr()}` group.
- `math.vec(delim: DelimiterPair, align: Halignment, gap: rel, ..children)` — A column vector.
- `math.mat(delim: DelimiterPair, align: Halignment, augment: none|Augment, gap: rel, row-gap: rel, column-gap: rel, rows: []Vec<content>)` — A matrix.
- `math.cases(delim: DelimiterPair, reverse: bool = false, gap: rel, ..children)` — A case distinction.
- `math.class(class, body)` — Forced use of a certain math class.
- `math.op(text, limits: bool = false)` — A text operator in an equation.
- `math.root(index: none|content, radicand)` — A general root.
- `math.underline(body)` — A horizontal line under content.
- `math.overline(body)` — A horizontal line over content.
- `math.underbrace(body, annotation: none|content)` — A horizontal brace under content, with an optional annotation below.
- `math.overbrace(body, annotation: none|content)` — A horizontal brace over content, with an optional annotation above.
- `math.underbracket(body, annotation: none|content)` — A horizontal bracket under content, with an optional annotation below.
- `math.overbracket(body, annotation: none|content)` — A horizontal bracket over content, with an optional annotation above.
- `math.underparen(body, annotation: none|content)` — A horizontal parenthesis under content, with an optional annotation below.
- `math.overparen(body, annotation: none|content)` — A horizontal parenthesis over content, with an optional annotation above.
- `math.undershell(body, annotation: none|content)` — A horizontal tortoise shell bracket under content, with an optional
- `math.overshell(body, annotation: none|content)` — A horizontal tortoise shell bracket over content, with an optional

### Model

- `bibliography(sources: OneOrMultiple<DataSource>, title: auto|none|content, full: bool = false, style: CslSource, target: auto|LocatableSelector, group: none|auto|str)` — A bibliography / reference listing.
- `cite(key, supplement: none|content, form: none|CitationForm, style: auto|CslSource)` — Cite a work from the bibliography.
- `divider()` — A thematic break that separates sections of content.
- `document(path, format: auto|DocumentFormat, title: none|content, author: OneOrMultiple<str>, description: none|content, keywords: OneOrMultiple<str>, date: auto|none|Datetime, body)` — Manages metadata and is used to add a document file to a bundle.
- `emph(body)` — Emphasizes content by toggling italics.
- `enum(tight: bool = true, numbering: numbering, start: auto|int, full: bool = false, reversed: bool = false, indent: length, body-indent: length = 0.5em, spacing: auto|length, number-align: alignment, children: []EnumItem)` — A numbered list.
- `enum.item(number: auto|int, body)` — An enumeration item.
- `figure(body, alt: none|str, placement: none|auto|Valignment, scope: PlacementScope, caption: none|FigureCaption, kind: auto|FigureKind, supplement: auto|none|Supplement, numbering: none|numbering, gap: length = 0.65em, outlined: bool = true, counter: none|Counter)` — A figure with an optional caption.
- `figure.caption(position: OuterValignment, separator: auto|content, body, kind: FigureKind, supplement: none|content, numbering: none|numbering, counter: none|Counter)` — The caption of a figure. This element can be used in set and show rules to
- `footnote(numbering: numbering, body)` — A footnote.
- `footnote.entry(note, separator: content, clearance: length = 1.0em, gap: length = 0.5em, indent: length = 1.0em)` — An entry in a footnote list.
- `heading(level: auto|int, depth: int = 1, offset: int = 0, numbering: none|numbering, supplement: auto|none|Supplement, outlined: bool = true, bookmarked: auto|bool, hanging-indent: auto|length, body)` — A section heading.
- `link(dest: LinkTarget, body: content)` — Links to a URL or a location in the document.
- `list(tight: bool = true, marker: ListMarker, indent: length, body-indent: length = 0.5em, spacing: auto|length, marker-align: alignment, ..children)` — A bullet list.
- `list.item(body)` — A bullet list item.
- `outline(title: auto|none|content, target: LocatableSelector, depth: none|int, indent: auto|OutlineIndent)` — A table of contents, figures, or other elements.
- `outline.entry(level, element, fill: none|content)` — Represents an entry line in an outline.
- `par(leading: length = 0.65em, spacing: length = 1.2em, justify: bool = false, justification-limits: JustificationLimits, linebreaks: auto|Linebreaks, first-line-indent: FirstLineIndent, hanging-indent: length, body)` — A logical subdivison of textual content.
- `par.line(numbering: none|numbering, number-align: auto|Halignment, number-margin: OuterHalignment, number-clearance: auto|length, numbering-scope: LinenumberingScope)` — A paragraph line.
- `quote(block: bool, quotes: auto|bool, attribution: none|Attribution, body)` — Displays a quote alongside an optional attribution.
- `ref(target, supplement: auto|none|Supplement, form: RefForm, citation: none|CiteElem, element: none|content)` — A reference to a label or bibliography.
- `strong(delta: int = 300, body)` — Strongly emphasizes content by increasing the font weight.
- `table(columns: tracks, rows: tracks, gutter: tracks, column-gutter: tracks, row-gutter: tracks, inset: none|rel*, align: auto|alignment*, fill: none|paint*, stroke: none|stroke*, ..children)` — A table of items.
- `table.header(repeat: bool = true, level: int = 1, ..children)` — A repeatable table header.
- `table.footer(repeat: bool = true, ..children)` — A repeatable table footer.
- `table.hline(y: auto|int, start: int, end: none|int, stroke: none|stroke, position: OuterValignment)` — A horizontal line in the table.
- `table.vline(x: auto|int, start: int, end: none|int, stroke: none|stroke, position: OuterHalignment)` — A vertical line in the table. See the docs for @grid.vline for more
- `table.cell(body, x: auto|int, y: auto|int, colspan: int = 1, rowspan: int = 1, inset: auto|none|rel, align: auto|alignment, fill: auto|none|paint, stroke: none|stroke, breakable: auto|bool)` — A cell in the table. Use this to position a cell manually or to apply
- `terms(tight: bool = true, separator: content, indent: length, hanging-indent: length = 2.0em, spacing: auto|length, children: []TermItem)` — A list of terms and their descriptions.
- `terms.item(term, description)` — A term list item.
- `title(body: auto|content)` — A document title.

### PDF

- `pdf.artifact(kind: ArtifactKind, body)` — 
- `pdf.attach(path: PathOrStr, data: Bytes, relationship: none|AttachedFileRelationship, mime-type: none|str, description: none|str)` — A file that will be attached to the output PDF.

### Text

- `underline(stroke: auto|stroke, offset: auto|length, extent: length, evade: bool = true, background: bool = false, body)` — Underlines text.
- `overline(stroke: auto|stroke, offset: auto|length, extent: length, evade: bool = true, background: bool = false, body)` — Adds a line over text.
- `strike(stroke: auto|stroke, offset: auto|length, extent: length, background: bool = false, body)` — Strikes through text.
- `highlight(fill: none|paint, stroke: none|stroke, top-edge: TopEdge, bottom-edge: BottomEdge, extent: length, radius: none|rel, body)` — Highlights text with a background color.
- `linebreak(justify: bool = false)` — Inserts a line break.
- `text(font: FontList, fallback: bool = true, style: FontStyle, weight: FontWeight, stretch: FontStretch, size: TextSize, fill: paint, stroke: none|stroke, tracking: length, spacing: rel, cjk-latin-spacing: auto|none|Never, baseline: length, overhang: bool = true, top-edge: TopEdge, bottom-edge: BottomEdge, lang: Lang, region: none|Region, script: auto|WritingScript, dir: Textdirection, hyphenate: auto|bool, costs: Costs, kerning: bool = true, alternates: Alternates, stylistic-set: StylisticSets, ligatures: bool = true, discretionary-ligatures: bool = false, historical-ligatures: bool = false, number-type: auto|NumberType, number-width: auto|NumberWidth, slashed-zero: bool = false, fractions: bool = false, features: FontFeatures, variations: FontVariations, body, text)` — Customizes the look and layout of text in a variety of ways.
- `raw(text, block: bool = false, lang: none|str, align: Halignment, syntaxes: OneOrMultiple<DataSource>, theme: auto|none|DataSource, tab-size: int = 2, lines: []RawLine)` — Raw text with optional syntax highlighting.
- `raw.line(number, count, text, body)` — A highlighted line of raw text.
- `sub(typographic: bool = true, baseline: auto|length, size: auto|TextSize, body)` — Renders text in subscript.
- `super(typographic: bool = true, baseline: auto|length, size: auto|TextSize, body)` — Renders text in superscript.
- `smallcaps(all: bool = false, body)` — Displays text in small capitals.
- `smartquote(double: bool = true, enabled: bool = true, alternative: bool = false, quotes: auto|SmartQuoteDict)` — A language-aware quote that reacts to its context.

### Visualize

- `curve(fill: none|paint, fill-rule: FillRule, stroke: auto|none|stroke, ..components)` — A curve consisting of movements, lines, and Bézier segments.
- `curve.move(start, relative: bool = false)` — Starts a new curve component.
- `curve.line(end, relative: bool = false)` — Adds a straight line from the current point to a following one.
- `curve.quad(control, end, relative: bool = false)` — Adds a quadratic Bézier curve segment from the last point to `end`, using
- `curve.cubic(control-start, control-end, end, relative: bool = false)` — Adds a cubic Bézier curve segment from the last point to `end`, using
- `curve.close(mode: CloseMode)` — Closes the curve by adding a segment from the last point to the start of the
- `image(source: DataSource, format: auto|ImageFormat, width: auto|rel, height: auto|rel|fr, alt: none|str, page: int = 1, fit: ImageFit, scaling: auto|ImageScaling, icc: auto|DataSource)` — A raster or vector graphic.
- `line(start: Axes<rel>, end: none|Axes<rel>, length: rel, angle: angle, stroke: stroke)` — A line from one point to another.
- `polygon(fill: none|paint, fill-rule: FillRule, stroke: auto|none|stroke, ..vertices)` — A closed polygon.
- `rect(width: auto|rel, height: auto|rel|fr, fill: none|paint, stroke: auto|none|stroke, radius: none|rel, inset: none|rel, outset: none|rel, body: none|content)` — A rectangle with optional content.
- `square(size: auto|length, width: auto|rel, height: auto|rel|fr, fill: none|paint, stroke: auto|none|stroke, radius: none|rel, inset: none|rel, outset: none|rel, body: none|content)` — A square with optional content.
- `ellipse(width: auto|rel, height: auto|rel|fr, fill: none|paint, stroke: auto|none|stroke, inset: none|rel, outset: none|rel, body: none|content)` — An ellipse with optional content.
- `circle(radius: length, width: auto|rel, height: auto|rel|fr, fill: none|paint, stroke: auto|none|stroke, inset: none|rel, outset: none|rel, body: none|content)` — A circle with optional content.

## Non-element functions, constructors and methods

### Foundations
- **Constructors**: `int(v, base: 10)`, `float(v)`, `decimal(v)`, `str(v, base: 10)`, `bytes(v)`, `array(v)`, `dictionary(module)` (module → dict; pairs → dict via `array.to-dict()`), `label(name)`, `symbol(...)`, `version(..)`, `datetime(year:, month:, day:, hour:, minute:, second:)`, `duration(seconds:, minutes:, hours:, days:, weeks:)`, `arguments(..)`, `path(str)` (0.15), `regex(str)`, `selector(x)`, `counter(x)`, `state(key, init)`, `type(v)`, `repr(v)`, `panic(..)`, `assert(cond, message:)`, `assert.eq/ne`, `eval(src, mode: "code"|"markup"|"math", scope:)`, `plugin(src)`, `target()`.
- **Modules**: `calc`, `sys` (`version`, `inputs`), `std`, `sym`, `emoji`, `math`, `pdf`, `html`, `color` (`color.map.*`, `color.mix`), `gradient`, `tiling`, `str`, `array`, `dictionary`, `float`, `int`, `datetime`, `duration`, `bytes`, `content` (methods only).
- **`calc`**: `abs pow exp sqrt root sin cos tan asin acos atan atan2 sinh cosh tanh asinh acosh atanh log(value, base:) ln fact perm binom gcd lcm floor ceil trunc fract round(v, digits:) clamp(v, min, max) min(..) max(..) even odd rem(a, b) div-euclid rem-euclid quo norm(..) erf` + constants `pi tau e inf nan`.
- **`str` methods**: `len first(default:) last(default:) at(i, default:) slice(start, end?, count:) clusters codepoints contains(pat) starts-with ends-with find position match matches replace(pat, with, count:) split(pat?) trim(pat?, at:, repeat:) rev normalize(form:)`; statics `str.to-unicode(c)`, `str.from-unicode(n)`; top-level `lower() upper()`.
- **`array` methods**: `len first last at push pop insert remove slice contains find position range filter map enumerate(start:) zip(..others, exact:) fold(init, f) reduce(f) sum(default:) product(default:) any all flatten rev split join(sep, last:) intersperse chunks(n, exact:) windows(n) dedup(key:) sorted(key:) to-dict()`; `array.range(..)`.
- **`dictionary` methods**: `len at(key, default:) insert remove keys values pairs filter map` (0.15).
- **`arguments`**: `.pos()`, `.named()`, `.at(k, default:)`, field access `args.name` (0.15), `.filter/.map` (0.15).
- **`content`**: `.func() .fields() .has(f) .at(f, default:) .location()`.
- **`function`**: `f.with(..args)`, `elem.where(..fields)` → selector. `within` exists only on selectors (`selector(heading).within(<a>)` or `heading.where(level: 2).within(<a>)`), not on bare element functions.
- **`selector`**: `.or(..) .and(..) .before(loc, inclusive:) .after(loc, inclusive:) .within(sel)` (0.15).
- **`datetime`**: `.year() .month() .day() .weekday() .hour() .minute() .second() .ordinal() .display(fmt)`; `datetime.today(offset: auto|int|duration)`; format strings like `"[year]-[month padding:zero]-[day] [hour]:[minute]"`, `"[month repr:long]"`, `"[weekday repr:short]"`.
- **`duration`**: `.seconds() .minutes() .hours() .days() .weeks()`; arithmetic with datetimes.
- **`int`/`float`**: `.signum() .bit-not() .bit-and() .bit-or() .bit-xor() .bit-lshift() .bit-rshift() .to-bytes()`; `float.is-nan() .is-infinite() .signum() float.from-bytes(..)`.
- **`bytes`**: `.len() .at(i) .slice(a, b)`; `bytes("str")`, `str(bytes)`.
- **`version`**: compare, `.at(i)`; `sys.version`.
- **`color`** (global constructors `rgb luma oklab oklch cmyk` ; `color.hsl hsv linear-rgb`): `.lighten(r) .darken(r) .saturate(r) .desaturate(r) .negate(space:) .rotate(angle, space:) .mix(..) .transparentize(r) .opacify(r) .to-hex() .components(alpha:) .space()`; `color.mix(..colors, space:)`.
- **`gradient`**: `gradient.linear(..stops, space:, relative:, dir:/angle:)`, `.radial(..stops, center:, radius:, focal-center:, focal-radius:)`, `.conic(..stops, angle:, center:)`; methods `.stops() .sample(t) .samples(..t) .repeat(n, mirror:) .sharp(n, smoothness:) .kind() .space() .relative() .angle() .center() .radius()`.
- **`tiling(body, size:, spacing:, relative:, offset:)`**.
- **`numbering(pattern|func, ..nums)`**, **`lorem(words)`**, **`lower/upper(text)`**, **`regex(str)`**, **`layout(size => ..)`**, **`measure(content, width:, height:)`** (context), **`here()`**, **`locate(selector)`**, **`query(selector)`**, **`metadata(v)`**, **`counter(key).get/at/final/update/step/display`**, **`state(key, init).get/at/final/update`**.
- **`length`**: `.pt() .mm() .cm() .inches() .to-absolute()`; **`angle`**: `.deg() .rad()`; **`ratio`**, **`relative`** `.ratio .length`; **`fraction`**; **`alignment`** `.axis() .inv()`; **`direction`** `.axis() .start() .end() .inv()`.
- **Data loading**: `read(path, encoding:)`, `csv(src, delimiter:, row-type:)`, `json(src)`, `yaml(src)`, `toml(src)`, `xml(src)`, `cbor(src)`; encoders `json.encode(v, pretty:)`, `yaml.encode`, `toml.encode`, `cbor.encode` (the `*.decode` forms were removed in 0.15).
- **Math functions** (inside `$..$`): `accent attach scripts limits stretch cancel frac binom lr mid vec mat cases op root sqrt underline overline underbrace overbrace underbracket overbracket underparen overparen undershell overshell class display inline script sscript bold upright italic serif sans cal scr frak mono bb floor ceil round abs norm primes`; accent shorthands `hat tilde bar dot dot.double arrow breve acute grave macron caron circle`.
- **Visualization**: `image line rect square ellipse circle polygon (polygon.regular) curve (+ curve.move/line/quad/cubic/close) gradient tiling color stroke`.
- **PDF module**: `pdf.attach pdf.artifact` (+ experimental `pdf.header-cell pdf.data-cell pdf.table-summary` under `a11y-extras`).
- **HTML module**: `html.elem(tag, attrs:, body)`, `html.frame(content)`, typed elements (`html.div html.span html.p html.a html.img html.video html.pre html.code …` with typed attributes), `html.script(str)`, `html.style(str)`.
