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
development of an ASIC design from RTL to GDSII**. To make this more specific,
I also define the following capabilities that should be supported:

- To **rerun everything from scratch** (as far as is possible), requiring full
  automation of an the end-to-end flow. This is to distribute the issue of
  integration as widely as possible.

- Provide a **full audit trail** such that a release of a design for tape out
  has a set of reports, logs, coverage metrics, documentation and signoffs that
  are tracable back to the original RTL source files. This is important for
  building confidence to tape out, as well as providing information for future
  work on a taped-out design.

- Support **multiple chips** to keep previous generations alive for debug of
  silicon issues or as a basis for a incremental tapeout (known as a *respin*),
  and to allow multiple designs to be built concurrently.

## Principles

1. Prefer explicit over complex.

1. Use a monorepository.

1. Leverage open source.

## Related projects

- [Gator](https://gator.intuity.io), a framework for running a hierarchy of
  jobs and aggregating logs, metrics, resource utilisation, and artefacts.
- [Siliconcompiler](https://github.com/siliconcompiler/siliconcompiler).
- Berkeley [Chipyard](https://github.com/ucb-bar/chipyard).
- Berkeley [Hammer](https://github.com/ucb-bar/hammer).
- Pulp Platform [Bender](https://github.com/pulp-platform/bender).
- [Dungspreader's series on digital verification](http://dungspreader.blogspot.com/)
  and [source code](https://github.com/rporter/verilog_integration).
