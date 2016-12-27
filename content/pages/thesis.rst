:title: PhD thesis
:date: 2014-12-03 10:20
:category: None

Scalable abstractions for general-purpose parallel computation
--------------------------------------------------------------

Ph.D. thesis, University of Bristol, March 2014.

Supervised by `David May <https://www.cs.bris.ac.uk/~dave/>`_ and `Simon Hollis
<http://www.cs.bris.ac.uk/staff/simon/>`_.

Abstract
--------

Parallelism has become the principal means of sustaining growth in
computational performance but there has been relatively little development in
general-purpose computer architectures or programming models that can deal
effectively with large amounts of it. A new general-purpose model of parallel
computing would enable standardisation between architectures, high-volume
production and software that is portable between different machines, now and as
they develop with future technology. There is substantial opportunity to
support this in emerging areas of embedded computing, where the problems of
sensing, interaction and decision making can exploit large amounts of
parallelism.

This thesis demonstrates the essential aspects of a scalable general-purpose
model of parallel computation by proposing a Universal Parallel Architecture
(UPA), based on a highly-connected communication network, and a high-level
parallel programming language for it called sire that can be compiled using
simple techniques. The design of sire combines the essential capabilities of
shared-memory programming with the benefits of message passing to support a
range of programming paradigms and to provide powerful capabilities for
abstraction to build and compose subroutines and data structures in a
distributed context. The design also enables program code to be distributed at
run time to reuse memory and for processor allocation to be dealt with during
compilation so that the overheads of using distributed parallelism are minimal.

To evaluate whether the UPA is practical to build, a high-level implementation
model using current technologies is described. It demonstrates that the cost of
generality is relatively small; for a system with 4,096 processors, an overall
investment of around 25% of the system is required for the communication
network. Executing on specific UPA implementations, sire's primitives for
parallelism, communication and abstraction incur minimal overheads,
demonstrating its close correspondence to the UPA and its scalability.
Furthermore, as well as executing highly-parallel programs, the UPA can support
sequential programming techniques by emulating large memories, allowing general
sequential programs to be executed with a factor of 2 to 3 overhead when
compared to contemporary sequential machines.

Published as
------------

James W. Hanlon, *Scalable abstractions for general-purpose parallel
computation*.  Ph.D. thesis, Department of Computer Science, University of
Bristol, March 2014.

This work is licensed under the `Creative Commons BY-NC-ND 4.0 license
<http://creativecommons.org/licenses/by-nc-nd/4.0/>`_.

Download
--------

- `PDF <{filename}/files/thesis.pdf>`_
- `Print PDF <{filename}/files/thesis-print.pdf>`_ (no hyperlink colours)

Other
-----

I was awarded an `Engineering Faculty commendation
<http://www.bristol.ac.uk/engineering/postgraduate/commendations/hanlon.html>`_ for
my work.
