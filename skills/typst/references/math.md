# Math

## Basics

- Inline: `$x^2$` (no spaces after `$`). Display: `$ x^2 $` (space or newline after the opening and before the closing `$`).
- Single letters are variables (italic); multi-letter words are looked up as symbols/functions (`alpha`, `sin`, `pi`); unknown multi-letter names are an error (`unknown variable: ab`). Write words as strings: `"if"`, `"rate"`, or `upright("d")`, `op("lcm")`.
- Numbers, `+ - = < >` and `( ) [ ] { }` are literal. Brackets auto-size when matched: `(a/b)` grows; prevent it with `lr(size: #100%, ..)` or escape `\(`.
- Fractions `a/b`, `(a+b)/(c+d)`; roots `sqrt(x)`, `root(3, x)`; sub/superscripts `x_i^2`, `x_(i j)` (multi-token needs parentheses); primes `f'(x)`, `f''`.
- Space separates tokens: `a b` renders `ab`; to force visible space use `a thin b`, `quad`, `wide`, `space`; `#h(1em)`. Line break in display math: `\`. Alignment point: `&`.
- Embedded code: `$ #calc.pi $`, `$ x = #(2 + 3) $`, `$ #text(red)[x] + y $`. In math, call functions without `#`: `$ upright(A) = vec(1, 2) $`.
- Escape a character with `\` (`\$`, `\#`, `\(`). Strings in math: `"text"`.
- Equation settings: `#set math.equation(numbering: "(1)", supplement: [Eq.], number-align: end + horizon)`; label with `<eq>` right after the closing `$`; reference `@eq` → "Equation 1" (supplement) / with `#set math.equation(supplement: none)` and `@eq` renders `(1)`. Unnumbered line in a numbered block: put the numbering off by splitting equations or `#math.equation(numbering: none, block: true)[...]`.
- Alt text for accessibility: `#math.equation(alt: "x squared plus 1", block: true, $x^2 + 1$)` (PDF/UA needs it; HTML export (0.15) emits MathML).
- Multi-line aligned:
  ```typ
  $ f(x) &= (x + 1)^2 \
         &= x^2 + 2x + 1 $
  ```

```typ
#set math.equation(numbering: "(1)")
Euler: $e^(i pi) + 1 = 0$ and the quadratic formula
$ x = (-b plus.minus sqrt(b^2 - 4 a c)) / (2 a) $ <quad>
see @quad.

$ sum_(k=0)^n k &= (n(n+1))/2 \
  integral_0^infinity e^(-x^2) dif x &= sqrt(pi)/2 \
  lim_(h -> 0) (f(x+h) - f(x))/h &= f'(x) $
```

## Common constructs

| Want | Syntax |
| --- | --- |
| Greek | `alpha beta gamma Gamma Delta lambda mu pi Pi sigma Sigma phi.alt epsilon epsilon.alt` (`varphi`, `varepsilon` → `phi.alt`, `epsilon.alt`) |
| Sums/products/limits | `sum_(i=1)^n`, `product_(i=1)^n`, `lim_(x -> 0)`, `max_(x in S)`, `limits(sum)_(i=0)^n` forces limits inline; `scripts(sum)` forces scripts |
| Integrals | `integral`, `integral.double`, `integral.triple`, `integral.cont`, `integral_a^b f(x) dif x` |
| Relations | `<= >= != approx eq.not equiv prop subset sect union in in.not subset.eq` |
| Arrows | `-> <- <-> => <== <=> arrow.r arrow.l.double mapsto arrow.r.long` |
| Dots | `dots` (`...`), `dots.h`, `dots.v`, `dots.down`, `dots.c` |
| Sets / logic | `NN ZZ QQ RR CC` (blackboard), `forall exists nexists not and or`, `emptyset`, `in` |
| Operators | `sin cos tan log ln exp det dim ker max min sup inf arg lim gcd Pr`; custom: `op("rank")`, `op("argmin", limits: #true)` or `#let argmin = math.op("arg min", limits: true)` |
| Derivative | `dif x` / `diff`/`partial`: `(partial f)/(partial x)`, `(dif y)/(dif x)` |
| Vectors | `vec(1, 2, 3)`, `vec(delim: "[", 1, 2)`, `arrow(v)` / `vec` accents: `arrow(v)`, `hat(x)`, `tilde(x)`, `bar(x)`, `dot(x)`, `dot.double(x)`, `macron`, `grave`, `acute`, `breve`, `circle(x)`, `caron` |
| Matrices | `mat(1, 2; 3, 4)` rows by `;`; `mat(delim: "[", ..)`, `mat(delim: "|", ..)`, `mat(augment: #1, ..)` (vertical line before col 1), `mat(a, b; c, d, gap: #1em)` |
| Cases | `cases(x quad "if" x > 0, -x quad "else")` ; `cases(reverse: true, ..)`; `cases(delim: "(", ..)` |
| Binomial | `binom(n, k)` |
| Absolute/norm | `abs(x)`, `norm(v)`, `floor(x)`, `ceil(x)`, `round(x)`, `angle.l x angle.r` / `chevron.l x chevron.r` |
| Over/under | `overline(x)`, `underline(x)`, `overbrace(x + y, n "terms")`, `underbrace(..)`, `overbracket`, `cancel(x)`, `cancel(x, cross: #true)`, `stretch(->, size: #200%)`, `xarrow`-like: `arrow.r.long`, `attach(->, t: "f")` |
| Fonts | `bold(x)`, `upright(x)`, `italic(x)`, `bb(R)`, `cal(L)`, `scr(L)`, `frak(g)`, `mono(x)`, `sans(x)`, `serif(x)` |
| Sizing | `display(x)`, `inline(x)`, `script(x)`, `sscript(x)` |
| Text-ish | `"if"`, `quad`, `wide`, `thin`, `med`, `thick`, `#h(1em)` |
| Piecewise/units | `5 "m/s"`, `10 "kg"`; with `unify`/`zero`-like packages: `#qty(...)` |
| Attach full | `attach(X, tl: a, tr: b, bl: c, br: d, t: e, b: f)` |
| Tags | `class("relation", x)` to force spacing class (applies to direct body only in 0.15) |

Delimiter-like symbols are callable in math since 0.15: `chevron.l(x)` renders ⟨x⟩ (previously `chevron.l (x)`).

### Shorthands and predefined operators

- Arrow/relation shorthands (math): `-> <- <-> => <= >= != <=> |-> ==> <== --> <-- ~> <~ ->> <<- >-> |- := ::= =: << >> <<< >>> ... [| |] ||` (e.g. `a -> b`, `x != y`, `f: A |-> B`). In **markup** only `~`, `--`, `---`, `-?`, `...` and a few more exist; a stray `<` starts a label (`\<`).
- Predefined text operators (upright, correct spacing; `limits` where customary): `sin cos tan cot sec csc sinh cosh tanh coth sech csch arcsin arccos arctan arg deg det dim exp gcd lcm hom ker lg ln log lim liminf limsup max min inf sup mod Pr Re Im im sinc`. Others via `op("name")`.
- Double-struck shortcuts `AA BB CC DD EE FF GG HH II JJ KK LL MM NN OO PP QQ RR SS TT UU VV WW XX YY ZZ` (`RR` = ℝ). Greek: lowercase `alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron pi rho sigma tau upsilon phi chi psi omega`, uppercase by capital (`Gamma Delta Theta Lambda Xi Pi Sigma Phi Psi Omega`); variants `.alt` (`phi.alt`, `epsilon.alt`, `theta.alt`, `rho.alt`, `kappa.alt`), `ell`, `planck`, `hbar` (`planck.reduce`).
- Frequent misc: `nabla partial infinity (oo) aleph emptyset therefore because qed perp bot top star degree prime angle angle.arc triangle diamond square bullet ast dagger ddagger`. Browse everything with `typst eval 'dictionary(math).keys()'` / `dictionary(sym).keys()` or the symbol pages in the docs.

### Matrices & systems

```typ
$ A = mat(1, 2; 3, 4), quad vec(x_1, x_2) = mat(delim: "[", 1, 0; 0, 1) vec(a, b), quad
  det A = abs(mat(1, 2; 3, 4)) $
$ mat(a, b, c; d, e, f; augment: #2) $
$ cases(x + y = 1, x - y = 0) $
$ vec(1, 2, 3)^T quad mat(1, 2; 3, 4)^(-1) quad A^* quad A^dagger $
```

(`augment: #2` draws a vertical line after column 2; `augment: #(hline: 1, vline: 2, stroke: 0.5pt)` for both axes — dictionaries need `#` in math args.) To build a matrix from data: `$ mat(..#rows) $` where `rows` is an array of row arrays of content.

### Custom operators and commands

```typ
#let dd(x) = $dif #x$
#let R = $bb(R)$
#let argmax = math.op("arg max", limits: true)
#let vv(x) = $bold(upright(#x))$
$ argmax_(x in RR) f(x), quad dd(t), quad vv(a) $
```

Math "macros" are ordinary functions/variables; wrap values with `#` when substituting into math so they stay content: in `$ ... $` write `#x` to splice variable `x`.

### Numbering, references, equation styling

```typ
#set math.equation(numbering: "(1.1)")     // combine with heading counter via #show heading: it => { counter(math.equation).update(0); it }
#show math.equation.where(block: true): set block(breakable: true)   // allow page breaks in display math
#show math.equation: set text(font: "STIX Two Math")                 // math font
#show math.equation: set text(stylistic-set: 6)                      // 0.14-style calligraphic letters in 0.15
```

- Math font must be an OpenType **math** font (New Computer Modern Math (default), Libertinus Math, STIX Two Math, Cambria Math, Fira Math, Latin Modern Math).
- Equation blocks can break across pages when `breakable`.
- `math.frac(num, denom, style: "skewed"/"horizontal")` (0.14) — `#set math.frac(style: "horizontal")` writes `a/b` inline; `$ frac(a, b, style: "skewed") $`.
- `math.equation(block: true)` or `inline`; `math.display(...)` in an inline equation forces display-size contents.
- Text size inside math follows `text.size`; scale all math: `#show math.equation: set text(1.05em)`.

## Symbols and `sym`

- All math names are in `sym`/the math module: `sym.alpha`, `sym.arrow.r`, `sym.plus.minus`; in markup use `#sym.arrow.r` or shorthand (`->`, `<=`, `...`, `-->`). `sym.*` variants use dot-modifiers (`arrow.r.double.long`). `emoji.*` module (`#emoji.rocket`).
- List/browse: <https://typst.app/docs/reference/symbols/sym/>; in the local docs `reference/library/sym.md`. 0.15 renamed some symbols (old names warn; see changelog).
- `dif` (upright differential d with thin space; `math.dif` / `math.Dif`) is a math-only name: `integral f dif x`. Most other math names live in `sym` and also work in code as `sym.name`.

## Math in other modes

- Pure text with math fonts: `#text(font: "New Computer Modern Math")[$...$]`.
- HTML export (`--features html`): equations become MathML automatically (0.15); older `html.frame` SVG approach no longer needed.
- Inline equation within text keeps baseline (0.15 improvement).
- LaTeX input: package `mitex` converts LaTeX math strings (`#mitex(`\frac{a}{b}`)`), or `pandoc` converts `.tex`/`.md` math to Typst.

## Troubleshooting math

| Symptom | Fix |
| --- | --- |
| `unknown variable: xy` | Use `x y`, `x*y`, or `"xy"`; multi-letter variables need strings or `italic("xy")` |
| Text italic in math | `"text"` (string) renders upright |
| Fraction wrong grouping | Wrap numerator/denominator: `(a+b)/(c+d)`; parentheses are removed from the fraction |
| Large operator limits wrong | `limits(op)` / `scripts(op)`; `display(sum)` |
| Brackets too big | `lr(size: #100%, ( ... ))` or `#h(0pt)` trick; or escape them: `\( ... \)` |
| `integral` too small | `display(integral)` or `#show math.equation: set text(...)` (stretch ratios resolve against base glyph size in 0.15) |
| Equation number placement | `number-align: end + horizon` |
| Spacing around custom op | `math.class("normal", ..)`/`class("relation", ..)` |
