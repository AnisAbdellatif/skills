# Special diagram types

Contents: [Sequence diagrams](#sequence-diagrams) · [SQL tables / ERDs](#sql-tables--erds) · [UML classes](#uml-classes) · [Grid diagrams](#grid-diagrams) · [Legends](#legends) · [Tooltips and links](#tooltips-and-links) · [C4 diagrams](#c4-diagrams)

All of these are ordinary D2 shapes: they can be contained, connected, styled and nested inside each other. Blocks tagged `d2` compile as-is.

## Sequence diagrams

Set `shape: sequence_diagram` on any object (or at the root). There is no special syntax, with two differences from the rest of D2.

1. **Scoping is flat.** Everything nested under the sequence diagram shares one scope, so `alice` inside two different groups is the *same* actor.
2. **Order matters.** Elsewhere declaration order is irrelevant; here it is the visual order, for actors (left to right) and messages (top to bottom).

```d2
shape: sequence_diagram
# declare actors first to fix their left-to-right order
user: User {shape: person}
web: Web App
api: API
db: Database

user -> web: submit order
web -> api: POST /orders
api -> db: INSERT
db -> api: ok {style.stroke-dash: 5}
api -> web: 201 Created {style.stroke-dash: 5}
web -> user: confirmation {style.stroke-dash: 5}
```

Convention: solid arrows for requests, **dashed** (`style.stroke-dash: 5`) for responses.

### Spans (activation bars)

A span is a nested object on an actor that is connected. Use any name for it (`t1`, `a`, ...).

```d2
shape: sequence_diagram
alice.t1 -> bob
alice.t2 -> bob.a
alice.t2.a -> bob.a
alice.t2.a <- bob.a
alice.t2 <- bob.a
```

### Groups (fragments: loop, alt, opt)

A group is a container with no connections to it. Its label is the fragment title. **Actors must already be declared at the top level before a group references them.**

```d2
shape: sequence_diagram
client
server
loop retry up to 3x: {
  client -> server: request
  server -> client: 503 {style.stroke-dash: 5}
}
alt success: {
  server -> client: 200 OK {style.stroke-dash: 5}
}
```

Groups nest.

### Notes

A note is a string-keyed child of an actor with no connections:

```d2
shape: sequence_diagram
alice -> bob
bob."Cold hands, no gloves."
important: {
  bob."Inside a group too"
}
bob -> alice: reply
```

### Self messages, styling, lifelines

```d2
shape: sequence_diagram
scorer: {shape: person}
scorer -> scorer: internal debate
scorer -> item: getRubric()
item -> scorer: rubric {style.stroke-dash: 5}
# lifelines inherit the actor's stroke / stroke-dash
scorer.style.stroke: red
scorer.style.stroke-dash: 0
```

Sequence diagrams can sit inside containers and next to other shapes:

```d2
direction: right
Before and after: {
  2007: Chatter in 2007 {
    shape: sequence_diagram
    alice -> bob: hi
  }
  2012: Chatter in 2012 {
    shape: sequence_diagram
    alice -> bob: want to play?
    bob -> alice: yes
  }
  2007 -> 2012: five years later
}
```

Tips: keep actor labels short; use `near`/long labels sparingly; `direction` does not apply inside; a message between actors in different diagrams is not possible.

## SQL tables / ERDs

`shape: sql_table`. Each key is a column; its value is the type; `constraint` is a nested attribute.

```d2
vars: {d2-config: {layout-engine: elk}}
users: {
  shape: sql_table
  id: int {constraint: primary_key}
  email: varchar(255) {constraint: unique}
  org_id: int {constraint: foreign_key}
  created_at: timestamp with time zone
}
orgs: {
  shape: sql_table
  id: int {constraint: primary_key}
  name: text
}
users.org_id -> orgs.id
```

- Recognized constraints are abbreviated: `primary_key` -> PK, `foreign_key` -> FK, `unique` -> UNQ. Any other string is shown as written (`NOT NULL`, `DEFAULT 0`).
- Several constraints: `constraint: [primary_key; unique]`.
- **Connect columns, not tables**: `orders.user_id -> users.id`. With ELK or TALA the edge ends at the exact row; dagre points at the table.
- A column whose name is a reserved keyword must be quoted: `"label": string`.
- Style: `fill` colors the header, `stroke` the body, `font-color` the header text. Theme controls the rest.
- Crow's-foot notation for cardinality: `orders.user_id -> users.id: {source-arrowhead.shape: cf-many; target-arrowhead.shape: cf-one-required}`.
- Tables can live in containers, and other shapes can connect to a table as a whole.

```d2
vars: {d2-config: {layout-engine: elk}}
direction: right
orders: {
  shape: sql_table
  id: int {constraint: primary_key}
  user_id: int {constraint: foreign_key}
}
users: {
  shape: sql_table
  id: int {constraint: primary_key}
}
orders.user_id -> users.id: {
  source-arrowhead.shape: cf-many
  target-arrowhead.shape: cf-one-required
}
```

## UML classes

`shape: class`. Keys without `(` are fields (value = type); keys containing `(` are methods (value = return type, or void if omitted).

```d2
vars: {d2-config: {layout-engine: elk}}
Animal: {
  shape: class
  +name: string
  -age: int
  \#id: uuid              # protected: escape the #
  +eat(food Food): bool
  speak()
}
Dog: {
  shape: class
  +breed: string
  +fetch()
}
Dog -> Animal: {
  target-arrowhead.shape: triangle
  target-arrowhead.style.filled: false   # hollow triangle = inheritance
}
```

| prefix | visibility |
|---|---|
| none or `+` | public |
| `-` | private |
| `\#` | protected (the `#` must be escaped or it becomes a comment) |

Relationship vocabulary:

```d2
vars: {d2-config: {layout-engine: elk}}
direction: right
Order: {shape: class; +id: int}
Line: {shape: class; +qty: int}
Customer: {shape: class; +name: string}
Product: {shape: class; +sku: string}
Special: {shape: class}

# composition: filled diamond at the whole. Draw the edge PART -> WHOLE so the
# diamond sits on the target end (see the arrowhead rule below)
Line -> Order: {
  source-arrowhead: 1..*
  target-arrowhead: 1 {shape: diamond; style.filled: true}
}
# aggregation: hollow diamond at the whole
Order -> Customer: {
  source-arrowhead: 0..*
  target-arrowhead: 1 {shape: diamond; style.filled: false}
}
# plain association: -- draws no arrowheads, only the multiplicity labels
Line -- Product: {
  source-arrowhead: *
  target-arrowhead: 1
}
# inheritance / realization (dashed)
Special -> Product: {
  target-arrowhead.shape: triangle
  target-arrowhead.style.filled: false
  style.stroke-dash: 3
}
```

**Arrowhead rule (verified, v0.9.0):** an arrowhead *shape* is drawn only at an end that has an arrow in the operator: `->` has one at the target, `<-` at the source, `<->` at both, `--` at neither. A `shape` on an end without an arrow is silently dropped (the label still shows). So put diamonds, triangles and crow's feet on the end that carries the arrow, and draw the edge in the direction that puts that end where you need it. `->` also draws a default filled triangle at the target; use `--` for a plain association, or `target-arrowhead.shape: none` on `<->` edges to clear a side.

Arrowhead labels (multiplicities) are short strings; they are not laid out by the engine.

## Grid diagrams

`grid-rows` and `grid-columns` turn a container (or the root) into a grid. Children fill cells in declaration order.

```d2
grid-rows: 2
grid-columns: 3
a; b; c; d; e; f
```

- **Only `grid-rows`**: that many rows; columns grow, and cells expand to fill the row.
- **Only `grid-columns`**: the transpose.
- **Both**: the one declared *first* is the dominant fill direction.
- `grid-gap: 0` fuses cells (good for tables, maps, matrices). `vertical-gap` and `horizontal-gap` override per axis.
- `width`/`height` on a cell resizes it; widths are shared within a column, heights within a row. If a cell has odd extra padding, equalize widths of its column-mates.
- Nest grids, sequence diagrams and ordinary diagrams inside cells.
- Connections between cells are straight center-to-center lines (dagre/ELK) or routed (TALA).
- Pad grids with invisible cells (`style.opacity: 0`) to center rows; move the real label with `label.near`.

```d2
# a table as a grid
grid-rows: 3
grid-columns: 3
grid-gap: 0
classes: {
  head: {style: {bold: true; fill: "#dbe7f5"}}
}
Service.class: head
Owner.class: head
Tier.class: head
Billing
Payments team
"1"
Search
Discovery team
"2"
```

For ordinary tables a Markdown block (`|md | a | b | ... |`) is often easier, but Markdown tables contain `|`, so the block needs the longer `||md ... ||` delimiter.

```d2
savings: ||md
  | Month | Savings | Balance |
  | ----- | ------- | ------- |
  | Jan   | $250    | $100    |
||
```

A common page-layout pattern:

```d2
grid-gap: 0
grid-columns: 1
header
body: "" {
  grid-gap: 0
  grid-columns: 2
  content
  sidebar
}
footer
```

## Legends

The legend is the special variable `d2-legend` inside `vars` (not a top-level shape). D2 builds it from the *styles you declare inside it*; it does not scan the diagram. Items are ordinary shapes and connections.

```d2
vars: {
  d2-legend: {
    svc: Microservice
    store: Database {
      shape: cylinder
      style.stroke-dash: 2
    }
    svc -> store: Reads
    a: {style.opacity: 0}     # hide helper shapes you don't want in the legend
    b: {style.opacity: 0}
    a -> b: Async {
      style.stroke: red
      style.stroke-dash: 2
    }
  }
}
api -> postgres
postgres: {shape: cylinder}
api -> queue: {style.stroke: red; style.stroke-dash: 2}
```

- `a -> b` declares three things (two shapes and a connection); give the shapes `style.opacity: 0` to show only the connection.
- Rename the legend with a label for non-English diagrams: `d2-legend: "凡例" {...}`.
- A legend is only worth it when colors, icons or line styles carry meaning that labels alone do not.
- For a manual legend, build a container with `near: bottom-center` and `shape: text` entries colored via `style.font-color`.

## Tooltips and links

```d2
x: Mac {
  tooltip: Total abstinence is easier than perfect moderation
  link: https://apple.com
}
y: PC {
  tooltip: hover text\nsecond line
  link: "https://example.com/page#section"
}
x -> y: compare {link: https://google.com}
```

- `tooltip` appears on hover (HTML `title`, plain text only, no Markdown). In static exports (PNG, PDF) tooltips become numbered icons plus an appendix; `--force-appendix` adds the appendix to SVG too.
- `link` makes the shape clickable. A `#` in a URL starts a comment unless the URL is quoted.
- Links work when the SVG is inlined or in `<object>`, `<iframe>` or `<embed>`; they do **not** work in `<img>` tags or CSS backgrounds.
- `link` can also point to another board (`link: layers.detail`); see `composition.md`.

## C4 diagrams

Use theme `303`, Markdown labels for the `## Title / [Type] / description` hierarchy, `shape: c4-person` for people, and `cylinder` for data stores. Quote edge labels that contain `[`.

```d2
vars: {d2-config: {theme-id: 303; layout-engine: elk}}
direction: down

customer: |md
  ## Customer
  [Person]

  A bank customer with accounts.
| {shape: c4-person}

bank: Internet Banking System {
  web: |md
    ## Web App
    [Container: Spring MVC]
  | {shape: rectangle}
  api: |md
    ## API
    [Container: Spring Boot]
  | {shape: rectangle}
  db: |md
    ## Database
    [Container: Oracle]
  | {shape: cylinder}
}
mainframe: |md
  ## Mainframe
  [Software System]
| {shape: rectangle}

customer -> bank.web: "Visits using\n[HTTPS]"
bank.web -> bank.api: "Calls\n[JSON/HTTPS]"
bank.api -> bank.db: "Reads/writes\n[SQL/TCP]"
bank.api -> mainframe: "Calls\n[XML/HTTPS]"
```

Drill-down between C4 levels is done with `layers` and `link` (see `composition.md`); PDF export keeps those links clickable.
