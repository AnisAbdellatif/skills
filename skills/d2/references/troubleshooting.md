# Troubleshooting

Contents: [Error messages](#error-messages) · [Silent surprises](#silent-surprises-it-compiled-but-looks-wrong) · [Layout problems](#layout-problems) · [Process tips](#process-tips)

Errors have the form `err: failed to compile FILE: FILE:LINE:COL: message`. Fix the first one, recompile; later ones often vanish. All messages below were reproduced with v0.9.0.

## Error messages

| message | cause | fix |
|---|---|---|
| `missing value after colon` (at `#fff`) | unquoted hex: `#` started a comment | `"#fff"` |
| `unexpected text after map key` | key contains `&`, `[ ]`, or other syntax characters | quote the key: `"R&D"`, `"svc[0]"` |
| `maps must be terminated with }` | unbalanced braces | find the unclosed `{`; `d2 fmt` indentation helps spot it |
| `unexpected text after md block string` / `block string must be terminated with |` | a `|` inside `|md ... |` closed the block early (Markdown tables!) | open with `||md` and close with `||` (or `|`` ... `|`) |
| `substitutions must begin on {` | a `$` not followed by `{` | `'costs $5'` (single quotes) or reword |
| `could not resolve variable "x"` | `${x}` with no `vars.x` in scope | define it in the same or an outer scope |
| `reserved keywords are prohibited in edges` | a shape named `link`, `label`, `class`, `top`, `style`, `near`, `icon`, `shape`, `direction`, `vars`... used in a connection | pick another key, or quote it |
| `edge with board keyword alone doesn't make sense` | a shape named `layers`, `scenarios` or `steps` in a connection | rename |
| `reserved field shape does not accept composite` | a shape named `Shape` (case-insensitive match of the keyword) with children | rename (`Figure`) |
| `unknown shape "x"` | typo or unsupported shape | see the catalog in `shapes-and-styling.md` |
| `expected "stroke-width" to be a number between 0 and 15` (also opacity 0-1, font-size 8-100) | out-of-range style | stay in range |
| `expected "text-transform" to be one of (none, uppercase, lowercase, capitalize)` | `title` is not accepted | `capitalize` |
| `key "3d" can only be applied to squares, rectangles, and hexagons` | `3d` on another shape | change shape or drop 3d |
| `near key "x" must be the absolute path to a shape or one of the following constants...` | invalid `near` | one of the eight constants (or a shape path with TALA) |
| `direction must be one of up, down, right, left` | bad direction | fix |
| `Connection "(a -> a.b)[0]" goes from a container to a descendant, but layout engine "dagre" does not support this` | container-to-child edge on dagre | `layout-engine: elk` (or tala) |
| `Object "c" has attribute "width" and/or "height" set, but layout engine "dagre" does not support dimensions set on containers` | sizing a container on dagre | elk/tala, or size the children |
| `Object "a" has "near" set to another object, but layout engine "dagre" only supports constant values for "near"` | `near: <shape>` | TALA, or use a constant |
| `indexed edge does not exist` | `(a -> b)[3]` beyond the count | indexes start at 0 per pair, in declaration order |
| `failed to import ".../x.d2": open ...: no such file` | wrong path (relative to the *importing file*, extension omitted, dots need quotes) | fix path |
| `failed to bundle local images: [./x.png]` | missing local icon file | fix path or use a URL |
| `"animate-interval" is not a valid config` | not a `d2-config` key | CLI flag `--animate-interval` |

## Silent surprises (it compiled but looks wrong)

- **Label cut short** (`a: C# language` shows "C"): `#` comment; quote the label.
- **Label missing, shape shows only the key** (`a: [JSON/HTTPS]`): parsed as an array; quote the label.
- **Extra nested boxes** (`svc v1.2`): the dot made a container; quote the key.
- **Duplicate shapes after using labels in edges**: edges use keys. `Backend -> Frontend` when keys are `be`/`fe` creates new shapes.
- **Two shapes merged into one**: keys are case-insensitive (`API` and `api`).
- **Label case changed to lowercase** (`Link` -> `link`, `Style` -> `style`): `d2 fmt` treats the bare word as a keyword; quote the label (`"Link"`).
- **Diamond/triangle/crow's foot missing from one end of an edge**: that end has no arrow in the operator (`->` has none at the source, `--` none at all); flip the edge or use `<->`.
- **Two arrows instead of one**: repeated connections are additive.
- **Legend missing or just a shape called d2-legend**: it must be `vars: {d2-legend: {...}}`.
- **Class has no effect**: class name typo is silently accepted; check spelling. Object attributes override class attributes. Later classes in `[a; b]` override earlier.
- **Glob did not hit a shape**: globs are scoped (`*` only current level, `**` recursive, `***` everything incl. layers/imports), case-insensitive, and `* -> *` skips self-loops and `**` connections skip containers.
- **Style ignored**: `3d` and `double-border` only on some shapes; `fill` on connections is meaningless (use `stroke`); a theme with special defaults (300/301/302) may override (e.g. caps); for sql_table/class `fill` is only the header.
- **Tooltips as Markdown** do not render as Markdown (HTML `title`).
- **Link not clickable**: SVG embedded via `<img>`; inline it or use `<object>`.
- **Icons missing in the render**: remote URL unreachable at render time (offline, wrong `%2F` encoding). Test the URL or use a local file.
- **Different look after upgrading D2**: engines were re-implemented in 0.8/0.9; regenerate stored images.
- **Output file exists but errors printed**: partial render; do not trust it.

## Layout problems

| symptom | try |
|---|---|
| tangled or overlapping edges | switch to `elk`; give hub shapes bigger `width`/`height`; shorten labels; reduce edge count per board |
| everything in one long row | change `direction`; group into containers; put separate flows in separate boards |
| wasted space / lopsided | `grid-*` for tabular parts; try `tala`; try `--elk-algorithm=stress` or `force` for non-hierarchical graphs |
| edge labels collide with shapes | add `\n` to labels, increase `--dagre-nodesep` / `--elk-nodeNodeBetweenLayers`, shorten |
| arrowhead label collides | arrowhead labels are not laid out; shorten or move into the edge label |
| sql_table edge ends at table, not row | use elk or tala |
| container-to-container routing ugly on dagre | elk |
| title/legend overlaps content | `near` constants plus `pad`; legends via `vars.d2-legend` are placed for you |
| text too wide | `\n` in the label |
| shapes in a grid have odd padding | equalize `width` across the column |
| layout changes on each tweak (TALA) | pin `data.tala-seeds` or switch to ELK |
| huge diagram times out | `--timeout 300`, split into layers; D2 targets whiteboard scale, not thousands of nodes |

## Process tips

- Build incrementally: nodes, then edges, then containers, then style; compile after each step.
- Compile with `scripts/d2check.sh`, then **look at the PNG**; only the picture reveals layout and readability problems.
- Use `d2 fmt` to normalize and expose structure errors.
- Bisect an inscrutable error by commenting half the file (`#`) or by wrapping a region in `"""` block comments.
- Ask `d2 layout <engine>` and `d2 themes` for the options your binary actually supports before using a flag.
- For a rendering that varies by D2 version, report `d2 --version` with the issue (https://github.com/terrastruct/d2/issues).
