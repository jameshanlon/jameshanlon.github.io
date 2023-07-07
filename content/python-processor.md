---
Title: Thoughts on building a Python processor
Date: 2023-06-27
Category: notes
Tags: computing, computer-architecture
Summary: A rationale and strawman for a processor to accelerate
         dynamic-language workloads.
Status: published
---

{% import 'post-macros.html' as macros %}

I have recently spent some time thinking about how hardware can be architected
and optimised to better support high-level dynamic languages such as Python and
JavaScript. There appears to be a significant gap between the way processors
and memory systems are built, which is to prioritise performance,  and the
characteristics of dynamic-language workloads, which prioritise ease of use. I
argue that dynamic languages are setting the direction of travel in the way we
use computers and this gap presents a huge opportunity for new hardware
innovation.

## Dynamic languages

According to [Stack Overflow's 2023 developer survey][dev-survey], JavaScript
has now been the most commonly-used language for the last 11 years and Python
has become the third most commonly-used language amongst all developers and the
first amongst non-professional developers and those learning to code. Nestled
amongst the most common languages are also TypeScript (a variant of
JavaScript), C#, PHP, Lua and Ruby. Applications of these languages are wide
ranging and varied, across all aspects of industry, science, business and
government.

Dynamic languages have become popular because they are easy to use when
compared with their statically-compiled counterparts. There are many aspects of
the languages that [contribute to this][dynamic-languages], such as dynamic
typing, high-level features, no requirement for a compilation step to produce
an executable format (leading to rapid iteration times), portability between
platforms, powerful debugging due to runtime introspection, integration with
editors and IDEs and natural support for metaprogramming. Ease of use improves
programmer productivity and widens participation to non-professionals and those
without expertise in low-level programming. These benefits are also a critical
factor in the development of new application areas and technologies such as AI,
where research and practice moves rapidly and participation across academia and
industry is broad.

The cost of these benefits when compared with compiled languages is a runtime
performance overhead due to the additional work the language implementation
must do, for example to resolve names and types. The overhead depends on the
workload, but is often in the realms of tens to hundreds of times slower. The
evidence in the use of dynamic languages however is proof that this performance
overhead is acceptable price to pay for their benefits. Having said this, there
are ongoing substantial efforts to close the gap by optimising the language
implementations and compilation strategies. As far as I can see, this effort
has not extended to optimisation of the underlying hardware.

[dev-survey]: https://survey.stackoverflow.co/2023/#technology-most-popular-technologies
[dynamic-languages]: https://erik-engheim.medium.com/the-many-advantages-of-dynamic-languages-267d08f4c7

## Python and AI

In this remainder of this note I will focus on Python and its application to
AI, a domain that is is significant enough to cause the development of new
computer hardware and rapid adoption of new process, integration and packaging
technologies.

Python has established itself as the main programming language in AI, and this
is due to ease-of-use considerations. Programming in AI is typically done using
*frameworks*, meaning a library that provides facilities to express a
computation that is compiled and run within the program, rather than expressing
the computation directly in the programming language. TensorFlow and PyTorch
are two pre-eminent examples, but with PyTorch having [taken the
lead][pytorch-lead] in becoming the most widely-used framework. TensorFlow
established itself early with support from Google, but it has lost its
dominance to PyTorch because PyTorch was easier to use and more flexible. It
was thus more widely adopted and more quickly applied to new application areas.

PyTorch's [first design principle][pytorch-principle] is *usability over
performance* which clearly indicates ease of use is the driving force in AI
model development and deployment. PyTorch's third design principle is *Python
first* meaning that working in Python natively (using the features of the
language) provides the best experience and results for users, rather than
deferring to optimised compiled-language libraries. PyTorch's primacy and clear
prioritisation of ease of use indicates the direction of travel: that Python
will continue to become a first-class citizen in AI programming and so its
performance will be increasingly under scrutiny.

Since around 2012, AI has undergone a renaissance by scaling the performance of
deep neural networks with GPUs. Looking forward, there are many ways in which AI
models are expected to develop, requiring programming techniques and hardware to
develop to provide these capabilities too:

- **Model size** is growing and will continue to grow. Although GPT-3 has 175
  bn parameters, there are an estimated 86 bn neurons in the human brain and an
  order-of 100 tn parameters (albeit encoded using analog mechanisms). It is
  likely that sparsity will increasingly be required to train and access these
  models efficiently.

- **Conditional sparsity** through conditionality in the structure of a
  network, eg routing of activity based on the data. In a dense network, every
  input interacts with every weight, but our brains don't fire all neurons in
  response to every stimulus, and **unconditional sparsity** that is not
  dependent on the input, such as from pruning of connections.

- **Symbolic representations**. Symbolic AI programs are based on creating
  explicit structures and behaviour rules. This approach was the dominant
  paradigm in AI from the 1950s up to the mid 1990s. It is however considered a
  complementary technique to deep learning, possibly reflecting [the fast and
  slow parts of the human cognitive system][rossi22]. Examples are [decision
  trees][decision-trees] and [PAC learning][pac-learning].

- **Composition**. New models will be created from parts such as whole sub models,
  or other reusable components. This is the way any complex system is
  constructed, including our brains.

[pytorch-lead]: https://www.semianalysis.com/p/nvidiaopenaitritonpytorch
[pytorch-principle]: https://pytorch.org/docs/stable/community/design.html
[rossi22]: https://aaai-2022.virtualchair.net/plenary_13.html
[decision-trees]: https://en.wikipedia.org/wiki/Decision_tree
[pac-learning]: https://en.wikipedia.org/wiki/Probably_approximately_correct_learning

## Python performance

Broadly, the performance of Python programs can be improved at three levels:

1. Optimising the application.
2. Optimising the language implementation.
3. Optimising the hardware.

The work in *Quantitative Overhead Analysis for Python* [1] provides a detailed
analysis of overheads in CPython. [^python-overheads] The different types of
overhead are described in the following table, which is taken from the paper.

[^python-overheads]: See [2] and [3] for other similar analyses that [1] builds on.

<table class="table table-sm table-striped">
  <caption>Sources of performance overhead in Python, from [1].</caption>
  <thead>
    <tr>
      <th scope="col">Group</th>
      <th scope="col">Overhead category</th>
      <th scope="col">Description</th>
    </tr>
  </thead>
  <tbody>
    <tr><td rowspan="4">Additional language features</td></tr>
    <tr><td>Error check</td><td>Check for overflow, out-of-bounds and other errors</td></tr>
    <tr><td>Garbage collection</td><td>Automatically freeing unused memory</td></tr>
    <tr><td>Rich flow control</td><td>Support for more condition cases and control structures</td></tr>
    <tr><td rowspan="6">Dynamic language features</td></tr>
    <tr><td>Type check</td><td>Checking variable type to determine operation</td></tr>
    <tr><td>Boxing/unboxing</td><td>Wrapping or unwrapping integer or float types</td></tr>
    <tr><td>Name resolution</td><td>Looking up variable in a map</td></tr>
    <tr><td>Function resolution</td><td>Dereferencing function pointers to perform an operation</td></tr>
    <tr><td>Function setup/cleanup</td><td>Setting up for a function call and cleaning up when finished</td></tr>
    <tr><td rowspan="7">Interpreter operations</td></tr>
    <tr><td>Dispatch</td><td>Reading and decoding bytecode instruction</td></tr>
    <tr><td>Stack</td><td>Reading, writing, and managing VM stack</td></tr>
    <tr><td>Const load</td><td>Reading constants</td></tr>
    <tr><td>Object allocation</td><td>Inefficient deallocation followed by allocation of objects</td></tr>
    <tr><td>Reg transfer</td><td>Calculating address of VM storage</td></tr>
    <tr><td>C function call</td><td>Following the C calling convention in the interpreter</td></tr>
  </tbody>
</table>

The following charts (also taken from the paper) show the proportions are given
as a percentage of total execution time, based on the measured execution of a
set of benchmarks. On average, 64.9% of overall execution time is overhead, and
the remaining 35.1% is used for the execution of the program. Of the language
features, name resolution and function setup/cleanup dominate. Of the
interpreter operations, dispatch (reading bytecode and executing the correct
operations) and C function calls dominate.

{{ macros.image('python-processor/measured-overheads.png', size='1000x1000',
                caption='Python overheads measured in various benchmarks, from [1].') }}

There has been significant work on tackling (2) the language implementation.
Prominent examples include:
[PyPy][pypy], an alternative [optimised][pypy-opt] implementation written in
Python that includes a just in-time (JIT) compiler to dynamically optimise
common code paths;
[Cinder][cinder] is Meta's internal performance-optimised version of
CPython that includes various performance optimisations and a per-method JIT;
[Cython][cython] translates Python to C/C++ for static compilation and
execution in the CPython runtime environment;
[Nuitka][nuitka] is similar to Cython, as a compiler from Python to C,
using the CPython interpreter as a library;
And not forgetting CPython itself has an active project led by Microsoft and
Guido van Rossum called [Faster CPython][faster-cpython] to explore
performance optimisations.
Approximately, these approaches achieve speedups of up to an order of magnitude
when compared to the standard CPython implementation.

Where the previous examples optimise Python as a general-purpose language, some
approaches such as [Codon][codon], [Numba][numba] and [Triton][triton] compile
subsets of Python into machine code for host or accelerator devices,
eliminating the runtime overhead altogether. These approaches can achieve
speedups of the order of 100 times for serial execution. They focus however
on accelerating numerical computations and therefore sidestep the difficulties
of statically-compiling dynamic features such as naming, large integers and
data structures, which are much more challenging.

Within the scope of (1) optimising the application, a significant issue
preventing the use of parallelism is Python's [Global Interpreter Lock
(GIL)][gil]. This lock allows only one thread to execute the interpreter at
once, which was done originally to make the counting of object references
simpler. It is possible to work around the constraints imposed by the GIL, such
as with the ``multiprocessing`` module but this makes it difficult to express
different types of parallelism and creates an ease-of-use problem. A
[PEP][pep-gil] submitted by a PyTorch developer makes the case for removing the
GIL, outlining motivating examples in scientific and numerical computing, and
tasks using Python for coordination and communication. A decision on adoption
of this PEP is yet to be made but a [reference implementation][nogil] is available.

There are various sources of overhead in the execution of a Python program that
can contribute to orders-of-magnitude slower runtime compared to a compiled
program. Strategies to reduce this overhead are in optimising the sources of
overhead directly by improving compilation strategies, improving runtime
strategies (such as caching of accesses or performing JIT compilation to
machine code of frequent code paths), statically compiling Python code to C
code including inline calls to the interpreter, and, for restricted subsets of
Python, statically compiling Python code to machine code without the
interpreter. These approaches are all within the software domain, so it is
interesting to consider in what ways computer hardware could be optimised to
further reduce the runtime overheads in Python programs.

[pypy]: https://www.pypy.org
[pypy-opt]: https://doc.pypy.org/en/latest/interpreter-optimizations.html
[cinder]: https://github.com/facebookincubator/cinder
[cython]: https://cython.org
[nuitka]: https://nuitka.net
[faster-cpython]: https://github.com/faster-cpython/ideas
[codon]: https://docs.exaloop.io/codon
[numba]: https://numba.pydata.org/
[triton]: https://triton-lang.org
[gil]: https://wiki.python.org/moin/GlobalInterpreterLock
[pep-gil]: https://peps.python.org/pep-0703/
[nogil]: https://github.com/colesbury/nogil-3.12

## Hardware impacts on Python performance

The main findings from the microarchitecture investigation in [1] summarised
below provide a useful basis for understanding how Python is limited by current
computer hardware. The study is based on a range of benchmarks run with CPython
and PyPy with and without JIT.

- **ILP**. Both CPython and PyPy exhibit low instruction-level parallelism.
  This suggests that choosing a deeply-pipelined out-of-order core may not
  provide good tradeoff between silicon area and performance. A simpler, in-order
  core may instead be a better choice, particularly when building a parallel
  processor with many cores.

- **Working memory**. Across all the benchmarks, large caches do not provide a
  performance benefit, implying that working sets tend to be relatively small.

- **Nursery sizing**. A critical factor related to working memory is an area
  used for the allocation for short-term objects called a *nursery*. When the
  nursery does not fit in cache, performance is impacted due to cache thrashing.
  However, there are two things to consider: reducing the nursery size will
  increase garbage-collection overheads and the optimal nursery size is dependent
  on the application.

- **JIT**. When JIT compilation is used, the memory system is put under more
  pressure, so although the number of instructions executed reduces, the
  latency of memory operations increases due to cache line misses. This implies
  the working memory increases and so accordingly the overhead of garbage
  collection also increases.

It is clear from these findings that optimising the memory system will yield a
more significant performance improvement than optimising the processor
microarchitecture and instruction set design (as is typically the focus of new
processor designs). Orthogonal to optimisations in the memory system, providing
more execution parallelism at the process level is the only other way to
significantly scale performance. This gives us the basis for a new Python
processor.

## Hardware support for Python

This section presents some rough ideas on what new computer hardware might
look like that optimises the execution of Python (or indeed other dynamic
languages).

### System architecture

The most straightforward way to deploy a new processor chip is as an
*accelerator* to a conventional *host* processor connected via PCIe. The host
processor can then offload parts or all of the Python workload to the
accelerator for improved performance. The following diagrams show two ways that
this could work: one where the host runs the Python interpreter and offloads
parts of the Python program (similar to the way *Eager Mode* works in PyTorch
and TensorFlow); the other where the accelerator runs the Python interpreter
and communicates to the host via a standard set of system calls. The first
scenario means that execution can fall back onto the host if the Python code
was not supported by the accelerator, thereby allowing the design of the
accelerator to be simpler. However, managing the communication of Python
objects over this boundary is complicated and potentially a significant
overhead. In the second scenario, the whole Python program is executed by the
interpreter running on the accelerator. This simplifies the interface between
the two devices, which would only need to provide basic system calls to the
interpreter.

{{ macros.pair_layout(
    macros.image('python-processor/offload-model-fine.png', size='1000x1000',
                 caption='Fine-grained offload'),
    macros.image('python-processor/offload-model-coarse.png', size='1000x1000',
                 caption='Coarse-grained offload')) }}

At a system level, an accelerator device for Python might be integrated between
the host processor and other accelerators (typically GPUs in data-centre-type
deployments) since Python will be responsible for coordinating offload of
computations. Access to external memory can either be to DRAM via the host or
on DRAM integrated with the device. The latter has the benefit of being able to
supply lower latency and higher bandwidth to the memories.

{{ macros.image('python-processor/accelerator.png', size='1000x1000') }}

## Core architecture

At the core level, it makes a lot of sense to use RISC-V as the base
architecture because it is a general-purpose ISA that is open and easily
extensible. As previously noted, the RISC-V microarchitecture can be kept
simple because interpreting Python is not heavily dependent on ILP. The
complexity of the microarchitecture depends on the best tradeoff between
sequential and parallel performance, which in turn depends on the workload. AI
for example will be weighted towards highly-parallel execution, so is better
suited to a large number of simple processor cores. Extensions to the core can
be added to provide optimised support for specific operations (eg
floating-point arithmetic and for matrix multiplication), support for
concurrency (threading, synchronisation, communication etc) or control over the
memory hierarchy.

## Memory system

One way to improve the way memory is managed is to bring some level of control
of the cache to the processor. In the following diagram, A RISC-V core has
extensions that allows it to control a 'smart cache'. Such a system could
enable aggressive caching of computations that are frequently recomputed, such
as in the processes of name and function resolution, or from calling a function
with the same arguments, which account for a substantial portion of the
language overhead. A motivating example is caching of the C `strlen` function
that is used frequently by the Python interpreter in name resolution. A
difficulty in caching this function entirely in software is that a full string
comparison is required to determine whether to invalidate the cache or not, and
this is roughly as expensive as `strlen`. A hardware caching scheme could be
implemented more simply by snooping memory writes and invalidating the cache
entry if any part of the string has changed. To support this, hardware
extensions would be required to place items in the cache, retrieve items in the
cache, monitor ranges of memory and invalidate items in monitored ranges.

{{ macros.image('python-processor/smart-cache.png', size='1000x1000') }}

Another memory-system optimisation is to provide garbage collection (GC) as a
hardware-managed function. GC is a technique that has been studied for decades,
including in hardware: it was first introduced in Lisp in the 1950s and
appeared as a hardware extension in the 1981 [Intel iAPX 432][Intel432] (see
[4] for a literature review of hardware GC techniques and implementations).
Surprisingly, hardware GC has never caught on and this is certainly related to
the [challenges][gc-hw-hard] of a performant solution requiring integration
across many levels of abstraction: microarchitecture, architecture, tooling,
operating systems and languages. However, it seems that this precedent should
be challenged given that GC is central to the way dynamic languages work.

## Scaling the number of cores

Building a system with multiple processing cores can be done in a conventional
way by sharing access to higher levels of cache and adding a coherency
mechanism for lower-level private caches, but this does not scale well past a
few tens or hundreds of cores due to the overheads of maintaining coherency. A
different and more radical approach is to use a distributed-memory architecture
where each core has a private memory and communication between cores or to
external DRAM is performed explicitly using messages. The major benefit of such
an architecture is that is scalable to large numbers of cores, providing more
performance from parallelism, and that processor-memory pairs can flexibly be
used as units of memory or processing dependent on the application. This
approach generalises the concept of a programmable cache hierarchy by using
processor-memory pairs as units of memory with the processor providing access
logic and building arbitrary caching schemes in software, dependent on the
characteristics of the workload. I have previously written about this idea in
my work on [emulating large memories](files/emulation.pdf).
Alternatively, processor-memory pairs can be turned over to processing and used
to execute parts of an application in parallel, a great example of which would
be running one or several JIT compiler processes concurrently with the
application.

The following diagram sketches how such a machine might be built. The main
building blocks are a processor-memory *tile* and a *router*. The tile includes
communication facilities, allowing it to communicate to all other tiles in the
system and to off-chip communication interfaces via routers. The arrangement of
routers and tiles is flexible but the routers have enough links that
high-dimensional topologies can be created to provide communication with
bounded latency and throughput, which is essential for a general-purpose
machine. The operation of the communications fabric could be dynamic allocated
with packet switching, or statically allocated with circuit switching. Special
packet types can be used for accessing external memory or other off-chip IO, or
for implementing shared-memory operations such as direct access to remote tile
memories. Collective operations such as scatters and gathers are likely to be
frequently used, so could be optimised with supporting hardware in the tile and
routers. These are the essential ingredients of a  general-purpose fine-grained
parallel machine. I have previously outlined a similar kind of machine in my
[PhD thesis][thesis], and I intend to post a note with a revised and fuller
description at some point soon.

{{ macros.image('python-processor/parallel-microarchitecture-top.png', size='1000x1000') }}

[intel432]: https://en.wikipedia.org/wiki/Intel_iAPX_432#Garbage_collection
[gc-hw-hard]: https://www.quora.com/Why-dont-modern-CPUs-offer-hardware-assisted-garbage-collection-and-memory-allocation
[thesis]: /scalable-abstractions-for-general-purpose-parallel-computation.html

## Summary

This note makes the argument that ease of use the critical factor in the
development of new application areas and the adoption of new computer hardware.
Ease of use has in many regards won as the most important factor in software
and programming, but new computer hardware prioritises performance. Closing
this gap would mean that rapidly-developing application areas such as AI would
benefit by moving the boundary away from optimised low-level libraries, making
fuller use of languages such as Python. For computer designers, there is a huge
opportunity for new architectural innovations that support a radically
different workload from conventional low-level compiled languages. Contrary to
conventional wisdom, hardware is easier to innovate rapidly and it is software
that bears the weight of legacy.

## References

1. Mohamed Ismail and G. Edward Suh, *Quantitative Overhead Analysis for
   Python*, 2018 IEEE International Symposium on Workload Characterization
   (IISWC). [[IEEE][python-overheads-ieee], [PDF][python-overheads-pdf]]

2. Nagy Mostafa, Chandra Krintz, Calin Cascaval, David Edelsohn, Priya
   Nagpurkar, Peng Wu, *Understanding the Potential of Interpreter-based
   Optimizations for Python*. UCSB Technical Report #2010-14 August, 2010.
   [[PDF][mostafa-ucsb]]

3. Gergö Barany, *Python Interpreter Performance Deconstructed*,
   Proceedings of the Workshop on Dynamic Languages and Applications, June 2014.
   [[ACM][barany-acm], [PDF][barany-pdf]]

4. Andres Amaya Garcia, Integrated hardware garbage collection for real-time
   embedded systems, PhD thesis, University of Bristol 2021.
   [[University of Bristol][garcia-gc], [PDF][garcia-gc-pdf]]


[python-overheads-ieee]: https://ieeexplore.ieee.org/document/8573512
[python-overheads-pdf]: https://www.cs.ucsb.edu/sites/default/files/documents/2010-14.pdf
[barany-acm]: https://dl.acm.org/doi/10.1145/2617548.2617552
[barany-pdf]: https://www.cs.ucsb.edu/sites/default/files/documents/2010-14.pdf
[mostafa-ucsb]: https://cs.ucsb.edu/research/tech-reports/2010-14
[garcia-gc]: https://research-information.bris.ac.uk/en/studentTheses/integrated-hardware-garbage-collection-for-real-time-embedded-sys
[garcia-gc-pdf]: https://research-information.bris.ac.uk/files/298185781/Final_Copy_2021_09_28_Amaya_Garcia_A_PhD.pdf

## Acknowledgements

The hardware ideas in this note were developed in conversations with [James
Pallister][jpallister]. Closely related to some of the ideas explored is a new
UK startup [VyperCore][vypercore] co-founded by [Ed Nutting][enutting] who are
building a RISC-V-based processor that includes facilities for hardware memory
allocation and GC for performance and safety.

[jpallister]: http://www.jpallister.com
[enutting]: https://ednutting.com
[vypercore]: https://www.vypercore.com
