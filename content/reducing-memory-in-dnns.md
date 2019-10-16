---
Title: Reducing memory use in deep neural networks
Date: 2017-2-5
Category: notes
Tags: computing; machine-intelligence
Status: published
---

The memory requirements for modern deep neural networks can be significant,
however memory on-chip is expensive relative to computational resources such as
integer and floating-point units, and access to external DRAM memory is orders
of magnitude slower. This article surveys some recent results that demonstrate
the economy of reducing memory use by reuse and re-computation.

Memory in neural networks is required to store input data, weight parameters,
and activations as an input propagates through the network. In training,
activations from an forward pass must be retained until they can be used to
calculate the error gradients in the backwards pass. A 50-layer ResNet network,
for example, has 25 million weight parameters and computes 16 million
activations in the forward pass. With a batch of 32, this data alone occupies 5
GB; additional memory is required to store the program's instructions, input
data and temporary values, the last of which is multiplied by the level
of parallelism in the execution. Measuring the memory use of ResNet-50 training
on a Maxwell-generation Nvidia TitanX GPU shows that it uses up to 7.5 GB of
the 12 GB available.

Reducing memory use is beneficial for neural networks for several reasons.
First, it enables deeper networks to be trained, which have been shown to
deliver superior performance for specific tasks and generalisation to new
tasks. Second, it allows larger batch sizes to be used, which improves
throughput and parallelisation. And third, and perhaps most importantly, it
allows data to remain closer to where it is being operated on, reducing the
effects of longer latency and lower bandwidth of larger-capacity off-chip
memory, and consequently improving performance. To illustrate the challenge of
last point with modern GPU architectures, it has been observed that [the
Maxwell TitanX GPU processor cores have only 1 KB of memory that can be read
fast enough to saturate the floating-point
datapath](http://jmlr.org/proceedings/papers/v48/diamos16.pdf).

Two techniques to reduce memory use draw on the dataflow analysis that has been
developed over decades of work with compilers for sequential programming
languages. First, [operations such as activation functions can be performed in
place when the input data can be overwritten directly by the output, so the
memory is
reused](http://mxnet.io/architecture/note_memory.html#in-place-operations).
Second, memory can be reused by [analysing the data dependencies between
operations in a network and allocating the same memory to operations that do
not use it
concurrently](http://mxnet.io/architecture/note_memory.html#standard-memory-sharing).

The second approach is particularly effective when the entire neural network
can be analysed at compile time to create a fixed allocation of memory since
the runtime overheads of memory management reduce to almost zero. The
combination of these techniques have been shown [to reduce memory in neural
networks by a factor of two to three](https://arxiv.org/pdf/1604.06174v2.pdf).
These optimisation techniques are analogous to the dataflow in a sequential
program graph to allow the reuse of registers and stack memory, with their
relatively higher efficiency compared to dynamic memory allocation routines.

Another approach is to trade reduced memory for an increase in computation.
When the computational resources are underused, as they typically are in GPUs,
an increase in computation won’t necessarily increase runtime, and if it does,
can produce relatively higher savings of memory compared to the additional
computation. A simple technique in this vein is to discard values that are
relatively cheap to compute, such as activation functions, and re-compute them
when necessary. More substantial reductions can be achieved by discarding
retained activations in sets of consecutive layers of a network and re-computing
them when they are required during the backwards pass, from the closest set of
remaining activations. Recomputing activations over sets of layers has been
demonstrated by the [MXNet team](https://mxnet.io) to deliver a factor-of-four
memory reduction for a ResNet-50 network, but more importantly, results in
memory use that scales sub-linearly with respect to the number of layers. The
team also demonstrated [training of a 1000-layer ResNet in under 12 GB on the
same Maxwell TitanX GPU](https://arxiv.org/pdf/1604.06174v2.pdf).

A similar memory-reuse approach has been developed by researchers ar [Google
DeepMind](https://deepmind.com/) with recurrent neural networks (RNNs). RNNs
are a special type of DNN that allows cycles in their structure to encode
behaviour over sequences of inputs.  For RNNs, [re-computation has been shown
to reduce memory by a factor of 20 for sequences of length 1000 with only a 30%
performance overhead](https://arxiv.org/pdf/1606.03401v1.pdf). The Baidu [Deep
Speech team](http://research.baidu.com/) recently showed how they applied
various memory-saving techniques obtain a factor of 16 reduction in memory for
activations, enabling them to [train networks with 100 layers on a Maxwell
TitanX, when previously they could only train
9](http://jmlr.org/proceedings/papers/v48/diamos16.pdf).

Relative to memory, compute resources are cheap. The state-of-the-art results
surveyed show efficient use of memory through reuse and trading increased
computation for reduced memory use can deliver dramatic improvements in the
performance of neural networks. However, these results are for a processor with
very limited on-chip memory, just a few megabytes, and just 1KB of fast memory
per core. A processor with a better balance between memory and compute,
allowing more of a neural network to be stored on-chip, may facilitate much
more dramatic improvements.

\[An adapted version of this article first appeared on the [Graphcore
blog](https://www.graphcore.ai/blog/why-is-so-much-memory-needed-for-deep-neural-networks)
and there was some discussion of it on [Hacker
News](https://news.ycombinator.com/item?id=13928523)\]
