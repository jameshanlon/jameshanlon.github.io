---
Title: Silicon infrastructure 
Date: 2023-07-31
Category: notes
Tags: computing, computer-architecture
Summary: Thoughts on the requirements of software infrastructure required
         to support ASIC design.
Status: published
---

{% import 'post-macros.html' as macros %}

This note lays out some thoughts on the components and structure of a
software infrastructure required to build ASIC chips.

## Mission

**Software supporting the development of an ASIC design from RTL to GDSII.**

Sub objectives:

- Rerun everything from scratch (full automation of end-to-end flow).
- Support for multiple chips.

## Related projects

- Berkeley [Chipyard](https://github.com/ucb-bar/chipyard).
- Berkeley [Hammer](https://github.com/ucb-bar/hammer).
- Pulp Platform [Bender](https://github.com/pulp-platform/bender).
- [Siliconcompiler](https://github.com/siliconcompiler/siliconcompiler).
- [Dungspreader's series on digital verification](http://dungspreader.blogspot.com/)
  and [source code](https://github.com/rporter/verilog_integration).
