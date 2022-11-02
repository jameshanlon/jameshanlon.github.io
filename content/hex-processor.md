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
correspond to the underlying hardware of a computer processor, or to provide a
useful reference for compilers and simulators, starting point for another
project or just a curiosity in itself.

First, to provide some background. The project is based on the Hex processor
architecture that was designed by [David
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
enough to fit on a single chip in the technology of the day. X draws on the
basic sequential features of the [occam programming
language](https://en.wikipedia.org/wiki/Occam_(programming_language)).

In my [implementation](https://github.com/jameshanlon/hex-processor), I have
created a simple C++ toolchain with a simulator, Hex assembler and X language
compiler, and a Verilog implementation of Hex. Before describing that, the
next two sections introducte Hex and X.

## The Hex architecture

The Hex architecture is described in detail in [a separate
PDF]({{'hex/hexb.pdf'|asset}}), but I will give a brief summary here and focus
on several important aspects for reference. Hex has four registers: program
counter ``pc``, operand register ``oreg`` and the A and B registers ``areg``
and ``breg`` used for expression evaluation. The architecture is agnostic of a
particular word size, but it has to be a miniumum of a byte and multiples of a
byte. In the included implementation the word size is 4 bytes. Hex has sixteen
instructions that are summarised in the following table. The instructions are
grouped into memory access with absolute or relative addressing modes, loading
of constants, branching, inter-register operations and supervisor calls.

<table class="table table-striped table-sm">
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
  <td>Store to absolute address from areg</td>
</tr>
<tr>
  <td><code>LDAC</code></td>
  <td><code>areg := oreg</code></td>
  <td>Load constant into areg</td>
</tr>
<tr>
  <td><code>LDBC</code></td>
  <td><code>breg := oreg</code></td>
  <td>Load constant into breg</td>
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
  <td><code>PFIX</code></td>
  <td><code>oreg := oreg << 4</code></td>
  <td>Positive prefix</td>
</tr>
<tr>
  <td><code>NFIX</code></td>
  <td><code>oreg = 0xFFFFFF00 | oreg << 4</code></td>
  <td>Negative prefix</td>
</tr>
<tr>
  <td><code>OPR</code></td>
  <td>-</td>
  <td>Inter-register operation</td>
</tr>
<tr>
  <td>&nbsp;&nbsp;<code>ADD</code></td>
  <td><code>areg := areg + breg</code></td>
  <td>Add areg and breg and set areg to the result</td>
</tr>
<tr>
  <td>&nbsp;&nbsp;<code>SUB</code></td>
  <td><code>areg := areg - breg</code></td>
  <td>Subtract areg and breg and set areg to the result</td>
</tr>
<tr>
  <td>&nbsp;&nbsp;<code>SVC</code></td>
  <td>-</td>
  <td>Supervisor call</td>
</tr>
</table>

### Prefixing

Prefixing using the ``PFIX`` and ``NFIX`` operations generates operand values
in ``oreg`` larger than the 4-bit instruction immediate. For example, the
following instructions generate the value 16 in ``oreg`` and use ``LDAC`` to
assign it to ``areg`` :

```
PFIX 1
LDAC 0
```

Prefixes can be chained to extend the operand range, for example, generating the
value 496 requires two positive prefixes before a load constant instruction:
```
PFIX 1
PFIX 15
LDAC 0
```

Negative values always require a negative prefix to fill the top most ``oreg``
bits with ones, so to load the value -1 into ``oreg`` then ``areg``:

```
NFIX 15
LDAC 15
```

And to load -512, a positive prefix is required to scale the negative value:

```
NFIX 14
PFIX 0
LDAC 0
```

### Inter-register opeations

The inter-register operations use the ``OPR`` opcode and consist only of
addition and substraction. The group can be extended by implementing additional
immediate opcodes to add new operations to the processor (such as other
arithmetic and bitwise operations). The 4-bit immediate supports up to 16
inter-register operations without the need for prefixing, but many more with
prefixing and the according overhead to form larger immediates. The following
instruction sequence adds two numbers from fixed locations in memory, with the
result written to ``areg``:

```
LDAM 1
LDBM 2
OPR ADD
```

A special inter-register operation is a supervisor call that transfers
control to the system to complete an action such as read or write from a
file, or to halt the program. The supervisor call type is encoded in the
``oreg`` and arguments and return values specific to the call type are passed
and returned on the stack using the standard calling convention. An example
code sequence to invoke the exit supervisor call is:

```
LDAC 0 # Set areg to 0, the exit opcode value.
LDBM 1 # Load the stack pointer in breg.
STAI 2 # Store areg into stack offset two as a parameter.
LDAC 0 # Load the exit opcode.
OPR SVC
```

### Load-store operations

There are two variants of load and store instructions: using absolute addresses
and addresses relative to a base address. Absolute addressing (``LDAM``,
``LDBM`` and ``STAM``) is intended to access objects in memory that are
allocated at offsets that are fixed with respect to a program, such as constant
values and global variables. Relative-addressing (``LDAI``, ``LDBI`` and
``STAI``) is typically used to access objects that are relative to a dynamic
position, such as the stack pointer, or index into an array. The particular
variants of load/store instructions is influenced by their targeting from a
compiler. Having pairs of load instructions that can write to ``areg`` or
``breg`` (such as ``LDAM`` and ``LDBM``) gives flexibility when generating
operands for binary operations, whereas having only single variants of stores
(``STAM`` and ``STAI``) fits most cases where expression results generated into
``areg`` need to be written to memory.

### Address generation

A special constant-loading instruction ``LDAP`` is used to generate bytewise
program addresses, relative to the program counter, such as for branch targets.

### Branching

For branching, a relative branch is provided with ``BR``, which can be used for
example to reach a label location. Conditional branch versions ``BRZ`` and
``BRN`` are used to implement logical binary operations (less than, equal etc)
and ``BRB`` is an absolute branch that is used, for example, to return to
a calling function using an address retrieved from memory.

## The X language

The X language is defined in [a separate PDF]({{'hex/xhexnotes.pdf'|asset}}). X
is simple enough that it can be compiled using simple techniques to the Hex
architecture, whilst providing enough flexibility to express complex programs
such as its own compiler (more on that later). X is an imperative language and
has features for procedure calling, composition of statements, looping and
conditional statements, expressions including function calls, and
representation of memory with variables and arrays. To give an indicative
example of X programming, the following program implements Bubblesort to sort
an array of four elements:

```
val length = 4;
var data[length];

proc sort(array a, val n) is
  var i;
  var j;
  var tmp;
{ i := 0;
  while i < n do
  { j := 0
  ; while j < n - i - 1 do
    { if a[j] > a[j+1] then
      { tmp := a[j]
      ; a[j] := a[j+1]
      ; a[j+1] := tmp
      }
      else skip
    ; j := j + 1
    }
  ; i := i + 1
  }
}

proc main() is
{ data[0] := 3
; data[1] := 2
; data[2] := 1
; data[3] := 0
; sort(data, length)
}
```

## Hex processor integrated circuit

A hardware implementation of the Hex processor is written in System Verilog,
[``processor.sv``](https://github.com/jameshanlon/hex-processor/blob/master/verilog/processor.sv),
in just 150 lines. This implementation is single cycle in that all elements of
instruction execution (ie instruction fetch from memory, decode, instruction
memory access and state writeback) are completed in that time. A separate
memory module,
[``memory.sv``](https://github.com/jameshanlon/hex-processor/blob/master/verilog/memory.sv)
implements a single-cycle random-access memory with two ports: one for
instruction fetch and the other for data access so that they can occur
simultaneously in the same cycle. Note that because memory access time
increases with the memory capacity, a implementation of Hex accessing a large
memory (ie more than a few thousand bytes) would add pipelining to hide the
latency to memory. Some degree of pipelining is standard in processor
implementations.

Using [OpenROAD](https://theopenroadproject.org/), an open-source tool chain
for performing synthesis, optimisation and physical layout of digital circuits,
we can compile Hex into an integrated circuit layout. OpenROAD uses the
[SkyWater Process Design Kit](https://github.com/google/skywater-pdk) (PDK),
for creating designs in 130 nm process technology, which was first
commercialised in 2001. The PDK is a collection of analog and digital cell
libraries, design rules and tooling. 

The final physical design has:

- A total of 9,719 standard cells.
- Occupies an area of 16,706 $^2\mu$.
- Clocks at 229 MHz.
- Total switching power is 4.12 mW. 

{{ macros.image('hex-processor/floorplan-stdcells.png', local=True) }}


## Hex tooling

There are three main tools provided in the Hex toolchain: a Hex simulator
``hexsim``, an assembler ``hexasm`` and an X compiler ``xcmp``.


## Similar projects

The following are some similar projects that include simple implementations of
processor toolchains.

- [Luz CPU](https://github.com/eliben/luz-cpu), a simulator, assembler and
  linker for the Luz processor architecture.

- [VSPL](https://www.cl.cam.ac.uk/~mr10/VSPL.html), is a very simple
  programming language designed to be used as a case study for comparing
  compiler implementations. The provided source distribution includes several
  implemenations of VSPL in different languages.
