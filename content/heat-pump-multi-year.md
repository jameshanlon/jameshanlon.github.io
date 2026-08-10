---
Title: Heat pump performance after three years of monitoring
Date: 2026-08-10
Category: Home and Sustainability
Tags: sustainability, energy-efficiency
Summary: Revisiting my Vaillant Arotherm heat pump with several heating seasons
         of logged data, looking at year-on-year efficiency and what changed to
         the house in between.
Status: draft
---

{% import 'post-macros.html' as macros %}

<!--
SKELETON — outline only. Set `Status: published` and update `Date:` when written.

This is the follow-up to "Review of heat pump use and performance" (2024-07-31,
content/heat-pump.md), which covered the single year July 2023 to July 2024.
Link the two in both directions: add a pointer at the top of heat-pump.md when
this is published, in the same style as the existing October 2024 update note.

CHECK BEFORE WRITING — the title above says "three years" deliberately:
- The pump was installed July 2022, so it has been running four years.
- The Sensonet gateway was added a year later, so *logged* data starts ~July 2023.
That gives four years of operation but only three of measurements. Decide which
number the note leads with and be explicit about the distinction early on, or
the year-on-year comparison will read as though a year is missing.
-->

<!--
INTRO
- One paragraph recapping the system for a reader arriving cold: 10 kW Vaillant
  Arotherm Plus, ~90 m2 house, continuous operation at 19 C, hot water at 50 C.
  Keep it to a few sentences and link to the 2024 note for the full setup.
- What is new since then: more heating seasons, and any changes to the house or
  the way the system is run.
- State what question the note answers. The interesting one is not "is it
  efficient" — the first note answered that — but "does it hold up, and what
  moved the number".
-->

## What has changed since 2024

<!--
- The extension: the 2024 note said work was planned and that the pump was
  oversized for the house as it then stood. Did it happen? A larger heated
  volume against the same 10 kW unit is the single most interesting variable
  here, and it is the thing no other heat pump write-up will have.
- Any fabric changes (insulation, glazing) that alter heat loss.
- Any changes to how the system is run: flow temperature, weather compensation,
  setback experiments, hot water schedule, Legionella cycle.
- Tariff changes, if they affect the running-cost section below.
-->

## Year-on-year performance

<!--
- The 2024 note used a single summary table (consumed electricity, heat
  generated, SCOP, split heating vs hot water). Reuse exactly those metrics with
  a column per year so the numbers are directly comparable — same definitions,
  same source, no redefinition mid-series.
- Baseline to compare against, from the 2023-24 year:
    heating SCOP 3.65, hot water SCOP 3.09, total SCOP 3.41,
    total consumed 2.36 MWh, total heat generated 8.04 MWh.
- Carry forward the same caveat about meter accuracy (the +8% / +20% adjustment)
  and apply it consistently across all years, or state that you have stopped
  adjusting and why.
-->

<!--
TABLE — one row per metric, one column per year. Same row order as the 2024 note.
-->

## Weather normalisation

<!--
- Raw year-on-year comparison is confounded by how cold each winter was. Without
  correcting for it the comparison says little. Degree-days for Bristol are the
  usual approach.
- This is the section that makes the note more than an updated table, and it is
  the part the 2024 note could not do with only one year.
- If the extension happened, heat loss changed too, so normalise for weather and
  discuss the floor-area change separately rather than trying to fold both into
  one number.
-->

## Degradation, or the absence of it

<!--
- Does efficiency trend down across seasons once weather is accounted for?
- Any faults, servicing, refrigerant checks, or component replacements.
- Defrost cycle behaviour across different winters, if the data shows it.
-->

## Running costs

<!--
- Cost per year and per kWh of heat delivered, against the tariff actually paid.
- Comparison against what the previous system would have cost over the same
  period, if that can be estimated honestly.
- Keep the tariff and the physics separate — cost moves for reasons that have
  nothing to do with the pump.
-->

## Data and tooling

<!--
- The analysis runs on the home-energy-data repo (Vaillant CSV exports rendered
  to charts and statistics). Worth a short section: what the export actually
  contains, its resolution, and where it is untrustworthy.
- Anything you changed in the tooling to handle several years rather than one.
- Charts: export from the tooling, then reference them here, e.g.
{% raw %}{{ macros.image('heat-pump/scop-by-year.png', caption="Heating and hot water SCOP by year.") }}{% endraw %}
-->

## Summary

<!--
- The honest verdict after several seasons, including anything that has
  disappointed.
- What you would tell someone specifying a pump for a similar house — the 2024
  note's oversizing question now has real evidence behind it.
-->

## References and further reading

<!--
Carry over the still-relevant links from heat-pump.md (Protons for Breakfast,
Energy Stats, Octopus API, Octograph) and add any new sources used here.
-->

- [Review of heat pump use and performance]({filename}/heat-pump.md) — the 2024 note
- [Cornish Unit House retrofit insulation]({filename}/house-insulation.md)
- [Home thermal-imaging survey]({filename}/thermal-survey.md)
- [home-energy-data on GitHub](https://github.com/jameshanlon/home-energy-data)
