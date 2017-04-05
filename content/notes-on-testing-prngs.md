Title: Notes on testing random number generators
Date: 2017-4-5
Category: computing

Recently I have been doing some work testing the quality of [random
number generators](https://en.wikipedia.org/wiki/Random_number_generator)
(RNGs), so I thought I would record things that should be useful as a
reference. I won't provide too much background here since there are many good
existing references to the theory and practice of RNGs, the ones of which I
have encountered I have linked to.

# Properties

More specifically, a [pseudorandom number
generator](https://en.wikipedia.org/wiki/Pseudorandom_number_generator) (PRNG)
is a **repeatable** process for producing numbers that have good statistical
random properties. A true RNG, in contrast, produces statistically random
numbers in a non-repeatable way, for example in electronics by using a physical
source of entropy. True RNGs have an obvious importance in cryptographic
applications.

A pseudorandom sequence can be repeated by starting with a particular **seed**
number.  The **period** of a PRNG is the longest unique sequence of numbers
generated from any seed. The period is bounded by the size of the internal
state of a generator ($n$ bits of state can encode $2^n$ numbers), however a
generator may produce shorter repeated sequences, called **cycles**.

The properties of a 'good' PRNG are:

1. That the length of its period exceeds the number of values that taken from
   the generator by a program.  [As a rule of
   thumb](http://xoroshiro.di.unimi.it/#remarks), the period should be at least
   the square of the numbers used.

2. For independent uses of a generator concurrently, that the probability is low
   that any two sequences starting at different seeds overlap.

3. That successive values are uniformly distributed. In the literature this
   property is also described as
   [equidistribution](https://en.wikipedia.org/wiki/Equidistributed_sequence),
   which can be stated as the probability of finding a number in an interval of
   a sequence is proportional to the length of the interval.

4. That successive values are uncorrelated.

5. That each value can be computed efficiently.

The first two properties can typically be determined analytically and it is
true that PRNGs are designed in order that they can be.  Uniformity can be
tested by sampling a large number of values and using statistical measures to
analyse the difference from the expected distribution.  The fifth
characteristic is straightforward to determine, whether the generator is
implemented in hardware or software.  Much harder to determine, however, is the
third property. If it were possible to prove whether a generator is free of
correlation, no PRNG would be considered random since by definition there
exists a well-defined relationship between successive numbers.

# Empirical testing

Conventional approaches to testing RNGs subject them to a collection of tests,
exploring different aspects of the generator's statistics. They cannot be
exhaustive, but are shown to be effective by their performance in detecting
correlations in existing standard RNGs. This pragmatism is summed up well in
[this paper](http://portal.acm.org/citation.cfm?doid=1268776.1268777) with the
comment: "the different between good and bad RNGs, in a nutshell, is that the
bad ones fail very simple tests whereas the good ones fail only very
complicated tests that are hard to figure out or impractical to run."

There are two popular empirical test suites:

- [TestU01](http://simul.iro.umontreal.ca/testu01/tu01.html), a comprehensive C
  library, containing example PRNGs, utilities and a collection of statistical
  tests drawn from the academic literature of RNGs. The statistical tests can
  be run individually, or as part of test batteries, which have various run
  times and levels of stringency.

- [PractRand](http://pracrand.sourceforge.net/), which provides similar
  functionality to TestU01 but implemented in C++, with more modern features
  such as multithreading, flexible interfaces and support for long sequence
  lengths (over 100 terabytes). [According to the
  author](http://pracrand.sourceforge.net/PractRand.txt), it's tests are not
  drawn from the literature (presumably designed by the author instead) and are
  therefore a good complement to testing with TestU01 or similar. It also
  requires more random bits than TestU01 and therefore takes longer to run.

Also worth investigating are the
[Dieharder](https://www.phy.duke.edu/~rgb/General/dieharder.php) test suite (an
updated version of the original
[Diehard](https://en.wikipedia.org/wiki/Diehard_tests)) and the
[RaBiGeTe](http://cristianopi.altervista.org/RaBiGeTe/) test suite. There is
also some interesting discussion from 2010 between the authors of PractRand and
RaBiGete [here](http://mathforum.org/kb/message.jspa?messageID=7152033).

# Testing with TestU01

TestU01 provides an interface to test external generators written in C. The
interface requires a method, `GetU01`, to generate numbers in the unit interval
$\[0, 1)$ as a `double` and a method, `GetBits`, to return 32 random bits as an
`unsigned int`. Some tests will use random bits and some will use random floats.
Just one function can be provided, with the other defined by TestU01 with
the relationship $\texttt{GetU01}=\texttt{GetBits}/2^{32}$.

Converting 32 random bits to a double-precision float is lossless in that it
has be represented exactly in the 52 bits of mantissa. However, the conversion
biases the higher bits since the lowest bits will be most affected by numerical
errors. For this reason, it is considered good practice to also test the
reversed output of generator, to expose the lowest bits. To test generators
with a larger output, say 64 bits, it is important that all the bits are
exposed to the tests. One way to do this is to alternately use the high and low
bits of a 64-bit value each call to `GetBits` or `GetU01`. A further reason to
run the reverse of a generator is that the Crush test battery are defined to
ignore the bottom-most bit of the generator's output, and most tests also
ignore the second bit (see the [TestU01
documentation](http://simul.iro.umontreal.ca/testu01/guideshorttestu01.pdf)).

In his testing of the `xorshift` family of generators, [Sebastiano
Vigna](http://vigna.di.unimi.it/) takes the following approach to measuring
quality with TestU01: for a particular generator, run it with 100 different
seeds, which are spaced at regular intervals in the state space, i.e.  for a
generator with $n$ bits of state, choose seeds at $1 + i\lfloor 2^n/100\rfloor$
for $0 \leq i < 100$. The quality of a generator is then measured by the total
number of failures over all seeds, with fewer failures meaning higher
quality. If a generator has 100 or more failures, the failure is called
*systematic* and the generator is disregarded. Quality is measured with the
BigCrush battery, but since it takes many hours to run (using approximately
$2^{38}$ random values in 106 tests), potential generators can be assessed by
running the smaller test batteries SmallCrush (10 tests) and Crush (96 tests),
continuing based on the number of failures.

Through my own experiments, I found that the reverse of a generator won't
always catch weak lower bits.  `xoroshiro128+` is currently the [highest
quality and fastest known generator](http://xoroshiro.di.unimi.it/#shootout),
as measured by the above process, with 31 failures and 27 failures when
reversed, but it has a known weak bit 0 that follows a [linear
recurrence](https://en.wikipedia.org/wiki/Linearity#Boolean_functions) that is
not detected by BigCrush, even when reversed.  However, the weak bit is
detectable with the matrix rank test with parameters $N=1$, $n=80$, $r=15$,
$s=15$, $L=k=5000$, or more simply by swapping the high and low 16-bit portions
of each 32-bit word to move the bottom bit into the middle. I didn't discover
anything new about `xoroshiro128+` here, but what this does highlight is that
comprehensive test sets like TestU01 are by no means exhaustive, and it
therefore worth testing some of their assumptions, particularly in this case if
you are interested in the quality of bit 0.

Incidentally, TestU01 includes a battery of nine tests called Alphabit, which
is allows specific bits or ranges of bits from a generator to be tested. It was
not stringent enough however to detect the correlation of `xoroshirt128+`'s bit
0.

# An example

I've put together a simple example, [available on
Github](https://github.com/jameshanlon/prng-testing), of using TestU01 to
assess the quality of a PRNG, which replicates Vigna's testing of
`xoroshiro128+`.  The code includes a C program to test `xoroshiro128+` with
the Crush batteries and Python scripts to run the test over different seeds and
to summarise the output of TestU01.

# Further reading and links

- [The PRNG shootout](http://xoroshiro.di.unimi.it/).
- Sebastiano Vigna. An experimental exploration of Marsaglia's xorshift
  generators, scrambled. ACM Trans. Math. Software, 42(4), 2016.
- For a comprehensive general introduction to PRNGs and testing them, see 'The
  art of computer systems performance analysis' by Raj Jain (1991) Chapters 26
  and 27.
