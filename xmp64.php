<? include "header.php"?>

<div class="column">

<h1>The XMOS XMP-64</h1>

<p>The XMP-64 was an experimental board developed by XMOS in 2009 to demonstrate
the scalablility of the XS1 architecture. Since details of the XMP-64 are no
longer available from XMOS, I've created this page to record them for reference
and anyone who may be interested in the future.</p>

<p>The XMP-64 was an interesting device. It consisted of a four-by-four grid of
XS1-G4 chips, each with four cores and eight hardware threads per core. The
chips themselves were connected in a hypercube topology. Each core had 64 KB of
memory and ran at 400 MHz. The whole array therefore provided 512 threads,
4&nbsp;MB of memory and a peak performance of 25.6 GIPS. There are many more
details in the performance experiment document linked below.</p>

<p>Because the XMP-64 was not competative with contemporary devices in terms of
compute performance, few were built or sold. It was however a great
demonstration of a highly parallel, yet simple to program, system and
fascinating to experiment with!</p>

<a href="./images/xmp64/xmp64-1.JPG">
<img src="thumb.php?src=./images/xmp64/xmp64-1.JPG&size=220x" /></a>
<a href="./images/xmp64/xmp64-2.JPG">
<img src="thumb.php?src=./images/xmp64/xmp64-2.JPG&size=220x" /></a>
<a href="./images/xmp64/xmp64-3.JPG">
<img src="thumb.php?src=./images/xmp64/xmp64-3.JPG&size=220x" /></a>
<a href="./images/xmp64/xmp64-4.JPG">
<img src="thumb.php?src=./images/xmp64/xmp64-4.JPG&size=220x" /></a>
<a href="./images/xmp64/xmp64-5.JPG">
<img src="thumb.php?src=./images/xmp64/xmp64-5.JPG&size=220x" /></a>
<a href="./images/xmp64/xmp64-6.JPG">
<img src="thumb.php?src=./images/xmp64/xmp64-6.JPG&size=220x" /></a>

<h2>Links</h2>

<ul>

<li><a href="docs/xmp64experiments.pdf">
XMP-64 performance experiments</a> (PDF), 2010.
(<a href="files/xmp64experiments.zip">source code archive</a>)</li>

<li><a href="https://github.com/xcore/proj_xmp64">Example programs and PCB design
files</a>
(GitHub).</li>

</ul>

</div>

<? include "footer.php"?>

