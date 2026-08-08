---
Title: Static netlist analysis with slang
Date: 2026-08-08
Category: Computing and Silicon
Tags: computing, microelectronics, verilog
Summary: A tool for analysing the source-level connectivity of a SystemVerilog
         design, built on the slang frontend, and what I learned rebuilding an
         idea I first tried with Verilator.
Status: draft
---

{% import 'post-macros.html' as macros %}

<!--
SKELETON — outline only. Each section below has a note on what to cover.
Set `Status: published` and update `Date:` when the content is written.

Framing: this is the sequel to "Querying logical paths in a Verilog design"
(2018, content/netlist-paths.md). That note is what search engines currently
find, and it now describes a superseded tool. Link the two in both directions:
add a line to the top of netlist-paths.md pointing here once this is published.
-->

<!--
INTRO
- One paragraph on the problem, restated for a reader who hasn't read the 2018
  note: it is easy to build complex cross-module logic in SystemVerilog and
  hard to see what actually drives a net without a full synthesis run.
- One paragraph on why this is a rewrite rather than an update — what the
  Verilator XML/netlist-graph route couldn't do, and what changed.
- One sentence stating what the note covers.
-->

## Background: what Netlist Paths did

<!--
- Brief recap of the original approach: a patched Verilator emitting a graph of
  variable/logic dependencies, queried with Boost Graph.
- The limits that motivated a rewrite. Candidates to check against reality
  before asserting: dependence on a fork of Verilator and the maintenance cost
  of tracking it upstream; post-elaboration flattening losing source-level
  structure; granularity of the dependency graph (whole-variable vs bit/field);
  language coverage.
- Keep this short — link to the old note rather than repeating it.
-->

## Why slang

<!--
- What slang provides: a standards-tracking SystemVerilog frontend with a
  documented AST and data-flow analysis, usable as a library.
- The key difference from the Verilator route — analysis at the source level
  against the elaborated AST, rather than reading a dumped artefact.
- Anything given up by the change (state a fair trade-off, not just upside).
-->

## Representation

<!--
- What a vertex is and what an edge means in the dependency graph.
- How the source-level view is retained: names, hierarchy, file/line locations.
- Handling of the awkward cases — structs and unions, packed vs unpacked
  arrays, partial assignments, generate blocks, interfaces, parameters.
- A small worked example is worth more than prose here. Consider a figure —
  drop the {% raw %}{% endraw %} markers below and it becomes a live macro call:
{% raw %}{{ macros.image('slang-netlist/graph-example.png', caption="Dependency graph for a small module.") }}{% endraw %}
-->

## Use

<!--
- Mirror the structure of the 2018 note: a real design, real command output.
- PicoRV32 was the example last time; using it again makes the two notes
  directly comparable. A SystemVerilog design would show more of what slang
  buys you — pick one and say why.
- Cover the queries: does a path exist, fan-in, fan-out, through-points.
- Paste actual terminal output rather than paraphrasing it.
-->

```
$ TODO: real command and output
```

## Implementation

<!--
- Structure of the code: how the analysis hangs off slang's AST, what the graph
  library is, how the Python interface is bound.
- The parts that were harder than expected — this is the most useful material
  for anyone attempting something similar, and the part nobody else can write.
- Performance on a design of meaningful size, if measured.
-->

## What I would do differently

<!--
- The 2018 note ended with an "Improvements" list. Worth revisiting it here:
  which of those ideas made it into this tool, which turned out not to matter,
  and what is still open.
- Honest limitations of the current implementation.
-->

## Links

- [slang-netlist on GitHub](https://github.com/jameshanlon/slang-netlist)
- [slang-netlist documentation](https://www.jameswhanlon.com/slang-netlist)
- [slang](https://sv-lang.com)
- [Querying logical paths in a Verilog design]({filename}/netlist-paths.md) — the 2018 predecessor
- [Netlist Paths on GitHub](https://github.com/jameshanlon/netlist-paths)
