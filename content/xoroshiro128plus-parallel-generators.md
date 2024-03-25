---
Title: Seeding parallel xoroshiro128+ generators
Date: 2022-7-1
Category: notes
Tags: computing, PRNGs
Summary: Choosing seeds for parallel xoroshiro128+ generators using fixed
         offsets produces correleated outputs
Status: published
---

As part of the [statistical quality
analysis](/the-hardware-pseudorandom-number-generator-of-the-graphcore-ipu) I
did of the of the `xoroshiro128aox` PRNG, I looked at interleaved parallel
generators (where a single generator is created by round-robin interleaving the
output $n$ identical generators with different seeds) as a way to test its
suitability for parallel processing. Against my intuition, I found that simple
seeding schemes produce poor interleaved generators, and even when the
subsequences are disjoint. These findings equally apply to `xoroshiro128+` as
we will see.

The `xoroshiro128+` creators [recommend using a jump
function](https://prng.di.unimi.it) to seed parallel generators to
deterministically move to disjoint parts of the sequence. However, computing
jumps is expensive to do in hardware because it involves 128-bit arithmetic and
so it is preferrable to compute seed values based on a simpler function of a
machine's state, such as an integer identifier for a process/thread. Since the
probability of any two randomly-chosen sequences overlap is very small even
with a large number of sequences, it seems reasonable to assume that a simple
seed generator will perform okay in practice. Note also that the creators
separately recommend "that initialization must be performed with a generator
radically different in nature from the one initialized to avoid correlation on
similar seeds", based on [research from
2007](https://dl.acm.org/citation.cfm?doid=1276927.1276928).

To investigate the use of simple seeding schemes, I ran tests against
interleaved generators with three representative options (the source code is
available on [GitHub](https://github.com/jameshanlon/prng-testing)):

With equidistant intervals from 1 in the natural number sequence [Scheme A],
defined in Python notation as:
```
for i in range(NUM_SEEDS):
    seed[i] = int(1 + i * ((2**128) // NUM_SEEDS))
```

With equidistant intervals starting from a random offset [Scheme B]:
```
for i in range(NUM_SEEDS):
    seed[i] = int(rand(0, (2**128) // NUM_SEEDS) + i * ((2**128) // NUM_SEEDS))
```

By adding a fixed offset to a initial state of balanced 0s and 1s [Scheme C]:
```
for i in range(NUM_SEEDS):
    seed[i] = 0x55555555555555555555555555555555 + i
```

And, as baselines:

- Using the `xoroshiro128` jump function, jumping $2^{64}$ steps [Scheme D].
- Using a minimum-size jump for the number of generators to pass PractRand [Scheme E]
  (for example, the distance for 1000 generators is 4398046511 = (32 * 1024**4) / (8 * 1000)
- Using a non-linear PRNG to choose seeds (PCG64) [Scheme F].

To test these seeding schemes, I ran each generator against the standard
PractRand test battery. PractRand is a good choice for these tests since it reports
results at intermediate points and consumes much more output than Big Crush or Gjrand:
32 TB by default. A pass is achieved if no overtly suspicious $p$-values are flagged.

The results are summarised in the following table:

<table class="table">
  <thead>
    <tr>
      <th scope="col">Seeding scheme</th>
      <th scope="col">Number of generators</th>
      <th scope="col">Failures</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Scheme A</td>
      <td>10</td>
      <td>256 MB</td>
      <td><code>DC6</code>, <code>FPF</code></td>
    </tr>
    <tr>
      <td>Scheme A</td>
      <td>100</td>
      <td>512 MB</td>
      <td><code>DC6</code>, <code>FPF</code></td>
    </tr>
    <tr>
      <td>Scheme A</td>
      <td>1000</td>
      <td>16 GB</td>
      <td><code>BCFN</code></td>
    </tr>
    <tr>
      <td>Scheme B</td>
      <td>10</td>
      <td>256 MB</td>
      <td><code>FPF</code></td>
    </tr>
    <tr>
      <td>Scheme B</td>
      <td>100</td>
      <td>2 GB</td>
      <td><code>DC6</code></td>
    </tr>
    <tr>
      <td>Scheme B</td>
      <td>1000</td>
      <td>32 GB</td>
      <td><code>BCFN</code></td>
    </tr>
  </tbody>
</table>

Note that DC6 and BCFN are both tests for linearity.

All tests failing within the first 1 GB are checked for dupilicate values between the different generators to establish that no two sequences overlap.

Sample output for Scheme A with 10 parallel generators that fails convincingly
within the first 256 MB of output:
```
RNG_test using PractRand version 0.95
RNG = RNG_stdin64, seed = unknown
test set = core, folding = standard (64 bit)

rng=RNG_stdin64, seed=unknown
length= 256 megabytes (2^28 bytes), time= 2.3 seconds
  Test Name                         Raw       Processed     Evaluation
  BCFN(2+0,13-2,T)                  R=  -0.0  p = 0.494     normal
  BCFN(2+1,13-2,T)                  R=  +4.1  p = 0.050     normal
  BCFN(2+2,13-3,T)                  R=  +0.0  p = 0.484     normal
  BCFN(2+3,13-3,T)                  R=  +1.3  p = 0.292     normal
...
  [Low16/64]BCFN(2+12,13-9,T)       R=  -2.1  p = 0.849     normal
  [Low16/64]DC6-9x1Bytes-1          R=  +1.6  p = 0.332     normal
  [Low16/64]Gap-16:A                R=  +0.5  p = 0.523     normal
  [Low16/64]Gap-16:B                R=  +4.3  p =  1.3e-3   normalish
  [Low16/64]FPF-14+6/16:(0,14-0)    R=  +0.2  p = 0.434     normal
  [Low16/64]FPF-14+6/16:(1,14-0)    R=  +2.2  p = 0.061     normal
...
  [Low4/64]BCFN(2+9,13-9,T)         R=  +0.6  p = 0.310     normal
  [Low4/64]BCFN(2+10,13-9,T)        R=  +0.2  p = 0.372     normal
  [Low4/64]DC6-9x1Bytes-1           R= +88.5  p =  5.9e-51    FAIL !!!!
  [Low4/64]Gap-16:A                 R=  +4.4  p =  4.6e-3   normalish
  [Low4/64]Gap-16:B                 R=  -0.6  p = 0.656     normal
  [Low4/64]FPF-14+6/16:(0,14-1)     R=  -1.0  p = 0.759     normal
  [Low4/64]FPF-14+6/16:(1,14-2)     R=  -3.7  p =1-4.2e-3   normal
  [Low4/64]FPF-14+6/16:(2,14-2)     R=  -0.9  p = 0.738     normal
  [Low4/64]FPF-14+6/16:(3,14-3)     R=  +1.3  p = 0.189     normal
  [Low4/64]FPF-14+6/16:(4,14-4)     R=  +1.6  p = 0.134     normal
  [Low4/64]FPF-14+6/16:(5,14-5)     R=  +1.2  p = 0.206     normal
  [Low4/64]FPF-14+6/16:(6,14-5)     R=  +1.4  p = 0.166     normal
  [Low4/64]FPF-14+6/16:(7,14-6)     R=  -1.6  p = 0.877     normal
  [Low4/64]FPF-14+6/16:(8,14-7)     R=  -0.7  p = 0.681     normal
  [Low4/64]FPF-14+6/16:(9,14-8)     R=  +1.2  p = 0.187     normal
  [Low4/64]FPF-14+6/16:(10,14-8)    R= +19.4  p =  5.5e-14    FAIL
  [Low4/64]FPF-14+6/16:(11,14-9)    R= +12.4  p =  4.0e-8   suspicious
  [Low4/64]FPF-14+6/16:(12,14-10)   R= +12.5  p =  3.0e-7   mildly suspicious
  [Low4/64]FPF-14+6/16:(13,14-11)   R=  +5.1  p =  4.8e-3   normal
  [Low4/64]FPF-14+6/16:(14,14-11)   R=  +8.8  p =  1.1e-4   normal
  [Low4/64]FPF-14+6/16:all          R=  +0.3  p = 0.435     normal
  [Low4/64]FPF-14+6/16:cross        R=  +2.1  p = 0.032     normal
  [Low4/64]BRank(12):128(4)         R=  -0.8  p~= 0.670     normal
  [Low4/64]BRank(12):256(2)         R=  +1.6  p~= 0.168     normal
  [Low4/64]BRank(12):384(1)         R=  +1.8  p~= 0.146     normal
  [Low4/64]BRank(12):512(2)         R=  -0.2  p~= 0.554     normal
  [Low4/64]BRank(12):768(1)         R=  -0.7  p~= 0.689     normal
  [Low4/64]mod3n(5):(0,9-6)         R= +14.0  p =  1.3e-5   mildly suspicious
  [Low4/64]mod3n(5):(1,9-6)         R=  -0.0  p = 0.451     normal
  [Low4/64]mod3n(5):(2,9-6)         R=  -0.2  p = 0.492     normal
  [Low4/64]mod3n(5):(3,9-6)         R=  -1.5  p = 0.781     normal
  [Low4/64]mod3n(5):(4,9-6)         R=  +0.0  p = 0.433     normal
  [Low4/64]mod3n(5):(5,9-6)         R=  +0.4  p = 0.353     normal
  [Low4/64]mod3n(5):(6,9-6)         R=  -1.3  p = 0.742     normal
  [Low4/64]mod3n(5):(7,9-6)         R=  +1.9  p = 0.152     normal
  [Low4/64]mod3n(5):(8,9-6)         R=  -1.3  p = 0.731     normal
  [Low4/64]mod3n(5):(9,9-6)         R=  -0.4  p = 0.540     normal
  [Low4/64]mod3n(5):(10,9-6)        R=  -0.6  p = 0.585     normal
  [Low4/64]mod3n(5):(11,9-6)        R=  +0.6  p = 0.322     normal
  [Low1/64]BCFN(2+0,13-6,T)         R=  +7.3  p =  6.5e-3   normalish
  [Low1/64]BCFN(2+1,13-6,T)         R=  -3.2  p = 0.926     normal
  [Low1/64]BCFN(2+2,13-6,T)         R=  -1.5  p = 0.716     normal
  [Low1/64]BCFN(2+3,13-6,T)         R=  +1.6  p = 0.238     normal
  [Low1/64]BCFN(2+4,13-7,T)         R=  +1.7  p = 0.212     normal
  [Low1/64]BCFN(2+5,13-8,T)         R=  +0.8  p = 0.304     normal
  [Low1/64]BCFN(2+6,13-8,T)         R=  +0.2  p = 0.403     normal
  [Low1/64]BCFN(2+7,13-9,T)         R=  +1.0  p = 0.257     normal
  [Low1/64]BCFN(2+8,13-9,T)         R=  -1.8  p = 0.790     normal
  [Low1/64]DC6-9x1Bytes-1           R= +1379  p =  3.6e-777   FAIL !!!!!!!
  [Low1/64]Gap-16:A                 R= +4863  p =  5e-3914    FAIL !!!!!!!!
  [Low1/64]Gap-16:B                 R=+11222  p =  6e-8467    FAIL !!!!!!!!
  [Low1/64]FPF-14+6/16:(0,14-2)     R=+10120  p =  5e-8851    FAIL !!!!!!!!
  [Low1/64]FPF-14+6/16:(1,14-3)     R= +7164  p =  2e-6279    FAIL !!!!!!!!
  [Low1/64]FPF-14+6/16:(2,14-4)     R= +5071  p =  9e-4144    FAIL !!!!!!!!
  [Low1/64]FPF-14+6/16:(3,14-5)     R= +3567  p =  1e-2956    FAIL !!!!!!!!
  [Low1/64]FPF-14+6/16:(4,14-5)     R= +2180  p =  7e-1807    FAIL !!!!!!!!
  [Low1/64]FPF-14+6/16:(5,14-6)     R= +1535  p =  1e-1174    FAIL !!!!!!!!
  [Low1/64]FPF-14+6/16:(6,14-7)     R=+350.5  p =  9.0e-279   FAIL !!!!!!
  [Low1/64]FPF-14+6/16:(7,14-8)     R=+255.2  p =  1.1e-183   FAIL !!!!!!
  [Low1/64]FPF-14+6/16:(8,14-8)     R=+235.5  p =  1.7e-169   FAIL !!!!!
  [Low1/64]FPF-14+6/16:(9,14-9)     R=+152.7  p =  2.0e-96    FAIL !!!!!
  [Low1/64]FPF-14+6/16:(10,14-10)   R= +87.1  p =  6.7e-47    FAIL !!!
  [Low1/64]FPF-14+6/16:(11,14-11)   R= +58.4  p =  2.6e-26    FAIL !!
  [Low1/64]FPF-14+6/16:(12,14-11)   R= +58.0  p =  3.9e-26    FAIL !!
  [Low1/64]FPF-14+6/16:all          R=+14029  p = 0           FAIL !!!!!!!!
  [Low1/64]FPF-14+6/16:cross        R= +3119  p =  3e-2681    FAIL !!!!!!!!
  [Low1/64]BRank(12):128(2)         R=  -0.2  p~= 0.554     normal
  [Low1/64]BRank(12):256(2)         R=  -1.0  p~= 0.744     normal
  [Low1/64]BRank(12):384(1)         R=  -0.7  p~= 0.689     normal
  [Low1/64]BRank(12):512(1)         R=  +0.4  p~= 0.366     normal
  [Low1/64]mod3n(5):(0,9-6)         R=+322.9  p =  4.1e-111   FAIL !!!!!
  [Low1/64]mod3n(5):(1,9-6)         R=  -0.5  p = 0.563     normal
  [Low1/64]mod3n(5):(2,9-6)         R=  +2.1  p = 0.129     normal
  [Low1/64]mod3n(5):(3,9-6)         R=  +5.0  p = 0.016     normal
  [Low1/64]mod3n(5):(4,9-6)         R=  +2.5  p = 0.099     normal
  [Low1/64]mod3n(5):(5,9-6)         R=  -0.8  p = 0.614     normal
  [Low1/64]mod3n(5):(6,9-6)         R=  -1.4  p = 0.757     normal
  [Low1/64]mod3n(5):(7,9-6)         R=  +1.7  p = 0.167     normal
  [Low1/64]mod3n(5):(8,9-6)         R=  +2.3  p = 0.111     normal
  [Low1/64]mod3n(5):(9,9-6)         R=  +2.2  p = 0.125     normal
```

## Conclusion

Inter-sequence correlations exist in PRNGs based on the `xoroshiro128` linear engine.
It is likely that these correlations manifest when sequences are chosen by a linear generator.
Use the jump function to traverse the state space or use a non-linear function to generate  

## References

- My [PRNG testing](https://github.com/jameshanlon/prng-testing) source code.
- [xoshiro / xoroshiro generators and the PRNG shootout](https://prng.di.unimi.it/).
- Makoto Matsumoto, Isaku Wada, Ai Kuramoto, and Hyo Ashihara. 2007.
  Common defects in initialization of pseudorandom number generators.
  [ACM Transactions on Modelling and Computer Simulation](https://doi.org/10.1145/1276927.1276928).
