# Recipes per diagram family, and conversion from other tools

Contents: [Picking a family](#picking-a-family) · [Architecture](#architecture--system-design) · [Flowchart](#flowchart--decision-tree) · [State machine](#state-machine) · [ERD](#erd) · [Sequence](#sequence) · [Class](#uml-class) · [C4](#c4) · [Org chart and trees](#org-chart--tree) · [Network and deployment](#network--deployment) · [Timeline-ish and tables](#timeline-ish-pipelines-tables-matrices) · [Converting from other tools](#converting-from-mermaid-plantuml-graphviz)

Ready-to-copy files live in `assets/templates/` (all compile and were visually checked): `architecture`, `flowchart`, `sequence`, `erd`, `uml-class`, `state-machine`, `c4-container`, `org-chart`, `grid-dashboard`, `multiboard`, `classes`. Copy, rename, edit.

## Picking a family

| request sounds like | use | engine | template |
|---|---|---|---|
| services, infra, "how does X fit together", cloud, deployment | containers + classes | `elk` | `architecture.d2` |
| process, algorithm, decision logic, runbook | shapes + labelled edges | `dagre` | `flowchart.d2` |
| lifecycle, statuses, transitions | rectangles + terminal circles | `elk` | `state-machine.d2` |
| tables, relations, schema | `sql_table` | `elk` | `erd.d2` |
| who calls whom over time, protocol, API flow | `sequence_diagram` | n/a | `sequence.d2` |
| OOP design, domain model | `class` | `elk` | `uml-class.d2` |
| C4 context/container/component | md labels + theme 303 | `elk` | `c4-container.d2` |
| hierarchy, reporting lines, taxonomy | tree | `dagre` | `org-chart.d2` |
| comparison matrix, table, page mock-up | grid | any | `grid-dashboard.d2` |
| overview plus drill-down, before/after, step-through | layers / scenarios / steps | `elk` | `multiboard.d2` |

## Architecture / system design

- **Group by boundary** (VPC, team, trust zone, runtime), not by technology. One level of nesting is usually enough; avoid more than three.
- Give each kind of thing one class: `svc` hexagon, `store` cylinder, `queue` queue, `ext` cloud with dashed stroke, `person`.
- Edge labels: protocol or verb (`HTTPS`, `gRPC`, `reads`, `publishes`). `style.animated: true` only on real runtime flows (event streams), never on structural relationships.
- Use `direction: right` for request paths; the layout then reads like a pipeline.
- Cross-container edges use full dotted paths (`edge.gw -> platform.orders`).
- Cloud icons: `icon: https://icons.d2lang.com/aws%2F...svg` on shapes (see `shapes-and-styling.md`).
- Too dense? Add `width`/`height` to hub shapes; split detail into `layers`.
- **Trust boundaries / zones**: one container per zone with a dashed stroke through a shared class (`classes: {zone: {style: {stroke-dash: 3; fill: transparent}}}`, then `untrusted.class: zone`). Name zones by trust level (Untrusted, DMZ, Internal, Third party).
- **Very wide result** (long left-to-right chain): switch to `direction: down`, or put the zones in a `grid-rows`/`grid-columns` wrapper, or try `--elk-algorithm=stress`. Collapse fan-out (many services consuming one topic) by connecting once to a container that holds the consumers, instead of one edge per consumer.

## Flowchart / decision tree

- Start/end `oval`, decision `diamond` (labelled yes/no edges), I/O `parallelogram`, subprocess default rectangle, document `document`.
- Dagre handles these well and fast; keep `direction: down` for tall flows, `right` for wide.
- Loops back are fine (cycles allowed).
- Keep decision text a short question; put the answer on the outgoing edge.

## State machine

- States are rounded rectangles (`style.border-radius`); initial state a small filled `circle` with `label: ""`; final state the same with `style.double-border: true`.
- Label every transition `event [guard] / action` or just `event`.
- Nested states: a container whose children are the substates; connect to the container for "any substate".
- ELK avoids the crossing mess dagre makes on cyclic graphs.

## ERD

- One `sql_table` per entity; `constraint` for PK/FK/unique; connect `child.fk -> parent.pk`.
- Cardinality with crow's foot arrowheads (`cf-many`, `cf-one`, `cf-one-required`, `cf-many-required`) on `source-arrowhead.shape` / `target-arrowhead.shape`.
- `direction: right` for wide schemas. Group related tables in containers named by bounded context.
- Large schema: one board per context via `layers`, plus a cross-context overview.

## Sequence

- Declare actors first, in order. Label messages with the call or event; responses dashed.
- Use groups named `alt ...`, `loop ...`, `opt ...` for fragments, spans for activations, notes for asides.
- Long label? Break with `\n`. More than ~12 messages: consider two diagrams or `steps`.

## UML class

- Fields `name: type`, methods `name(args): return`; visibility prefixes `+ - \#`.
- Inheritance = hollow triangle at the parent; composition = filled diamond at the whole; aggregation = hollow diamond; dependency = dashed edge. Arrowhead shapes only render on ends that have an arrow, so draw part -> whole and put the diamond on the target (see `diagram-types.md`). Plain association: `--`.
- **Don't name a class `Shape`, `Label`, `Style`, `Class`, `Link`, `Icon`, `Near`, `Width`, `Height`, `Top`, `Left`, `Vars`...**: keys are case-insensitive, so `Shape` is the reserved word `shape` and fails with "reserved field shape does not accept composite". Rename (`Figure`) or quote the key and verify it compiles.

## C4

- Level 1 context: people (`c4-person`) and software systems. Level 2 container: boxes inside a system container. Level 3: components.
- Label format: `## Name` / `[Type: tech]` / description, in a `|md` block; `shape: rectangle` set explicitly after the block.
- Quote edge labels containing `[...]`.
- Drill down with `layers` plus `link: layers.x`; export to PDF to keep the links.

## Org chart / tree

`direction: down`, `shape: person` via a class, connect boss -> report. For wide trees try `--elk-algorithm=mrtree` or `radial`. Use a `grid` instead when the "tree" is really a table.

## Network / deployment

Nested containers for region > VPC > subnet > host; connect leaf shapes with full paths; ELK, with `width`/`height` on containers for breathing room. Mark trust boundaries with dashed container strokes (`style.stroke-dash: 3`).

## Timeline-ish, pipelines, tables, matrices

D2 has no Gantt or timeline type. Approximate:
- **Pipeline**: `direction: right` chain of `step` shapes.
- **Roadmap**: `grid-columns: N` with one column per quarter, cards as cells.
- **Matrix / table**: grid with `grid-gap: 0`, or a Markdown table in a `||md ... ||` block.
- If the user needs a true Gantt, mind map, Venn diagram, pie/bar chart or map, say D2 does not do those and suggest another tool.

## Converting from Mermaid, PlantUML, Graphviz

Translate *meaning*, then restyle with D2 idioms; don't mimic the other tool's layout hacks.

| source | D2 |
|---|---|
| Mermaid `graph LR` / `flowchart TD` | `direction: right` / `down` |
| `A[Label]`, `A(Label)`, `A{Label}`, `A[(DB)]`, `A((C))` | `A: Label`, rounded via `style.border-radius`, `shape: diamond`, `shape: cylinder`, `shape: circle` |
| `A --> B`, `A -->|text| B`, `A --- B`, `A -.-> B` | `A -> B`, `A -> B: text`, `A -- B`, `A -> B: {style.stroke-dash: 3}` |
| `subgraph X ... end` | container `X: { ... }` |
| `classDef`/`class` | `classes: {...}` and `.class:` |
| Mermaid `sequenceDiagram`, `participant`, `->>`, `-->>`, `alt/loop/opt`, `Note over` | `shape: sequence_diagram`, declare actors, `->`, `-> ... {style.stroke-dash: 5}`, groups, `actor."note"` |
| Mermaid `erDiagram` | `sql_table` + crow's foot arrowheads |
| Mermaid `classDiagram` | `shape: class` + arrowhead shapes |
| Mermaid `stateDiagram-v2` | state-machine pattern; `[*]` becomes a small circle |
| Mermaid `gantt`, `pie`, `mindmap`, `journey`, `gitGraph` | no equivalent: say so |
| PlantUML `component`, `node`, `database`, `queue`, `actor`, `cloud`, `package`, `rectangle` | shapes `rectangle`, `rectangle`, `cylinder`, `queue`, `person`, `cloud`, `package`, `rectangle` |
| PlantUML `skinparam`, `!theme` | `theme-id`, classes, `d2-config` |
| Graphviz `digraph { a -> b [label=x] }`, `rankdir=LR`, `cluster_x`, `shape=box/ellipse/diamond/cylinder` | `a -> b: x`, `direction: right`, container, `rectangle/oval/diamond/cylinder` |
| Graphviz `node [...]`/`edge [...]` defaults | `***.style.*` and `(*** -> ***)[*].style.*` globs |

**Mermaid `subgraph` as drill-down**: a subgraph becomes a container (default) or, when the user wants "drill into each subsystem", a `layers` board linked from the container (`backend.link: layers.backend`); export to PDF. Edges that cross a container border can loop around it under ELK; fix by declaring nodes in flow order, giving the endpoint shapes more `width`/`height`, or trying `layout-engine: dagre` (but dagre cannot connect a container to its own child).

After converting, quote labels with `#`, `[`, `$`, `&`, check that keys with dots are quoted, and compile.
