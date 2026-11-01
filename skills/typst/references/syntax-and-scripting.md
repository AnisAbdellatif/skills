# Syntax and scripting

Typst has three syntactic modes that nest freely: **markup**, **math**, **code**.

## Markup

| Syntax | Result |
| --- | --- |
| `= Heading`, `== Sub` … | heading level = number of `=` (needs a space) |
| `*strong*`, `_emph_` | `strong`, `emph` (word-internal underscores like `snake_case` are fine) |
| `` `code` `` / ```` ```rust ... ``` ```` | inline / block `raw`; language tag enables highlighting |
| `- item` / `+ item` | bullet list / numbered list; indent to nest |
| `/ Term: description` | term list |
| `<name>` / `@name` | label (attached to the preceding element) / reference |
| `@name[supplement]`, `@key` | reference with custom supplement; citation if `key` is in the bibliography |
| `$...$` | math (spaces inside = display equation) |
| `#expr` | embedded code |
| `\` at line end, `\ ` | forced line break |
| blank line | paragraph break |
| `~` | non-breaking space; `-?` soft hyphen; `--` en-dash, `---` em-dash, `...` ellipsis |
| `"..."` and `'...'` | smart quotes (language-aware; `\"` for literal) |
| `// ...`, `/* ... */` | comments (block comments nest) |
| `https://example.com` | auto-linked URL |
| `\u{1F600}`, `\#` | unicode escape, escaped special char |

Special characters to escape in markup: `\ # $ @ * _ < ` ~ /` as needed (`\#`, `\$`, `\@`, `\*`, `\_`, `\<`, `` \` ``, `\~`, `\/`). A `/` only matters at the start of a line (term list); `//` always starts a comment (write `https:/\/...` only if not auto-link).

```typ
#set heading(numbering: "1.")
= Intro <intro>
Some *bold*, _italic_, `code`, a footnote#footnote[Like this.], and a link to
#link("https://typst.app")[Typst]. See @intro. Escapes: \# \$ \@ \* \_ and \u{1F600}.

- First
  - Nested
+ One
+ Two

/ Term: Definition text.
```

### Raw blocks

````typ
```python
def f(x): return x
```
#raw("inline text", lang: "txt")
#raw(block: true, lang: "rust", "fn main() {}")
````

`raw` options: `block`, `lang`, `align`, `theme` (`.tmTheme`, or `none`), `syntaxes` (`.sublime-syntax`), `tab-size`. Show rule for custom look: `#show raw: set text(font: "DejaVu Sans Mono", size: 9pt)`; `#show raw.where(block: true): block.with(fill: luma(240), inset: 8pt, radius: 4pt, width: 100%)`. Highlight lines via `raw.line` show rules. A raw block with ```` ```typ ```` / ```` ```example ```` has no special meaning.

### Labels and references

`<label>` attaches to the **immediately preceding** element (heading, figure, equation, table cell paragraph…). Label names may contain letters, digits, `_ - : .`. `@label` references it with automatic supplement ("Figure 1", "Section 2.1", "Equation (3)"). Controlling the reference text: `@label[custom]` or `#ref(<label>, supplement: [Sec.])`. Page reference: `#ref(<label>, form: "page")`. Dynamic label: `label("fig-" + str(i))`; reference with `#ref(label(...))`.

If a label does not attach, you probably put it after a `#let`, a blank line, or on a non-labelable thing (labels on `#context` blocks don't work; label the `metadata`/figure inside).

## Math mode (summary — see `math.md`)

```typ
Inline $a^2 + b^2 = c^2$ and display:
$ sum_(k=1)^n k = (n(n+1))/2 $ <eq:gauss>
```

## Identifiers, keywords, literals

- Identifiers: letters/`_` first, then letters, digits, `_`, **and `-`** (`my-var`, `show-title` — subtraction therefore needs spaces: `a - b`). In math, hyphens aren't allowed in names; use underscores/camelCase or `#`.
- Reserved words: `none auto true false not and or in let set show if else for while break continue return import include as context`.
- Escapes in strings: `\\ \" \n \r \t \u{1f600}`; in markup `\#` etc. Raw strings preserve everything but are content.
- Numbers: plain digits (no `_` separators); hex/octal/binary `0xff 0o17 0b101`; `1e3`, `0.5`, `calc.pi`, `calc.e`.
- `none` is the empty value (renders nothing); `auto` is the "figure it out" value. Booleans from comparisons; no truthiness (`if x` requires a bool).

## Code mode

Enter code with `#`; the expression ends at the first thing that cannot continue it. In code blocks `{ ... }`, newlines or `;` separate statements and **values are joined** into the block's result (content concatenates, strings join, `none` is dropped).

```typ
#let name = "Typst"          // binding (any value)
#let add(a, b: 1) = a + b    // function with default named arg
#let (x, y) = (1, 2)         // destructuring
#let (first, ..rest) = (1, 2, 3)
#let (a: a1, ..others) = (a: 1, b: 2)
#let args-sum(..nums) = nums.pos().sum(default: 0)
#let sq = x => x * x         // closure
#let title = [*Rich* content]
#let _ = 5                   // discard

#add(1, b: 5) #sq(4) #args-sum(1, 2, 3) \
#if x > 1 [big] else if x == 1 [one] else [small] \
#for (i, w) in ("a", "b").enumerate() [#i:#w ] \
#let n = 0
#while n < 3 { n += 1 }
#n

#{
  let total = 0
  for v in (1, 2, 3) {
    if v == 2 { continue }
    total += v
  }
  total   // value of the block
}
```

- Control flow: `if / else if / else`, `for … in` (arrays, dicts → `(k, v)`, strings → graphemes, `range(n)`), `while`, `break`, `continue`, `return`. There is **no `if let`**, no `switch` (use `if` chains or dictionary lookup), no `try/catch` (use `.at(key, default: ...)` and `assert`).
- Function bodies after `=` may be an expression, a code block `{}`, or content `[...]`.
- A trailing content block is the last positional argument: `#f(1, 2)[body]` ≡ `#f(1, 2, [body])`; `#f[a][b]` passes two content args.
- Spread: `f(..arr)`, `(..a, ..b)`, `(..dict1, ..dict2)`; `..rest` collects extra args as `arguments` (`.pos()`, `.named()`).
- Operators: `+ - * /`, unary `- + not`, `== != < <= > >=`, `and or not`, `in`, `not in`, `=  += -= *= /=`, `..`. `+` joins arrays, strings, content, dicts. `*` repeats strings/arrays (`"ab" * 3`). `/` always yields float for ints. Integer division: `calc.quo(a, b)`; remainder `calc.rem(a, b)` / `calc.rem-euclid`. Precedence: unary > `* /` > `+ -` > comparisons/`in` > `not` > `and` > `or` > assignment.
- Field access `a.b`, method call `a.f(x)`, index `arr.at(i)` / `dict.at("k")` (negative `i` counts from the end).
- `set` and `show` are also valid in code blocks: `{ set text(red); [x] }`.

### Value types (quick table)

| Type | Literal / constructor | Notes |
| --- | --- | --- |
| `none`, `auto` | `none`, `auto` | `auto` = "decide for me"; `none` = nothing |
| `bool` | `true`, `false` | |
| `int`, `float` | `3`, `-2`, `0x1F`, `0b101`, `3.14`, `1e3`; `float.inf`, `float.nan` | `int.max`/`int.min` (0.15); `int("ff", base: 16)` (0.15) |
| `decimal` | `decimal("1.10")` | exact arithmetic, for money |
| `str` | `"text"` | UTF‑8; byte indices; `.clusters()` for graphemes |
| `content` | `[text]` | `.func()`, `.fields()`, `.at(f)`, `.has(f)`, `.location()` |
| `symbol` | `sym.arrow.r`, `emoji.face` | modifiers via `.` |
| `array` | `(1, 2)`, `()`, `(1,)` | |
| `dictionary` | `(a: 1)`, `(:)` | keys are strings, order preserved |
| `length` | `1pt 2mm 3cm 4in 5em` | `.pt()`, `.mm()`, `.cm()`, `.inches()`, `.to-absolute()` (context) |
| `angle` | `90deg 1.5rad` | `.deg()`, `.rad()` |
| `ratio`, `relative` | `50%`, `100% - 2cm`, `50% + 1em` | |
| `fraction` | `1fr 2fr` | share of leftover space (`h(1fr)`, grid tracks) |
| `color` | `red`, `rgb("#ff8800")`, `luma(50%)`, `oklch(...)`, `cmyk(...)`, `hsl(...)` | |
| `gradient`, `tiling`, `stroke` | `gradient.linear(red, blue)`, `tiling(...)`, `2pt + red` | |
| `alignment`, `direction` | `left + top`, `center`, `ltr`, `ttb` | `+` combines axes; `.inv()` |
| `datetime`, `duration` | `datetime.today()`, `datetime(year: 2025, month: 1, day: 2)`, `duration(days: 3)` | `.display(...)` |
| `version` | `version(0, 15, 1)`, `sys.version` | compare with `<`, `>=` |
| `bytes` | `bytes("ab")`, `read("f.bin", encoding: none)` | |
| `label`, `selector`, `location`, `counter`, `state`, `module`, `function`, `arguments`, `type`, `path` (0.15) | | |

`type(x)` returns the type (`type(1) == int`); `repr(x)` gives a debug string (`repr(red)`), `x == none`. Calls on type: `str(5)`, `int("7")`, `float("1.5")`, `array(bytes)`, `bool`? (no — no constructor).

### Strings

Methods: `len`, `first`, `last`, `at`, `slice(start, end?)` (also `count:`), `clusters`, `codepoints`, `contains`, `starts-with`, `ends-with`, `find`, `position`, `match`, `matches`, `replace(pat, repl-or-func, count: n)`, `split(pat?)`, `trim(pat?, at:, repeat:)`, `rev`, `normalize`, `to-unicode` / `from-unicode` (static: `str.to-unicode("a")`), `lower(s)` / `upper(s)` (functions, also work on content). Patterns can be strings or `regex("...")`. Regex is Rust syntax (no backreferences/lookaround).

```typ
#let s = "Hello, World"
#s.len() #s.slice(0, 5) #s.replace(regex("o"), "0") #s.split(", ") \
#upper(s) #s.matches(regex("[A-Z]")).map(m => m.text)
#str(12) #int("42") #float("2.5") #str(255, base: 16)
```

### Arrays

`len first last at push pop insert remove slice contains find position filter map enumerate(start:) zip fold reduce sum product any all flatten rev split join(sep, last:) intersperse chunks(n, exact:) windows(n) dedup(key:) sorted(key:, by?) to-dict(pairs) range(...) .pairs`. `array.range` ≡ top-level `range(start?, end, step: n, inclusive: bool)`.

```typ
#let a = (3, 1, 2)
#a.sorted() #a.map(x => x * 2) #a.filter(x => x > 1) #a.sum() #a.map(str).join(", ") \
#a.fold(0, (acc, x) => acc + x) #a.zip(("a", "b", "c")) #a.enumerate(start: 1) \
#range(5) #range(1, 10, step: 3) #range(1, 4, inclusive: true) #(1, 2, 3).rev()
#(a, a).flatten() #a.contains(2) #a.position(x => x == 1)
```

`.at(i, default: v)` avoids out-of-range errors. `(1,2,3).sorted(key: x => -x)`. Arrays are **values**: `push` on a copy doesn't affect the original unless you reassign in the same scope.

### Dictionaries

`len at(key, default:) insert remove keys values pairs filter(f) map(f) (0.15)`. Iteration: `for (k, v) in dict`. Merge: `(..a, ..b)`. Dict keys must be strings; `dict.key` works for identifier-like keys.

### Functions as values

`f.with(1, name: "x")` partial application. `f.where(...)` for element functions builds a selector (`heading.where(level: 1)`). Recursion works (`let fact(n) = if n <= 1 { 1 } else { n * fact(n - 1) }`). Max call depth is limited — prefer loops for deep recursion.

Documentation comments: `/// Description` and tidy-style `/// - arg (type): text` are conventions for packages (tool: `tidy`).

### Content access and conversion

```typ
#let to-string(c) = {
  if type(c) == str { c }
  else if c.has("text") { c.text }
  else if c.has("children") { c.children.map(to-string).join() }
  else if c.has("body") { to-string(c.body) }
  else if c == [ ] { " " }
  else { "" }
}
#to-string([Some *bold* text])
```

`content.fields()` lists fields; `content.func()` is the element function (`strong`, `heading`, …); compare with `c.func() == heading`. Use `repr(c)` while debugging.

## Modules, imports, includes

```typ-x
#import "lib.typ"                       // binds `lib`; use lib.func(...)
#import "lib.typ": a, b as c, *         // names, rename, glob
#import "lib.typ" as mylib
#import "@preview/cetz:0.5.3": canvas, draw
#import "@local/my-pkg:0.1.0": *        // ~/.local/share/typst/packages/local/... (macOS: ~/Library/Application Support/typst/packages/local)
#include "chapter1.typ"                 // inserts the file's content (its top-level content), set rules inside don't leak out
```

- A file is a module whose scope is its top-level `let`s; `#import "f.typ": x` gives you `x`. `#include` yields the *content* of the file.
- Set/show rules at the top of an **included** file apply only within that file's content. To share style, put it in a template function (`#show: conf`) or a `style.typ` module that exports a function applied via `#show: style`.
- A bare `#import "x" + "y.typ"` (computed path, no `as`/import list) is a hard error since 0.13 because the bound name must be known statically; write `#import expr as name` or an import list.
- Import cycles are errors. Prefix `_` is a naming convention only (no privacy); nested modules via `#import "x.typ"` then `x.y.z`.
- Paths: `"a/b.typ"` relative to the current file; `"/a/b.typ"` relative to **project root** (`--root`, default = directory of the compiled file; files outside the root can't be read); forward slashes only. Typed path (`path("...")`, 0.15) can cross package boundaries.

## Context expressions (essentials)

```typ
#context text.size                        // read a style value at this location
#context counter(page).get().first()      // current page number
#context { let n = counter(heading).get(); [Heading #n] }
```

Rules: `context` evaluates its body *after* layout information is known; the result is **content** (not a value you can compute with outside). Reading styles inside `context` gives the value in effect *at that place*. `set` rules inside `context` do not feed back into the same context. Details and patterns: `introspection.md`.

## Scripting features worth knowing

```typ
// Helper: layout of data
#let table-from(rows) = table(columns: rows.first().len(), ..rows.flatten().map(c => [#c]))
#table-from(((1, 2), (3, 4)))

// Conditional/feature polyfills
#let tiling-fn = if "tiling" in std { std.tiling } else { std.pattern }

// Version gating
#if sys.version >= version(0, 15, 0) [new] else [old]

// Assertions and errors
#assert(1 + 1 == 2, message: "math broke")
#assert.eq(2, 1 + 1)
// #panic("stop with message")   // prints strings as-is (0.15)

// Evaluate strings
#eval("1 + 2") #eval("*bold*", mode: "markup") #eval("x^2", mode: "math", scope: (x: 3))

// Dates
#datetime.today().display("[year]-[month]-[day]") \
#datetime(year: 2024, month: 3, day: 5).display("[month repr:long] [day], [year]")

// Randomness: none built in; use `suiji`/pseudo-random with a seed in a package, or derive from datetime/state.
// Sorting, numbering
#numbering("1.a.i", 2, 1, 3) #numbering("A", 3) #numbering("I", 14) #numbering("一", 5)
```

`std` holds all globals (use when you shadowed `text`, `par`, …: `std.text`). `sys.version` and `sys.inputs` (dict of `--input key=val` strings) are in `sys`. `calc` module: `abs pow exp sqrt root sin cos tan asin acos atan atan2 sinh cosh tanh asinh acosh atanh log ln fact perm binom gcd lcm floor ceil trunc fract round(digits:) clamp min max even odd rem quo div-euclid rem-euclid norm erf pi tau e inf`. `calc.round(3.14159, digits: 2)`.

Not available: file writing, networking (except package download), shell, randomness, mutation of outer variables from closures, regex lookaround. Compilation is **pure and deterministic**; `datetime.today()` is the compile date (`--creation-timestamp` pins it).

## Style/typography quick refs (see `styling-and-layout.md` for more)

`#set text(...)`, `#set par(...)`, `#set page(...)`, `#show ...: ...` — the whole look of a document is configured with these.
