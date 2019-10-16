---
Title: Three-channel high-power LED driver
Date: 2018-12-31
Category: projects
Tags: electronics
Status: published
---

<div class="float-right">
<a href="{{'LED-driver/board-layers.png'|asset}}" data-lightbox="led-driver">
  <img class="thumbnail rounded" src="{{'LED-driver/board-layers.png'|thumbnail('400x400')}}">
</a>
</div>

This note describes an LED driver I designed for a lighting project. I decided
on a custom solution because I couldn't find any suitable boards available to
buy at a reasonable price. The intended application (which I will describe in
another note) requires 12 high-power (~1W) LEDs to be driven individually a 3 by 3
grid measuring approximately 1 metre square, with each of the nine cell
containing a red, green, blue and white LED.

I embarked on this project without any experience of designing PCBs, and with
relatively little knowledge of electronics, so it was a steep but fantastic
learning experience. I wanted to record some of the details of this project for
others who may find them useful, as I did with some of the resources I've
linked to at the end. All of the PCB design files and processor firmware are
[available on GitHub](https://github.com/jameshanlon/3C-HP-LED-driver).

# Design

The board is designed around the following main IC components:

- Microchip PIC12F1572 for PWM LED control and serial communication. This was
  the simplest PIC I could find that had multiple PWM outputs and UART serial
communication capability. It's an 8-bit device with 16-bit PWMs and 3.5 KBs of
program memory.

- Maxim MAX485 for communication to multiple of these boards. This IC provides
  half-duplex communication over a 2-wire differential pair using the RS485
protocol, allowing communication over long distances. Importantly it supports
multiple drops, so a number of boards can be wired together with a bus. I chose
this as it is very simple to integrate, with no additional components required,
compared to the capacitors necessary for the MAX232. Talking to the PIC, this
can support a baud rate of 115,200 bps.

- ON Semiconductor CAT4101 for driving LEDs with a constant-current up to 1A
with PWM control. Because the temperature fluctuations of high-power LEDs
affects their forward voltage, driving them with a constant current is
important to avoid damage due to over voltage. These chips neatly integrate
this with the PWM control ability. Their only downsides were their cost (~£2
each - with 36 of them needed for my lighting project, they were the greatest
single expense) and package which isn't designed to be hand soldered.

Other features:

- Header for in-circuit PIC programming. To disconnect the UART pins (required
  for programming) and to attach a 10K pull up resistor, I included three
  jumper headers. However, I found connecting the pull up wasn't necessary for
  programming.

- Screw terminals for all installation connections.

- Indicator LEDs for UART TX and RX directions, and power.

I designed the PCB using the excellent [KiCAD](http://kicad-pcb.org/) and had
it manufactured very cheaply by [Seeed Studio](https://www.seeedstudio.com/fusion_pcb.html)
in Shenzhen, China.

Here's the schematic:

<div class="text-center">
  <a href="{{'LED-driver/schematic.png'|asset}}" data-lightbox="led-driver">
    <img class="rounded" src="{{'LED-driver/schematic.png'|thumbnail('800x800')}}">
  </a>
</div>

# Parts list

| Quantity | Package | Description                     |
| -------- | ------- | --------------------------------|
| 3        | TO-263  | CAT4101 LED drivers 5.5V        |
| 1        | DIP-8   | PIC12F1572 microcontroller      |
| 1        | DIP-8   | MAX485 serial interface         |
| 3        | 0805    | Green LEDs                      |
| 3        | 0805    | Resistor 10K                    |
| 3        | 0805    | Resistor 1.4K                   |
| 3        | 0805    | Resistor 510                    |
| 5        | 0805    | Capacitor 0.1 uF                |
| 3        | SOT-23  | 2N7002 N-channel MOSFET 300 mA  |
| 4        | -       | 2 way 5mm pitch terminal blocks |
| 1        | -       | 3 way 5mm pitch terminal blocks |
| 12       | -       | 2.54mm pitch pin headers        |
| 3        | -       | 2.54mm pin header jumper caps   |

<p></p><!--Add some space after the table-->

The CAT4101 sense resistors are chosen to give a constant current of 300 mA.

For reference, I have assumed the following parameters of the LEDs I
used (you should however check the datasheet for a particular LED):

| Colour  | Typical forward voltage (@ 350 mA) | Part                                     |                |
|---------|------------------------------------|------------------------------------------|----------------|
| Red     | 2.4                                | 3W RGB module                            | [Datasheet][1] |
| Green   | 3.4                                | 3W RGB module                            | [Datasheet][1] |
| Blue    | 3.5                                | 3W RGB module                            | [Datasheet][1] |
| White   | 2.8-3.4                            | 1W Ice White LED (Bridgelux 9000-15000k) | [Datasheet][2] |

[1]: https://www.sparkfun.com/datasheets/Components/LED/COM-08718-datasheet.pdf
[2]: https://futureeden.co.uk/collections/ice-white-bridgelux-power-led-9000-15000k/products/1w-ice-white-led-bridgelux-12000k-with-pcb

<p></p><!--Add some space after the table-->

# Programming

The intention of the PIC microcontrollers is to react to a simple set of
commands sent via the serial interface. In deployment, an array of these driver
boards would be controlled by another processor broadcasting on the RS485 bus.
I used a Raspberry Pi with an RS485 shield to do this.

At a minimum, the PICs need to set the intensity of each LED they control,
which is the current operation of the firmware. They could however be triggered
to perform more complex modulations. This would reduce the data transmission
requirements on the RS485 bus, potentially improving the quality of animations
produced by an array.

The PIC microcontrollers are programmed in C, which I did using Microchip's XC
compiler and MPLab IDE software. In order that each board can uniquely identify
it's control data, they are compiled with a unique ID. With a deployment of 12
boards, firmware updates are a little arduous, particularly since the two
jumpers need to be removed as well.

I found that an efficient communication protocol between an array of boards
and the main controller (Raspberry Pi) is a sequence of bytes with the first
uniquely determining the header and the following 36 determining the intensity
of each of the individual LEDs. Each board uses its ID to choose three values
in the payload. At 115,200 bps, this in theory allows up to 1,107 commands to
be sent per second. Note that the boards do not send an acknowledgement, since
this significantly reduces the throughput. In Python a packet can be sent with
([snippet from here](https://github.com/jameshanlon/rgb-stacks/blob/master/rgbstacks.py)):

```
def set_colour(payload):
    assert len(payload) == (3*12)
    usart.write(bytearray([chr(255)]+payload))
    usart.flush()
```

The PICs receive UART data and set the output PWMs thus
([snippet from here](https://github.com/jameshanlon/rgb-stacks/blob/master/PIC/main.c)):

```
...
// Reset if we see the start of packet marker.
if (RCREGbits.RCREG == START_PACKET) {
  uart_count = 0;
} else {
  // Packet payload.
  uart_data[uart_count++] = RCREGbits.RCREG;
  // When we've received the payload, update PWMs and setup for next packet.
  if (uart_count == PAYLOAD_SIZE) {
    // Set the duty cycles, scale an 8-bit range into 16 bits.
    PWM1DC = uart_data[DRIVER_OFFSET+0] * 256;
    PWM2DC = uart_data[DRIVER_OFFSET+1] * 256;
    PWM3DC = uart_data[DRIVER_OFFSET+2] * 256;
    // Reload the PWMs.
    PWM1LD = 1;
    PWM2LD = 1;
    PWM3LD = 1;
    uart_count = 0;
  }
}
...
```

# Pictures

<div class="text-center">
  <a href="{{'LED-driver/unpopulated-boards.jpg'|asset}}" data-lightbox="led-driver">
    <img class="thumbnail rounded" src="{{'LED-driver/unpopulated-boards.jpg'|thumbnail('320x320')}}">
  </a>
  <a href="{{'LED-driver/assembled-1.jpg'|asset}}" data-lightbox="led-driver">
    <img class="thumbnail rounded" src="{{'LED-driver/assembled-1.jpg'|thumbnail('320x320')}}">
  </a>
  <a href="{{'LED-driver/assembled-2.jpg'|asset}}" data-lightbox="led-driver">
    <img class="thumbnail rounded" src="{{'LED-driver/assembled-2.jpg'|thumbnail('320x320')}}">
  </a>
  <a href="{{'LED-driver/assembled-programmer.jpg'|asset}}" data-lightbox="led-driver">
    <img class="thumbnail rounded" src="{{'LED-driver/assembled-programmer.jpg'|thumbnail('320x320')}}">
  </a>
  <a href="{{'LED-driver/assembled-top.jpg'|asset}}" data-lightbox="led-driver">
    <img class="thumbnail rounded" src="{{'LED-driver/assembled-top.jpg'|thumbnail('320x320')}}">
  </a>
  <a href="{{'LED-driver/array-1.jpg'|asset}}" data-lightbox="led-driver">
    <img class="thumbnail rounded" src="{{'LED-driver/array-1.jpg'|thumbnail('320x320')}}">
  </a>
  <a href="{{'LED-driver/array-2.jpg'|asset}}" data-lightbox="led-driver">
    <img class="thumbnail rounded" src="{{'LED-driver/array-2.jpg'|thumbnail('320x320')}}">
  </a>
  <a href="{{'LED-driver/4up-1.jpg'|asset}}" data-lightbox="led-driver">
    <img class="thumbnail rounded" src="{{'LED-driver/4up-1.jpg'|thumbnail('320x320')}}">
  </a>
  <a href="{{'LED-driver/4up-2.jpg'|asset}}" data-lightbox="led-driver">
    <img class="thumbnail rounded" src="{{'LED-driver/4up-2.jpg'|thumbnail('320x320')}}">
  </a>
  <a href="{{'LED-driver/8up.jpg'|asset}}" data-lightbox="led-driver">
    <img class="thumbnail rounded" src="{{'LED-driver/8up.jpg'|thumbnail('320x320')}}">
  </a>
</div>

# Improvements

- Remove the 10K pull up resistor for programming the PIC since it is
  unnecessary.
- Update the defunct silk screen URL to my new jameswhanlon.com domain.

# References

- [Board design and microcontroller source code on GitHub](https://github.com/jameshanlon/3C-HP-LED-driver)
- [RGBW LED Controller v3.1 (The Custom Geek)](http://thecustomgeek.com/2013/12/28/rgbw31/).
- [Make an RGB lighting controller (Bigclivedotcom)](http://www.bigclive.com/newrgb.htm)
- [Easy CAT4101 LED Driver (Instructables)](https://www.instructables.com/id/Easy-CAT4101-LED-Driver/)
- [High power LED driver circuits (Instructables)](https://www.instructables.com/id/Circuits-for-using-High-Power-LED-s/)
- [Power LED's - Simplest Light With Constant-current Circuit (Instructables)](https://www.instructables.com/id/Power-LED-s---simplest-light-with-constant-current/)
