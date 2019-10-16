---
Title: A convolutional neural network from scratch
Date: 2017-2-10
Category: notes
Tags: machine-intelligence
Status: published
---

The online book '[Neural Networks and Deep
Learning](http://neuralnetworksanddeeplearning.com)' by Michael Nielsen is an
excellent introduction to neural networks and the world of deep learning.  As
the book works through the theory, it makes it concrete by explaining how the
concepts are implemented using Python. The complete Python programs are
[available on
Github](https://github.com/mnielsen/neural-networks-and-deep-learning) for
further inspection and experimentation.

I decided to write my own implementations of the examples however. Partly to
develop a better understanding but also because I felt that the matrix-based
presentation of the mathematics and use of NumPy operations in the examples
obscured some of the intuition around neurons and their connections, and
because the later examples of convolutional layers are implemented using
[Theano](deeplearning.net/software/theano/).

So, in the hope that it might be interesting as a simple and self-contained
example of a convolutional neural network where nothing is hidden, I've put he
source code for my implementation (written in C++) on
[GitHub](https://github.com/jameshanlon/convolutional-neural-network). For
reference I've also written up below the various equations for the
fully-connected and convolutional layers in element-wise notation. I should
thank two particularly useful blog posts by [Andrew
Gibiansky](http://andrew.gibiansky.com/blog/machine-learning/convolutional-neural-networks/)
and [Grzegorz Gwardys](https://grzegorzgwardys.wordpress.com/2016/04/22/8/)
which helped me to derive the convolutional equations for back propagation.

# The source code

The [repository](https://github.com/jameshanlon/convolutional-neural-network)
contains several example programs with different network
configurations. They are instantiated from a generic header ``Network.hpp``,
which contains classes for fully-connected, softmax, convolutional and
max-pooling layer types, and a network class that performs the stochastic
gradient descent, minibatching and training over multiple epochs with
randomly-shuffled training data. The header also contains definitions for
quadratic and cross-entropy cost functions, and sigmoid and rectified-linear
activation functions, which are specified as template parameters to the
network. The code is written primarily primarily to be clear and
understandable, as such there will be many opportunities for optimisations and
other improvements (please let me know if you have any suggestions).

For instructions on how to build and run the examples, see the ``README.md``
file. Note that Boost is required for ``multi_array`` and Threading Building
Blocks to parallelise the training over minibatches and accuracy evaluation by
performing inferences in parallel, up to the minibatch size.  It should be
straightforward to build other network configurations or to modify the
implementations or to experiment with new features.

Included in the ``extra`` folder, are implementations of the example programs
in [TensorFlow](https://www.tensorflow.org/), adapted from the [MNIST
tutorial](https://www.tensorflow.org/tutorials/mnist/pros/). I found these
useful as a point of comparison to validate the behaviour of the networks.

# Equations

The following notation roughly follows the notation in the Neural Networks and
Deep Learning book:

- $l$ is an index of a layer;
- $w$ is a weight;
- $z$ is a weighted input;
- $a$ is an activation;
- $y$ is a label;
- $\delta$ is an error;
- $\sigma$ is the activation function, $\sigma'$ is the derivative of it;
- $C$ is the cost function.

## For a fully-connected layer

In the forward pass, each neuron takes a weighted sum of its inputs, adds the bias
and uses the result as the input to the activation function:
$$z_i^l = \sum_j w_{j,i}^{l-1} a_j^{l-1} + b^l$$
$$a_i^l = \sigma(z_i^l)$$

The error of a neuron $i$ in the output layer is given by
$\delta_i = (a_i -y_i)\sigma'(z_i)$
for the sigmoid activation function and by
$\delta_i = a_i - y_i$
for the cross-entropy activation function.

In the backwards pass, errors are propagated to a neuron from neurons that are
connected as outputs.  The weighted sum of the output neuron's errors and
connection weight is calculated and this value is then multiplied by the
derivative of the activation function:
$$\delta_i^l = \sum_j w_{j,i}^{l+1} \delta_j^{l+1} \sigma'(z_i^l)$$

The delta for a weight is calculated from the error held by a neuron and the
activation from the neuron connected by the input:
$$\frac{\partial C}{\partial w_i^l} = a_i^{l-1}\delta_i^l$$

The delta for the bias is equal to the error held by a neuron:
$$\frac{\partial C}{\partial b_i^l} = \delta_i^l$$

## For a convolutional layer

Assuming a two-dimensional input of size $N\times N$ and convolutional mask of
size $m\times m$.

In the forward pass, each neuron convolves the weights with its receptive field:
$$z_{x,y}^l = \sum_{a=0}^{m-1}\sum_{b=0}^{m-1} w_{a,b}^{l-1}a_{x+a,y+b}^{l-1} + b^l$$
$$a_{x,y}^l = \sigma(z_{x,y}^l)$$

In the backwards pass, errors are propagated to a neuron from the neurons
connected as outputs in the next layer:
$$\delta_{x,y}^l = \sum_{a=0}^{m-1}\sum_{b=0}^{m-1} w_{a,b}^{l+1}\delta_{x-a,y-b}^{l+1}\sigma'(z_{x,y}^l)$$
One way to simplify this is to [think of the convolutional layer as one
dimensional](https://grzegorzgwardys.wordpress.com/2016/04/22/8/) (as with a
fully-connected layer), where each neuron has only $m\times m$ inputs connections.
Then, back propagation operates in the same way as it does with fully-connected
layers. You can in fact use this approach to derive the above equation.

The delta of a weight is calculated from the activations in the previous layer
that influence that weight and the errors held by the neurons that use it:
$$\frac{\partial C}{\partial w_{a,b}^l} = \sum_{i=0}^{N-m}\sum_{j=0}^{N-m} a_{i+a, j+b}^{l-1}\delta_{i,j}^l$$

The delta of a bias is calculated from the errors held by the neurons that
use it:
$$\frac{\partial C}{\partial b^l} = \sum_{i=0}^{N-m}\sum_{j=0}^{N-m} \delta_{i,j}^l$$

With three-dimensional inputs, convolutional layers convolve a
three-dimensional mask into the depth of the input. Convolutional layers can
themselves produce three-dimensional outputs by stacking up separate
convolutional processes in the same layer (called feature maps or channels),
each contributing one element in the depth of the output. In this case, the
backpropagation of the error must sum over the feature maps to get the
contributions of each expression that contribute to the error. The weight and
bias updates must sum errors over the input volume they are applied to.

# Further reading

- [Convolutional neural networks tutorial](http://deeplearning.net/tutorial/lenet.html)
- [CS231n Convolutional Neural Networks for Visual Recognition](http://cs231n.github.io/)
- [Introduction to debugging neural networks](http://russellsstewart.com/notes/0.html)
