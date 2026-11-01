# Reuse: classes, variables, globs, overrides, imports, models

Contents: [Classes](#classes) · [Variables](#variables-and-substitutions) · [Globs](#globs) · [Filters](#glob-filters) · [Overrides and null](#overrides-and-null) · [Imports](#imports) · [Models with suspend](#models-with-suspend) · [Recipes](#recipes)

D2 separates *what the system is* from *how the diagram looks*. Keep nodes and edges in the main file, styling in `classes`/globs, and shared pieces in imports. Blocks tagged `d2` compile as-is; `d2-fragment` blocks need files that don't exist here.

## Classes

A class is a named bundle of attributes. Define under `classes`, apply with `class`.

```d2
direction: right
classes: {
  load balancer: {
    label: load\nbalancer
    width: 100
    height: 200
    style: {
      stroke-width: 0
      fill: "#44C7B1"
      shadow: true
      border-radius: 5
    }
  }
  unhealthy: {
    style: {
      fill: "#FE7070"
      stroke: "#F69E03"
    }
  }
}

web traffic -> web lb
web lb.class: load balancer
web lb -> api1
web lb -> api2
api2.class: unhealthy
```

- **Connections too**: `a -> b: {class: hot}` or later `(a -> b)[0].class: hot`.
- **Object attributes win** over class attributes: `x.class: unhealthy` then `x.style.fill: orange` renders orange.
- **Multiple classes**: `x.class: [base; error]`, applied left to right, later wins (`[uno; dos]` != `[dos; uno]`).
- Class definitions can hold any attribute (`shape`, `label`, `icon`, `width`, `style.*`, arrowheads), not only style.
- **Classes as tags**: every applied class name is written to the SVG as a CSS `class`, so web pages can style or script by it, and glob filters can select by it (`&class: server`). A class need not be defined to be used as a tag (an undefined class is silently accepted; it just does nothing).
- Classes defined on the root board are usable in `layers`, `scenarios` and `steps` boards too (verified), even though layers inherit no shapes.

## Variables and substitutions

`vars` declares variables; `${name}` substitutes. Dots reach nested values.

```d2
vars: {
  server-name: Cat
  palette: {
    button: {
      active: "#4baae5"
      border: black
    }
  }
}
s1: ${server-name}-1
s2: ${server-name}-2
s1 <-> s2
button: {
  width: 100
  height: 40
  style: {
    fill: ${palette.button.active}
    stroke: ${palette.button.border}
  }
}
```

- **Scoped like code**: inner scope shadows outer; a substitution cannot see a more inner scope.

```d2
vars: {region: Global}
lb: ${region} load balancer
zone1: {
  vars: {region: us-east-1}
  server: ${region} API
}
```

- **Single quotes bypass substitution**: `a -> b: 'Send ${names}'` prints literally. A `$` not followed by `{` must be single-quoted too.
- **Spread**: `...${x}` expands a map or array.

```d2
vars: {
  base-constraints: [NOT NULL; UNQ]
  disclaimer: DISCLAIMER {
    I am not a lawyer
    near: top-center
  }
}
data: {
  shape: sql_table
  a: int {constraint: [PK; ...${base-constraints}]}
}
custom-disclaimer: DRAFT DISCLAIMER {
  ...${disclaimer}
}
```

- Unresolvable variables are a compile error (`could not resolve variable "x"`).
- `vars` also hosts the special keys `d2-config` (render settings, see `cli-and-rendering.md`) and `d2-legend` (see `diagram-types.md`).

## Globs

`*` matches within the current scope, `**` recursively, `***` across the entire diagram including nested boards and imports. Globs are **case-insensitive**, apply **backwards and forwards** (to shapes declared before or after), and **scope-local**.

```d2
iphone 10
iphone 11 mini
iphone 11 pro
iphone 12 mini

*.height: 300
*.width: 140
*mini.height: 200     # later, more specific globs override
*pro.height: 400
```

Patterns can have the wildcard anywhere (`t*h*r`, `*kong`, `lady*`).

```d2
foods: {
  pizzas: {
    cheese
    pineapple
    *.shape: circle        # only inside pizzas
  }
  humans: {
    john
    *.shape: person
  }
  humans.* -> pizzas.pineapple: eats
}
```

**Glob connections**: `* -> *` connects everything to everything except itself (self-loops are deliberately skipped). `container.** -> x` connects every *leaf* descendant (containers are skipped).

```d2
vars: {d2-config: {layout-engine: elk}}
a
b
c
* -> *: 👉
```

**Targeting existing connections**: `(lady* -> barbie)[*].style.stroke: pink` styles every matching connection (`[*]` = all indexes).

**Triple globs** persist across `layers` and imports, so they are the right tool for global defaults:

```d2
***.style.fill: lightblue
(*** -> ***)[*]: {
  style.stroke: red
}
x -> y
layers: {
  next: {
    a -> b      # also lightblue / red
  }
}
```

`**.style.border-radius: 7` styles everything recursively in the current board only.

## Glob filters

Inside a glob block, `&key: value` keeps only matches; `!&key: value` excludes.

```d2
bravo team.shape: person
charlie team.shape: person
command center.shape: cloud
hq.shape: rectangle

*: {
  &shape: person
  style.multiple: true
}
*: {
  !&shape: person
  style.opacity: 0.7
}
```

- Any reserved keyword can be a filter: `&shape`, `&class`, `&link`, `&label`, `&style.fill`.
- Property filters: `&connected: true|false`, `&leaf: true|false`, `&level: 1` (nesting depth).
- **Array values** match if any element matches: `&class: server` matches `class: [server; deployed]`.
- **Glob as value**: `&link: *` means "has a link set".
- **Several `&` lines are ANDed.**
- **Connection endpoints**: `&src: a`, `&dst: c`, and attribute paths such as `&src.style.fill: blue`, `&dst.shape: rectangle`. Endpoint IDs are absolute (`a.c`, not `c`).
- **Nested globs** combine: `**: {&shape: sequence_diagram; **: {shape: person}}`.

```d2
(** -> **)[*]: {
  &src: a
  &dst: c
  style.stroke: yellow
}
a -> b
a -> c
```

## Overrides and null

Redeclaring merges; the last explicit label wins; `null` deletes.

```d2
visual studio code text editor
visual studio code text editor: visual_studio_code_text_editor
visual studio CODE text editor: VisualStudioCodeTextEditor    # same shape (case-insensitive)
```

```d2
one -> two
three
(one -> two)[0]: null          # delete the connection
three: null                    # delete a shape (and its connections and children)
one.style.fill: null           # unset an attribute
```

Typical uses: remove things you imported, make a scenario that drops something, exclude one item from a glob-created set.

## Imports

Imports behave like dependencies: modularize large diagrams, share styling, reuse components. They need real files (relative to the importing `.d2` file, not the working directory) and the extension is omitted.

```d2-fragment
# main.d2
a: @x            # regular import: the whole file x.d2 becomes a's body
b: {
  ...@x          # spread import: x.d2's contents are inserted here
}
...@classes      # spread at root: pull in shared classes
c: @people.alice # partial import: just the `alice` object from people.d2
d: @../shared/y  # relative path
e: @/abs/path/z  # absolute path (Windows needs quotes: @"C:\path\z")
f: @"schema-v0.1.2"  # a dot in the file name needs quotes
```

Rules:
- Only `.d2` files can be imported.
- **Spread imports work only inside maps** (`a: ...@x` is invalid).
- Globs declared in imported files are not carried over, except triple globs (`***`).
- Imported files may import others; cycles are an error.
- `d2 fmt` normalizes `@./x` to `@x`.
- Variables in an imported file are resolved at that file's scope first.
- Missing files fail with `failed to import ".../x.d2"`.

### Patterns

**Shared classes ("CSS")**

```d2-fragment
# classes.d2
classes: {
  base: {style: {border-radius: 4; shadow: true}}
  error: {style: {fill: pink; stroke: red}}
}
# main.d2
...@classes
user.class: base
```

**Model-view**: define shapes once, make several views.

```d2-fragment
# models.d2
postgres: {shape: cylinder}
it: IT Guy {shape: person}
vpn
# access-view.d2
...@models
it -> vpn -> postgres
# ssh-view.d2
...@models
it -> postgres: ssh, bypassing VPN
```

**Wrapper template**: wrap a diagram in a branded container.

```d2-fragment
# diagram.d2
template: {
  ...@wrapper-template
  a -> b
}
# wrapper-template.d2
style: {fill: "#E3EDE6"; fill-pattern: dots; stroke: "#820758"; stroke-width: 3}
label: ""
```

**Version comparison**: check out old versions of a file (`git checkout tags/v0.1 users.d2`; `mv users.d2 users-v0.1.d2`) and show them side by side: `Old: {...@"users-v0.1"}` and `New: {...@users-current}`.

## Models with suspend

When you want one model and many filtered views *inside a single file*, mark everything `suspend` (hidden, but still defined) and `unsuspend` what to show:

```d2
restaurants: Restaurants {
  chip: Chipotle
  bk: Burger King
  chip -> bk: competes with
}
diners: Diners {
  daniel
  zack
}
diners.daniel -> restaurants.chip: likes
diners.daniel -> restaurants.bk: dislikes
diners.zack -> restaurants.bk: likes

# treat everything above as a model
**: suspend
(** -> **)[*]: suspend

# view: only who likes what
(** -> **)[*]: unsuspend {
  &label: likes
}
```

Other views: `*: unsuspend` plus `(* -> *)[*]: unsuspend` for top-level only; `&dst: restaurants.bk` for connections into one shape. Combine with imports so the model lives in its own file.

## Recipes

**Consistent look with one classes block**

```d2
classes: {
  svc: {shape: hexagon; style.fill: "#e8f0fe"}
  store: {shape: cylinder; style.fill: "#fff4e5"}
  ext: {shape: cloud; style.stroke-dash: 3}
}
api.class: svc
auth.class: svc
pg.class: store
stripe.class: ext
api -> pg
api -> stripe
```

**Make all arrows dashed and rounded** (ELK corners): `(*** -> ***)[*].style.stroke-dash: 3` and `(*** -> ***)[*].style.border-radius: 8`.

**Add a person icon to every `person`**: `*: {&shape: person; icon: https://icons.d2lang.com/essentials%2F005-programmer.svg}`.

**Reduce repetition with a parent glob**: set `*.style.fill: lightblue` inside a container to style only its children.
