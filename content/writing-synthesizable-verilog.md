---
Title: Writing synthesizable Verilog
Date: 2018-5-4
Category: notes
Tags: computing, microelectronics, programming-languages, verilog
Summary: Coding style for RTL design using Verilog / SystemVerilog. Updated 2024.
Status: published
---

> **_NOTE:_**  Updated Feburary 2024 with improvements and new guidance.

In the last year, I've started from scratch writing SystemVerilog for hardware
design. Coming from a software background where I was mainly using C/C++ and
Python, it has been interesting to experience the contrasting philosophy and
mindset associated with using a language to describe hardware circuits. Much of
this is because SystemVerilog provides little abstraction of hardware
structures, and only through disciplined/idiomatic use, can efficient designs
be implemented. A compounding issue is that complex hardware designs rely on a
complex ecosystem of proprietary tooling.

As I see it, there are three aspects to writing synthesizable SystemVerilog
code: the particular features of the language to use, the style and idioms
employed in using those features, and the tooling support for a design. Good
coding style can help achieve better results in synthesis and simulation, as
well as producing code that contains less errors and is understandable,
reusable, and easily modifiable. Many of the observations in this note relate
to coding style. The next sections give some context around the use of
SystemVerilog in digital design, or you can [skip ahead](#guidance) to the
guidance.


### The SystemVerilog language

SystemVerilog (which subsumed Verilog as of the 2009 standardisation) is a
unified language, serving distinct purposes of modern hardware design. These
can be enumerated as:

- Circuit design/specification at different levels of abstraction:
    * Behavioural.
    * Structural/register-transfer level (RTL).
    * Gate.
    * Switch/transistor.
- Testbench-based verification.
- Specification of formal properties.
- Specification of functional coverage.

SystemVerilog provides specific features to serve each of these
purposes. For circuit specification, each level of abstraction uses a different
language subset, generally with fewer features at lower levels. Behavioural
design uses the procedural features of SystemVerilog (with little regard for the
structural realisation of the circuit). RTL design specifies a circuit in terms
of data flow through registers and logical operations. Gate- and switch-level
design use only primitive operations. Typical modern hardware design uses a mix
of register-transfer- and gate-level design.

It is interesting to note that the SystemVerilog specification does not specify
which features are synthesizable; that depends on the tooling used.


### Tooling

There is a variety of standard tooling that is used with SystemVerilog, and
indeed other hardware description languages (HDLs). This includes simulation,
formal analysis/model checking, formal equivalence checking, coverage analysis,
synthesis and physical layout, known collectively as electronic design
automation tools (EDA). Since standard EDA tooling is developed and maintained
as proprietary and closed-source software by companies like Cadence, Synopsys
and Mentor, the tooling options are multiplied.

In contrast with the open-source software ecosystems of programming languages
(for example), closed-source EDA tools do not benefit from the scale and
momentum of open projects, in the way that conventional software languages do,
with a one (or perhaps two) compilers and associated tooling such as debuggers
and program analysers. Such a fragmented ecosystem inevitably has a larger
variability in precisely how features of SystemVerilog language are implemented
and which features are not supported, particularly since there is no standard
synthesizable subset. Consequently, engineers using SystemVerilog/HDLs with
proprietary EDA tools do so conservatively, sticking to a lowest common
denominator of the language features (within their chosen synthesizable
subset), to ensure compatibility and good results.

<hr>

<a name="guidance" class="anchor"></a>
## Overview

This note records rules, conventions and guidance for writing SystemVerilog
approaches that I have observed interact well with the supporting tooling and
to encourage good coding style and produce good synthesis results. They can be
followed by anyone writing synthesizable SystemVerilog. I owe many of these
insights to the guidance from my colleagues.

This note assumes familiarity with SystemVerilog. As such it is not a
comprehensive guide to programming practices. Some of the references at the end
will serve those purposes better.

The guidance is presented in the following sections:

- [Combinatorial logic](#comb-logic)
- [Sequential logic](#seq-logic)
- [If statements](#if-statements)
- [Case statements](#case-statements)
- [Expressions](#expressions)
- [Constants](#constants)
- [Code structure](#code-structure)
- [Naming](#naming)
- [Preprocessor](#preprocessor)
- [Formatting](#formatting)


<a name="comb-logic" class="anchor"></a>
## Combinatorial logic

**Use `always_comb` instead of `always` for combinatorial logic.** The
`always_comb` procedure allows tools to check that it does not contain any
latched state and that no other processes assign to variables appearing on the
left-hand side. (It's worth checking the language reference manual (LRM) for
details of of the other differences.) The use of an `always_comb` block is also
a much clearer indication of a combinatorial block that the use of `=` as
opposed to `<=`.

**Always provide an initial value.** A latch will be inferred if there exists a
control-flow path in which a value of a signal is not set. Since `always_comb`
specifically precludes the creation of latches, doing so will cause a warning
or error in simulation or synthesis. For example, the following code implies a
latch since there is no assignment to `foo` when the condition is not true.

```
always_comb
  if (condition)
    foo = 1'b1;
```

Instead, always provide an initial value:

```
always_comb
  foo = 1'b0;
  if (condition)
    foo = 1'b1;
```

**Avoid reading and writing a signal in an `always_comb` block.** The
sensitivity list includes variables and expressions
but it excludes variables that occur on the right-hand side of assignments.
According to these restrictions, a variable that is read and written in a block
only causes the block to be reevaluated when the left-hand-side instance
changes. However, this style can cause some tools to warn of a
simulation-synthesis mismatch (presumably because they apply conservative rules
from older versions of the language standard).

In the following code, the block is triggered only when the the right-hand-side
`foo` changes, rather than entering a feedback loop where it shifts
continuously:

```
always_comb
  foo = foo << 1;
```

To avoid reading and writing foo in the same block and possible warnings
from tools, a new signal can be introduced:

```
always_comb
  next_foo = foo << 1;
```

**Where possible extract logic into `assign` statements.** Extract single
assignments to a variable into a separate `assign` statement, where it is
possible to do so. This approach uses the features of SystemVerilog
consistently, rather than using two mechanisms to achieve the same effect. This
makes it clear that an `always_comb` is used to introduce sequentiality.
Another opportunity to move logic into separate `assign` statements is with
complex expressions, such as the Boolean value for a conditional statement.
Doing this makes the control flow structure clearer, potentially provide
opportunities for reuse, and provides a separate signal when inspecting the
signals in a waveform viewer.

**Avoid unnecessary sequentiality.** It is easy to add statements to an
`always_comb` to expand its behaviour, but this should only be done when there
are true sequential dependencies between statements in the block. In general,
parallelism should be exposed where ever possible. In the the following
example, the sequentiality is not necessary since the output `set_foo` depends
independently on the various conditions:

```
always_comb begin
  set_foo = 1'b0;
  if (signal_a &&
      signal_b)
    set_foo = 1'b1;
  if (signal_c ||
      signal_d)
    set_foo = 1'b1;
  if (signal_e)
    set_foo = 1'b1;
end
```

Clearly the sequencing of the conditions is not necessary, so the block could
be transformed to separate the logic for each condition into separate parallel
processes (extracting into `assign` statements as per the rule above) and
explicitly combine them with the implied logical disjunction of the original
block:

```
assign condition_a = signal_a && signal_b;
assign condition_b = signal_c || signal_d;
always_comb begin
  set_foo = 1'b0;
  if (condition_a ||
      condition_b ||
      signal_e)
    set_foo = 1'b1;
end
```

It is [recommended][verilator-internals] by the author of Verilator to split up
``always`` blocks (combinatorial or sequential) so they contain as few
statements as possible. This allows Verilator the most freedom to order the
code to improve execution performance.

**Drive one signal per block.**
With complex control flow statements, it is tempting to use a single
`always_comb` block to drive multiple signals. In some circumstances, there may
be good reasons to do this, such as when many output signals are used in a
similar way, but in the general case, splitting each signal into a separate
block makes it clear what logic involved in driving that signal, and as such,
facilitates further simplification.

An additional reason to avoid driving multiple signals per `always_comb` block
is that [Verilator][verilator] can infer a dependence between two signals,
leading to false circular combinatorial loops. In these cases, it issues an
[`UPOPTFLAT` warning][unoptflat] and cannot optimise the path, leading to
reduced emulation performance. Generally, fixing warnings pertaning to
unoptimisable constructs can improve Verilator's simulation performance by [up
to a factor of two][verilator-internals].

[verilator-internals]: https://www.veripool.org/papers/verilator_philips_internals.pdf
[verilator]: https://www.veripool.org/wiki/verilator
[unoptflat]: https://www.embecosm.com/appnotes/ean6/html/ch07s02s07.html

```
always_comb begin
  foo = foo_q;
  bar = bar_q;
  if (condition_a)
    case (condition_b)
      0: begin
        foo = ...;
        if (condition_c)
          bar = ...;
      end
      1: foo = ...;
      2: bar = ...;
      default:;
    endcase
end
```
The above block could be split into two processes:
```
always_comb begin
  foo = foo_q;
  if (condition_a)
    case (condition_b)
      0: foo = ...;
      1: foo = ...;
      default:;
    endcase
end

always_comb begin
  bar = bar_q;
  if (condition_a)
    case (condition_b)
      0: if (condition_b)
           bar = ...;
      2: bar = ...;
      default:;
    endcase
end
```

<a name="seq-logic" class="anchor"></a>
## Sequential logic

**Use `always_ff` instead of `always` for sequential logic** Similarly to
`always_comb`, use of `always_ff` permits tools to check that the procedure
only contains sequential logic behaviour (no timing controls and only one event
control) that variables on the left-hand side are not written to by any other
process, and makes clear the intent for sequential logic behaviour with
non-blocking assignments, `<=`.

**Avoid adding logic to non-blocking assignments.** This is primarily a matter
of taste, but having non-blocking assignments in `always_ff` blocks only from a
logic signal name, rather than a logical expression, keeps the block simple and
limits combinatorial logic to `always_comb` blocks and `assign` statements
elsewhere in the module. Since synthesizable `always_ff`s are additionally
restricted in that variables assigned to must have a reset condition of a
constant value, maintaining this clarity aids the programmer. Having separate
combinatorial blocks is also useful since it allows the logic signal driving a
flip-flop as well as the registered value to be apparent in a waveform viewer,
particularly when clock gates are used.

A typical pattern when implementing combinatorial logic and registers is to
define the set and clear conditions in an `always_comb` and register the value
in an accompanying `always_ff`, for example:

```
logic bit;
logic bit_q;

always_comb begin
  bit <= bit_q;
  if (set_condition)
    bit = 1'b1;
  if (clear_condition)
    bit = 1'b0;
end

always_ff @(posedge i_clk or posedge i_rst)
  if (i_rst)
    bit_q <= 1'b0;
  else
    bit_q <= bit;
```

<a name="if-statements" class="anchor"></a>
## If statements

**Use `if` qualifiers** for single `if` and chained `if-else`
statements for additional checking and guidance to synthesis:

 - `unique` to ensure exactly one condition is matched and to indicate the
   conditions can be checked in parallel.
 - `unique0` to ensure one or no conditions match and to indicate the
   conditions can be checked in parallel.
 - `priority` to ensure one condition is matched and to indicate the conditions
   should be evaluated in sequence and only the body of the first matching
   condition is evaluated.

Note that:

- The use of an `else` precludes violation reports for non-existing matches in
  `unique` and `priority`.
- The default behaviour of a chained `if-else` block is `priority` but without
  any violation checks.

For example, when the conditions are mutually exclusive, so evaluation order is
not important:
```
unique if (condition_a) statement;
else if (condition_b) statement;
else if (condition_c) statement;
```
A violation warning is given in the above when no condition or multiple conditions are
selected. Changing to `unique0` will only check for multiple conditions being selected:
```
unique0 if (condition_a) statement;
...
```
And adding an `else` will suppress violation warnings all together:
```
unique0 if (condition_a) statement;
...
else statement;
```

<a name="case-statements" class="anchor"></a>
## Case statements

**Use case qualifiers** for additional checking and guidance to synthesis:

 - `unique` to ensure exactly one condition is matched and to indicate the
   conditions can be checked in parallel.
 - `unique0` to ensure that one or no conditions are matched and to indicate
   the conditions can be checked in parallel.
 - `priority` to ensure one condition is matched and to indicate the conditions
   should be evaluated in sequence and only the body of the first matching case
   is evaluated.

Note that:

 - The use of a `default` case precludes violation reports for non-existing matches in `unique` and `priority`.
 - The default behaviour of a `case` statement is that of `priority`, but without violation checks.

**Use `case (...) inside` instead of `casex` or `casez` for matching don't care
bits.** Since set-membership `case (...) inside` matches `?` don't care bits in
the same way `casez` does, it should be used for clarity unless matching `x`s
or `z`s is specifically required. For example:

```
logic [3:0] state_q;
case (state_q) inside
  4'b000?: statement;
  4'b01?0: statement;
  4'b110?: statement;
endcase
```

**Use `case (1'b1)` for one-hot conditions.** For example:

```
logic [2:0] status_q;
unique case (1'b1) inside
  status_q[0]: statement;
  status_q[1]: statement;
  status_q[2]: statement;
endcase
```

As an aside, it is convenient to define a one-hot encoding in a union type with
another struct to provide named access to each member. For example, `status_q`
above could be redefined as:
```
typedef enum logic [2:0] {
  STATUS_START = 3'b001,
  STATUS_END   = 3'b010,
  STATUS_ERROR = 3'b100
} status_enum_t;
typedef union packed {
  status_enum_t u;
  struct packed {
    logic status_start;
    logic status_end;
    logic status_error;
  } ctrl;
} status_t;
status_t status_q;
```

**Minimise the amount of logic inside a case statement.** The rationale for
this is similar to extracting logic from `always_comb` blocks into `assign`
statements where possible: to make the control flow structure clearer to the
designer and tooling, and to provide opportunities for reuse or
further simplification. For example, avoid nesting `case` statements:

```
status_t status_q;
status_t next_status;
logic [3:0] mode_q;
always_comb begin
  next_status = state_q;
  unique case(1'b1)
    status_q.ctrl.stat_start:
      unique0 case (mode) inside
        4'b000?,
        4'b0?00: next_status = STATUS_ERROR;
        default: next_status = STATUS_END;
      endcase
    status_q.ctrl.status_end: ...;
    status_q.ctrl.status_error: ...;
  endcase
end
```

And instead extract a nested `case` into a separate process, providing a
result signal to use in the parent case:
```
status_t status_q;
status_t next_status;
status_t start_next_status;
logic [3:0] mode_q;
always_comb begin
  start_next_status = state_q;
  case (mode_q) inside
    4'b000?,
    4'b0?00: start_next_status = STATUS_ERROR;
    default: start_next_status = STATUS_END;
  endcase
end
always_comb begin
  unique case(1'b1)
    status_q.ctrl.status_start: next_status = start_next_status;
    status_q.ctrl.status_end: ...;
    status_q.ctrl.status_error: ...;
  endcase
end
```

Although this example seems simple, the `case`-based logic driving a state
machine can quickly become complicated.

<a name="expressions" class="anchor"></a>
## Expressions

**Make operator associativity explicit.** This is to avoid any ambiguity over
the ordering of operators. In particular, always bracket the condition of a
ternary/conditional expression (`?:`), especially if you are nesting them,
since they associate left to right, and all other arithmetic and logical
operators associate right to left.

```
... = (a && b) ||
      (c && d)
... = |(a[7:0] & b[7:0])
... = valid && (|a[3:0])
... = (a == b) ? c : d
... = cond_a              ? e1 :
      (cond_b && !cond_c) ? e2 :
                            e3
... = !(a[1:0] inside {2'b00, 2'b01}) &&
      ^(b[31:0])
```

**Make expression bit lengths explicit.** Although the SystemVerilog
specification provides rules for the extension of operands as inputs to binary
operations and assignments, these are complicated and not always obvious. In
particular, the extension is determined either by the operands or by the
context of the expression. Since there may be inconsistencies between tools,
particularly between simulation and synthesis, explicitly specifying expression
bit widths avoids these issues and makes the intent obvious. For example, pad
the result of a narrower expression for assignment:

```
logic [31:0] result;
logic [7:0] op1, op2;
assign result = {24'b0, {op1 & op2}};
```

Use an explicit type cast to specify the width of an intermediate expression
(note that integer literals are interpreted as 32-bit integers):

```
always_ff @(posedge i_clk or posedge i_rst)
  value_q <= i_rst ? value_t'(42) : value;
```

Special care should be taken with sub expressions, since their result length is
determined automatically by the width of the largest operand. For example,
without an explicit type cast to a 17-bit result around `a + b`, the carry out
bit would be lost:
```
logic [15:0] result, a b;
typedef logic [16:0] sum_t;
assign result = sum_t'(a + b) >> 1;
```

Capture carry out bits (even if they are unused) so the left-hand-side
assignment width matches the full width of the right hand side. Using a prefix
like `unused_` makes the process of signing off any related warnings with the
downstream synthesis and physical build simpler:
```
assign {unused_co, result} = a + b;
```

Exceptions to this rule can be made for the common constants 0, 1 and -1 to be
specified as `integer` literals, for example:
```
assign result = 0;
assign sum = value - 1;
```

**Use `signed` types for signed arithmetic,** and avoid implementing signed
arithmetic with manual sign extensions. Verilog uses the signedness of an
expression to determine how to extend its width (as well as inferring
signedness of parent expressions). Since the rules for sign determination is
similar to expression size but not the same, making it explicit avoids errors.
It also facilitates the use of optimised arithmetic implementations in
synthesis, particularly with multipliers. The following example (adapted from
[this presentation][arithmetic-gotcha])
shows how these rules can be confusing:

```
logic signed [3:0] a, b;
logic signed [4:0] sum;
logic ci;
sum = a + b + ci; // Unsigned addition due to unsigned ci.
sum = a + b + signed'(ci); // Signed addition, but ci == 1'b1 will be
                           // sign extended to 4'b1111 or -1.
sum = a + b + signed'({1'b0, ci}); // Safe sign extension.
```

Note that an operation is only considered signed if all of the operands are
signed, and that literal values can be specified as signed, for example:
`2'sb11` is -1 in 2 bits.

[arithmetic-gotcha]: http://www.sutherland-hdl.com/papers/2006-SNUG-Boston_standard_gotchas_presentation.pdf

**Avoid splitting arithmetic** between statements or modules. This facilitates
optimisation during synthesis, for example, to choose or generate an optimised
adder implementation for the given set of operands and carry ins/outs. Instead of:
```
logic [3:0] a, b, c;
logic [4:0] int_sum, sum;
int_sum = a + b;
{unused_co, sum} = int_sum + {1'b0, c};
```

All of the arithmetic contributing to `sum` can be written in a single
expression:
```
{unused_co, sum} = a + b + c;
```

<a name="constants" class="anchor"></a>
## Constants

**Avoid magic numbers.** All numeric constants, with the exception of zero and
one (for incrementing) should be defined symbolically. All assignment to
constants must be sized correctly to avoid width-mismatch warnings that must be
signed off later in the flow.

**Constants should be declared inside packages.** Derived constants with a
meaning specific to a module should be defined in the appropriate scope of the
module.

**Constants assigned to an `enum` port must be of the same `enum` type.** Not
doing so relies on an implicit conversion, which can have inconsistent
behaviour between tools. Assign an enum value directly, or by using a static
cast. For example:

```
package m_foo_pkg;
  typedef logic [1:0] {
    A, B, C, D
  } enum_t;
endpackage

module m_foo (
  input xm_foo_pkg::enum_t in,
  ...
);
...
endmodule

module m_bar (...);
  ...
  m_foo u_foo (
    // Tie the input to a constant value using the enum type, rather than
    // via a value of any other type.
    .in(xm_foo_pkg::D),
    ...
  );
  ...
endmodule
```


<a name="code-structure" class="anchor"></a>
## Code structure

<a name="modules" class="anchor"></a>
### Modules

**Place parameters and variables at the top of their containing scope.**
Nets/variables/parameters should be declared in the minimum scope in which they
will be used to avoid polluting namespaces. For example, nets global to a
module should be declared at the top of the module for use in the code that
follows.

**Separate combinatorial and sequential nets.** Declarations of combinatorial
and sequential nets should be separated into different sections for clarity.
This allows the flip-flops in the design to be seen clearly providing a feel
for the size and complexity of the block.

The following ripple-carry adder with registered outputs illustrates this
structuring:

```
module m_rca
  #(parameter p_width = 8)
  ( input  logic               i_clk,
    input  logic               i_rst,
    input  logic [p_width-1:0] i_op1,
    input  logic [p_width-1:0] i_op2,
    output logic               o_co,
    output logic [p_width-1:0] o_sum );

  // Wires.
  logic [p_width-1:0] carry;
  // Registers.
  logic [p_width-1:0] sum_q;
  logic               co_q;
  // Variables.
  genvar              i;

  assign carry[0] = 1'b0;
  assign {o_co, o_sum} = {co_q, sum_q};

  // Named generate block for per-bit continuous assignments.
  for (i = 0; i < p_width; i = i + 1) begin: bit
    assign {carry[i+1], sum[i]} = i_op1[i] + i_op2[i] + carry[i];
  end

  always_ff @(posedge i_clk or posedge i_rst) begin
    if (i_rst) begin
      sum_q <= {p_width{1'b0}};
      co_q  <= 1'b0;
    end else begin
      sum_q <= sum;
      co_q  <= carry[p_width-1];
    end
  end

endmodule
```

**Use `.*` and `.name()` syntax in some circumstances to simplify port lists in module
instantiations.** Doing so can reduce the amount of boilerplate code and thus the
scope for typing or copy-paste errors. The wildcard `.*` also provides additional checks:

- It requires all nets be connected.
- It requires all nets to be the same size.
- It prevents implicit nets from being inferred.

Named connections with `.name()` can be used with wildcards to add specific
exceptions, such as when names do not match or for unconnected or tied-off
ports. For example:

```
module foo (input logic i_clk,
            input logic i_rst,
            input logic in,
            output logic out);
  ...
endmodule

u_module foo (.*,
              .in(in),
              .out(out));
```

Bear in mind that implicit hookups wuth wildcards may obscure module
connectivity when navigating source code during debug. It is up to the designer
to make the right tradeoff. Specific exampls of where wildcard hookups are
useful are in wrapper modules and testbenches.

**Avoid logic in module instantiations.** By instantiating a module with a set
of named signals, mapping one-to-one with ports, it is easier to inspect the
port hookups and the widths of the signals for correctness. Not doing so
obscures functionality in the design.

**In parameter lists, separate parameters that are intended to be set
externally from secondary parameters that are only used internally.** There is
no way to prevent some parameters being set externally, ie with `localparam`,
so a comment can be used to do this, for example:

```
module m_rf
#(parameter
  p_entry_width = 32,
  p_num_entries = 64,
  // Internal parameter(s) - do not set.
  p_idx_width = $clog2(p_num_entries-1))
( ...,
  input logic [p_entry_width-1:0] wr_data,
  input logic [p_idx_width-1:0] wr_idx,
  input logic wr_en,
...
);
```


<a name="packages" class="anchor"></a>
### Packages

**Define packages to share definitions (types, constants, tasks, functions etc)
between multiple modules or IPs.**

**Qualify types, constants, tasks or functions with their package name and
avoid \* imports.** This resolves any potential ambiguity in the providence of
symbols to the designer and avoids polluting the current scope with all names
defined by the package. For example:

```
// Avoid
import m_core_pkg::*;

// Prefer
m_core_pkg::FIFO_RAM_WIDTH
m_core_pkg::grey_code(...)
```


<a name="assertions" class="anchor"></a>
### Assertions

**Assertions should be written in a separate file that is bound in to the
appropriate scope.** Verification tests must be written to specifically ensure
that the assertions are present in simulation.

**Assertion files must be named after the block they apply to, with an
`_assert.sv` suffix.** Where assertions have been split into different groups
to allow use in gate-level simulations (or other environments), the file name
may have a `_ports_assert.sv`, `_regs_assert.sv` or `_nets_assert.sv` suffix as
appropriate.


<a name="naming" class="anchor"></a>
## Naming

Clear and consistent naming is important for a design to be easily understood
and maintainability by a designer, but naming must facilitate easy manipulation
by various tools in the Frontend and Backend flows.

During Frontend debug, names should allow simple sorting and searching in a
wave viewer. By using common prefixes for related signals, sorting will place
them together. Similarly, common substrings are useful to filter a subset of
signals over, for example to select a set of registers or similar signals
different in pipeline stages.

Throughout the Backend flows, names must allow sensible flattening. It is
typical for synthesis to flatten the hierarchical structure and consequently
symbol names are derived from their place in the module hierarchy. A suitable
naming scheme really only requires consistency across a design. As an example,
a flip-flop clock pin might be named
`u_toplevel_u_submodule_p0_signal_q_reg_17_/CK` corresponding to the register
`u_toplevel/u_submodule/p0_signal_q[17]`.

**Names should be meaningful, whilst avoiding excessive verbosity.** For example,
`n3` should be avoided as it lacks meaning whereas `floating_point_opcode_bus` is
excessively long. `fp_opcode` is a reasonable compromise.

**Avoid using C/C++/Verilog/SystemVerilog/VHDL keywords as names.** Even if
they are not reserved names in the language being used in that file. For
example: `auto`, `unsigned`, `task`, `register` or `asm`.

**All names must be all lower case and underscore separated.**
For example:
```
module m_cpu;
module m_cpu_pkg;
logic unused_co
logic p3_ctrl
logic p4_prod_q
begin : ecc_encode
```

<a name="naming-prefixes-suffixes" class="anchor"></a>
### Prefixes and suffixes

Name prefixes are generally used to indicate object types (such as module
instances, flip flops, ports etc), and suffixes are generally used to convey
semantic information. A good standard set of prefixes and suffixes are
enumerated below:

<table class="table table-striped table-sm">
<thead>
  <th scope="col" style="width:20%">Prefix</th>
  <th scope="col">Usage</th>
</thead>
<tbody>
<tr>
  <td><code>i_</code></td>
  <td>Input port</td>
</tr>
<tr>
  <td><code>o_</code></td>
  <td>Output port</td>
</tr>
<tr>
  <td><code>io_</code></td>
  <td>Bidirecitonal (inout) port</td>
</tr>
<tr>
  <td><code>u_</code></td>
  <td>Module instance</td>
</tr>
<tr>
  <td><code>m_</code></td>
  <td>Module definition</td>
</tr>
<tr>
  <td><code>p_</code></td>
  <td>Parameter/localparam</td>
</tr>
<tr>
  <td><code>g_</code></td>
  <td>Generate block</td>
</tr>
<tr>
  <td><code>[a-z][0-9]_</code></td>
  <td>Pipeline stage</td>
</tr>
<tr>
  <td><code>unused_</code></td>
  <td>Unused signal for lint signoff</td>
</tr>
</tbody>
</table>

<table class="table table-striped table-sm">
<thead>
  <th scope="col" style="width:20%">Suffix</th>
  <th scope="col">Usage</th>
</thead>
<tbody>
<tr>
  <td><code>_clk</code></td>
  <td>Clock signal</td>
</tr>
<tr>
  <td><code>_gclk</code></td>
  <td>Gated clock signal</td>
</tr>
<tr>
  <td><code>_rst</code></td>
  <td>Reset signal</td>
</tr>
<tr>
  <td><code>_q</code></td>
  <td>Signal driven from a flip flop</td>
</tr>
<tr>
  <td><code>_n</code></td>
  <td>Active-low signal</code></td>
</tr>
<tr>
  <td><code>_t</code></td>
  <td>Type via a typedef</td>
</tr>
<tr>
  <td><code>_pkg</code></td>
  <td>Package</td>
</tr>
<tr>
  <td><code>_if</code></td>
  <td>Interface</td>
</tr>
</tbody>
</table>

Where signals are both active-low and require a suffix from elsewhere in the
table, the `_n` suffix should be appended without an extra underscore. For
example, `_q` becomes `_qn` for an active-low flop output, and `_clk` becomes
`_clkn` for an inverted clock.

The following code example shows appropriate usage of the above prefix and
suffix guidelines:

```
module xm_ctrl_fsm (
  input logic         i_clk,
  input logic         i_rst,
  input logic         i_ready,
  input logic         i_done,
  output logic [2:0]  o_control
);

  typedef enum logic [2:0] {
    IDLE = 3'b000,
    LOAD = 3'b110,
    DONE = 3'b001
  } state_t;

  state_t state_q;
  state_t next;

  assign o_control = state_q;

  always_ff @(posedge i_clk or posedge i_rst) begin
    if (i_rst) begin
      state_q <= IDLE;
    end else begin
      state_q <= next;
    end
  end

  always_comb begin
    unique case (state_q)
      IDLE: if (i_ready) next = LOAD;
            else         next = IDLE;
      LOAD: if (i_done)  next = DONE;
            else         next = LOAD;
      DONE:              next = IDLE;
    endcase
  end

endmodule
```

Another example illustrates the use of the pipeline prefix, using `e` to denote
an external signal and `p` an internal one:

```
module m_mempipe (
  input  logic        i_clk,
  input  logic        i_rst,
  input  logic        i_e1_valid,
  input  logic [18:2] i_e1_addr,
  output logic [31:0] o_e2_data
);
  ...
  logic        p2_valid_q;
  logic [31:0] p2_data;
  logic [31:0] p3_data_q;
  ...

  always_ff @(posedge i_clk or posedge i_rst) begin
    if (i_rst) begin
      p3_data_q <= 32'h00000000;
    end else if (e2_valid_q) begin
      p3_data_q <= p2_data;
    end
  end

  assign o_e2_data = p3_data_q;

endmodule

```

<a name="signal-naming" class="anchor"></a>
### Signal naming

A strict approach to signal naming should be taken to make it easier to
understand and navigate a design:

**To make clear their relationship to the structure of a module**. Prefixes and
suffices can denote, for example, whether a signal is an input or output, the
pipeline stage it corresponds to and whether it is driven by logic or directly
from a flip-flop. The exact naming convention will be tailored to a project,
but here are some examples:

```
i_p0_operand     // Input into pipeline stage 0.
p1_state         // A current state of a state machine.
p1_state_ns      // The next state.
state_clk        // A clock signal.
m1_sum_co_unused // An unused carryout bit from an addition.
m2_result_ff     // A registered result, driven by a flip-flop.
o_x4_state       // An output signal driven from stage x4.
```

**To allow simple sorting and searching in wave viewer**. By using common
prefixes for related signals, sorting will place them together. Similarly,
common substrings are useful to filter a subset of signals over, for example to
select a set of registers or similar signals different in pipeline stages.

**To be flattened sensibly by downstream tools**. It is typical for synthesis
to flatten the hierarchical structure of a SystemVerilog design. Consequently
symbols names are derived from their place in the module hierarchy. A suitable
naming scheme really only requires consistency across a design. As an example,
a flip-flop clock pin might be named
`u_toplevel_u_submodule_p0_signal_q_reg_17_/CK` corresponding to the register
`u_toplevel/u_submodule/p0_signal_q[17]`.


<a name="preprocessor" class="anchor"></a>
## Preprocessor

**In general, it should be possible to avoid any preprocessing of code.** Other
built-in language structures such as parameters and generate statements should
be used instead. Don't use local `define` statements in modules unless
absolutely necessary, use `localparam` instead of `define`:

```
// Avoid
`define CONSTANT 1

// Prefer
localparam p_constant = 1;
```

This is because SystemVerilog macro definitions are not scoped within a module,
which can easily lead to them 'leaking' between files in a filelist, making the
elaboration dependent on the ordering of the list.

For similar reasons, **use generate-if blocks instead of `ifdef`.**

```
// Avoid
`ifdef FLAG
...
`endif

// Prefer
generate
  if (p_flag) begin
  ...
  end
endgenerate
```

**If a local define is unavoidable, then a corresponding `undef` must be included
before the end of the file.** This is to avoid macro definitions polluting the
global namespace.

```
`define LOCAL_DEFINE

...

// End of the file or use of LOCAL_DEFINE
`undef LOCAL_DEFINE
```


<a name="formatting" class="anchor"></a>
## Formatting

Rules for formatting are not mandated so to provide some flexibility to
designer's own tastes and the inevitable exceptions to rules. Above all, the
most important issue with formatting is to maintain consistency within a
logical part of the design.

**Use spaces instead of tabs**, consitent with the accepted approach in other
programming languages for compatability with version control and editors etc.

**Split long lines or complex expressions with continuations or across
statements.** Apply indent as appropriate  for clarity. In this context, 'long'
is a reasonable value chosen by the author, but typically between 80 and 120
characters.

**Use begin and end to wrap `if`/`else`, `always_ff` and `always_comb`
blocks.** This adds consistency to the code and can help to prevent statements
from unintentionally being excluded from a block. Only use begin and end in
case alternatives when they contain multiple statements.


<a name="summary" class="anchor"></a>
## Summary

Verilog is a large language with features supporting different purposes. It is
used as a standard in hardware design but its specification does not define a
synthesizable subset. Although there is a general consensus on which features
can be used for synthesis, the fine details are determined by the particular
EDA tooling flow used by a design team. SystemVerilog is consequently used in a
conservative way for specifying synthesizable designs. The rules and rationale
given in this note outline some of the important aspects of a coding style for
hardware design. There are many more details of SystemVerilog's features that are
relevant; the references below are a good place to find out more.


<a name="refs" class="anchor"></a>
## References/further reading

- IEEE Standard for SystemVerilog (IEEE 1800-2012 and 1800-2017).

- [Sutherland HDL papers](http://www.sutherland-hdl.com/papers.html) on
  Verilog/SystemVerilog, in particular:

    * Stuart Sutherland and Don Mills, Standard gotchas subtleties in the
      Verilog and SystemVerilog standards that every engineer should know. SNUG 2006.
      ([PDF](http://www.sutherland-hdl.com/papers/2006-SNUG-Boston_standard_gotchas_paper.pdf))

    * Stuart Sutherland, A Proposal for a Standard Synthesizable SystemVerilog Subset. DVCon 2006.
      ([PDF](http://www.sutherland-hdl.com/papers/2006-DVCon_SystemVerilog_synthesis_subset_paper.pdf))

    * Stuart Sutherland and Don Mills, Synthesizing SystemVerilog: Busting the
      myth that SystemVerilog is only for verification, SNUG 2013.
      ([PDF](http://www.sutherland-hdl.com/papers/2013-SNUG-SV_Synthesizable-SystemVerilog_paper.pdf)).

    * Stuart Sutherland and Don Mills, Can my synthesis compiler do that? What ASIC
      and FPGA synthesis compilers support in the SystemVerilog-2012 standard, DVCon 2014
      ([PDF](http://www.sutherland-hdl.com/papers/2014-DVCon_ASIC-FPGA_SV_Synthesis_paper.pdf)).

- SystemVerilog's priority & unique - A Solution to Verilog's "full_case" & "parallel_case" Evil Twins!,
  Clifford E. Cummings, SNUG 2005
  ([PDF](http://www.sunburst-design.com/papers/CummingsSNUG2005Israel_SystemVerilog_UniquePriority.pdf)).

- Verilog HDL Coding, Semiconductor Reuse Standard, Freescale Semiconductor
  ([PDF](https://people.ece.cornell.edu/land/courses/ece5760/Verilog/FreescaleVerilog.pdf)).

- Complex Digital Systems, Synthesis, MIT OCW, 2005 (presentation slides,
  ([PDF](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-884-complex-digital-systems-spring-2005/lecture-notes/l05_synthesis.pdf)).
