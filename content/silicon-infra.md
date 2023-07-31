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

Modern ASIC design differs to conventional software engineering in two
fundamental aspects that require a somewhat different approach to project
development:

- **Transformations and representations**. The creation of an ASIC design from
  a source-level representation through to a final GDSII description of the
  layout involves many stages of incremental transformations of the circuit and
  layout, and then incremental assembly of components into various subsystems
  before finally the entire chip. At various stages through this process, checks
  are performed on the design typically using simplified representations to
  reduce complexity and make run times practical.

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

- **Tape out**. When a design is released for manufacture (known in the
  industry as a *tape out*), there are typically high non-recoverable expenses associated
  with setting up the processes and a long lead time in receiving a (hopefully)
  working device. There are two implications of this situation:
    (1) chip tape outs precludes incremental releases, for example to fix trivial bugs, and
    therefore means that the confidence in the correct functionality of the
    design must be very high;
    (2) post tape out, the design source code is effectively frozen forever more for
    the purposes of debug and analysis.

Despite these differences, many of the techniques and tools from software
engineering can readily be applied to ASIC development, particularly to manage
complexity and maintain high standards of code quality, testing and
integration. This note lays out some thoughts and opinions on the components
and structure of a software infrastructure to build ASIC chips.

### Table of contents

1. [Aims](#aims)
1. [Guiding principles](#principles)
1. [Flows](#flows)
1. [Components](#components)
1. [Related projects](#related-projects)

## Aims <a name="aims" class="anchor"></a> 

The overall objective of a silicon infrastructure is to **support the
development of a verified ASIC design from RTL to GDSII**. To make this more
specific, I also define the following capabilities that should be supported as
an overall philosophy of the approach that is explored in this note:

- To **rerun everything from scratch**, requiring full
  automation of an the end-to-end flow. This is intended to: (1) distribute the
  task of integrating components of a design across a team, thereby revealing
  issues at as earlier stage in the project as possible to avoid disruptive
  changes towards the end; (2) enable faster design iterational; and (3)
  provide tracability of results, providing a foundation for the next aim.

- Provide a **full audit trail** such that a release of a design for tape out
  has data and a set of reports, logs, coverage metrics, documentation and
  signoffs that are tracable back to the original RTL source files. This is
  important for building confidence to tape out, as well as providing information
  for future work on a taped-out design.

- Support **multiple chips and frozen designs** to keep previous generations
  alive for debug of silicon issues and/or as a basis for a incremental tape out
  (known as a *respin*), and to allow multiple designs to be built concurrently.

## Guiding principles <a name="principles" class="anchor"></a>

I think it is useful to underpin the aims, implementation and operation of an
ASIC design infrastructure are a set of guiding principles for the project team
to employ when design decisions need to be made.  These principles are formed
from my own experience and through conversations with others. I am sure that
alternative foundations can be constructed and argued for.

1. **Simple and explicit**. Build a complex system using simple, well-defined
components composed and controlled using explicit mechanisms. Conversely, avoid
easy-to-use high-level interfaces that hide important behaviours. This borrows
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
unexpected breakages, prevent refactoring and preclude focused testing. In
general: isolate components by restricting them to only be able to access their
listed dependencies; divide components by function and abstraction level (eg
don't group by language or technology); and use a standard structure for each
component (such as ``lib``, ``sources``, ``README`` etc).

1. **Embrace open source**. To save on effort, leverage freely-available tools
and libraries wherever possible in the infrastructure, rather than implementing
custom versions. Where open source is used, contributions back upstream benefit
the community and help to align the project with the way it is being deployed.
This particularly applies to open source in the ASIC/FPGA domain, where
[open-source software][oss-hw] is unencumbered by licensing restrictions.  Often
chip projects will be on tight schedules, so careful judgement of the
effort-benefit tradeoff must be made.

1. **Performance is important**. With the ability to rerun everything from
scratch coupled with a multi-chip and monorepository approach, the compute
demands can scale quickly so it is crucial that the infrastructure is
performant. This can easily become a problem with codebases make extensive use
of a scripting language such as Python.  Mitigations include writing (or
rewriting) parts in a lower-level language such as C++, and setting things up in
such a way that this Python and C++ components can interoperate cleanly (eg
well-defined boundaries and dependencies).

[oss-hw]: https://github.com/aolofsson/awesome-opensource-hardware

## Flows <a name="flows" class="anchor"></a> 

{#
What do we need to do with the infrastructure?
What are some specific supporting tools that we need?
#}

This section outlines the high-level *flows* that an ASIC infrastructure needs
to support, meaning (typically) a sequence of steps to achieve some *task*.
This is not meant to be exhaustive, but characteristic of the types of tasks
that need to be performed. Flows can be just a single step or can be composed
together to create different flows.

- **Design representation**. To read a design into a tool, it must have a
  complete representation including tool-agnostic configuration, macro defines,
  library files and RTL sources. Often, RTL code will need to be generated
  programatically using templates or other types of code generators. It is also
  typical that a design will be implemented in a hierarchical fashion, so a
  configuration step must gather together the required modules and package it
  into a single representation. As an example, the open-source [Bender][bender]
  dependency management tool provides very similar functionality.

{{ macros.imagenothumb('sili-infra/design-representation.png') }}

- **Verification representation**. For the purposes of simulation and
  analysis, a verification representation is a variation of a design
  representation, adding configuration and macro defines, source files for a test
  bench, monitors, assertions etc, and possibly substituting parts of the design
  for fast models or block boxes. These verification components will likely live
  with the corresponding parts of the design and be collected together as they
  were for the design representation during a configure step.

{{ macros.imagenothumb('sili-infra/verif-representation.png') }}

- **Lint checking**. RTL source code can be checked for basic coding issues
  (referred to as *linting*) by passing it through tools that perform various
  built-in or custom checks. The input to this task is the specification of a
  design and the output is a list of warnings to be reviewed. Example open-source
  tools that can be used for linting are [Verilator][verilator],
  [Verible][verible], [Slang][slang], [svlint][svlint] and [Yosys][yosys].

{{ macros.image('sili-infra/lint-check.png', size='1000x1000') }}

- **CDC and RDC checking**. Clock- and reset-domain crossings can be checked
  automatically with tools that analyse a design, typically with a set of
  annotations and constraints. The output will be warning messages from the
  checker that need to be investigated.

{{ macros.imagenothumb('sili-infra/cdc-rdc-check.png') }}

- **Simulation testbench**. A simulation test bench requires a representaiton
  of the design, a verification environment and test stimulus. Test stimulus
  is often randomly generated. Coverage (structural or functional) can be
  collected during simulation, and when many test instances are run for a
  particular test generator or over a larger regression of different test
  generators, coverage may need to be merged then reported on. Simulation is
  typically performed on an RTL representation, but is also done on gate-level
  netlists and with delay annotations.

{{ macros.imagenothumb('sili-infra/simulation-flow.png') }}

- **Formal property test bench**. Analysing and proving formal properties of a
  design is a complementary technique to standard functional coverage. Inputs
  to this are a verification representation of the design and a set of
  assumptions and properties to be checked.

{{ macros.imagenothumb('sili-infra/formal-property-check.png') }}

- **Formal equivalence check**. As a design is incrementally transformed
  between RTL and GDSII, it is essential to perform equivalence checks to
  prove that each transformation maintains the functional behaviour of the
  design. Inputs to an equivalence check are two representations, typically
  called a *reference* that is the baseline and an *implementation* to check.

{{ macros.imagenothumb('sili-infra/equivalence-flow.png') }}

- **Physical build**. All flows up to this point have mainly operated on RTL
  representations of a design. A physical build flow starts off by
  transforming RTL into gates using a synthesis tool, then progressively
  transforms the design into a set of two-dimensional layers. Following synthesis
  are: scan insertion for DFT, floorplanning (placing ports and macros),
  placement (placing cells), clock tree synthesis, routing (establishing all
  required connections using the available routing layers, finishing and
  checking. See [OpenROAD][OpenROAD] for an example open source physical build
  flow.

{{ macros.imagenothumb('sili-infra/phys-build-flow.png') }}

> **A note on DFT**. A central aspect of any ASIC design is the DFT (device
> test) strategy. Testability is achieved by adding logic in the form of
> *instruments* and *connectivity* to make the the existing logic
> *controllable* and *observable*. The means by which this is done and the
> point in the ASIC process is heavily dependent on the design and the tooling
> used. Typically, DFT logic is inserted using automated tools during the
> physical build but increasingly it is being added in RTL also using automated
> tooling - either way adding additional transformation steps to the front- or
> back-end flows.

[bender]: https://github.com/pulp-platform/bender
[verilator]: https://verilator.org/guide/latest
[verible]: https://chipsalliance.github.io/verible
[slang]: https://sv-lang.com
[svlint]: https://github.com/dalance/svlint
[yosys]: https://yosyshq.net/yosys
[OpenROAD]: https://github.com/The-OpenROAD-Project/OpenROAD

## Components <a name="components" class="anchor"></a>

What are the components of the infrastructure?

What are some specific useful features?

{#
Orchestration: ability to deploy tools onto compute.
  Containerisation
  Queueing system
Buildsystem: dependencies, inputs, outputs, tasks.
  Design
  Flows
  Messaging/logging
  Storage
  Releasing to immutable storage
  Referencing releases within the repository
CI
  Regressions run on patches.
  Periodic jobs: hourly, nightly, weekly.
Dashboard
  Reporting of CI
  Performance reporting (Grafana)
Documentation
Collaboration
  Code review
  Issue tracking
#}

{#
Laundry list of useful features
- Stubbing out of dependencies
- Filtering of tests (a la xpath)
- Making all functionality available on the command line
#}

## Acknowledgements

...

## Related projects <a name="related-projects" class="anchor"></a>

- [Gator](https://gator.intuity.io), a framework for running a hierarchy of
  jobs and aggregating logs, metrics, resource utilisation, and artefacts.
- [Blade](https://blu-blade.readthedocs.io) is a tool for autogenerating
  modules, interconnects and register definitions from an YAML schema.
- [Siliconcompiler](https://github.com/siliconcompiler/siliconcompiler) is a modular
  build system for silicon hardware.
- Berkeley [Chipyard](https://github.com/ucb-bar/chipyard) is an agile framework
  for hardware design, using Chisel for RTL specification.
- Berkeley [Hammer](https://github.com/ucb-bar/hammer) is a physical design framework.
- Pulp Platform [Bender](https://github.com/pulp-platform/bender) is a dependency
  management tool for hardware design projects.
- [Rich Porter's series on digital verification](http://dungspreader.blogspot.com/)
  and [source code](https://github.com/rporter/verilog_integration) for the project.
- [Melding hardware and software: a story in the making](https://medium.com/enfabrica/melding-hardware-and-software-a-story-in-the-making-bcce28b821a8),
  a position piece by Enfabrica on their approach to ASIC design.
- [faketree](https://blog.enfabrica.net/different-file-system-views-for-different-tools-a425f13bb7f0)
  is an Enfabrica open-source tool for managing EDA tools in containers and sandboxes.
