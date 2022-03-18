Title: Projects
Status: published

## Netlist Paths

Netlist Paths is a library and command-line tool for querying a Verilog
netlist. It reads an XML representation of a design's netlist, produced by
[Verilator](https://www.veripool.org/projects/verilator), and provides
facilities for inspecting types, variables and paths. The library is written in
C++ and has a Python interface.

- [GitHub](https://github.com/jameshanlon/netlist-paths)
- [Documentation](https://jameshanlon.github.io/netlist-paths)

## Hex processor

The Hex Architecture is a very simple processor designed by David May and
intended for explaining how a computer works. This repository contains an
implementation in Verilog and basic tooling written in C++ for developing
programs (a compiler, assembler and simulator). It was written out of curiosity
and to serve as an example of how high-level programs relate to the underlying
hardware implementation.

- [GitHub](https://github.com/jameshanlon/hex-processor)

## PRNG testing

This repository contains facilities for comprehensively testing PRNGs using
statistical test suites. It provides a facility to run a PRNG against TestU01,
PractRand and Gjrand, with parallel runs from different seeds and permutations
of the output bits, and a script for summarising results across all the runs.
This testing methodology was used for the investigation in [this
paper](https://arxiv.org/abs/2203.04058).

- [GitHub](https://github.com/jameshanlon/prng-testing)

<hr>

#### Older projects

- [Three-channel, high-power LED driver](https://github.com/jameshanlon/3C-HP-LED-driver),<br>
  PCB design files and microcontroller code.
- [Convolutional neural network from scratch](https://github.com/jameshanlon/convolutional-neural-network),<br>
  a simple C++ implementation of a convolutional neural network.
- [Sire compiler](https://github.com/jameshanlon/tool_sire),<br>
  a language and runtime system for dynamic process creation on the XMOS XS1 architecture, targeting the XC language.
- [Sire pre](https://github.com/jameshanlon/sire-pre),<br>
  an early version of the sire language, directly targeting the XMOS XS1 architecture.
