Title: Projects
Status: published

### Slang Netlist

**[WIP]** Slang Netlist is a library and tool leveraging
[slang](https://sv-lang.com) to analyse the source-level static connectivity of
a System Verilog design and is intended to be a replacement for Netlist Paths
(see below). Slang Netlist is included as a tool in the slang project.

- [GitHub](https://github.com/MikePopoloski/slang)

### RISC-V processor

A C++ simulator and SystemVerilog implementation (the latter is still a WIP) of
the RISC-V 32IM architecture that I developed to learn about RISC-V.

- [GitHub](https://github.com/jameshanlon/riscv-processor)

### Hex processor

The Hex Architecture is a very simple processor designed by David May and
intended for explaining how a computer works. This repository contains an
implementation in Verilog and basic tooling written in C++ for developing
programs (a compiler, assembler and simulator). It was written out of curiosity
and to serve as an example of how high-level programs relate to the underlying
hardware implementation.

- [GitHub](https://github.com/jameshanlon/hex-processor)
- [Documentation](https://jameshanlon.github.io/hex-processor)

### PRNG testing

This repository contains facilities for comprehensively testing PRNGs using
statistical test suites. It provides a facility to run a PRNG against TestU01,
PractRand and Gjrand, with parallel runs from different seeds and permutations
of the output bits, and a script for summarising results across all the runs.
This testing methodology was used for the investigation in [this
paper](https://arxiv.org/abs/2203.04058).

- [GitHub](https://github.com/jameshanlon/prng-testing)

### Personal finances

A Python-based project that I use fetch personal finance data from Google
Sheets and then generate a set of summary HTML reports.

- [GitHub](https://github.com/jameshanlon/finances)

### Netlist Paths

Netlist Paths is a library and command-line tool for querying a Verilog
netlist. It reads an XML representation of a design's netlist, produced by
[Verilator](https://www.veripool.org/projects/verilator), and provides
facilities for inspecting types, variables and paths. The library is written in
C++ and has a Python interface. This project has now been superseded by Slang
Netlist (see above).

- [GitHub](https://github.com/jameshanlon/netlist-paths)
- [Documentation](https://jameshanlon.github.io/netlist-paths)

<hr>

#### Older projects

- [Convolutional neural network from scratch](https://github.com/jameshanlon/convolutional-neural-network),<br>
  a simple C++ implementation of a convolutional neural network.
- [Three-channel, high-power LED driver](https://github.com/jameshanlon/3C-HP-LED-driver),<br>
  PCB design files and microcontroller code.
- [Sire compiler v2](https://github.com/jameshanlon/tool_sire),<br>
  a rewrite of the original sire implementation in Python, and this time
  targeting the XMOS XS1 architecture via the
  [XC language](/the-xc-programming-language.html).
- [Sire compiler v1](https://github.com/jameshanlon/sire),<br>
  a first version of the sire language and runtime system for dynamic process
  creation, directly targeting the XMOS XS1 architecture.
