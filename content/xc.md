---
Title: The XC Programming Language 
Date: 2014-12-13
Category: notes 
Tags: computing, computer-architecture, programming-languages 
Status: published 
---

{% import 'post-macros.html' as macros %}

XC is a programming language developed by XMOS for real-time embedded parallel
programming of their XCore processor architecture. XC is based on the features
for parallelism and communication in occam, and the syntax and some sequential
features of C. In addition, XC provides primitives to expose hardware
resources: locks, ports and timers. XC programs can be executed with levels of
I/O real-time performance that is usually attributed to FPGA or ASIC devices.
The design of XC was heavily influenced by the occam programming language,
which first introduced channel communication, alternation, ports and timers.
Occam was developed by [David
May](https://en.wikipedia.org/wiki/David_May_(computer_scientist)) and built on
the [Communicating Sequential Processes]() formalism, a process algebra
developed by [Tony Hoare](https://en.wikipedia.org/wiki/Tony_Hoare).

This note was originally written for
[Wikipedia](https://en.wikipedia.org/w/index.php?title=XC_(programming_language)),
but the content was removed owing to it being too much like a manual. To save
it from being lost, I've posted it here (December 2021).


## Architectural model

An XC program executes on a collection of XCore tiles. Each tile contains one
or more processing cores and resources that can be shared between the cores,
including I/O and memory. All tiles are connected by a communication network
that allows any tile to communicate with any other tile. A given target system
is specified during compilation and the compiler ensures that a sufficient
number of tiles, cores and resources are available to execute the program being
compiled. 


## Features

The following sections outline the key features of XC.

### Parallelism

Statements in XC are executed in sequence (as they are in C), so that in the
execution of:

```C
f(); g();
```

the function `g` is only executed once the execution of the function `f` has
completed. A set of statements can be made to execute in parallel using a `par`
statement, so that the statement

```C
par { f(); g(); }
```

causes `f` and `g` to be executed simultaneously. The execution of parallel
statement only completes when each of the component statements have completed.
The component statements are called tasks in XC.

Because the sharing of variables can lead to race conditions and
non-deterministic behaviour, XC enforces parallel disjointness. Disjointness
means that a variable that is changed in one component statement of a par may
not be used in any other statement.

Parallel statements can be written with a replicator, in a similar fashion to a
for loop, so that many similar instances of a task can be created without
having to write each one separately, so that the statement:

```C
par (size_t i=0; i<4; ++i)
  f(i);
```

is equivalent to:

```C
par { f(0); f(1); f(2); f(3); }
```

The tasks in a parallel statement are executed by creating threads on the
processor executing the statement. Tasks can be placed on different tiles by
using an `on` prefix. In following example:

```C
par {
  on tile[0] : f();
  par (size_t i=0; i<4; ++i)
    on tile[1].core[i] : g();
}
```

the task `f` is placed on any available core of tile 0 and instances of the task
g placed on cores 0, 1, 2 and 3 of tile 1. Task placement is restricted to the
main function of an XC program. Conceptually, this is because when an XC
program is compiled, it is divided up at its top level, into separately
executable programs for each tile. 

### Communication

Parallel tasks are able to communicate with each other using interfaces or channels.
Interfaces

An interface specifies a set of transaction types, where each type is defined
as a function with parameter and return types. When two tasks are connected via
an interface, one operates as a server and the other as a client. The client is
able to initiate a transaction with the corresponding server, with syntax
similar to a conventional function call. This interaction can be seen as a
remote procedure call. For example, in the parallel statement:

```C
interface I { void f(int x); };
interface I i;
par {
  select { // server
    i.f(int x):
      printf("Received %d\n", x);
      break;
  }
  i.f(42); // client
}
```

the client initiates the transaction `f`, with the parameter value 42, from the
interface `i`. The server waits on the transaction (as a case in the select
statement) and responds when the client initiates it by printing out a message
with the received parameter value. Transaction functions can also be used for
two-way communication by using reference parameters, allowing data to be
transferred from a client to a server, and then back again.

Interfaces can only be used by two tasks; they do not allow multiple clients to
be connected to one server. The types of either end of an interface connection
of type `T` are server interface `T` and client interface `T`. Therefore, when
interface types are passed as parameters, the type of connection must also be
specified, for example:

```C
interface T i;
void s(server interface T i) { ... }
void c(client interface T i) { ... }
par {
  s(i);
  c(i);
}
```

Transaction functions in an interface restrict servers to reacting only in
response to client requests, but in some circumstances it is useful for a
server to be able to trigger a response from the client. This can be achieved
by annotating a function in the interface with no parameters and a void return
type, with `[[notification]]` slave. The client waits on the notification
transaction in a select statement for the server to initiate it. A
corresponding function can be annotated with `[[clears_notification]]`, which is
called by the slave to clear the notification. In the following simple example:

```
interface I {
  void f(int x);
  [[notification]] slave void isReady();
  [[clears_notification]] int getValue();
};
interface I i1, i2;
par {
  for (size_t i=0; i<2; ++i) { // server
    select {
      i2.f(int x):
        i1.isReady();
        break;
      i1.getValue() -> int data:
        data = 100;
        break;
    }
  }
  { int d;                     // client 1
    select {
      i1.isReady():
        d = i1.getValue();
        break;
    }
  }
  i2.f(42);                    // client 2
}
```

when client 2 initiates the transaction function `f`, the server notifies client
1 via the transaction function `isReady`. Client 1 waits for the server
notification, and then initiates `getValue` when it is received.

So that it is easier to connect many clients to one server, interfaces can also
be declared as arrays. A server can select over an interface array using an
index variable.

Interfaces can also be extended, so that basic client interfaces can be
augmented with new functionality. In particular, client interface extensions
can invoke transaction functions in the base interface to provide a layer of
additional complexity.

### Channels

Communication channels provide a more primitive way of communicating between
tasks than interfaces. A channel connects two tasks and allows them to send and
receive data, using the in `<:` and out `:>` operators respectively. A
communication only occurs when an input is matched with an output, and because
either side waits for the other to be ready, this also causes the tasks to
synchronise. In the following:

```C
chan c;
int x;
par {
  c <: 42;
  c :> x;
}
```

the value 42 is sent over the channel `c` and assigned to the variable `x`.

### Streaming channels

A streaming channel does not require each input and matching output to
synchronise, so communication can occur asynchronously.

### Event handling

The select statement waits for events to occur. It is similar to the
alternation process in occam. Each component of a select is an event, such as
an interface transaction, channel input or port input (see #IO), and an
associated action. When a select is executed, it waits until the first event is
enabled and then executes that event's action. In the following example:

```C
select {
  case left :> v:
    out <: v;
    break;
  case right :> v:
    out <: v;
    break;
}
```

the select statement merges data from left and right channels on to an out
channel.

A select case can be guarded, so that the case is only selected if the guard
expression is true at the same time the event is enabled. For example, with a
guard:

```C
case enable => left :> v:
  out <: v;
  break;
```

the left-hand channel of the above example can only input data when the
variable enable is true.

The selection of events is arbitrary, but event priority can be enforced with
the `[[ordered]]` attribute for selects. The effect is that higher-priority
events occur earlier in the body of the statement.

To aid in creating reusable components and libraries, select functions can be
used to abstract multiple cases of a select into a single unit. The following
select function encapsulates the cases of the above select statement:

```C
select merge(chanend left, chanend right, chanend out) {
  case left :> v:
    out <: v;
    break;
  case right :> v:
    out <: v;
    break;
}
```

so that the select statement can be written:

```C
select {
  merge(left, right, out);
}
```

### Timing

Every tile has a reference clock that can be accessed via timer variables.
Performing an output operation on a timer reads the current time in cycles. For
example, to calculate the elapsed execution time of a function `f`:

```C
timer t;
uint32_t start, end;
t :> start;
f();
t :> end;
printf("Elapsed time %u s\n", (end-start)/CYCLES_PER_SEC);
```

where `CYCLES_PER_SEC` is defined to be the number of cycles per second.

Timers can also be used in select statements to trigger events. For example,
the select statement:

```C
timer t;
uint32_t time;
...
select {
  case t when timerafter(time) :> void:
    // Action to be performed after the delay
    ...
    break;
}
```

waits for the timer `t` to exceed the value of time before reacting to it. The
value of `t` is discarded with the syntax `:> void`, but it can be assigned to a
variable `x` with the syntax `:> int x`.

### IO

Variables of the type port provide access to IO pins on an XCore device in XC.
Ports can have power-of-two widths, allowing the same number of bits to be
input or output every cycle. The same channel input and output operators `<`
and `>` respectively are used for this.

The following program continuously reads the value on one port and outputs it
on another:

```C
#include <xs1.h>
in port p = XS1_PORT_1A;
out port q = XS1_PORT_1B;
int main (void) {
  bool b;
  while (1) {
    p :> b;
    q <: b;
  }
}
```

The declaration of ports must have global scope and each port must specify
whether it is inputting or outputting, and is assigned a fixed value to specify
which pins it corresponds to. These values are defined as macros in a system
header file (`xs1.h`).

By default, ports are driven at the tile's reference clock. However, clock
block resources can be used to provide different clock signals, either by
dividing the reference clock, or based on an external signal. Ports can be
further configured to use buffering and to synchronise with other ports. This
configuration is performed using library functions. Port events

Ports can generate events, which can be handled in select statements. For
example, the statement:

```C
select {
  case p when pinseq(v) :> void:
    printf("Received input %d\n", v);
    break;
}
```

uses the predicate when `pinseq` to wait for the value on the port `p` to equal `v`
before triggering the response to print a notification.

### Port timing

To be able to control when outputs on a port occur with respect to the port's
clock, outputs can be timestamped or timed. The timestamped statement:

```C
p <: v @ count;
```

causes the value `v` to be output on the port `p` and for count to be set to the
value of the port's counter (incremented by one each reference clock cycle).
The timed output statement:

```C
p @ count <: v;
```

causes the port to wait until its counter reaches the value of count before the
value v is output.

### Multiplexing tasks onto cores

By default, each task maps to one core on a tile. Because the number of cores
is limited (eight in current XCore devices), XC provides two ways to map
multiple tasks to cores and better exploit the available cores.

Server tasks that are composed of a never-ending loop containing a select
statement can be marked as combinable with the attribute `[[combinable]]`. This
allows the compiler to combine two or more combinable tasks to run on the same
core, by merging the cases into a single select.

Tasks of the same form as combinable ones, except that each case of the select
handles a transaction function, can be marked with the attribute
`[[distributable]]`. This allows the compiler to convert the select cases into
local function calls.

### Memory access

XC has two models of memory access: safe and unsafe. Safe access is the default
in which checks are made to ensure that:

- memory accesses do not occur outside of their bounds;
- memory aliases are not created;
- dangling pointers are not created.

These guarantees are achieved through a combination of a different kinds of
pointers (restricted, aliasing, movable), static checking during compilation
and run-time checks.

Unsafe pointers provide the same behaviour as pointers in C. An unsafe pointer
must be declared with the unsafe keyword, and they can only be used within
`unsafe { ... }` regions.

### Additional features

#### References

XC provides references, that are similar to those in C++ and are specified with
the & symbol after the type. A reference provides another name for an existing
variable, such that reading and writing it is the same as reading and writing
the original variable. References can refer to elements of an array or
structure and can be used as parameters to regular and transaction functions.

#### Nullable types

Resource types such as interfaces, channel ends, ports and clocks must always
have a valid value. The nullable qualifier allows these types to have no value,
which is specified with the `?` symbol. For example, a nullable channel is
declared with:

```C
chan ?c;
```

Nullable resource types can also be used to implement optional resource
arguments for functions. The `isnull()` builtin function can be used to check
if a resource is null.

#### Multiple returns

In XC, functions can return multiple values. For example, the following
function implements the swap operation:

```C
{int, int} swap(int a, int b) {
  return {b, a};
}
```

The function swap is called with a multiple assignment:

```C
{x, y} = swap(x, y);
```

## Multicore Hello World

The following program prints `Hello World` on four processors:

```C
#include <stdio.h>
#include <platform.h>

void hello(int id, chanend cin, chanend cout){
  if (id > 0) cin :> int;
  printf("Hello from core %d!", id);
  if (id < 3) cout <: 1;
}

int main(void) {
  chan c[3];
  par (int i=0; i<4; i++)
    on tile[i] : hello(i, c[i], c[(i+1)%4]);
  return 0;
}
```

## References and further reading

- David May. The XMOS XS1 Architecture
   ([PDF](http://www.xmos.com/download/public/The-XMOS-XS1-Architecture\(X7879A\).pdf)).
- Douglas R. Watt. Programming XC on XMOS Devices
   ([PDF](https://www.xmos.com/download/public/XC-Programming-Guide\(X1009B\).pdf)).
- The XMOS programming guide
   ([HTML](https://web.archive.org/web/20141129060750/https://www.xmos.com/support/xtools/documentation?subcategory=Programming%20in%20C%20and%20XC&component=17653),
   [PDF](https://www.xmos.com/download/public/XMOS-Programming-Guide-\(documentation\)\(E\).pdf))
- The XC Language Specification
   ([HTML](https://web.archive.org/web/20141129060737/https://www.xmos.com/support/xtools/documentation?subcategory=Programming%20in%20C%20and%20XC&component=14805))
