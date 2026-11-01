# Data loading, I/O and dynamic input

Typst can **read** files in the project root and **evaluate** data, but cannot write files, access the network, or run programs. All loaders take a path string, a typed `path` (0.15), or raw `bytes` (e.g. `read("f", encoding: none)`, a string wrapped with `bytes(...)`).

| Function | Returns | Notes |
| --- | --- | --- |
| `read(path, encoding: "utf8" \| none)` | `str` / `bytes` | any file; `encoding: none` → bytes |
| `csv(src, delimiter: ",", row-type: array \| dictionary)` | array of rows | all cells are **strings**; `row-type: dictionary` uses the header as keys |
| `json(src)` | value | objects → dicts, null → `none`, numbers → int/float |
| `yaml(src)` | value | |
| `toml(src)` | dict | |
| `xml(src)` | array of nodes | node = `(tag:, attrs:, children:)` or string; 0.15 supports namespaces |
| `cbor(src)` | value | binary JSON |
| `json.encode(v, pretty: true)`, `yaml.encode`, `toml.encode`, `cbor.encode` | str/bytes | serialize values (e.g. to show config, or bundle assets) |
| `image(src)`, `bibliography(src)`, `raw(theme:, syntaxes:)`, `plugin(src)` | | also accept bytes |
| `eval(str, mode:, scope:)` | value | evaluate Typst code from a string (e.g. user-provided markup) |
| `sys.inputs` | dict of str | from `typst compile --input key=value` |

```typ
#let rows = csv("data.csv", row-type: dictionary)
#table(
  columns: 2,
  table.header[*Name*][*Score*],
  ..for r in rows { (r.name, r.score) },
)
#let total = rows.map(r => int(r.score)).sum()
Total: #total, mean: #calc.round(total / rows.len(), digits: 2)
```

```typ
#let cfg = json("data.json")
= #cfg.title
#for it in cfg.items [- Item #it]
#cfg.at("missing", default: "n/a")
```

- **Paths** are relative to the current file; `/data/x.csv` is relative to the project root. Reading outside the root fails — compile with `--root` set to a parent directory if data lives elsewhere (also relevant for packages: they can't read your files unless you pass bytes/paths, 0.15 `path` type).
- **Type conversions**: CSV cells are strings → `int(s)`, `float(s)`, `decimal(s)`. Dates: `datetime(year: int(y), month: int(m), day: int(d))`. Content from strings: `[#s]` / `eval(s, mode: "markup")`.
- **Binary/large data**: `read("big.bin", encoding: none)` returns bytes (`.len()`, `.at(i)`, `.slice()`); `bytes(array-of-ints)`; `str(bytes)` decodes UTF-8; `array(bytes)`.
- **JSON with BOM** gives a friendly error (0.15); strip it or re-save without BOM.
- Remote data isn't supported: fetch with `curl` in a Makefile/CI and commit or generate before compiling.

## XML

```typ
#let doc = xml(bytes("<root><item id='1'>A</item><item id='2'>B</item></root>"))
#let root = doc.first()
#for c in root.children.filter(c => type(c) == dictionary) [
  - #c.tag #c.attrs.id: #c.children.first()
]
```

Nodes: `(tag: "item", attrs: (id: "1"), children: ("A",))`. Whitespace text nodes appear as strings — filter them.

## Passing parameters from the CLI

```bash
typst compile report.typ --input client=ACME --input draft=true
```

```typ
#let client = sys.inputs.at("client", default: "N/A")
#let draft = sys.inputs.at("draft", default: "false") == "true"
```

Values are always strings. Use for batch generation (one template, many PDFs): loop in the shell, `--input` per run, output path per run. JSON payload: `--input data='{"a":1}'` then `json(bytes(sys.inputs.data))`.

## Templated documents from data

```typ
#let invoice(client, items) = {
  set page(margin: 2cm)
  [= Invoice for #client]
  table(columns: (1fr, auto, auto),
    table.header[*Item*][*Qty*][*Price*],
    ..items.map(i => (i.name, str(i.qty), str(i.price))).flatten())
  let total = items.map(i => i.qty * i.price).sum()
  align(right)[*Total: #total*]
}
#invoice("ACME", ((name: "Widget", qty: 2, price: 5), (name: "Gadget", qty: 1, price: 12)))
```

Tip: use `decimal` for currency (`decimal("0.1") + decimal("0.2") == decimal("0.3")`).

## Evaluating strings

```typ
#let run(code) = eval(code, mode: "markup", scope: (name: "World"))
#run("Hello, #name!")
#eval("(1, 2, 3).map(x => x * 2)")     // code mode (default) → array
#eval("x^2 + 1", mode: "math", scope: (x: 5))
```

`eval` is sandboxed to Typst code (no file access beyond normal rules); packages/imports work. Errors in the evaluated string are reported at the `eval` call.

## Plugins (WebAssembly)

`#let p = plugin("my.wasm")` returns a module of functions taking/returning `bytes` (0.13+); e.g. `#p.hello(bytes("x"))`. Functions run in parallel; for state-ful init use `plugin.transition(f, ..args)`. Typical sources: Rust with `wasm-minimal-protocol`, Zig/C/Go. Packages built on this: `mitex` (LaTeX math), `diagraph`, `typst-jaq`, `rexllent`, `jogs`, `tiaoma`. Plugins must be committed/bundled; they cannot do I/O.

## Writing data out

You cannot write files from Typst, but you can export data through the CLI:

```bash
typst eval --in doc.typ 'query(<export>).first().value' > data.json   # metadata export (see introspection.md)
typst compile doc.typ out.pdf --deps deps.json                        # list of files read
```

In bundle export (`--features bundle`), `asset("name.json", json.encode(v))` writes arbitrary files as part of the bundle output.

## File-watching & `include`

`#include "section.typ"` splits a document. The included file sees the *project root* for `/` paths, not its own folder. Set `--root` to the top directory when sources live in subfolders:

```bash
typst compile src/main.typ --root .
```
