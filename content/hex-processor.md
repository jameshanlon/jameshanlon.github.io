---
Title: Hex processor architecture
Date: 2022-03-29
Category: projects
Tags: computing, computer architecture, microelectronics 
Status: published
---

{% import 'post-macros.html' as macros %}

This note is intended to be a reference for 

# Hex architecture

The Hex architecture is designed to be very simple and suitable for explaining
how a computer works, whilst being flexible enough to execute substantial
programs, and easily extensible. 

This repository contains an assembler, simulator and hardware implementation of
the Hex processor architecture, as well as a compiler for a simple programming
language 'X' that is targeted at it.  With complexities of modern computer
architectures and compilers/tool chains being difficult to penetrate, the
intention of this project is to provide a simple example Verilog implementation
and supporting C++ tooling that can be used as the basis for another project or
just as a curiosity in itself.

# X compiler

## Procedure calling

LDAP return address (label following next BR)

BR <label> to procedure entry point

Procedure entry stores the return address
...
Exit loads return address into breg
BRB to branch back

```
Frame 0: sp[0] return address (written by callee)
         sp[1] arg0
         sp[2] arg1
         sp[3] arg2
         sp[4] temp0
         sp[5] temp1
Frame 1: sp[6] return address (written by callee)
         ...
```
