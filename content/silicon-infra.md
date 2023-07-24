---
Title: Silicon infrastructure
Date: 2023-07-31
Category: notes
Tags: computing, computer-architecture
Summary: Thoughts on the requirements of software infrastructure
         to support ASIC design.
Status: published
---

{% import 'post-macros.html' as macros %}

Modern ASIC design differs to conventional software engineering in several
important aspects that require a somewhat different approach to project
development:

- **Tapeout**. When a design is released for manufacture (known in the
  industry as a *tape out*), there are typically high non-recoverable expenses associated
  with setting up the processes and a long lead time in receiving a (hopefully)
  working device. There are two implications of this situation:
    (1) chip tapeouts precludes incremental releases, for example to fix trivial bugs, and
    therefore means that the confidence in the correct functionality of the
    design must be very high;
    (2) post tape out, the design source code is effectively frozen forever more for
    the purposes of debug and analsys.

- **Tooling**. Compared to software tooling, standard ASIC design tooling
  (known in the industry as *electronic design automation*) :
    (1) is almost all proprietary and used under license, meaning that interactive
    and automated use is limited and at odds with a continuous-integration model
    of development; and
    (2) can have long run times (upwards of 12 hours for a job are not uncommon) and produce
    vast quantities of data, making it very unattractive to rerun something
    unless absolutely necessary; and
    (3) can be non-deterministic in that rerunning a job with the same set of inputs
    produces a different output.

Despite these differences, many of the techniques and tools from software
engineering can readily be applied to ASIC development, particularly to manage
complexity and maintain high standards of code quality, testing and
integration. This note lays out some thoughts and opinions on the components
and structure of a software infrastructure to build ASIC chips.

## Aims

The overall objective of a silicon infrastructure is to **support the
development of an ASIC design from RTL to GDSII**. To make this more specific, I
also define the following capabilities that should be supported as an overall
philosophy of the approach that is explored in this note:

- To **rerun everything from scratch** (as far as is possible), requiring full
  automation of an the end-to-end flow. This is intended to: (1) distribute the
  task of integrating components of a design across a team, thereby revealing
  issues at as earlier stage in the project as possible to avoid disruptive
  changes towards the end; and (2) to enable faster design iteration.

- Provide a **full audit trail** such that a release of a design for tape out
  has a set of reports, logs, coverage metrics, documentation and signoffs that
  are tracable back to the original RTL source files. This is important for
  building confidence to tape out, as well as providing information for future
  work on a taped-out design.

- Support **multiple chips and frozen designs** to keep previous generations
  alive for debug of silicon issues and/or as a basis for a incremental tapeout
  (known as a *respin*), and to allow multiple designs to be built concurrently.

## Guiding principles

I think it is useful to underpin the aims, implementation and operation of an
ASIC design infrastructure are a set of guiding principles for the project team
to employ when design decisions need to be made.  These principles are formed
from my own experience and through conversations with others. I am sure that
alternative foundations can be constructed and argued for.

1. **Simple and explicit**. Build a complex system using simple, well-defined
components composed and controlled using explicit mechanisms. Conversely, avoid
easy-to-use high-level interfaces that hide important behvaiours. This borrows
from the [Zen of Python](https://peps.python.org/pep-0020/): *explicit is better
than implicit and simple is better than complex*. Examples include avoiding the
use of global variables, preferring flat rather than nested, preferring
decisions to be made explicitly and avoiding special cases that break the rules.

1. **Use a monorepository**. One repository should contain all the code for all
active projects. This enhances all team members' ability to integrate their
changes across projects and removes barriers to interaction between different
teams and/or areas of the design. Other [general
benefits](https://en.wikipedia.org/wiki/Monorepo) of a monorepository are the
ability to reuse code and do large-scale refactoring. A great deal of care must
be taken to manage dependencies between projects/components within a
monorepository. Without such care, unexpected interdependencies can cause
unexpected breakages, prevent refactoring and preclude focussed testing. In
general: isolate components by restricting them to only be able to access their
listed dependencies; divide components by function and abstraction level (eg
don't group by language or technology); and use a standard structure for each
component (such as ``lib``, ``sources``, ``README`` etc).

1. **Embrace open source**. To save on effort, leaverage freely-available tools
and libraries whereever possible in the infrastructure, rather than implementing
custom versions. Where open source is used, contributions back upstream benefit
the community and help to align the project with the way it is being deployed.
This particularly applies to open source in the ASIC/FPGA domain, where
[open-source software][oss-hw] is unemcumbered by licensing restrictions.  Often
chip projects will be on tight schedules, so careful judgement of the
effort-benefit tradeoff must be made.

1. **Performance is important**. With the ability to rerun everything from
scratch coupled with a multi-chip and monorepository approach, the compute
demands can scale quickly so it is crucial that the infrastructure is
performant. This can easily become a problem with codebases make extensive use
of a scripting language such as Python.  Mitigations include writing (or
rewriting) parts in a lower-level language such as C++, and setting things up in
such a way that this Python and C++ components can interoperate cleanly (eg
well-defined boundaries and dependenceis).

[oss-hw]: https://github.com/aolofsson/awesome-opensource-hardware

## Infrastructure components

What are the components of the infrastructure?

What are some specific useful features?

## Flows

What do we need to do with the infrastructure?

What are some specific supporting tools that we need?

## Acknowledgements

...

## Related projects

- [Gator](https://gator.intuity.io), a framework for running a hierarchy of
  jobs and aggregating logs, metrics, resource utilisation, and artefacts.
- [Siliconcompiler](https://github.com/siliconcompiler/siliconcompiler) is a modular
  build system for silicon hardware.
- Berkeley [Chipyard](https://github.com/ucb-bar/chipyard) is an agile framework
  for hardware design, using Chisel for RTL specification.
- Berkeley [Hammer](https://github.com/ucb-bar/hammer) is a physical design framework.
- Pulp Platform [Bender](https://github.com/pulp-platform/bender) is a dependency
  management tool for hardware design projects.
- [Rich Porter's series on digital verification](http://dungspreader.blogspot.com/)
  and [source code](https://github.com/rporter/verilog_integration) for the project.
