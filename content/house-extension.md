---
Title: Extending and decarbonising a Cornish Unit house
Date: 2026-08-10
Category: Home and Sustainability
Tags: sustainability, energy-efficiency, retrofit, construction
Summary: Adding to a 1940s precast concrete prefab rather than demolishing it,
         and what the fabric and heating measurements show before and after.
Status: draft
---

{% import 'post-macros.html' as macros %}

<!--
================================================================================
PRE-PUBLICATION CHECKLIST — work through this before setting Status: published.
================================================================================

IMAGES
[ ] Strip EXIF from every original before uploading to Spaces. The build does
    NOT do this for you: get_thumbnail() strips metadata from the thumbnail, but
    macros.image() links the thumbnail to the full-size original on Spaces,
    which is served exactly as uploaded, and macros.imagenothumb() copies the
    file byte-for-byte via shutil.copyfile. Verified by test, not assumed.
        exiftool -all= -tagsFromFile @ -Orientation <files>
    Confirm with: exiftool -gps:all -make -model <files>
[ ] Same check over the ~150 photos already published across thermal-survey.md,
    garden-workshop.md, house-insulation.md and allotment-shed.md — this note is
    a good prompt to audit the existing set.
[ ] No exterior elevations in street context; no neighbouring properties,
    numbers, or distinguishing street features in frame.
[ ] Prefer drawn details over site photographs throughout (see DIAGRAMS below).

DISCLOSURE
[ ] Do not link or cite the planning application or building control records —
    those portals are searchable by address, and they also expose neighbour
    correspondence, which is not yours to publish.
[ ] No whole-house floor plan with room labels, door and window positions.
    Buildup sections and junction details only.
[ ] Nothing on locks, alarm, cameras, gates, access, or workshop contents.
[ ] No dates or duration for which the house stood open or unoccupied.
[ ] Costs as percentages against budget, not absolute figures (see COSTS).
[ ] Energy data at monthly or seasonal resolution only (see PERFORMANCE).
[ ] Publish after completion, not during. A live build log advertises a
    scaffolded house at a location this site already narrows considerably.

AGGREGATION
[ ] The site already discloses house type, city, floor area, room-by-room
    interiors, garden layout, allotment, and continuous occupancy. Judge each
    inclusion here by what it ADDS to that, not by whether it is sensitive
    on its own.

================================================================================
FRAMING
================================================================================

This is a case study of an archetype, not a build log of a house. The Cornish
Unit is a hard-to-treat 1940s precast concrete prefab with tens of thousands
still occupied, frequently non-mortgageable and poorly performing. That framing
is the point of the note — it is what makes it useful to a reader who owns one,
and generalising away from the specific property is also what keeps it safe to
publish.

Organise by thermal question, not by build sequence. The chronological structure
(groundworks, structure, fit out) pulls the note toward "here is my house, stage
by stage"; the build sequence belongs as supporting detail under the questions
below.

This connects directly to the CHEESE Project and First Thermal work — applying
the retrofit and thermal-imaging principles you have advocated professionally to
a genuinely difficult case. Worth stating once, early; it gives the note its
audience.

Existing notes this builds on — cross-link, do not repeat, and add reciprocal
links when publishing:
- thermal-survey.md — the documented fabric faults, the baseline nobody else has
- house-insulation.md — the first-floor timber-frame retrofit
- heat-pump.md — the 10 kW unit, sized in anticipation of this work

DIAGRAMS — the single highest-value substitution. Buildup sections, U-value
tables, airtightness and thermal-bridging junction details carry the argument
better than site photographs and contain no location information at all. Budget
drawing time accordingly.
-->

<!--
INTRO
- The archetype: what a Cornish Unit is, how many there are, why they are hard
  to treat, and what that means for the people living in them.
- The decision this note is about: extend and upgrade, or demolish and rebuild.
- What the reader gets — measurements before and after, on a house with an
  unusually well documented starting point.
-->

## Why extend rather than demolish

<!--
- The embodied carbon argument, made properly rather than gestured at. Retaining
  existing structure against the carbon cost of demolition and new build.
- The counter-argument taken seriously: these are poor-performing buildings and
  there is a real case for replacement. Say where the balance fell for you and
  why, including the non-carbon reasons.
- Anything specific to precast concrete construction that bears on this —
  condition assessment, structural viability, known failure modes.
- This is the most substantive sustainability section and it is about buildings
  in general, not about your house in particular. Give it room.
-->

## The baseline

<!--
- What the house was before, in measurements: heat loss, U-values of the
  original construction, the faults found by thermal imaging, energy demand.
- Draw on thermal-survey.md and house-insulation.md for this — the value is that
  the "before" state is documented rather than reconstructed from memory.
- Keep it to fabric and energy. Room-by-room interior narrative is not needed
  here and adds disclosure the earlier notes already made.
-->

## Fabric

<!--
- Wall, roof and floor buildups for the new construction, with U-values.
- What was done to the retained fabric, and how far it could realistically be
  improved given precast concrete construction.
- Where you exceeded building regulations and where you did not, honestly, with
  the reasoning — regulations-minimum decisions are informative too.
- Materials: insulation choices and their embodied carbon, not just their
  lambda values.
- Drawn sections rather than photographs. Example figure — drop the
  {% raw %}{% endraw %} markers to make it live:
{% raw %}{{ macros.image('house-extension/wall-buildup.png', caption="Wall buildup and U-value.") }}{% endraw %}
-->

## The junction

<!--
- Where new construction meets 1940s precast is the technically interesting part
  of the whole project and the part least covered anywhere online. This is the
  section that justifies the note existing.
- Airtightness strategy across the junction, and how it was detailed. This is
  where performance is normally lost.
- Thermal bridging, and what you could not eliminate.
- Moisture and interstitial condensation risk when you insulate one side of a
  concrete structure and butt a modern envelope against it.
- Junction detail drawings. Again: drawings, not site photographs.
-->

## Heating and ventilation

<!--
- Integrating the extension into the existing heat pump system: emitters, flow
  temperature, rebalancing, whether the 10 kW capacity turned out to be the
  right call now that the floor area it was sized for actually exists.
  heat-pump.md set this question up in 2024; this is where it gets answered.
- Ventilation: an airtight extension attached to a leaky house changes the
  moisture and air quality picture. MVHR or its absence deserves a paragraph
  either way.
-->

## Construction

<!--
- Compressed. Enough for a reader to understand how the fabric decisions above
  were actually realised — foundations, frame, envelope sequence — without
  becoming a stage-by-stage log.
- Who did what: self-build, contractor, or a mix.
- The buildability problems, especially anything that forced a change to the
  fabric or junction detailing. Compromises made on site are the useful content
  here, not the sequence of events.
-->

## Costs

<!--
- Percentages against budget, not absolute figures: "18% over, mostly
  groundworks" carries everything useful without profiling your finances against
  a house type and a city already published on this site.
- Where retrofit cost more than new build would have, and where it cost less.
- Cost per unit of heat loss avoided is the sustainability-relevant framing and
  is far more useful to a reader than a total.
-->

## Measured performance

<!--
- Before and after, using the same metrics as the baseline section so the
  comparison is like-for-like: heat loss in W/K, U-values, air permeability if a
  test was done, kWh/m2/yr, SCOP.
- RESOLUTION: monthly or seasonal aggregates only. Daily or hourly heat pump
  data is an occupancy record — holidays and working patterns are legible in it.
  Aggregates make every argument this note needs and leak nothing.
- Normalise for the larger floor area and for weather, or the comparison
  misleads. Demand rising in absolute terms while intensity falls is the
  expected result and worth stating plainly.
- Overlap with the multi-year heat pump note: decide which note owns the
  analysis and which links to it, so the numbers are not maintained twice.
- A repeat thermal-imaging survey of the junction and new fabric is the natural
  closing figure and parallels thermal-survey.md directly. Check the frames for
  anything identifying before publishing.
-->

## What generalises

<!--
- What a reader with the same house type should take from this — the decisions
  that would transfer, and the ones that were specific to this site.
- What you would do differently. house-insulation.md and garden-workshop.md are
  both usefully candid and that is why they are worth reading.
- Where the remaining losses are, and whether they are worth chasing.
-->

## Related links

- [Cornish Unit House retrofit insulation]({filename}/house-insulation.md)
- [Home thermal-imaging survey]({filename}/thermal-survey.md)
- [Review of heat pump use and performance]({filename}/heat-pump.md)
- [The CHEESE Project](http://www.cheeseproject.co.uk)
