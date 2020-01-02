---
Title: RGB lightbox stacks
Date: 2018-12-30
Category: projects
Tags: making, lighting, electronics
Status: published
---

{% import 'post-macros.html' as macros %}

{{ macros.image('RGB-stacks/completed-boxes-3.jpg', size='800x800') }}

The 'RGB stacks' lightboxes are an experiment with using high-power LEDs,
generous volumes and translucent acrylic plastic to create big blocks of
colour. They are constructed from 12 mm birch ply and each pixel measures 300 x
300 (outer dimensions). They are built as three columns of three pixels to
allow them to be arranged in a square, a line, or in different locations. This
note records some of the details of their construction. Although they are now
functional, refinement of their controls and modulation continues to be a work
in progress. This note records some of the details of how they were built (I
will it updated with any new developments).

The project was inspired by a similar light box project (that unfortunately I
can no longer find on the internet), but which was a single 3 x 3 cabinet
achieving a similar block-colour effect. My motivation was to build something
similar but that could also be used as subtle/ambient lighting, making use of
the amazing colours and ability to accurately modulate LEDs to create smooth
transitions between rich colours and interesting combinations.

{{ macros.pair_layout(
     macros.image('RGB-stacks/colour-experiment-blue.jpg'),
     macros.image('RGB-stacks/colour-experiment-red.jpg'),
     caption='An early experiment to see how the LED light diffuses through the acrylic in a plywood volume.' )}}

Construction of the stacks was straightforward: all panel dimensions are
multiples of 300 and all joints biscuited and glued to avoid any visible
fixings. (I unfortunately don't have any pictures of the construction of the
stacks.)

{{ macros.triple_layout(
     macros.image('RGB-stacks/bead-detail-1.jpg'),
     macros.image('RGB-stacks/bead-detail-2.jpg'),
     macros.image('RGB-stacks/tape.jpg'),
     caption='Detail of the lip added to seat the acrylic panels and the narrow double-sided tape to fix them in place.') }}

The acrylic panels were cut to fit the inner box dimensions exactly, but with
small variations in the dimensions of the boxes. Getting them all to fit was a
long process of sanding down each one to fit a particular opening. A secure fit
of the panels was achieved with tight tolerances and narrow double-sided sticky
tape (pictured above right).

{{ macros.image('RGB-stacks/completed-boxes-1.jpg',
          caption='The boxes with all acrylic panels in place.') }}

Pairs of white and RGB LEDs were mounted on aluminium bar in each pixel. The
LED were fixed in place with small bolts. I made small plastic washers to avoid
shorting any of the contacts with the bolt heads. Although the aluminium bar
probably provides a sufficient heat sink, I added additional heatsink blocks on
the rear side, fixed with thermal glue (these were cut up from larger IC
heatsinks). All of the LED wiring was conveniently done with CAT6 cable, using
all of the eight cores to wire the four channels. Each channel draws about
1 W at 5 V (200 mA), which is within the specification of the CAT6.

{{ macros.pair_layout(
     macros.image('RGB-stacks/led-bar-2.jpg'),
     macros.image('RGB-stacks/led-heatsinks.jpg'),
     caption='The system used to mount the LEDs in the middle of each box.')}}

{{ macros.pair_layout(
     macros.image('RGB-stacks/skeleton-boxes-with-leds.jpg'),
     macros.image('RGB-stacks/boxes-in-workshop.jpg'),
     caption='The boxes with all of the LEDs and their cabling installed.') }}

Each box has a rear plug panel. The central box acts as a master and has
connections for power, Ethernet, and provides serial data and power to the
other outer boxes.

{{ macros.triple_layout(
     macros.image('RGB-stacks/power-supply.jpg'),
     macros.image('RGB-stacks/plug-panel.jpg'),
     macros.image('RGB-stacks/slave-box-control-boards.jpg'),
     caption='The master and slave plug panels for each stack.') }}

The inter-box wiring uses 5-pin XLR sockets, to carry power, ground and the
differential pair for the serial signal. The wires were made with a dual-core
power wire (sufficient to carry the required power at 5V) with a another
dual-core wire for the serial, wrapped in a heatshrink coat.

{{ macros.image('RGB-stacks/cables.jpg',
                caption='Custom cabling to connect the left and right hand boxes, containing a dual-core wire for power and two CAT-6 cores for serial data.') }}

The electronics for the LED drivers is described in a [separate
note]({filename}/led-driver.md). Each of the LED driver boards has three
outputs, so four boards are required to drive a single stack. The Raspberry Pi
microcontroller is used to control all the pixels, and does so with a dual-wire
RS-485 serial bus. This bus connects each of the driver boards in series, and
the outer boxes are wired in parallel. Despite some concerns about this
topology from notes on the MAX-485 driver IC datasheet and that I didn't use
terminating resistors, the arrangement performs fine.

So that I could easily access the electronics, I integrated the drivers and
their wiring on a plywood board that sits in the base of a stack. The master
stack has the power supply, taking mains voltage and providing 5V up to 60W
(12A) for the three stacks. See the table below for calculated power of the
LEDs only. Note that the power supply does not output enough power do drive
the boxes comfortably (80W would be more comfortable).

<table class="table table-sm">
  <thead>
    <tr>
      <th scope="col">Channel</th>
      <th scope="col">Voltage (V)</th>
      <th scope="col">Current (A)</th>
      <th scope="col">LED power (W)</th>
      <th scope="col">Driver efficiency</th>
      <th scope="col">Driver power (W)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Red</td>
      <td>2.4</td>
      <td>0.3</td>
      <td>0.72</td>
      <td>0.48</td>
      <td>1.5</td>
    </tr>
    <tr>
      <td>Green</td>
      <td>3.4</td>
      <td>0.3</td>
      <td>1.02</td>
      <td>0.68</td>
      <td>1.5</td>
    </tr>
    <tr>
      <td>Blue</td>
      <td>3.5</td>
      <td>0.3</td>
      <td>1.05</td>
      <td>0.7</td>
      <td>1.5</td>
    </tr>
    <tr>
      <td>White</td>
      <td>3.2</td>
      <td>0.3</td>
      <td>0.96</td>
      <td>0.64</td>
      <td>1.5</td>
    </tr>
    <tr>
      <td>Total (per pixel)</td>
      <td>-</td>
      <td>-</td>
      <td>3.75</td>
      <td>-</td>
      <td>6</td>
    </tr>
    <tr>
      <td>Total (per stack)</td>
      <td>-</td>
      <td>-</td>
      <td>11.25</td>
      <td>-</td>
      <td>18</td>
    </tr>
    <tr>
      <td>Total</td>
      <td>-</td>
      <td>-</td>
      <td>33.75</td>
      <td>-</td>
      <td>54</td>
    </tr>
  </tbody>
</table>

To check the above power numbers I performed some measurments with a clamp
meter of the central stack:

- With all LEDs off, the quiesence current is 360 mA at 5 V, dissipating 1.8 W.
- With all LEDs on at full intensity, the current is 4.75 A at 5 V, dissipating
  23.75 W.

These numbers are slightly higher than expected, due to the LED driver current
ranging between 0.357 mA (blue) and 0.370 mA (green).

{{ macros.triple_layout(
     macros.image('RGB-stacks/control-board-and-psu.jpg'),
     macros.image('RGB-stacks/control-board-1.jpg'),
     macros.image('RGB-stacks/one-stack-test-with-board.jpg'),
     caption='Integration of the electronics into the master stack (similar for the outer stacks).') }}

The back panels fasten with M8 bolts into T-nuts.

{{ macros.pair_layout(
     macros.image('RGB-stacks/back-panels.jpg',
                  caption='Details of the back plates, fastened by M8 Allen key bolts.'),
     macros.image('RGB-stacks/completed-boxes-2.jpg',
                  caption='The boxes in a complete state'),
     caption='') }}

It's hard to capture the quality of the effect of the light boxes on camera.
The images below are two early tests: left just using a lamp in one of the
pixels, right with no blending of the RGB channels.

{{ macros.pair_layout(
     macros.image('RGB-stacks/one-cell-illuminated.jpg',
                  caption='Seeing the effect of the acrylic diffusion with just a lamp in one of the cells.'),
     macros.image('RGB-stacks/rgb-test.jpg',
                  caption='The first RGB test of a stack.'),
     caption='') }}

The behaviour of the boxes is determined by the PIC programs and the Raspberry
Pi. Since changes to the PIC program requires each of the boards to be
programmed individually and for each program to be compiled with a unique
identifier, this is not an easy way to experiment with modulating schemes.
Instead, each PIC is programmed only to change the output intensity, and
experimentation can be done using Python on the Raspberry Pi over SSH. In these
scheme, updates are sent to the LED drivers synchronously, as a frame. At
115,200 bps baud rate over RS485, this is sufficient to deliver up to 389
updates per second. In practice there are overheads that will reduce this. If,
for smooth graduations between colours the frame rate was not adequate, an
optimisation could be to expand the capability of the PIC driver code to
perform more complex actions like sweeps over intensity ranges, thereby
reducing the number of updates required.

As I mentioned, these boxes are not yet complete. To finish them, I want to add
a button panel to switch them on off and control the lighting patterns.
