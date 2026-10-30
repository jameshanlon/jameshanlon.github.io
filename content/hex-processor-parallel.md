---
Title: Building a Hex parallel processor
Slug: building-a-hex-parallel-processor
Date: 2026-10-30
Category: Computing and Silicon
Tags: computing, computer-architecture, microelectronics, verilog
Summary: A minimal set of changes for Hex to be a message-passing
         multiprocessor and X to write parallel programs for it.
Status: published
---

{% import 'post-macros.html' as macros %}

A few years ago I wrote about [an implementation of the Hex processor
architecture]({filename}/hex-processor.md): a deliberately simple processor, a
Verilog implementation of it, and a compiler for a simple imperative language
called X that targets it. The point of the exercise was to have a complete,
readable path from logic gates to a programming language, small enough to read
in an afternoon.

That version was resolutely sequential. Since Hex borrows a lot from the
[Transputer](https://en.wikipedia.org/wiki/Transputer), and X borrows its syntax
from [occam](https://en.wikipedia.org/wiki/Occam_(programming_language)), the
obvious omission was the thing those two were actually built for: parallelism
and message passing. The
[repository](https://github.com/jameshanlon/hex-processor) now has it with two
new instructions in the ISA, a link interface and a router in the RTL, the
concept of a process network in the simulator, and `par`, `chan` and the `!` and
`?` operators in X. The result is a self-contained parallel processor with a
parallel language targeted at it, where every layer is still small enough to
read.

## Two new instructions

Hex has four registers (PC, A, B and O) and 8-bit instructions made of a 4-bit
opcode and a 4-bit operand. The `OPR` opcode selects a register-to-register
sub-operation, and that is where the new instructions appear:

| Sub-op | Operand | Description |
|--------|---------|-------------|
| `IN`   | 0x4     | Receive a word from channel slot B into A |
| `OUT`  | 0x5     | Send word A to channel slot B |

Both perform a *synchronous rendezvous* over a point-to-point channel, meaning
that the two parties meet at the moment of transfer, so neither proceeds until
both have arrived. Whichever gets there first blocks until the other is ready,
at which point the value is exchanged and both continue. There is no buffering
visible to the program and the transfer doubles as synchronisation. The B register
selects one of the processor's four *link slots*; the A register carries the
value, received for `IN` and sent for `OUT`. Operating on an unwired slot is a
runtime error.

## The hardware

{{ macros.imagenothumb('hex-processor/hex-network.svg',
     caption='Four Hex cores connected by the router. Each core has a private memory and a link interface with four channel slots, wired to one router port. The data and acknowledgement networks are two structurally identical routers, drawn here as a single block.') }}

A core is a processor, a private memory, and a *link interface*. The processor
side of that interface is small: when an `IN` or `OUT` reaches its execute
phase, the core presents the slot index and the A register to the link
interface and stalls while the interface reports itself busy. The blocking
semantics of a channel operation are therefore a pipeline stall, rather than
an exception or trap, and the architectural state does not advance until the
operation completes.

The link interface holds a *route table* mapping each of its four slots to a
destination `(core, slot)` pair, and a one-word receive buffer per slot. Its
state machine operates as follows:

- An `OUT` injects a data *flit*, the granularity of network buffering, carrying
  `(dst core, dst slot, src core, word)`, then waits for an acknowledgement.
  A whole message is one flit, so there are no partial messages in flight to
  track.

- A delivered data flit lands in the receive buffer of the slot it names,
  whether or not that core has reached its `IN` yet.

- An `IN` whose slot buffer is full returns an acknowledgement to the source
  core recorded with the word, and completes.

Data moves eagerly in the network, one buffer deep, but the writer is only
released when the reader has actually taken the value. That preserves rendezvous
semantics while keeping the network itself free of any handshake state, and it
makes the two arrival orders differ only in who waits:

{{ macros.imagenothumb('hex-processor/hex-rendezvous.svg',
     caption='A rendezvous in each arrival order. The writer always stalls from its OUT until the acknowledgement returns; the reader only stalls if its IN finds the slot buffer empty.') }}

If the writer gets there first, its word is sitting in the reader's slot buffer
by the time the reader executes `IN`, so the `IN` completes immediately and
acknowledges. If the reader gets there first, its `IN` finds the buffer empty
and stalls until the flit lands. Either way the writer's `OUT` does not retire
until the acknowledgement comes back, so neither side can run ahead of the
other by more than the word in flight.

Acknowledgements travel on a network of their own. Sharing one network with
the data would allow an acknowledgement to sit behind data flits that cannot be
delivered until that same acknowledgement has released their writer, which is a
cycle. So there are two routers, structurally identical: a 4&times;4 crossbar
with a one-deep buffer per input, round-robin arbitration per output, and
registered outputs that back-pressure their input buffer when the destination
is not ready. The crossbar keeps no per-channel state, and a flit's destination
core selects its output port directly.

{{ macros.imagenothumb('hex-processor/hex-router.svg',
     caption='One plane of the router. Each output port has a round-robin arbiter that grants among the input buffers addressed to it, driving the mux that reads the granted buffer; the result is registered, and an output that cannot drain holds its flit and back-pressures that buffer.') }}

Topology is then a matter of configuration rather than elaboration. The cores
all connect to the routers, and the per-core route tables are programmed over a
configuration port while reset is asserted. Any topology that fits within four
cores of four links each, such as a pipeline, a ring, a tree, a line of
bidirectional neighbours, is just a different set of route table entries.

## Mapping X onto it

X was extended with four new syntax elements: `chan` declarations and formal
parameters, a `par` statement, and `!` and `?` operators for sending and
receiving.

```text
proc relay(chan in, chan out) is
  var v;
  { in ? v; out ! v }
```

A `chan` formal is compiled as a one-word value holding a link slot index, so
`out ! v` evaluates `v` into A, the channel expression into B, and emits `OPR
OUT`. Receiving is the same in reverse, with `OPR IN` leaving the word in A to
be stored into the target variable or array element. Channels are ordinary
values in the generated code, which is what makes it possible to write a
process once and run it on several cores with different arguments.

The `par` statement is only supported as the body of the `main` process. The
compiler then treats this as a description of a static process network rather
than as a statement to generate code for. Additionally, each branch must be a
call to a procedure, and its arguments must be channels; that branch becomes one
processor, the called procedure becomes its entry point, and its channel
arguments are assigned link slots 0, 1, 2… in argument order. A channel named by
two different branches becomes a wiring edge between the two slots it occupies.
Permitting `par` to occur at arbitrary points would require runtime allocation
of execution resources, increasing the hardware complexity considerably. Occam
has the concept of `placed par` to allocate processes to processors, and regular
`par` maps processes to local threads.

{{ macros.imagenothumb('hex-processor/hex-par-mapping.svg',
     caption='The three-stage pipeline of examples/pipe.x mapped onto hardware. Each par branch becomes a core, each channel argument takes the next link slot, and each channel becomes one wiring edge, written into both endpoints\' route tables at reset.') }}

Both endpoints of an edge are programmed, so either may be the writer; the
route table is consulted only by `OUT`, since an `IN` takes the source core
from the word waiting in its slot buffer.

The compiler then checks the things that make the network well formed, and
rejects the program with a source location otherwise: every channel must have
exactly two endpoints, with exactly one writer and one reader, and no process
may use more than four channels. These are static checks on the network, done
once at compile time, rather than runtime errors.

Each processor is then compiled separately. The source is re-parsed, `main` is
replaced by a call to that processor's entry procedure with its slot indices as
literal constants, and the normal pipeline runs to produce an image. So every
core gets an image containing only the code it can reach, with its channel
arguments constant-folded into slot numbers.

The output of the compiler is a *network container*, containing the magic `HEXN`,
a processor count, the list of wiring edges as `(proc, slot, proc, slot)`
quadruples, and then one size-prefixed image per processor. A file without the
magic is treated as a single plain image, so the container is transparent to
everything that handles sequential programs.

The simulator and RTL testbench consume the same container. `hexsim` builds a
channel object per edge, boots one simulated processor per image, steps them
round-robin, and implements the rendezvous directly: a channel is idle,
writer-waiting or reader-waiting, and a processor that blocks simply does not
advance its PC. It reports the exit code of the first processor to halt, and
raises an error naming the blocked processors and slots when no core is runnable
(deadlock detection for free). `hextb`, the Verilator testbench, loads the
images into the RTL cores' memories, walks the same edge list to program both
directions of each route table during reset, and services each core's syscalls.
Cores with no image are filled with a halt loop so they stay quiescent.

The two are cross-checked against each other: each message-passing example is
compiled once to a container, then run on both the C++ simulator and the RTL,
and the outputs must agree. There are also RTL testbenches for the router, the
link interface and a single core in isolation.

## Examples

The smallest interesting program is a three-stage pipeline. Three processes, two
channels, three cores:

```text
val put = 1;

proc putval(val c) is put(c, 0)

proc source(chan out) is out ! 'P'

proc relay(chan in, chan out) is
  var v;
  { in ? v; out ! v }

proc sink(chan in) is
  var v;
  { in ? v; putval(v) }

proc main() is
  chan a;
  chan b;
  par { source(a); relay(a, b); sink(b) }
```

This is the program whose mapping is drawn above. Running it prints `P`,
having moved one word across two cores:

```bash
$ xcmp examples/pipe.x -o pipe.bin
$ hexsim pipe.bin
P
$ hextb pipe.bin
Loaded 3 processor image(s)
P
```

A better demonstration is the concurrent prime sieve, the classic occam
example. A generator emits the integers from 2 upwards down a pipeline of
filters, terminated by a zero sentinel. The first value a filter receives is
prime, which it prints; thereafter it forwards only the values not divisible by
that prime:

```text
proc generator(chan out) is
  var i;
{ i := 2;
  while i <= 12 do
  { out ! i;
    i := i + 1
  };
  out ! 0
}

proc filter(chan in, chan out) is
  var p;
  var v;
{ in ? p;
  printn(p);
  putval('\n');
  v := 1;
  while v ~= 0 do
  { in ? v;
    if v = 0
    then
      out ! 0
    else if rem(v, p) ~= 0
      then
        out ! v
      else
        skip
  }
}

proc main() is
  chan a;
  chan b;
  chan c;
  par { generator(a); filter(a, b); filter(b, c); sink(c) }
```

The same `filter` procedure runs on two different cores with different channel
arguments, which works precisely because channels are values. With four cores
this prints the first three primes, `2`, `3` and `5`. (`sink` is a `filter`
that prints its prime and then just drains the rest, and `printn` and `rem` are
ordinary X code, since Hex has no multiply or divide instruction.)

The `examples/` directory has more: a token ring, a worker farm
with fan-out and fan-in, a parallel reduction over a binary tree of cores, a
prefix sum along a line, a nearest-neighbour halo exchange with bidirectional
channels, a divide-and-conquer sort with a stream merge, and a systolic
multiply-accumulate pipeline for Horner's rule. Four cores is not many, but it
is enough for the shape of each of these to be the real one.

## Links

- [hex-processor on GitHub](https://github.com/jameshanlon/hex-processor)
- [From logic gates to a programming language using the Hex
  architecture]({filename}/hex-processor.md), the original note on the
  sequential processor, compiler and tooling
