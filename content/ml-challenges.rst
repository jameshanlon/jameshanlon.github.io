:Title: Machine learning challenges for computer architecture
:Date: 2016-11-4
:Category: notes
:Tags: machine-intelligence, computing

Neural networks have become a hot topic in computing and their development is
progressing rapidly. They have a long history with some of the first designs
proposed in the 1940s.  But despite being an active area of research since
then, it has not been until the last five to ten years that the field has
started to deliver state-of-the-art results, with deep neural network-based
algorithms displacing conventional machine-learning and programmed ones in many
areas.

The recent developments in neural networks, since around 2010,  has coincided
with the availability of commodity high-performance GPUs. These devices provide
enough memory and compute that networks can be trained with large datasets, in
the order of hours or days, to perform classification tasks for practical and
interesting problems such as image and speech recognition. Although GPUs have
established themselves as the standard way to accelerate neural networks, they
have done this by transitioning relatively quickly from applications in
traditional HPC, but they are already evolving to meet the needs of machine
learning. In this article I want to discuss some of the challenges that neural
networks and their development present to GPUs, and indeed more generally to
the status quo of computer architecture.

Compute and memory
~~~~~~~~~~~~~~~~~~

The fundamental operations of a neural network are floating-point
multiplications and additions. These are used to combine input data with the
parameters of the network that control the influence of connections between
neurons.  Modern networks require considerable resources to store millions of
parameters and perform billions of operations per input.

`Neurons <NeuronLink_>`_ in `fully-connected layers <FCLayerLink_>`_ take
weighted sums of their inputs (a multiplication and an accumulation, MAC, for
each input) from every neuron in the previous layer. The number of MACs grows
with the square of the layer size, and the number of layers, so even with
modest numbers of layers and neurons per layer, the number of MACs can be
large. In the `AlexNet network <AlexNetLink_>`_, the last three layers are
fully connected with 4,096, 4,096 and 1,000 neurons respectively, requiring
58.6 million parameters and, for the `forward pass <FwdPassLink_>`_ to classify
a single input image with a trained network, the same number of MACs.

The use of `convolutional layers <ConvNetsLink_>`_ reduces the number of
parameters by sharing a small sets between the neurons. The five
convolutional layers preceding the fully-connected layers in AlexNet contain
just 2.5 million neurons, but require 655.6 million MACs per input. AlexNet was
state of the art in 2009 and networks since then have developed with many more
convolutional layers and a smaller fully connected component, resulting in
relatively slow growth in the number of parameters but significant increases in
the number of MACs. A variant of the `VGG network <VGGNetLink_>`_
(2014) with 19 layers (three fully connected) has 143.6 million parameters and
requires a total of 19.6 million MACs in the forward pass. A variant of the
`ResNet network <ResNetLink_>`_ (2015) with 50 layers (one fully connected) has
25.5 million parameters and 3.8 billion MACs for the forward pass. More `recent
work <StocDepthLink_>`_ has demonstrated benefits of networks with more than
1,000 layers.

When a network is being trained, more compute is required by an additional
backwards pass and and memory requirements increase since intermediate values
for each parameter must be maintained from the forward pass.

The challenge for computer architecture here is to deliver the huge number of
MACs required for training and inference, whilst minimising the movement of
data between fast local memory and slower main memory, or via a communication
link.  This will of course require corresponding developments in the
implementation of neural networks. A `recent result <RNNOnChipLink_>`_
demonstrated that when data is kept on chip, much better use of GPU compute
resource can be made to achieve an order of magnitude improvement in the depth
of network that could be trained. Another has `demonstrated
<SubLinearMemLink_>`_ that compute can be traded for a logarithmic reduction of
memory in the number of layers.

.. _NeuronLink: https://en.wikipedia.org/wiki/Artificial_neuron

.. _FCLayerLink: http://neuralnetworksanddeeplearning.com/chap1.html#the_architecture_of_neural_networks

.. _AlexNetLink: https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks.pdf

.. _FwdPassLink: http://neuralnetworksanddeeplearning.com/chap2.html

.. _ConvNetsLink: http://deeplearning.net/tutorial/lenet.html

.. _VGGNetLink: https://arxiv.org/abs/1409.1556

.. _ResNetLink: https://arxiv.org/abs/1512.03385

.. _StocDepthLink: https://arxiv.org/abs/1603.09382

.. _RNNOnChipLink: http://jmlr.org/proceedings/papers/v48/diamos16.pdf

.. _SubLinearMemLink: https://arxiv.org/pdf/1604.06174v2.pdf

Precision
~~~~~~~~~

Reducing the precision of arithmetic reduces the cost of memory and compute
since lower-precision floating-point numbers require less bits of storage and
require smaller more power-efficient structures in silicon to implement
arithmetic operations. Recent research has demonstrated that representations
between 8 and 16 bits can deliver `similar results <LowPrecisionLink_>`_ to
32-bit precision for inference and training. This has already has an impact on
architecture: Google has claimed a `10x increase in efficiency <TPULink_>`_
with it's Tensor Processing Unit (TPU) using `8-bit precision <8BitTFLink_>`_,
and Nvidia's new Pascal architecture supports `16-bit floating-point arithmetic
<PascalFP16Link_>`_ at twice the rate of single precision, and `8-bit integer
arithmetic <PascalInt8Link_>`_ at four times the rate. Intel have also
`recently announced <KnightsMillLink_>`_ a variant of their Xeon Phi processor,
code named Knights Mill, that will be optimised for deep learning with variable
precision floating-point arithmetic.

.. _LowPrecisionLink: https://arxiv.org/abs/1412.7024

.. _TPULink: http://www.tomshardware.com/news/google-tensor-processing-unit-machine-learning,31834.html

.. _8BitTFLink: https://petewarden.com/2016/05/03/how-to-quantize-neural-networks-with-tensorflow/

.. _PascalFP16Link: https://blogs.nvidia.com/blog/2015/03/17/pascal/

.. _PascalInt8Link: https://www.hpcwire.com/2016/09/12/nvidia-aims-gpus-deep-learning-inferencing/

.. _KnightsMillLink: http://www.anandtech.com/show/10575/intel-announces-knights-mill-a-xeon-phi-for-deep-learning

Structure
~~~~~~~~~

There is no single structure for data movement in deep neural networks. The
simplest networks have connections between adjacent layers, which are evaluated
in sequence, but many `more complex structures have been proposed
<NNArchLink_>`_. For example, `residual connections <ResNetLink_>`_ provide a
pathway between non-adjacent layers, `fractal architectures
<FractalArchLink_>`_ have self-similar structures at different scales and
entire neural networks can be `used as basic building blocks
<NetInNetArchLink_>`_. There can also by dynamism in the structure; `dropout
<DropoutLink_>`_ prevents overfitting by randomly removing connections during
training to 'thin' the network, and networks with `stochastic depth
<StochasticDepthLink_>`_ randomly exclude subsets of layers during training to
make deep networks more shallow.

These neural-network structures contrast with traditional HPC-style programs,
which have long been the focus of parallel computing research and development
and are characterised by a `single structure and algorithm <DwarfsLink)>`_. The
challenge here is for computing hardware and the programming models targeting
it to support complex, highly-connected and potentially dynamic communication
structures.

.. _NNArchLink: https://culurciello.github.io/tech/2016/06/04/nets.html

.. _ResNetLink: https://arxiv.org/abs/1512.03385

.. _FractalArchLink: https://arxiv.org/pdf/1605.07648v1.pdf

.. _NetInNetArchLink: https://arxiv.org/abs/1312.4400

.. _DropoutLink: https://www.cs.toronto.edu/~hinton/absps/JMLRdropout.pdf

.. _StochasticDepthLink: https://arxiv.org/abs/1603.09382v1

.. _DwarfsLink: http://view.eecs.berkeley.edu/wiki/Dwarfs

Programming
~~~~~~~~~~~

There are `many languages, frameworks and libraries <MLProgrammingListLink_>`_
available for creating deep-learning applications and they are having to
evolve quickly though to keep up with the pace of research. This is a strong
indication that the means by which we program neural networks need to be
general enough to facilitate experimentation but also deliver reasonable
performance so that it is practical to explore different designs and
hyper parameters.

However, there is a gulf between the high-level representations of neural
networks used by researchers and their actual implementation on hardware.  For
example, Google's `TensorFlow <TFLink_>`_ programming framework is written in
C++ and interfaces with GPUs via an abstraction layer that calls CUDA library
routines. On top of this, Google have released a high-level Python wrapper for
TensorFlow, called `TensorFlow-Slim <TFSlimLink_>`_.  But despite the
abstraction and generality of the TensorFlow framework, achieving good
computational efficiency on GPUs depends on a heavily-optimised high-level deep
neural network library, such as `cuDNN <CUDNNLink_>`_ or `NEON <NeonLink_>`_.
The problem for all high-level programming approaches is that the performance
of neural network designs that cannot exploit an underlying optimised library
directly will degrade significantly. Closing the gap between the methods used
to build neural networks and their mapping to a machine architecture would
deliver more performance for a wider range of programs.

.. _MLProgrammingListLink: https://github.com/josephmisiti/awesome-machine-learning

.. _TFLink: https://www.tensorflow.org/

.. _TFSlimLink: https://research.googleblog.com/2016/08/tf-slim-high-level-library-to-define.html

.. _CUDNNLink: https://developer.nvidia.com/cudnn

.. _NeonLink: https://github.com/NervanaSystems/neon

Deployment and portability
~~~~~~~~~~~~~~~~~~~~~~~~~~

Finally, a unique aspect of machine-learning algorithms is the separation
between the phase in which they are trained and their subsequent deployment for
inference.  Since training demands more compute and memory resources and is
typically carried out in a data-centre environment where space, power and, to
some extent, time are not constraining issues.  A trained neural network can be
deployed in more constrained environments, such as mobile or robotics, where
they may be reacting in real time, to a voice user interface or sensor input
for example, with limited memory and power. They may also continue to learn as
they are exposed to more data.

The result of training is a set of parameter values and portability to another
platform requires the weights to be loaded in an implementation of the same
neural network. The implementation may differ in the numerical precision it
uses since trained networks are known to be robust to low-precision parameter
representations, and doing so takes advantage of the associated memory,
performance and power benefits. A portable neural network might therefore need
separate implementations for training and inference, optimised for the memory
and compute constraints and to be targeted at different machine architectures.
A standardised specification of neural networks, including trained parameters,
would further improve portability between platforms.

There have been some efforts to try to measure aspects of the implementation,
deployment and performance of deep neural networks. In particular `Deepmark
<DeepMarkLink_>`_, which is based on specific networks, and `Deepbench
<DeepBenchLink_>`_, which takes a simpler approach by just looking at important
kernels.

.. _DeepMarkLink: https://github.com/DeepMark/deepmark

.. _DeepBenchLink: https://github.com/baidu-research/DeepBench

In summary
~~~~~~~~~~

Modern deep neural networks are now state-of-the-art in many application areas
of computing but with their unique characteristics, they pose a significant
challenge to conventional computer architecture. This challenge however is also
an opportunity to build new machines and programming languages that break away
from the status quo of sequential shared-memory von Neumann machines.
