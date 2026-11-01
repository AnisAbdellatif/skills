# D2 language reference

Contents: [Keys and labels](#keys-and-labels) · [Strings and quoting](#strings-and-quoting) · [Comments](#comments) · [Connections](#connections) · [Containers](#containers) · [Referencing things](#referencing-things) · [Reserved keywords](#reserved-keywords) · [Maps, arrays, values](#maps-arrays-values) · [Identity rules](#identity-rules)

Fenced blocks tagged `d2` compile as-is. Blocks tagged `d2-fragment` are partial snippets.

## Keys and labels

A **key** is a shape's identity; a **label** is the text displayed. They are the same unless you give a label after a colon.

```d2
api                    # key "api", label "api"
pg: PostgreSQL         # key "pg", label "PostgreSQL"
SQLite; Cassandra      # semicolons put several on a line
big idea: A longer label that is still one shape   # spaces are allowed in keys
```

Leading and trailing whitespace is trimmed. Keys may contain spaces, digits (`1 -> 2` works), and most punctuation, but see quoting below.

Set the label later, or on containers, with the `label` keyword:

```d2
gcloud: {
  label: Google Cloud
  auth -> db
}
gcloud2: Google Cloud {   # equivalent shorthand
  auth -> db
}
```

A shape's `shape:` defaults to `rectangle`.

```d2
Cloud: my cloud
Cloud.shape: cloud        # dotted form
db: {shape: cylinder}     # map form
```

## Strings and quoting

Unquoted strings cover most text. Quote with `"..."` or `'...'` when the text contains `#`, a leading `[`, `{`, `|`, `$` (other than `${`), a `.`, `&` or `[` in a key, a reserved word used as a key, or a leading/trailing space you want to keep. Use double quotes if the text contains `'` and vice versa; otherwise escape with `\`.

```d2
"x(int y)": "[]int"
'$dollarbills$'
a: "C# language"
b: "[JSON/HTTPS]"
"svc v1.2" -> a
c: 'costs $5'          # single quotes also disable ${...} substitution
```

Escapes: `\n` newline, `\"`, `\\`, `\#` (a literal `#` in unquoted text, for example UML protected members), `\$`. A label that is too wide can be wrapped with `\n`.

```d2
x: When you go out to buy,\ndon't show your silver.
```

Non-Latin text and emoji are fine. Punctuation must be ASCII: a full-width `：` is not a colon.

### Block strings (multi-line text)

Block strings start with `|tag` and end with `|`. The tag selects how the text renders: `md` (Markdown), `latex`/`tex`, `text`, or a programming language for syntax highlighting (`go`, `ts`/`typescript`, `py`/`python`, `js`, `rb`, `sql`, `json`, `yaml`, `bash`...; any [Chroma](https://github.com/alecthomas/chroma) lexer; unknown tags fall back to plain text).

```d2
notes: |md
  # Heading
  - bullet one
  - bullet two
  **bold** and `code`
|
snippet: |go
  func main() {
    fmt.Println("hi")
  }
|
formula: |latex
  \lim_{h \rightarrow 0} \frac{f(x+h)-f(x)}{h}
|
```

If the text itself contains `|`, lengthen the delimiter with `||` or `|||`, or use any run of non-alphanumeric, non-space, non-underscore symbols after the first pipe:

```d2
my_code: |`ts
  declare function getSmallPet(): Fish | Bird;
  const works = (a > 1) || (b < 2)
`|
```

Notes:
- Indentation is auto-corrected by `d2 fmt`; you can paste code at column 0.
- A standalone block string (no `shape`) is rendered as Markdown text with no box. To give Markdown to a box, declare the shape explicitly: `box: |md ... | {shape: rectangle}`.
- Markdown HTML must be well-formed XML (`<br/>`, not `<br>`).
- LaTeX is MathJax: no line breaks (use `\displaylines{...}`), font size via `\tiny`, `\small`, `\large`, `\huge`, not `font-size`.
- Markdown, LaTeX and code blocks can be used as shape labels and (v0.7+) as connection labels.

## Comments

```d2
# line comment (also valid after code on the same line)
x -> y # trailing
"""
block comment
"""
```

`#` begins a comment *anywhere* an unquoted string could continue, so quote hex colors, URLs with `#fragment`, and labels such as `C#`.

## Connections

Four operators: `--` (no arrowheads), `->`, `<-`, `<->`. Undeclared endpoints are created.

```d2
Write Replica Canada <-> Write Replica Australia
Read Replica <- Master
Write Replica -> Master
Read Replica 1 -- Read Replica 2: Kept in sync
```

**Chains** apply the label to every hop: `a -> b -> c: label`.

**Cycles are fine**, and self-connections (`a -> a: retry`) are allowed.

**Repeats declare new connections** instead of overriding:

```d2
Database -> S3: backup
Database -> S3
Database -> S3: backup
```

**Connections reference keys, not labels.**

```d2
be: Backend
fe: Frontend
be -> fe             # correct
# Backend -> Frontend would create two NEW shapes
```

### Connection attributes

```d2
a -> b: label {
  style: {
    stroke: red
    stroke-width: 3
    stroke-dash: 4
    animated: true
    font-color: red
    opacity: 0.8
  }
  source-arrowhead: 1          # label next to the source end
  target-arrowhead: * {        # label plus shape
    shape: diamond
    style.filled: true
  }
}
x -> y: {icon: https://icons.d2lang.com/infra%2F002-backup.svg}   # v0.7.1+
```

Arrowhead shapes: `triangle` (default), `arrow`, `diamond`, `circle`, `box`, `cross`, `cf-one`, `cf-one-required`, `cf-many`, `cf-many-required` (crow's foot). `triangle` takes `style.filled: false` (hollow, UML inheritance); `diamond`, `circle` and `box` take `style.filled: true` (solid, UML composition). Keep arrowhead labels short: they are not laid out by the engine and can collide.

An arrowhead *shape* on an end without an arrow does nothing: `x -> y` has no source arrowhead, and `--` has none at all (labels still appear). Use `<->`, or flip the edge direction so the shape sits on the arrow end.

### Referencing a connection

Connections are addressed as `(src -> dst)[index]`, indexes counted per endpoint pair in declaration order:

```d2
x -> y: hi
x -> y: hello
(x -> y)[0].style.stroke: red
(x -> y)[1].style.stroke: blue
```

Globs can target many at once: `(* -> *)[*].style.stroke: red` (see `reuse-and-globs.md`).

## Containers

Dots nest; maps nest; both can be mixed.

```d2
server.process                      # child inside server
im a parent.im a child
apartment.Bedroom.Bathroom -> office.Spare Room.Bathroom: Portal

clouds: {
  aws: AWS {
    load_balancer -> api
    api -> db
  }
  gcloud: Google Cloud {
    auth -> db
  }
  gcloud -> aws
}
users -> clouds.aws.load_balancer
```

Notes:
- `_` is the parent scope: inside `birthdays`, `_.christmas.presents` reaches outward.
- A key reached through different parents is a *different* shape (`aws.db` and `gcloud.db` are distinct). A shape can live in only one container.
- Connections may cross container borders using full dotted paths from the current scope.
- Connections from a container to its own descendant are not supported by `dagre` (use `elk` or `tala`).
- `width`/`height` on containers need ELK or TALA.

```d2
christmas: {presents}
birthdays: {
  presents
  _.christmas.presents -> presents: regift
}
```

## Referencing things

- Shapes by dotted path: `clouds.aws.api`.
- Connection by `(a -> b)[i]`.
- Layers, scenarios, steps by path: `layers.x`, `scenarios.y`, `steps.1` (see `composition.md`).
- Globs (`*`, `**`, `***`) in place of any path segment.
- Attributes by path: `a.style.fill`, `a.label.near`, `a.icon.near`, `(a -> b)[0].target-arrowhead.shape`.

## Reserved keywords

These cannot be used as plain shape keys (quote them to use as keys: `"width": width`):

`label shape icon constraint tooltip link near width height direction top left grid-rows grid-columns grid-gap vertical-gap horizontal-gap class classes vars style source-arrowhead target-arrowhead layers scenarios steps`

Style-only keys (valid only under `style`): `opacity stroke fill fill-pattern stroke-width stroke-dash border-radius font font-size font-color bold italic underline text-transform shadow multiple double-border 3d animated filled`.

Special names: `d2-config`, `d2-legend` (inside `vars`), `suspend`/`unsuspend` (values), `null` (value), `_` (parent). Glob filters starting `&`/`!&` are only valid inside glob blocks.

## Maps, arrays, values

```d2
x: {                      # map
  a: 1
  b: 2
}
x.c: 3                    # same map
y: [one; two; three]      # array, items separated by ; or newline
z: [
  one
  two
]
```

Arrays appear in `class: [a; b]`, `constraint: [primary_key; unique]`, and `vars`. Spread with `...${var}` (see `reuse-and-globs.md`).

Numbers, booleans (`true`/`false`) and `null` are recognised by attributes that expect them (`width: 200`, `style.shadow: true`). Everything else is a string.

## Identity rules

- Keys are **case-insensitive**: `api`, `API`, `Api` are one shape. The **last explicit label wins**.
- Repeated declarations **merge** (attributes accumulate; later values override earlier).
- Globs apply backwards and forwards: a glob declared before a shape still applies to it once created.
- `x: null` deletes shape `x` and everything attached to it (its connections and descendants); `x.style.fill: null` unsets an attribute; `(a -> b)[0]: null` deletes one connection.
- A very long key (almost always a missing quote) is rejected by the parser.

```d2
one
two
one: null            # "one" is gone
```

## Autoformat

`d2 fmt file.d2` rewrites the file canonically (indentation, `@x.d2` -> `@x`, block-string indent). `d2 --check file.d2` verifies formatting without writing. It preserves board order and comments.
