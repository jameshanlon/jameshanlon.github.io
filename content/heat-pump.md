---
Title: Review of heat pump use and performance
Date: 2024-07-01
Category: non-technical
Tags: sustainability
Summary: A review of one year's worth of data from my home heat pump.
Status: published
---

{% import 'post-macros.html' as macros %}

After having had a [Valiant gateway][gateway] fitted to my heat pump
installation in July last year (2023, a year after it was installed), I wanted
to review the data it has logged in that time to see how it is performing.

[gateway]: https://www.vaillant.co.uk/product-systems/smart-controls/myvaillant-connect-internet-gateway

{{ macros.image('heat-pump/heat-pump.jpg') }}
{{ macros.imagenothumb('heat-pump/COP.png') }}
{{ macros.imagenothumb('heat-pump/consumed.png') }}
{{ macros.imagenothumb('heat-pump/generated.png') }}
{{ macros.imagenothumb('heat-pump/water-temperature.png') }}
{{ macros.imagenothumb('heat-pump/internal-external-temperature.png') }}
{{ macros.imagenothumb('heat-pump/Grafana-Octopus-electricity-use.png') }}

## References

- [Protons for Breakfast, articles about heat
  pumps](https://protonsforbreakfast.wordpress.com/heat-pump-articles/) is a
  fantasitic set of articles by physicist Michael de Podesta.
- [Energy Stats](https://energy-stats.uk) provides pricing data for various
  Octopus Energy tarrifs.
- [Guy Lipman's Octopus Energy resources](https://www.guylipman.com/octopus) is
  a collection of notes focusing on using the Octopus API to access energy
  data.
- [Octopus Energy API](https://octopus.energy/blog/agile-smart-home-diy) is the
  landing page for using their API.
