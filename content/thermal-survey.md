---
Title: Home thermal-imaging survey
Date: 2021-03-31
Category: notes
Status: published
Tags: retrofit, sustainability
---

{% import 'post-macros.html' as macros %}

I recently moved into a [Cornish Unit Type 1 house][cornish-unit-house], and
with my involvement with [The CHEESE Project][cheese-project] I was keen to
perform a thermal-imaging survey to better understand how well the building
performs thermally. Also, with the first few months in the house being in
winter and it feeling very cold in places, I had extra motivaiton to find out
where heat was being lost, and to try and resolve some faults. I have written
this note to record what I found as a case study that others may find useful,
from the point of view of understanding the benefits of using thermal imaging
to assess building performance, and to see the kinds of thermal faults that are
standard among domestic buildings.

I followed the methodology of The CHEESE Project to perform the survey (more
details about [home surveys][cheese-home-survey] and the
[process][cheese-preparation]). To summarise: the best thermal imaging results
are obtained when there is a good temperature differential (at least 10
degrees) between inside the building and outside. For this reason, winter is
the best period, with the building heated for 24 hours to warm up the fabric
rather than just the air inside it. A blower door fitted to an external door is
used to reduce the internal air pressure and excentuate any draughts. Once the
heating is switched off, the house will start to cool down by thermal
conduction through materials and ingress of cold air through draughts. While
this is happening the thermal camera is used to capture the effects of any
areas of rapid cooling, ie 'thermal faults.


[cheese-project]: https://cheeseproject.co.uk
[cheese-home-survey]: https://cheeseproject.co.uk/home-surveys
[cheese-preparation]: https://cheeseproject.co.uk/pre-survey-guide
[cornish-unit-house]: https://nonstandardhouse.com/cornish-unit-type-1-precast-reinforced-concrete-house/

## External

I did the survey in December, and the external temperature was close to 0
degrees. The images below show the back of the house in infra red (thermal) and
visible light. There is little to learn from the thermal picture, and note that
the windows will be reflecting some of the cool night sky.

{{ macros.pair_layout(
     macros.image('thermal-survey/external/back-thermal.jpg'),
     macros.image('thermal-survey/external/back-visible.jpg'), ) }}

## Front door

The area by the front door was noticably cold when walking past it. The thermal
images reveal cold single glazed glass sections (at ~15 degrees compared with
~22 degress ambient temperature of the hallway), and draughts, particularly at
the bottom where the temperature drops to 10 degress.

{{ macros.pair_layout(
     macros.image('thermal-survey/front-door/front-door-thermal.jpg'),
     macros.image('thermal-survey/front-door/front-door-bottom-thermal.jpg'), ) }}

To tackle the leakiness of the front door, I added some acrylic secondary
glazing to the glass sections and blocked up the letter box with glass fiber
insulation and a wooden plug.

{{ macros.pair_layout(
     macros.image('thermal-survey/front-door/secondary-glazing-visible.jpg'),
     macros.image('thermal-survey/front-door/letter-box-visible.jpg'), ) }}


## Windows

The house has uPVC double glazing throughout (installed within the last 10
years), but a main finding of the survey was the windows had several faults.

### Leaking trim

The biggest culprit was draughts around the edges of the frames, from behind a
plastic trim. In the left-hand images, the cold area is a draught emerging from
a section of silicon sealant that had detached.

{{ macros.pair_layout(
     macros.image('thermal-survey/windows/leaking-trim-1-thermal.jpg'),
     macros.image('thermal-survey/windows/leaking-trim-1-visible.jpg'), ) }}

{{ macros.pair_layout(
     macros.image('thermal-survey/windows/leaking-trim-2-thermal.jpg'),
     macros.image('thermal-survey/windows/leaking-trim-2-visible.jpg'), ) }}

When I removed the trim to investigate, I found the frames had not been sealed
to the wall in any way (left), so there was a gap all around where air could
penetrate. Mostly the plastic trims were doing a good job preventing draughts,
but they were not providing much insulation against air circulating behind
them. I fixed the issue by using expanding foam to fill the gaps, and used
filler to address any smaller gaps and make it flush with the window reveals.

{{ macros.pair_layout(
     macros.image('thermal-survey/windows/removed-trim-visible.jpg'),
     macros.image('thermal-survey/windows/filled-gap-visible.jpg'), ) }}

### Leaking seals

{{ macros.pair_layout(
     macros.image('thermal-survey/windows/seal-thermal.jpg'),
     macros.image('thermal-survey/windows/dining-room-window-thermal.jpg'), ) }}

### Missing insulation

{{ macros.pair_layout(
     macros.image('thermal-survey/windows/top-insulation-thermal.jpg'),
     macros.image('thermal-survey/windows/top-insulation-visible.jpg'), ) }}

### Leaking sill

{{ macros.pair_layout(
     macros.image('thermal-survey/windows/sill-thermal.jpg'),
     macros.image('thermal-survey/windows/sill-visible.jpg'), ) }}


## Ground wall

{{ macros.pair_layout(
     macros.image('thermal-survey/ground-wall/blockwork-stairs-1-thermal.jpg'),
     macros.image('thermal-survey/ground-wall/blockwork-stairs-2-thermal.jpg'), ) }}

{{ macros.pair_layout(
     macros.image('thermal-survey/ground-wall/floorboard-leak-thermal.jpg'),
     macros.image('thermal-survey/ground-wall/floorboard-leak-visible.jpg'), ) }}


## First floor walls

{{ macros.pair_layout(
     macros.image('thermal-survey/upper-walls/below-window-landing-thermal.jpg'),
     macros.image('thermal-survey/upper-walls/bedroom-2-thermal.jpg'), ) }}

{{ macros.pair_layout(
     macros.image('thermal-survey/upper-walls/bedroom-1-thermal.jpg'),
     macros.image('thermal-survey/upper-walls/bedroom-3-thermal.jpg'), ) }}


## Air brick

{{ macros.pair_layout(
     macros.image('thermal-survey/air-brick/air-brick-thermal.jpg'),
     macros.image('thermal-survey/air-brick/air-brick-visible.jpg'), ) }}


## Loft hatch

{{ macros.pair_layout(
     macros.image('thermal-survey/loft-hatch/hatch-thermal.jpg'),
     macros.image('thermal-survey/loft-hatch/hatch-visible.jpg'), ) }}


## Loft insulation

{{ macros.pair_layout(
     macros.image('thermal-survey/loft-insulation/missing-bathroom-1-thermal.jpg'),
     macros.image('thermal-survey/loft-insulation/missing-bathroom-2-thermal.jpg'), ) }}


## Kitchen

{{ macros.pair_layout(
     macros.image('thermal-survey/kitchen/cold-cupboard-1-thermal.jpg'),
     macros.image('thermal-survey/kitchen/cold-cupboard-2-thermal.jpg'), ) }}


## Bathroom

{{ macros.pair_layout(
     macros.image('thermal-survey/bathroom/bathroom-thermal.jpg'),
     macros.image('thermal-survey/bathroom/sink-thermal.jpg'), ) }}

{{ macros.pair_layout(
     macros.image('thermal-survey/bathroom/toilet-thermal.jpg'),
     macros.image('thermal-survey/bathroom/toilet-visible.jpg'), ) }}


## Central heating

{{ macros.pair_layout(
     macros.image('thermal-survey/central-heating/boiler-thermal.jpg'),
     macros.image('thermal-survey/central-heating/boiler-visible.jpg'), ) }}

{{ macros.pair_layout(
     macros.image('thermal-survey/central-heating/water-tank-thermal.jpg'),
     macros.image('thermal-survey/central-heating/radiator-thermal.jpg'), ) }}

{{ macros.pair_layout(
     macros.image('thermal-survey/central-heating/pipe-thermal.jpg'),
     macros.image('thermal-survey/central-heating/pipe-ceiling-thermal.jpg'), ) }}


## Kit

{{ macros.pair_layout(
     macros.image('thermal-survey/kit/blower-door.jpg'),
     macros.image('thermal-survey/kit/cheese-camera-kit.jpg'), ) }}

