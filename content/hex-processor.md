---
Title: Logic gates to a programming language using the Hex architecture
Date: 2022-10-02
Category: projects
Tags: computing, computer architecture, microelectronics
Status: published
---

{% import 'post-macros.html' as macros %}

This note walks through a hardware implementation of a simple processor and
complete compiler for a sequential programming language targeted at it. The
processor architecture is designed to as simple as possible but provide a
sensible target for the compilation of complex programs using simple
strategies. The implementation of the processor and its supporting tooling is
self contained so to be understandable and extendable. 

Besides being an interesting side project, my motivation for doing this was
to create a complete example as a point of reference to explain how programming
languages work and correspond to the underlying hardware of a computer
processor.


## Hex architecture

The Hex architecture is designed to be very simple and suitable for explaining
how a computer works, whilst being flexible enough to execute substantial
programs, and easily extensible. The sixteen instructions are summarised in the
following table.

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
  <td><code>breg := mem[breg + oreg]</code></td>
  <td>Load from memory with base and offset into breg</td>
</tr>
<tr>
  <td><code>STAI</code></td>
  <td><code>mem[breg + oreg] := areg</code></td>
  <td>Store to memory with base and offset from areg</td>
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
