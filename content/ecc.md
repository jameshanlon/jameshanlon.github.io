---
Title: Error-correcting codes
Date: 2020-05-02
Category: notes
Tags: computing
Status: published
---

Error correcting codes (ECCs) are used in computer and communication systems to
improve resiliency to bit flips caused by permanent hardware faults or
transient conditions, such as neutron particles from cosmic rays, known
generally as [soft errors](https://en.wikipedia.org/wiki/Soft_error). This note
describes the principles of Hamming codes that underpin ECC schemes, ECC codes
are constructed, focusing on single-error correction and double error
detection, and how they are implemented.

ECCs work by adding additional redundant bits to be stored or transported with
data. The bits are encoded as a function of the data in such a way that it is
possible to detect erroneous bit flips and to correct them. The ratio of the
number of data bits to the total number of bits encoded is called the *code
rate*, with a rate of 1 being a an impossible encoding with no overhead.

## Simple ECCs

**Parity coding** adds a single bit that indicates whether the number of set
bits in the data is odd or even. When the data and parity bit is accessed or
received, the parity can be recomputed and compared. This is sufficient to
detect any odd number of bit flips but not to correct them. For applications
where the error rate is low, so that only single bit flips are likely and
double bit flips are rare enough to be ignored, parity error detection is
sufficient and desirable due to it's low overhead (just a single bit) and
simple implementation.

**Repetition coding** simply repeats each data bit a fixed number of times. When
the encoded data is received, if each of the repeated bits are non identical,
an error has occurred. With a repetition of two, single-bit errors can be
detected but not corrected. With a repetition of three, single bit flips can be
corrected by determining each data bit as the majority value in each triple,
but double bit flips are undetectable and will cause an erroneous correction.
Repetition codes are simple to implement but have a high overhead.

## Hamming codes

Hamming codes are an efficient family of codes using additional redundant bits to
detect up to two-bit errors and correct single-bit errors (technically, they are
*[linear error-correcting codes](https://en.wikipedia.org/wiki/Linear_code)*).
In them, *check bits* are added to data bits to form a *codeword*, and the
codeword is *valid* only when the check bits have been generated from the data
bits, according to the Hamming code. The check bits are chosen so that there is
a fixed *Hamming distance* between any two valid codewords (the number of
positions in which bits differ).

When valid codewords have a Hamming distance of two, any single bit flip will
invalidate the word and allow the error to be detected. For example, the valid
codewords `00` and `11` are separated for single bit flips by the invalid
codewords `01` and `10`. If either of the invalid words is obtained an error
has occurred, but neither can be associated with a valid codeword. Two bit
flips are undetectable since they always map to a valid codeword. Note that
parity encoding is an example of a distance-two Hamming code.

```
00 < Valid codeword
|
10 < Invalid codeword (obtained by exactly 1 bit flip)
|
11 < Valid codeword
```

With Hamming distance three, any single bit flip in a valid codeword makes an
invalid one, and the invalid codeword is Hamming distance one from exactly one
valid codeword. Using this, the valid codeword can be restored, enabling single
error correction. Any two bit flips map to an invalid codeword, which would
cause correction to the wrong valid codeword.

```
000 < Valid codeword
 |
001
 |
011
 |
111 < Valid codeword
```

With Hamming distance four, two bit flips moves any valid codeword Hamming
distance two from exactly two valid codewords, allowing detection of two flips
but not correction. Single bit flips can be corrected as they were for distance
three. Distance-four codes are widely used in computing, where is it often the
case where single errors are frequent, double errors are rare and triple errors
occur so rarely they can be ignored. These codes are referred to as 'SECDED
ECC' (single error correction, double error detection).

```
0000 < Valid codeword
 |
0001
 |
0011 < Two bit flips from either codeword.
 |
0111
 |
1111 < Valid codeword
```

Double errors can be corrected with a distance-five code, as well as enabling
the detection of triple errors. In general, if a Hamming code can detect $d$
errors, it must have a minimum distance of $d+1$ so there is no way $d$ errors
can change one valid codeword into another one. If a code can correct $d$
errors, it must have a minimum distance of $2d+1$ so that the originating code
is always the closest one. The following table summarises Hamming codes.

<table class="table table-sm">
<thead>
  <tr>
    <th scope="col">Distance</th>
    <th scope="col">Max bits corrected</th>
    <th scope="col">Max bits detected</th>
    <th scope="col"></th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>2</td>
    <td>1</td>
    <td>0</td>
    <td>Single error detection (eg parity code)</td>
  </tr>
  <tr>
    <td>3</td>
    <td>1</td>
    <td>1</td>
    <td>Single error correction (eg triple repetition code)</td>
  </tr>
  <tr>
    <td>4</td>
    <td>1</td>
    <td>2</td>
    <td>Single error correction, double error detection (a 'SECDED' code)</td>
  </tr>
  <tr>
    <td>5</td>
    <td>2</td>
    <td>2</td>
    <td>Double error correction</td>
  </tr>
  <tr>
    <td>6</td>
    <td>2</td>
    <td>3</td>
    <td>Double error correction, triple error detection</td>
  </tr>
</tbody>
</table>


## Creating a Hamming code

A codeword includes the data bits and checkbits. Each check bit corresponds to
a subset of the data bits and it is set when the parity of those data bits is
odd. To obtain a code with a particular Hamming distance, the number of check
bits and their mapping to data bits must be chosen carefully.

To build a single-error correcting (SEC) code that requires Hamming distance
three between valid codewords, it is necessary for:

- The mapping of each data bit to check bits is unique.
- Each data bit to map to at least two check bits.

To see why this works, consider two distinct codewords that necessarily
must have different data bits. If the data bits differ by:

- **1 bit**, at least two check bits are flipped, giving a total of three
  different bits.

- **2 bits**, these will cause at least one flip in the check bits since any two
  data bits cannot share the same check-bit mapping (ie by taking the XOR of
  the two check bit patterns). This also gives a total of three different bits as
  required.

- **3 bits**, this is already sufficient to give a Hamming distance of three.

To build a SECDED code that requires Hamming distance of four between valid
codewords, it is necessary for:

- The mapping of each data bit to check bits is unique.
- Each data bit to map to at least three check bits.
- Each check bit pattern to have an odd number of bits set.

Following a similar argument, consider two distinct codewords, data differing
by:

- **1 bit** flips three check bits, giving a total of four different bits.

- **2 bits** flip check bits in two patterns, and since any two odd-length patterns
  must have at least two non-overlapping bits, the results is at least two
  flipped bits, giving a total of four different bits. For example:

```
Check bits:  0 1 2 3
data[a]      x x x
data[b]        x x x
-----------  --------
Flips        x     x

Check bits:  0 1 2 3 4
data[a]      x x x
data[b]      x x x x x
----------   ---------
Flips              x x
```

- **3 bits** flip check bits in three patterns, and this time it is possible to
  overlap odd-length patterns in such a way that a minimum of 1 bit is flipped.
  For example:

```
Check bits:  0 1 2 3 4
data[a]      x x x
data[b]        x x x
data[c]      x     x x
-----------  ---------
Flips                x

Check bits:  0 1 2 3 4
data[a]      x x x x x
data[b]      x x x
data[c]      x     x x
-----------  ---------
Flips        x
```

- **4 bits** is already sufficient to provide a Hamming distance of four.

An example SEC code for eight data bits with four parity bits:
```
Check bits:  0 1 2 3
data[0]      x x x
data[1]        x x x
data[2]      x   x x
data[3]      x x   x
data[4]      x x
data[5]        x x
data[6]          x x
data[7]      x     x
```

An example SECDED code for eight data bits with five parity bits:
```
Check bits:  0 1 2 3 4
data[0]      x x x
data[1]      x x   x
data[2]      x   x x
data[3]        x x x
data[4]      x x     x
data[5]      x   x   x
data[6]        x x   x
data[7]      x     x x
```

Note that mappings of data bits to check bits can be chosen flexibly, providing
they maintain the rules that set the Hamming distance. This flexibility is
useful when implementing ECC to reduce the cost of calculating the check bits.
In contrast, many descriptions of ECC that I have found in text books and on
[Wikipedia](https://en.wikipedia.org/wiki/Hamming_code) describe a specific
encoding that does not acknowledge this freedom. The encoding they describe
allows the syndrome to be interpreted as the bit index of the single bit error,
by the check bit in position $i$ covering data bits in position $i$.
Additionally, they specify that parity bits are positioned in the codeword at
power-of-two positions, for no apparent benefit.


## Implementing ECC

Given data bits and check bits, and mapping of data bits to check bits, ECC
encoding works by calculating the check bits from the data bits, then combining
data bits and check bits to form the codeword. Decoding works by taking the
data bits from a codeword, recalculating the check bits, then calculating the
bitwise XOR between the original check bits and the recalculated ones. This
value is called the *syndrome*. By inspecting the number of bits set in the
syndrome, it is possible to determine whether there has been an error,
whether it is correctable, and how to correct it.

Using the SEC check-bit encoding above, creating a codeword from `data[7:0]`,
the check bits are calculated as follows (using Verilog syntax):

```
assign check_word[0] = data[0] ^ data[2] ^ data[3] ^ data[4] ^ data[7];
assign check_word[1] = data[0] ^ data[1] ^ data[3] ^ data[4] ^ data[5];
assign check_word[2] = data[0] ^ data[1] ^ data[2] ^ data[5] ^ data[6];
assign check_word[3] = data[1] ^ data[2] ^ data[3] ^ data[6] ^ data[7];
```

And the codeword formed by concatenating the check bits and data:

```
assign codeword = {check[3:0], data[7:0]};
```

Decoding of a codeword, splits it into the checkword and data bits, recomputes
the check bits and calculates the syndrome:

```
assign {old_check_word, old_data} = codeword;
assign new_check_word[0] = ...;
assign new_check_word[1] = ...;
assign new_check_word[2] = ...;
assign new_check_word[3] = ...;
assign syndrome = new_check_word ^ old_check_word;
```

When single bit errors occur, the syndrome will have the bit pattern
corresponding to a particular data bit, so a correction can be applied by
creating a mask to flip the bit in that position:

```
unique case(syndrome)
  4'b1110: correction = 1<<0;
  4'b0111: correction = 1<<1;
  4'b1011: correction = 1<<2;
  4'b1101: correction = 1<<3;
  4'b1100: correction = 1<<4;
  4'b0110: correction = 1<<5;
  4'b0011: correction = 1<<6;
  4'b1001: correction = 1<<7;
  default: correction = 0;
endcase
```

And using it to generate the corrected data:
```
assign corrected_data = data ^ correction;
```

The value of the syndrome can be further inspected to signal what action has
been taken. If the syndrome is:

- Equal to zero, no error occurred.
- Has one bit set, then this is a flip of a check bit and can be ignored.
- Has a value matching a pattern (three bits set or two bits in the adjacent positions), a correctable error occurred.
- Has a value not matching a pattern (two bits set in the other non-adjacent positions: `4'b1010`, `4'b0101`), or four bits set, a multi-bit uncorrectable error occurred.

The above SECDED check-bit encoding can be implemented in a similar way, but
since it uses only three-bit patterns, mapping syndromes to correction masks
can be done with three-input AND gates:

```
unique case(syndrome)
  syndrome[0] && syndrome[1] && syndrome[2]: correction = 1<<0;
  syndrome[0] && syndrome[1] && syndrome[3]: correction = 1<<1;
  syndrome[0] && syndrome[2] && syndrome[3]: correction = 1<<2;
  syndrome[1] && syndrome[2] && syndrome[3]: correction = 1<<3;
  syndrome[0] && syndrome[1] && syndrome[4]: correction = 1<<4;
  syndrome[0] && syndrome[2] && syndrome[4]: correction = 1<<5;
  syndrome[1] && syndrome[2] && syndrome[4]: correction = 1<<6;
  syndrome[0] && syndrome[3] && syndrome[4]: correction = 1<<7;
  default:                                   correction = 0;
endcase
```

And any syndromes with one or two bits set are correctable, and otherwise
uncorrectable.


## References / further reading

- [Error correction code](https://en.wikipedia.org/wiki/Error_correction_code), Wikipedia.
- [Hamming code](https://en.wikipedia.org/wiki/Hamming_code), Wikipedia.
- [ECC memory](https://en.wikipedia.org/wiki/ECC_memory), Wikipedia.
- [Error detecting and error correcting codes (PDF)](https://signallake.com/innovation/hamming.pdf),
  R. W. Hamming, in The Bell System Technical Journal, vol. 29, no. 2, pp. 147-160, April 1950.
- [Constructing an Error Correcting Code (PDF)](http://pages.cs.wisc.edu/~david/courses/cs552/S12/handouts/ecc-phelps.pdf),
  Andrew E. Phelps, University of Wisconsin, Madison, November 2006.
