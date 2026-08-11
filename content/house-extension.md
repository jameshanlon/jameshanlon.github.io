---
Title: House extension and renovation
Date: 2026-08-10
Category: Physical Projects
Tags: construction, retrofit, energy-efficiency
Summary: Design and construction of an extension to a 1940s Cornish Unit house,
         and the renovation work that went with it.
Status: draft
---

{% import 'post-macros.html' as macros %}

<!--
SKELETON — outline only. Set `Status: published` and update `Date:` when written.

CATEGORY — filed under Physical Projects to sit with the garden workshop and
allotment shed, since this is primarily a build log. If the note ends up leading
on fabric performance and energy rather than construction, move it to Home and
Sustainability alongside house-insulation.md and thermal-survey.md. Pick one
before publishing rather than trying to serve both.

MODEL — content/garden-workshop.md is the closest existing note and the right
template: chronological build stages, short prose per stage, heavy use of paired
photographs, CAD drawings at the end. Follow its shape. Note that it mixes `#`
and `##` for stage headings inconsistently; use `##` throughout here.

CONTEXT THIS CONNECTS TO — the extension is already referenced across three
published notes, so this one is the payoff:
- heat-pump.md (2024) said the 10 kW unit exceeded the requirements of the
  ~90 m2 house because an extension was planned. This note supplies the "before".
- house-insulation.md covers the first-floor retrofit on the timber frame.
- thermal-survey.md identified the original fabric faults.
Add reciprocal links to those notes when this is published.

PHOTOGRAPHS — take them as you go, including the stages that get buried. The
garden workshop note works because of the sequence of build photos, and those
cannot be recovered afterwards. Groundworks, insulation and first-fix are the
ones always missed.
-->

<!--
INTRO
- What the house is: 1940s Cornish Unit, precast concrete ground floor with a
  timber-framed first floor, ~90 m2 before the work.
- What was built and why, in a few sentences. What the house could not do before.
- Who did what — self-build, main contractor, or a mix. The garden workshop note
  is explicit about this and it sets reader expectations correctly.
- Whether the design was yours, an architect's, or a package.
-->

## Design and planning

<!--
- The brief and the constraints that shaped it.
- Planning permission or permitted development, and how long it took. Cornish
  Unit houses have specific structural quirks worth mentioning if they bore on
  the design.
- Building regulations approach — the fabric standards you were held to, and
  whether you chose to exceed them.
- Structural engineering for the connection into the existing house.
- CAD drawings and 3D views. The workshop note put drawings in a section at the
  end; either works, but decide once.
-->

## Groundworks and foundations

<!--
- Site clearance, dig, and what was found once open. Services, drains, and the
  original foundation detail.
- Foundation type and why.
- Any insulation below slab.
-->

## Structure

<!--
- Frame or masonry, and the reasoning.
- Connection into the existing Cornish Unit structure — likely the most
  technically interesting part, and the part least covered elsewhere online.
- Openings, lintels, steels.
-->

## Envelope

<!--
- Wall, roof and floor buildups with U-values. The workshop note has a
  "Buildups" section; do the same here, and give the actual figures.
- Airtightness strategy and how it was detailed, especially at the junction with
  the existing house where the two constructions meet. This is where the
  performance is usually lost.
- Thermal bridging at that junction.
- Windows and glazing specification.
-->

## Renovation of the existing house

<!--
- What was done to the original fabric while the work was open: rewiring,
  replumbing, insulation upgrades, replastering.
- Cross-reference house-insulation.md rather than repeating it, and note
  anything that revised or undid that earlier work.
- Faults from thermal-survey.md that this was the opportunity to fix — closing
  that loop explicitly is worth a paragraph.
-->

## Services and heating

<!--
- How the extension was integrated into the existing heat pump system:
  emitters, flow temperatures, whether the 10 kW unit was resized or rebalanced.
- Underfloor heating versus radiators, if relevant.
- Ventilation — an airtight extension on a leaky house changes the picture, and
  MVHR or its absence deserves a sentence either way.
- Electrical work, and anything left as provision for later.
-->

## Internal fit out

<!--
- Follow the workshop note's subsections where they apply: socket and switch
  positions, boarding, second-fix.
- Finishes and anything made rather than bought.
-->

## What it cost and how long it took

<!--
- Budget against outturn, honestly, and where the overrun was. Almost no
  self-build write-up does this and it is the section readers most want.
- Programme against actual.
- If publishing exact figures is uncomfortable, percentages against budget still
  carry the useful information.
-->

## Performance

<!--
- This is what makes the note more than a build log, and what nobody else can
  write about this house: there is a documented before state.
- Heat pump data before and after — heating demand against the larger floor
  area. Note that this interacts with the multi-year heat pump note; decide
  which note carries the analysis and which one links to it, so the numbers
  are not maintained in two places.
- Air test result if one was done.
- A repeat thermal-imaging survey of the junction and the new fabric would be
  the natural closing figure, and directly parallels thermal-survey.md.
-->

## What I would do differently

<!--
- The mistakes. house-insulation.md and the workshop note are both usefully
  candid, and that is why they are worth reading.
-->

## Drawings

<!--
Plans, sections and 3D views, as in the workshop note. Example figure and paired
layout — drop the {% raw %}{% endraw %} markers to make these live:
{% raw %}{{ macros.image('house-extension/3D.png', caption="Extension design.") }}

{{ macros.pair_layout(
     macros.image('house-extension/before.jpg'),
     macros.image('house-extension/after.jpg'),
     caption="Before and after.") }}{% endraw %}
-->

## Related links

- [Cornish Unit House retrofit insulation]({filename}/house-insulation.md)
- [Home thermal-imaging survey]({filename}/thermal-survey.md)
- [Review of heat pump use and performance]({filename}/heat-pump.md)
- [Garden workshop]({filename}/garden-workshop.md)
