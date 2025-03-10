---
Title: Review of heat pump use and performance
Date: 2024-07-31
Category: non-technical
Tags: sustainability
Summary: A review of one year's worth of data from my home heat pump.
Status: published
---

{% import 'post-macros.html' as macros %}

> **_NOTE:_**  Updated October 2024 with improved charts.

{{ macros.imagenothumb('heat-pump/heat-pump-cropped.jpg', caption="My 10kW Vaillant Arotherm
Plus.") }}

I had a 10 kW Vaillant Arotherm heat pump installed in July 2022, and a year
later a [Vaillant Sensonet gateway][gateway], which provides monitoring and
logging services via the 'myVaillant' smartphone app. Since I now have a year's
worth of data, this note reviews what has been logged to see how the system is
performing.

[gateway]: https://www.vaillant.co.uk/product-systems/smart-controls/myvaillant-connect-internet-gateway

The heat pump serves my house of approximately 90 square meters internal area.
I have previously posted about the building's [energy
efficiency](home-thermal-imaging-survey.html) and [additional first floor
insulation](cornish-unit-house-retrofit-insulation.html) added. This pump's
capacity exceeds the current requirements of the house, but we are planning an
extension in the near future.

## System operation

The way I run the system is for space heating to run continuously with a fixed
temperature of 19 degrees C is set in the downstairs hallway (a central point
in the house), and hot water to run continuously at 50 degrees C. In the first
year of running the system, I experimented with running heating and hot water
for set periods during each day of the week, but I found that the heat pump had
to work hard to bring the system and the fabric of the house back up to
temperature.

I was advised that continuous operation was more efficient and since the house
is almost always occupied, this matched our use. At that point I hadn't taken a
close look at the measured performance and was just monitoring the electricity
demand ad hoc. It is not to say that running the system with setback
temperatures would not be effective and may better match occupancy: see
analysis from [Heatgeek][heatgeek-setback] or [Protons for
Breakfast][pfb-setback] on this subject, But for me, having a continuous
temperature is the most comfortable and seems to work well.

[heatgeek-setback]: https://www.heatgeek.com/should-your-heating-be-left-on-all-the-time-or-not
[pfb-setback]: https://protonsforbreakfast.wordpress.com/2022/12/19/setback-should-you-lower-heating-overnight

## The *myViallant* app

The *myVaillant* app usefully provides a button to download all logged data per
year in a set of CSV files and this code is [available on
Github][home-energy-data]. I have summarised the year period from July 2023 to
July 2024 in the following charts. Having read this [PFB review][pfb-vaillant-app],
I am aware that there are issues with the quality of the logged data.
The review measured a ~8% error in electricity consumed and a ~20% error in the heat
energy produced, as well as pointing out many logged values are quantised to
kWh units, which I also observe in my data. Significantly, this means that the
raw Vaillant data under reports COP. I don't have a point of comparison with
with an alternative measurement of the consumed and generated energy (although I
would like to install an [OpenEnergyMonitor][OpenEnergyMonitor] to do this).
Despite the potential inaccuracies of the Vaillant data, it remains useful for
a high-level review of the system.

[home-energy-data]: https://github.com/jameshanlon/home-energy-data
[OpenEnergyMonitor]: https://openenergymonitor.org

## Analysis

The overall performance of the system for the year from July 2023 to July 2024
is summarised in the following table.

<table class="table">
  <thead>
    <tr>
      <th scope="col">Metric</th>
      <th scope="col">Value</th>
    </tr>
  </thead>
 <tbody>
    <tr>
      <td>Consumed electricity heating</td>
      <td>1.34 MWh</td>
    </tr>
    <tr>
      <td>Consumed electricity hot water</td>
      <td>1.01 MWh</td>
    </tr>
    <tr>
      <td>Total consumed electricity</td>
      <td>2.36 MWh</td>
    </tr>
    <tr>
      <td>Average daily electricity consumption</td>
      <td>6.65 kWh</td>
    </tr>
    <tr>
      <td>Heat generated heating</td>
      <td>4.91 MWh</td>
    </tr>
    <tr>
      <td>Heat generated hot water</td>
      <td>3.13 MWh</td>
    </tr>
    <tr>
      <td>Total heat generated</td>
      <td>8.04 MWh</td>
    </tr>
    <tr>
      <td>Heating SCOP</td>
      <td>3.65</td>
    </tr>
    <tr>
      <td>Hot water SCOP</td>
      <td>3.09</td>
    </tr>
    <tr>
      <td>Total SCOP</td>
      <td>3.41</td>
    </tr>
  </tbody>
</table>

Note that when scaling consumed electricity by 8% and generated electricity by
20% to adjust for possible inaccuracy, heating SCOP is 4.06, hot water SCOP is
3.43 and they are combined at 3.79. Note also, that these figures do not include
the electricity used for the weekly Legionella purge performed by an immersion
heater I have installed in my system.

Looking more closely at consumption, the chart below shows all measurements
over this period for heating, hot water and their combination.

{{ macros.imagenothumb('heat-pump/consumed.png',
                       caption="Electrical energy consumed in kWh.") }}

Most obviously, electricity consumption during the winter months increases
significantly when the heat pump is using approximately 10 kWh per day. There
are two spikes in November and January where temperatures went below zero, and
at these times consumption went up close to 30 kWh per day. As expected,
electricity consumption for hot water is more consistent throughout the year
with a lesser increase through the winter months. The short periods where both
drop to zero are due either to a holiday and the system being in 'absence' mode
or a technical issue. The technical issue has been due to a loss of pressure in
the system, requiring a manual top up from the mains water supply.

The next chart is the heat energy generated, which is tightly correlated with
the consumption graph.

{{ macros.imagenothumb('heat-pump/generated.png',
                       caption="Heat energy generated (hot water and heating) in kWh.") }}

Combining the previous two charts by calculating the ratio between generated and
consumed, gives the coefficient of performance (COP). A handful of measurements
produced very large COP values, that are unrealistic, so I have clipped these
with a maximum COP of 6.

{{ macros.imagenothumb('heat-pump/COP.png',
                       caption="COP calculated by dividing heat generated by electrical energy consumed.") }}

This is the same COP data averaged over weekly intervals.

{{ macros.imagenothumb('heat-pump/weekly-COP.png',
                       caption="Weekly averaged COP.") }}

The next chart is a different presentation of the COP data, with COP plotted as
a function of heat output. It's clear that peak COP is at ~10 kW heat output,
but there is little penalty in efficiency between that and the highest recorded
output.

{{ macros.imagenothumb('heat-pump/heat-output-vs-COP.png',
                       caption="Heat output versus weekly averaged COP.") }}

Looking at the temperature of the hot water tank, this stays constant as expected
but with a few exceptions: when I changed the temperature from 45 to 50 degrees C
in October 2023; when the system has been off or out of order; and when every week
on a Monday the immersion heater kicks in to perform a Legionella purge (which
curiously it has stopped since March 2024. After later investigation this
appears to be a faulty timer or immersion heater, so I switched to performing
the purge using the heat pump itself).

{{ macros.imagenothumb('heat-pump/water-temperature.png',
                       caption="Hot water temperature in degrees Celsius.") }}

Finally, we have a plot of internal (red) vs external (blue) temperature in
degrees C. This clearly shows that the 19 degrees C target was maintained
throughout the year, notwithstanding the periods of absence/downtime and on
particular hot days when the temperature rose above the target. Given how
quickly our summers are changing with more intense heat, having a system that
can also perform cooling would be a big benefit. But overall, I think this
chart well represents the benefit of having a heat pump, providing a home
environment with a continuous temperature throughout the year.

{{ macros.imagenothumb('heat-pump/internal-external-temperature.png',
                       caption="Internal and external temperatures in degrees Celsius.") }}

For the same period I obtained the electricity use and cost data from Octopus
using their excellent API via the [Octograph tool][octograph], visualised below
on a Grafana dashboard. According to the Vaillant data, the heat pump used 2.39
MWh of energy, which is only 32% of the total electricity use. I am suspicious
that this is inaccurate, even factoring in an 8% underestimate from the Vaillant
measurements. I would expect the heat pump to be using more like half of total
electricity on average, given that other electricity use is cooking and
appliances etc, but perhaps I am wrong. Otherwise the usage profile matches between
the two data sets.

{{ macros.imagenothumb('heat-pump/Grafana-Octopus-electricity-use.png',
                       caption="Electricity use from Octopus data.") }}

## Summary

The data collected by the Vaillant heat pump control system appears to be
somewhat inaccurate but nevertheless provides a high-level overview of the
performance of the system. I've been very pleased with how it has performed
over the last year, and this is backed up by the statistics I have collated.
With work planned on the house, there are more thermal-efficiency gains to be
made, so hopefully I can further improve it's running efficiency.


[pfb-vaillant-app]: https://protonsforbreakfast.wordpress.com/2023/02/06/the-myvaillant-app-a-review
[pfb-vaillant-arotherm]: https://protonsforbreakfast.wordpress.com/2022/10/19/vaillant-arotherm-plus-heat-pump-the-good-the-bad-and-the-ugly
[pfb-cop]: https://protonsforbreakfast.wordpress.com/2024/03/13/can-i-believe-my-vaillant-heat-pump-cop
[octograph]: https://github.com/Yanson/octograph

## References and further reading

- [Protons for Breakfast, articles about heat
  pumps](https://protonsforbreakfast.wordpress.com/heat-pump-articles/) is a
  fantastic set of articles by physicist Michael de Podesta.
- [Energy Stats](https://energy-stats.uk) provides pricing data for various
  Octopus Energy tariffs.
- [Guy Lipman's Octopus Energy resources](https://www.guylipman.com/octopus) is
  a collection of notes focusing on using the Octopus API to access energy
  data.
- [Octopus Energy API](https://octopus.energy/blog/agile-smart-home-diy) is the
  landing page for using their API.
- [Octograph (Github)](https://github.com/Yanson/octograph) A Python tool for
  extracting Octopus Energy meter readings to InfluxDB and Grafana.
