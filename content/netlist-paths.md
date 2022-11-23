---
Title: Querying logical paths in a Verilog design
Date: 2018-11-20
Category: notes
Tags: computing, microelectronics, verilog
status: published
---

I wrote a simple command-line tool for querying logical paths in a Verilog
design. My motivation for doing this is that it's easy to create complex logic
in Verilog, particularly between modules, but more difficult to understand
exactly what is driving a particular net, just from inspecting the code. It is
the complex cones of logic that lead to timing problems in a synthesised
design, but having to push a design through a synthesis flow takes time, making
speculative timing fixes a lengthy process. A command-line tool is useful as it
can be integrated into more complex workflows, in contrast with using more
complex and usually graphical EDA tooling.

The tool addresses high-level structural problems in a design, such as
incorrect dependencies when a signal including logic that is not necessary to
its function. It does not deal with other timing issues that are a product of
the synthesis and physical build of the design. As such, all the structural
information required is contained within the Verilog source code.

This note briefly explains how the tool works and records some ideas on how it
could be extended.

## Use

Instructions to build the tool are in the README in the [GitHub
repository](https://github.com/jameshanlon/netlist-paths/blob/master/README.md).
Assuming the `netlist-paths` install `bin` directory is available in your
`PATH`, then using the [PicoRV32 processor
implementation](https://github.com/cliffordwolf/picorv32) as an example, its
netlist can be generated as follows:

```
$ git clone https://github.com/cliffordwolf/picorv32.git
$ cd picorv32
$ verilator --dump-netlist-graph -o netlist.graph picorv32.v --top-module picorv32_axi
... # lots of warnings
```

Here a modified version of [Verilator](https://www.veripool.org/wiki/verilator)
is used to generate the netlist. (Note that `netlist-paths` can invoke
Verilator but with the `--compile` option, but PicoRV32 requires Verilator's
`--top-module` option. It may be useful to extend the command line arguments to
allow arbitrary arguments to be passed to Verilator.) Verilator performs the
generation by traversing the abstract syntax tree of the design and constructs
a graph of dependencies between variables and combinatorial logical constructs,
and identifies variables corresponding to sequential elements (flip flops).

The graph structure/netlist is written to file in [Graphviz dot
format](https://graphviz.gitlab.io/_pages/doc/info/lang.html), and specifies
the vertices, with their type and source code location information, and the
edges between them. The analysis tool reads this file and reports on the
connectivity between points.

```
digraph netlist {
  n0[id=0, type="ASSIGNW", loc="picorv32.v:2539"];
  n1[id=1, type="PORT", dir="OUTPUT", name="picorv32_axi.trace_data", loc="picorv32.v:2539"];
  n2[id=2, type="PORT", dir="OUTPUT", name="trace_data", loc="picorv32.v:2539"];
  n3[id=3, type="ASSIGNW", loc="picorv32.v:2538"];
  n4[id=4, type="PORT", dir="OUTPUT", name="picorv32_axi.trace_valid", loc="picorv32.v:2538"];
  ...
  n0 -> n2;
  n1 -> n0;
  n3 -> n5;
  n4 -> n3;
  n6 -> n8;
  ...
}
```

A vertex in this netlist corresponds to the occurrence of a variable (ie a
symbolic name). A given symbolic name can appear in different vertices,
corresponding to its different uses. To see this, the option `--dumpnames`
prints the names, types and directions of all the vertices in the graph. This
output can be piped through `grep` to locate particular signals. For example,
to see all the output variables:

```
$ netlist-paths netlist.graph --dumpnames | grep OUTPUT
PORT OUTPUT eoi
PORT OUTPUT mem_axi_araddr
PORT OUTPUT mem_axi_arprot
PORT OUTPUT mem_axi_arvalid
PORT OUTPUT mem_axi_awaddr
PORT OUTPUT mem_axi_awprot
PORT OUTPUT mem_axi_awvalid
...
```

Or all the registers:

```
$ netlist-paths netlist.graph --dumpnames | grep REG_DST
REG_DST picorv32_axi.axi_adapter.ack_arvalid
REG_DST picorv32_axi.axi_adapter.ack_awvalid
REG_DST picorv32_axi.axi_adapter.ack_wvalid
REG_DST picorv32_axi.axi_adapter.xfer_done
REG_DST picorv32_axi.picorv32_core.alu_out_0_q
REG_DST picorv32_axi.picorv32_core.alu_out_q
REG_DST picorv32_axi.picorv32_core.alu_wait
REG_DST picorv32_axi.picorv32_core.alu_wait_2
REG_DST picorv32_axi.picorv32_core.cached_ascii_instr
REG_DST picorv32_axi.picorv32_core.cached_insn_imm
...
```

Here, the `REG_DST` type corresponds to a variable that is the left-hand side
of a non-blocking assignment `<=`. Conversely, the `REG_SRC` type is where the
same variable appears in an expression on the right-hand side. In general,
there can only be a single ``REG_DST`` node with a specific name, whereas there
can be multiple ``REG_SRC`` nodes with a specific names. The same is true with
``VAR``, ``WIRE`` and ``PORT`` types. When using this tool, I've found it
straight forward to locate the variables I need using `grep` with
`--dumpnames`, but there may be more sophisticated approaches that could be
implemented.

A start or end point can be specified as any named vertex, which is anything
except logic statements. You can query if a path exists between two points:

```
$ netlist-paths netlist.graph --start picorv32_axi.picorv32_core.cpu_state --end picorv32_axi.picorv32_core.dbg_valid_insn
  picorv32_axi.picorv32_core.cpu_state        REG_SRC         picorv32.v:1160
  ASSIGNW                                     LOGIC           picorv32.v:1373
  picorv32_axi.picorv32_core.launch_next_insn WIRE            picorv32.v:750
  ALWAYS                                      LOGIC           picorv32.v:760
  picorv32_axi.picorv32_core.dbg_valid_insn   REG_DST         picorv32.v:751
```

In this path report, it lists the sequential dependencies from the start point
to the end point, through a sequence of zero or more combinatorial logic
statements/blocks, with each dependency corresponding to a variable.
Importantly, the filenames and line numbers given reference the original source
code.

Since there may be multiple vertices with a name matching the specified start
and end points, the register version is preferentially located (``SRC`` for a
start point and ``DST`` for an end point), followed by ``VAR``, ``WIRE`` and
``PORT`` types.

You can also query all the paths that fan out from a particular start point:

```
netlist-paths netlist.graph --start picorv32_axi.picorv32_core.cpu_state
Path 1
  picorv32_axi.picorv32_core.cpu_state        REG_SRC         picorv32.v:1160
  ASSIGNW                                     LOGIC           picorv32.v:1373
  picorv32_axi.picorv32_core.launch_next_insn WIRE            picorv32.v:750
  ALWAYS                                      LOGIC           picorv32.v:760
  picorv32_axi.picorv32_core.q_ascii_instr    REG_DST         picorv32.v:742

Path 2
  picorv32_axi.picorv32_core.cpu_state        REG_SRC         picorv32.v:1160
  ASSIGNW                                     LOGIC           picorv32.v:1373
  picorv32_axi.picorv32_core.launch_next_insn WIRE            picorv32.v:750
  ALWAYS                                      LOGIC           picorv32.v:760
  picorv32_axi.picorv32_core.q_insn_imm       REG_DST         picorv32.v:743

Path 3
  picorv32_axi.picorv32_core.cpu_state        REG_SRC         picorv32.v:1160
  ASSIGNW                                     LOGIC           picorv32.v:1373
  picorv32_axi.picorv32_core.launch_next_insn WIRE            picorv32.v:750
  ALWAYS                                      LOGIC           picorv32.v:760
  picorv32_axi.picorv32_core.q_insn_opcode    REG_DST         picorv32.v:744
...
Found 223 path(s)
```

Or query all the paths that fan in to a particular end point:

```
$ netlist-paths netlist.graph --end picorv32_axi.picorv32_core.dbg_valid_insn
Path 1
  picorv32_axi.picorv32_core.trap           REG_SRC         picorv32.v:86
  ALWAYS                                    LOGIC           picorv32.v:760
  picorv32_axi.picorv32_core.dbg_valid_insn REG_DST         picorv32.v:751

Path 2
  picorv32_axi.picorv32_core.instr_lui       REG_SRC         picorv32.v:630
  ALWAYS                                     LOGIC           picorv32.v:684
  ASSIGN                                     LOGIC           picorv32.v:685
  picorv32_axi.picorv32_core.new_ascii_instr VAR             picorv32.v:673
  ALWAYS                                     LOGIC           picorv32.v:760
  picorv32_axi.picorv32_core.dbg_valid_insn  REG_DST         picorv32.v:751

Path 3
  picorv32_axi.picorv32_core.instr_auipc     REG_SRC         picorv32.v:630
  ALWAYS                                     LOGIC           picorv32.v:684
  ASSIGN                                     LOGIC           picorv32.v:685
  picorv32_axi.picorv32_core.new_ascii_instr VAR             picorv32.v:673
  ALWAYS                                     LOGIC           picorv32.v:760
  picorv32_axi.picorv32_core.dbg_valid_insn  REG_DST         picorv32.v:751
...
Found 74 paths
```

Since the number of paths between any two points in an arbitrary graph grows
exponentially with the size of the graph, it infeasible to report all paths
between two points, so this tool simply looks for any path that satisfies those
constraints. (An option is provided to enumerate all paths, but it can only be
used on small netlists.)

When trying to match a particular path in a physical build it it useful to
further constrain the search to force it to match the same path. This can be
done by specifying through points with the `--through` option. Each through
argument is taken in order as an intermediate point in the path. The same
search algorithm is used on each pair of points to build up a composite report.
For example:

```
$ netlist-paths netlist.graph --start picorv32_axi.axi_adapter.ack_wvalid --through picorv32_axi.axi_adapter.mem_axi_wvalid --end mem_axi_wvalid
  picorv32_axi.axi_adapter.ack_wvalid     REG_SRC         picorv32.v:2700
  ASSIGNW                                 LOGIC           picorv32.v:2711
  picorv32_axi.axi_adapter.mem_axi_wvalid PORT            picorv32.v:2671
  ASSIGNW                                 LOGIC           picorv32.v:2556
  picorv32_axi.mem_axi_wvalid             PORT            picorv32.v:2484
  ASSIGNW                                 LOGIC           picorv32.v:2484
  mem_axi_wvalid                          PORT            picorv32.v:2484
```

## Implementation

To avoid writing a preprocessor and parser for Verilog, I modified
[Verilator](https://www.veripool.org/wiki/verilator) to obtain the netlist of a
Verilog design. (I would have liked to use
[Yosys](http://www.clifford.at/yosys/) to do this because it provides a neat
interface to adding custom AST passes, but unfortunately it does not currently
support enough of the SystemVerilog standard.) The Verilator modifications add
a new AST visitor, which walks the tree after it has been processed, for
example to propagate constants and inline tasks and modules.

The `netlist-paths` tool is implemented in C++ and makes use of the Boost Graph
Library. Paths are identified using the `boost::depth_first_search` algorithm.
The all-fan-out report enumerates paths to all the end points in a depth-first
traversal of the graph, the fan-in variant uses the `boost::reverse_graph`
adaptor and performs the same algorithm. Properties are associated with
vertices in the graph using a `boost::dynamic_property_map`. I put together a
[simple example program](https://github.com/jameshanlon/boost_graph_example) to
illustrate how to use these maps (plus some other library features) since I
found there were some subtleties in getting this to work.

## Improvements

There are many ways this tool could be extended and improved. Here are a few
ideas:

- Provide additional flexibility to allow a choice between multiple matching start, through or end points.
- Provide a mechanism to search for high fan-out variables.
- Provide a mechanism to seach for the longest paths in the graph.
- Provide a mechanism to assert there is no logical path between two sub
  modules.
- Detect and report timing loops.
- Add options to `dumpnames` to filter by type or direction.
- Add options to the querys to select only internal paths or only input/output
  paths.

## Links

- [Netlist paths tool on GitHub](https://github.com/jameshanlon/netlist-paths)
- [Modified Verilator on GitHub](https://github.com/jameshanlon/verilator)
- [Boost Graph Library example](https://github.com/jameshanlon/boost_graph_example)
