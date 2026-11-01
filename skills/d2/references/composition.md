# Composition: layers, scenarios, steps, linking

Contents: [The three board types](#the-three-board-types) · [Layers](#layers) · [Scenarios](#scenarios) · [Steps](#steps) · [Linking between boards](#linking-between-boards) · [Nesting and imports](#nesting-and-imports) · [Exporting multi-board diagrams](#exporting-multi-board-diagrams) · [Choosing](#choosing)

One file can hold many *boards*. The file itself is the **root board**; the keywords `layers`, `scenarios` and `steps` declare more boards that differ only in what they inherit. Blocks tagged `d2` compile as-is.

## The three board types

| keyword | inherits | use for |
|---|---|---|
| `layers` | nothing: a blank board (root `classes` and globs `***` still apply) | a different abstraction level: zoom in on a component, drill down C4 levels |
| `scenarios` | the **base board** (the one that contains them) | what-if variants: failure, cache hit vs miss, hotfix deployment |
| `steps` | the **previous step** (the first step inherits from the parent) | sequence of events, build-up animation, a process shown stage by stage |

Boards nest arbitrarily. A name is any key (`cat`, `2012.06` needs quotes when referenced). A board can have a label like any shape (`layers: {x: Pretty Label {...}}`).

## Layers

```d2
# root: the overview
client -> api -> db
api.link: layers.api
db.link: layers.db

layers: {
  api: API internals {
    router -> handler -> service
    service -> repo
  }
  db: Database {
    primary -> replica: replicates
  }
}
```

Layers share nothing with the root: re-declare any shape you need. They may contain their own `layers`, `scenarios` and `steps`.

## Scenarios

New objects are added on top of the base; you may refer to any base object to change it.

```d2
direction: right
client -> lb -> api1
lb -> api2
api1 -> db
api2 -> db

scenarios: {
  api2 down: {
    api2.style.opacity: 0.2
    (lb -> api2)[0].style.stroke-dash: 4
    lb -> api1: all traffic {style.stroke: red}
  }
  failover to replica: {
    db.style.opacity: 0.3
    replica
    api1 -> replica: promoted
  }
}
```

Use `null` to remove inherited things in a scenario (`api2: null`, `(lb -> api2)[0]: null`).

## Steps

Each step inherits all previous steps, so objects accumulate.

```d2
direction: right
steps: {
  1: Request {
    browser -> cdn
  }
  2: Cache miss {
    cdn -> origin
  }
  3: Response {
    origin -> cdn: 200
    cdn -> browser: 200
  }
}
```

Step 3 contains `browser`, `cdn` and `origin` although it declares only connections.

Labels on scenario/step boards can be set with the primary value (`1: Request {...}`) from v0.7.1.

## Linking between boards

`link` accepts a board path and becomes clickable in SVG and PDF; the SVG/PDF exporter adds a breadcrumb navigation bar to every board for going back.

```d2
how does the cat go?: {link: layers.cat}
layers: {
  cat: {
    meoowww
  }
}
```

- `_` in a **link value** refers to the *parent board* (not the parent container). `link: _` goes up one level, `link: _._` two.

```d2
The shire
journey: {link: layers.rivendell}
layers: {
  rivendell: {
    elves: {elrond -> frodo: gives advice}
    take me home sam.link: _
    go deeper: {link: layers.moria}
    layers: {
      moria: {
        dwarves
        take me home sam.link: _._
      }
    }
  }
}
```

- Board names with a dot need quotes: `a.link: layers."2012.06"`.
- Links to other URLs and to root paths (`/xyz`) also work; keep the `#` quoted in URLs.

## Nesting and imports

Keep each board in its own file and import it as a layer, so every file stays flat:

```d2-fragment
# overview.d2
serviceA -> serviceB
serviceB.link: layers.serviceB
layers: {
  serviceB: @serviceB
}

# serviceB.d2
vault.key -> data
data.link: layers.data
layers: {
  data: @data
}

# data.d2
users: {shape: sql_table; id: int; token: string}
```

Spread imports of scenarios/steps inherit correctly (v0.8+).

## Exporting multi-board diagrams

A single image cannot hold several boards, so the output depends on format:

| output | result |
|---|---|
| `out.svg` | a **directory** `out/` with `index.svg` plus `layers/<name>.svg`, `scenarios/<name>.svg`, `steps/<n>.svg`; internal links are rewritten to the files, so clicking works when opened locally |
| `out.svg --animate-interval=1200` | **one animated SVG** cycling through boards every 1200 ms (SVG and GIF only) |
| `out.gif` | animated GIF (interval defaults to 1000 ms) |
| `out.pdf` | one **page per board**, links clickable; best format for layers |
| `out.pptx` | one **slide per board**; imports to Google Slides |
| `out.png` | with multiple boards, a folder of PNGs like SVG |
| `--target=''` | render only the root board |
| `--target='layers.x'` | render only that board |
| `--target='layers.x.*'` | that board and all its children |
| `out.txt` (ASCII) | requires a single board; pass `--target` for multi-board files |

`--animate-interval` is a CLI flag only (not a `d2-config` key). `animated: true` on a *connection* is a different thing: marching-ants animation on one edge.

## Choosing

- Too many shapes on one board? Group into containers first, then split with `layers`.
- Same system, different situation? `scenarios`.
- Order or time matters, or you want a reveal? `steps`.
- Interaction order between participants over time? A `sequence_diagram` shape instead.
- Anything shared by all boards: triple globs, root `classes`, imports.
