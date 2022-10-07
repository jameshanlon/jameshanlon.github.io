---
Title: Logic gates to a programming language using the Hex architecture
Date: 2022-10-02
Category: projects
Tags: computing, computer architecture, microelectronics
Status: published
---

{% import 'post-macros.html' as macros %}

This note walks through a hardware implementation of a simple processor and
complete compiler for a sequential programming language targeted at it. The
processor architecture is designed to as simple as possible but provide a
sensible target for the compilation of complex programs using simple
strategies. The implementation of the processor and its supporting tooling is
small and self contained so to be understandable and easily extendable. Besides
being an interesting side project, my motivation was to create a complete
example as a point of reference to explain how programming languages work and
correspond to the underlying hardware of a computer processor.

The Hex processor architecture was designed by [David
May](http://people.cs.bris.ac.uk/~dave) as a vehicle for teaching about how
computers work at the University of Bristol, whilst being flexible enough to
execute substantial programs and easily extensible. David provided a simulator
written in C and a bootstrapping compiler written in an accompanying simple
language called X. The design of Hex draws on the [Transputer
architecture](https://en.wikipedia.org/wiki/Transputer) and the earlier [Simple
42](http://people.cs.bris.ac.uk/~dave/S42ISA.pdf), particulary with the use of
short instruction encodings, prefixing mechanism for creating larger immediates
and A, B and C registers for expression evaluation. These kind of architectural
features made the silicon implementation of the Simple 42 and Transputers small
enough to fit on a single chip. X draws on the basic sequential features of the
[occam programming
language](https://en.wikipedia.org/wiki/Occam_(programming_language)).

In my [implementation](https://github.com/jameshanlon/hex-processor), I have
created a simple C++ toolchain with a simulator, Hex assembler and X language
compiler. I have also created a Verilog implementation of Hex that is simulated
with Verilator.

## Hex architecture

The Hex architecture is described in detail in [a separate
PDF]({{'hex/hexb.pdf'|asset}}). It has four registers: program counter ``pc``,
operand register ``oreg`` and the A and B registers ``areg`` and ``breg`` used
for expression evaluation. It has sixteen instructions that are summarised in
the following table. The instructions are grouped into memory access with
absolute or relative addressing modes, loading of constants, branching,
supervisor calls and inter-register operations. The latter group consist only
of addition and substraction operations, but this group can be extended by
implementing additional immediate opcodes.

<table class="table">
<thead>
  <th scope="col">Opcode</th>
  <th scope="col">Behaviour</th>
  <th scope="col">Description</th>
</thead>
<tbody>
<tr>
  <td><code>LDAM</code></td>
  <td><code>areg := mem[oreg]</code></td>
  <td>Load from memory with an absolute address into areg</td>
</tr>
<tr>
  <td><code>LDBM</code></td>
  <td><code>breg := mem[oreg]</code></td>
  <td>Load from memory with an absolute address into breg</td>
</tr>
<tr>
  <td><code>STAM</code></td>
  <td><code>mem[oreg] := areg</code></td>
  <td>Store absolute from areg</td>
</tr>
<tr>
  <td><code>LDAC</code></td>
  <td><code>areg := oreg</code></td>
  <td>Load absolute into areg</td>
</tr>
<tr>
  <td><code>LDBC</code></td>
  <td><code>breg := oreg</code></td>
  <td>Load absolute into breg</td>
</tr>
<tr>
  <td><code>LDAP</code></td>
  <td><code>areg := pc + oreg</code></td>
  <td>Load program counter-relative address into areg</td>
</tr>
<tr>
  <td><code>LDAI</code></td>
  <td><code>areg := mem[areg + oreg]</code></td>
  <td>Load from memory with base and offset into areg</td>
</tr>
<tr>
  <td><code>LDBI</code></td>
  <td><code>breg := mem[breg + oreg]</code></td>
  <td>Load from memory with base and offset into breg</td>
</tr>
<tr>
  <td><code>STAI</code></td>
  <td><code>mem[breg + oreg] := areg</code></td>
  <td>Store to memory with base and offset from areg</td>
</tr>
<tr>
  <td><code>BR</code></td>
  <td><code>pc := pc + oreg</code></td>
  <td>Branch relative</td>
</tr>
<tr>
  <td><code>BRZ</code></td>
  <td><code>if areg = 0: pc := pc + oreg</code></td>
  <td>Conditional branch relative on areg being zero</td>
</tr>
<tr>
  <td><code>BRN</code></td>
  <td><code>if areg < 0: pc := pc + oreg</code></td>
  <td>Conditional branch relative on areg being negative</td>
</tr>
<tr>
  <td><code>BRB</code></td>
  <td><code>pc := breg</code></td>
  <td>Absolute branch</td>
</tr>
<tr>
  <td><code>OPR</code></td>
  <td><code></code></td>
  <td>Inter-register operation</td>
</tr>
<tr>
  <td>&nbsp;&nbsp;<code>ADD</code></td>
  <td><code>areg := areg + breg</code></td>
  <td>Add areg and breg and set areg to the result</td>
</tr>
<tr>
  <td>&nbsp;&nbsp;<code>SUB</code></td>
  <td><code>areg := areg + breg</code></td>
  <td>Subtract areg and breg and set areg to the result</td>
</tr>
<tr>
  <td><code>SVC</code></td>
  <td><code></code></td>
  <td>System call</td>
</tr>
</table>
