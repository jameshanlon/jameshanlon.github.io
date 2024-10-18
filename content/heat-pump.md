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

I had a Vaillant heat pump installed in my house in July 2022, and a year later
a [Vaillant gateway][gateway], which provides monitoring and logging services
via the 'myVaillant' smartphone app. Since I now have a year's worth of data,
this note reviews what has been logged to see how the system is performing.

[gateway]: https://www.vaillant.co.uk/product-systems/smart-controls/myvaillant-connect-internet-gateway

{{ macros.image('heat-pump/heat-pump.jpg') }}

The heat pump is a 10 kW Vaillant Arotherm plus (pictured above), serving my
house of approximately 90 square meters internal area. I have previously posted
about the building's [energy efficiency](home-thermal-imaging-survey.html) and
[additional first floor
insulation](cornish-unit-house-retrofit-insulation.html) added. This pump's
capacity exceeds the current requirements of the house, but we are planning an
extension in the near future.

In terms of the operation of the heating and hot water system, space heating is
set to run continuously with a fixed temperature of 19 degrees C is set in the
downstairs hallway (a central point in the house), and hot water is set to run
continuously at 50 degrees C. In the first year of running the system, I
experimented with running heating and hot water for set periods during each day
of the week, but I found that the heat pump had to work hard to bring the
system back up to temperature, particularly with the heating during the winter
where the not only is the system heating the water but also the fabric of the
building. I was advised that continuous operation was more efficient and since
the house is almost always occupied, this matched our use. At that point I
hadn't taken a close look at the measured performance and was just ad hoc
monitoring the electricity demand, so it is not to say that running the system
with setback temperatures would not be effective and may better match occupancy
(see analysis in [this Heatgeek article][heatgeek-setback], but having a
continuous temperature is the most comfortable and works well in my case.

[heatgeek-setback]: https://www.heatgeek.com/should-your-heating-be-left-on-all-the-time-or-not

The *myVaillant* app usefully provides a button to download all logged data per
year in a set of CSV files and this code is [available on
Github][home-energy-data]. I have summarised the year period from July 2023 to
July 2024 in the following charts. Having read this [review][pfb-vaillant-app]
by Michael de Podesta of the *myVaillant* app and the quality of the logged
data, I am aware that there are accuracy/quantisation issues. The review
measured a ~8% error in electricity consumed and a ~20% error in the heat
energy produced, as well as pointing out many logged values are quantised to
kWh units, which I also observe in the data. Significantly, this means that the
raw Vaillant data under reports COP. I don't have a point of comparison with
with another way to measuring the consumed and generated energy (although I
would like to install an [OpenEnergyMonitor][OpenEnergyMonitor] to do this). I
hope that Vaillant have improved the reported measurements in the last year,
but even with these errors the data is still useful for a high-level review of
the system.

[home-energy-data]: https://github.com/jameshanlon/home-energy-data
[OpenEnergyMonitor]: https://openenergymonitor.org

# Analysis

The overall performance of the system for the year from July 2023 is summarised in the following table.

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
      <td>Average daily electicity consumption</td>
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

Note that when scaling consumed electricity by 8% and generated electicity by
20%, heating SCOP is 4.06, hot water SCOP is 3.43 and combined at 3.79.

Diving into the data, the first chart below shows the consumption of electrical
energy for heating, hot water and them combined.

{{ macros.imagenothumb('heat-pump/consumed.png',
                       caption="Electrical energy consumed in kWh.") }}

Most obviously, electricity consumption during the winter months increases
significantly when the heat pump is using approximately 10 kWh per day. There
are two spikes in November and January where temperatures went below zero, and
at these times consumption went up close to 30 kWh per day. As expected,
electricity consumption for hot water is more consistent throughout the year
with a lesser increase through the winter months. The short periods where both
drop to zero are due either to a holiday and the system being in 'absence' mode
or a technical issue. Regarding the latter, these have only been due to a loss
of pressure in the system, requiring a manual top up from the mains. The total
electrical energy for heating for the year is 1.35 MWh and 1.04 MWh for hot
water.

The next chart is the heat energy generated, which is tightly correlated with
the consumption graph.

{{ macros.imagenothumb('heat-pump/generated.png',
                       caption="Heat energy generated (hot water and heating) in kWh.") }}

Combining the previous two charts by calculating the ratio between generated and
consumed, gives the coefficient of performance (COP). The average COP in this
period is 3.3 (the red line). The Vaillant app reports 3.4, which may be taking
into account the quiescent periods, which broadly means the system is
functioning well. However, caution is [again advised][pfb-cop] by Michael de
Podesta because of the inaccuracies in the Vaillant data, but noting that he
found that the Vaillant data underestimated COP.

{{ macros.imagenothumb('heat-pump/COP.png',
                       caption="COP calculated by dividing heat generated by electrical energy consumed.") }}

{{ macros.imagenothumb('heat-pump/weekly-COP.png',
                       caption="COP calculated by dividing heat generated by electrical energy consumed.") }}

{{ macros.imagenothumb('heat-pump/heat-output-vs-COP.png',
                       caption="") }}

The following chart shows the temperature of the contents of the hot water
tank. As expected, this stays constant, with a few exceptions: when I changed
the temperature from 45 to 50 degrees C in October 2023; when the system has
been off or out of order; and when every week on a Monday the immersion heater
kicks in to perform a Legionella purge (which curiously it has stopped since
March 2024, something I need to investigate).

{{ macros.imagenothumb('heat-pump/water-temperature.png',
                       caption="Hot water temperature in degrees Celsius.") }}

Finally, we have a plot of internal (red) vs external (blue) temperature in
degrees C. This clearly shows that the 19 degrees C target was maintained
throughout the year, notwithstanding the periods of absence/downtime and on
particular hot days when the temperature rose above the target. Given how
quickly our summers are changing in terms of heat waves, having a system that
can also perform cooling would be a big benefit. I think this chart represents
well the benefit of having a heat pump, and a home with a continuous temperature
throughout the year.


{{ macros.imagenothumb('heat-pump/internal-external-temperature.png',
                       caption="Internal and external temperatures in degrees Celsius.") }}

For the same period I obtained the electricity use and cost data from Octopus
using their excellent API via the [Octograph tool][octograph], visualised below
on a Grafana dashboard. According to the Vaillant data, the heat pump used 2.39
MWh of energy, which is only 32% of the total electricity use. I am suspicious
that this is incorrect, even factoring in a 10% underestimate from the Vaillant
system. I would expect the heat pump to be using more like 50-60% of total
electricity on average, given that other electricity use is cooking and
appliances etc. Otherwise the usage profile matches between the two
data sets.

{{ macros.imagenothumb('heat-pump/Grafana-Octopus-electricity-use.png',
                       caption="Electricity use from Octopus data.") }}

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
