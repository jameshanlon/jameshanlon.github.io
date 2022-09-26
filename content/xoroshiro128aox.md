---
Title: The Graphcore IPU’s Hardware Pseudorandom Number Generator
Date: 2022-09-21
Category: notes
Tags: computing, PRNGs
Status: published
---

{% import 'post-macros.html' as macros %}

This note is a summary of a [journal
paper](https://ieeexplore.ieee.org/document/9875973) and was originally written
for the Graphcore blog. 

The Graphcore IPU contains a novel pseudorandom number generator (PRNG) that
was designed to produce high-quality statistical randomness, whist also being
cheap to implement in hardware. Having an efficient hardware RNG means
randomness can be used frequently: the IPUs generator can produce 64-bits of
unique randomness from all of its 1,216 tiles every clock cycle. This, for
example, makes it possible to perform on-the-fly stochastic rounding of
low-precision floating-point numbers.

We needed a new PRNG because typical state-of-the-art generators are designed
to be performant when run as software routines, but operations that are cheap
to execute on a processor may not be cheap to implement in hardware as is the
case for multiplication or division. Our generator ``xoroshiro128aox`` is based
on [Sebastiano Vigna’s](https://vigna.di.unimi.it/) ``xoroshiro128``
linear-feedback shift register (LFSR), which is attractive because it uses 128
bits of state and is cheap to implement in hardware. The LFSR operates by
performing XOR and fixed-distance shift and rotate operations on the state.
Following Vigna’s approach of adding a function to ‘scramble’ the LFSR state,
we have devised a function consisting of AND, OR and XOR operations (called AOX
for short). An implementation of ``xoroshiro128aox`` is listed below:

```
uint64_t s0, s1; // State vectors

uint64_t rotl(uint64_t x, int k) {
  return (x << k) | (x >> (64 - k));
}

uint64_t next(void) {
  uint64_t sx = s0 ^ s1;

  // Calculate the result, the 'AOX' step.
  uint64_t sa = s0 & s1;
  uint64_t res = sx ^ (rotl(sa, 1) | rotl(sa, 2));

  // xoroshiro128 state update
  s0 = rotl(s0, 55) ^ sx ^ (sx << 14);
  s1 = rotl(sx, 36);
  return res;
}
```

To determine that this new PRNG provides a good source of randomness, we took
the conventional approach of subjecting the generator to batteries of
statistical tests, that aim to detect correlations over large portions of the
generator’s output. Given that any PRNG is inherently non-random because they
produce numbers according to a fixed sequence, statistical testing is only as
good as the tests that they run, and their performance can only be judged on
their ability to distinguish existing good generators from bad ones. Indeed, a
novel statistical test could immediately raise the bar for all PRNGs.

Within the field of PRNG design,
[TestU01’s](http://simul.iro.umontreal.ca/testu01/tu01.html) BigCrush battery
is accepted as the gold-standard statistical test, however it is not always
clear exactly what methodology has been used to obtain a pass/fail result. In
particular, the choice of initial state (the seed) is important because
different parts of a sequence may have different properties, and TestU01 has
known biases in the way it uses bits from a generator’s output. To mitigate
these issues, we run every generator from 100 unique seeds and supply six
permutations of the output bits. And as well as running TestU01, we also run
[PractRand](http://pracrand.sourceforge.net/) and
[Gjrand](http://gjrand.sourceforge.net/) with the same 100 seeds, which are the
two other most well-regarded test sets. This gives us a comprehensive testing
methodology that goes beyond the typical level of analysis.

To provide a point of comparison, we include the following PRNGs:

-	32-bit Mersenne Twister since it is one of the most widely used software
	PRNGs (although it has 19,937 bits of state!).

-	``Xoroshiro128+``, which is Vigna’s closest variant of ``xoroshiro128``,
	using 64-bit addition to scramble 128-bit LFSR states.

And to represent the current state-of-the-art 128-bit generators, we include:

-	``Philox4x32-10``, a counter-based generator whose transition between states
	is a 128-bit increment and output scrambling function is 10 rounds of 32-bit
  multiplications and XORs.

-	Pcg64, a linear-congruential generator (LCG) that uses multiplication and
	addition by 128-bit constants for the state-transition function, and XOR and
  variable rotation operations to produce outputs.


