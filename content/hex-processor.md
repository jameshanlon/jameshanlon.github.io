---
Title: Hex processor architecture
Date: 2022-04-16
Category: projects
Tags: computing, computer architecture, microelectronics 
Status: published
---

{% import 'post-macros.html' as macros %}

This note is intended to be a reference for 

## Hex architecture

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

## Hex instruction set

<table class="table">
<thead>
  <th scope="col">Opcode</th>
  <th scope="col">Behaviour</th>
  <th scope="col">Description</th>
</thead>
<tbody>
<tr>
  <td><code>LDAM</code></td>
  <td><code>areg := mem[oreg]</code></td>
  <td>Load from memory with an absolute address into areg</td>
</tr>
<tr>
  <td><code>LDBM</code></td>
  <td><code>breg := mem[oreg]</code></td>
  <td>Load from memory with an absolute address from memory into breg</td>
</tr>
<tr>
  <td><code>STAM</code></td>
  <td><code>mem[oreg] := areg</code></td>
  <td>Store absolute from areg</td>
</tr>
<tr>
  <td><code>LDAC</code></td>
  <td><code>areg := oreg</code></td>
  <td>Load absolute into areg</td>
</tr>
<tr>
  <td><code>LDBC</code></td>
  <td><code>breg := oreg</code></td>
  <td>Load absolute into breg</td>
</tr>
<tr>
  <td><code>LDAP</code></td>
  <td><code>areg := pc + oreg</code></td>
  <td>Load program counter-relative address into areg</td>
</tr>
<tr>
  <td><code>LDAI</code></td>
  <td><code>areg := mem[areg + oreg]</code></td>
  <td>Load from memory with base and offset into areg</td>
</tr>
<tr>
  <td><code>LDBI</code></td>
  <td><code>breg := mem[areg + oreg]</code></td>
  <td>Load from memory with base and offset into breg</td>
</tr>
<tr>
  <td><code>STAI</code></td>
  <td><code>mem[breg + oreg] := areg</code></td>
  <td>Load from memory with base and offset into breg</td>
</tr>
<tr>
  <td><code>BR</code></td>
  <td><code>pc := pc + oreg</code></td>
  <td>Branch relative</td>
</tr>
<tr>
  <td><code>BRZ</code></td>
  <td><code>if areg = 0: pc := pc + oreg</code></td>
  <td>Conditional branch relative on areg being zero</td>
</tr>
<tr>
  <td><code>BRN</code></td>
  <td><code>if areg < 0: pc := pc + oreg</code></td>
  <td>Conditional branch relative on areg being negative</td>
</tr>
<tr>
  <td><code>BRB</code></td>
  <td><code>pc := breg</code></td>
  <td>Absolute branch</td>
</tr>
<tr>
  <td><code>OPR</code></td>
  <td><code></code></td>
  <td>Inter-register operation</td>
</tr>
<tr>
  <td><code>ADD</code></td>
  <td><code>areg := areg + breg</code></td>
  <td>Add areg and breg and set areg to the result</td>
</tr>
<tr>
  <td><code>SUB</code></td>
  <td><code>areg := areg + breg</code></td>
  <td>Subtract areg and breg and set areg to the result</td>
</tr>
<tr>
  <td><code>SVC</code></td>
  <td><code></code></td>
  <td>System call</td>
</tr>
</table>

### Hardware implemenation

Blah.

### Hex tools

### Simulator (``hexsim``)

Blah.

### Assembler (``hexasm``)

Blah

### Compiler (``xcmp``)

Blah.

### Self-hosting compiler (``xhexb``)

Blah.

#### Structure

#### Procedure calling

LDAP return address (label following next BR)

BR <label> to procedure entry point

Procedure entry stores the return address
...
Exit loads return address into breg
BRB to branch back

```
Callee frame: 0 Return address (written by callee)
              1 Return value 
              2 Actual 0
              3 Actual 1
              4 Actual 2
              5 Temporary 0
              6 Temporary 1
              7 Temporary 2
Caller frame: 8 Return address (written by callee)
              9 Return value 
                Actual 0
                Actual 1
                Actual 2
                Temporary 0
                Temporary 1
                Temporary 2
                ...
```
