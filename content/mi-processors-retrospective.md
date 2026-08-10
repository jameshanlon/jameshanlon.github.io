---
Title: New chips for machine intelligence, revisited
Date: 2026-08-10
Category: Computing and Silicon
Tags: computing, computer-architecture, machine-intelligence
Summary: Revisiting a 2019 survey of machine intelligence accelerators to see
         which architectural bets survived contact with large language models,
         and scoring the predictions I made in 2016.
Status: draft
---

{% import 'post-macros.html' as macros %}

<!--
SKELETON — outline only. Set `Status: published` and update `Date:` when written.

This closes a loop over two existing notes:
- "Machine learning challenges for computer architecture" (2016-11-04,
  content/ml-challenges.md) — the predictions.
- "New chips for machine intelligence" (2019-10-04, content/mi-processors.md) —
  the survey, covering Cerebras WSE, Google TPU v1/v2/v3, Graphcore IPU,
  Habana Gaudi, Huawei Ascend 910, Intel NNP-T, Nvidia Volta and Turing.
Link all three when published.

FRAMING — the reason to write this rather than a fresh survey: both notes predate
the transformer-scaling era entirely, so the question is not "what is new" but
"what did the 2019 designs assume about workloads, and what happened to those
assumptions". A note that only lists newer parts adds nothing that a vendor
comparison table does not already give a reader.

SCOPE WARNING — mi-processors.md is 600 lines because it profiled ten parts
individually. Do not repeat that structure; a per-part survey of the current
field would be enormous and stale within a year. Organise by architectural
question instead, using specific parts as evidence. Aim for something closer to
ml-challenges.md in shape.

DISCLOSURE — you worked at Graphcore 2016-2023 and now work at XTX. Say so once,
early, and be careful that the IPU section is judged on the same evidence as
everything else. Keep to what is public.
-->

<!--
INTRO
- What the 2019 survey was trying to capture, and the moment it was written in.
- What the reader gets from this note: an audit, not a catalogue.
- One sentence on the disclosure above.
-->

## What the 2016 note got right and wrong

<!--
- ml-challenges.md was organised as: compute and memory, precision, structure,
  programming, deployment and portability. Walk those five in order and mark
  each one honestly.
- Likely candidates worth examining rather than asserting:
    - Precision: the note's expectations against what actually shipped
      (bf16, fp8, and lower for inference). This is probably the clearest hit.
    - Compute and memory: whether the memory wall landed where it was expected.
      HBM capacity and bandwidth, not FLOPs, became the binding constraint.
    - Structure: expectations about sparsity and irregular models against how
      little unstructured sparsity is used in practice.
    - Programming: whether the framework and compiler picture went where it
      looked like it was going.
- Being specific about a wrong call is worth more to a reader than three right
  ones. Do not soften them.
-->

## The workload moved

<!--
- The single fact that reorders everything: the 2019 parts were designed against
  a workload mix of convnets and mixed model sizes, with training as the
  headline use. Transformer inference at scale is a different problem —
  memory-bandwidth-bound decode, enormous weights, KV cache, batching dynamics.
- Consequences to draw out:
    - Large on-chip SRAM versus large off-chip HBM, and how that bet aged.
    - Model size against single-device memory, and why distribution stopped
      being optional.
    - Training-versus-inference split of the market and of the silicon.
    - Interconnect and scale-out moving from a feature to the product.
- Tie back to the specific designs in mi-processors.md rather than talking about
  the field in the abstract. That is the material only this note has.
-->

## Which bets survived

<!--
- Go design decision by design decision, not company by company:
    - Wafer-scale and very large die.
    - Distributed SRAM as the primary store versus HBM.
    - Systolic arrays versus more general parallel cores.
    - Bulk-synchronous execution models.
    - Custom interconnect versus commodity networking.
- For each: what it optimised for, and whether that thing turned out to matter.
- Where a design was sound but the company did not survive, separate the two.
  Commercial failure is not the same as an architectural mistake, and the
  distinction is the most useful thing an engineer can offer here.
-->

## What happened to the companies

<!--
- Short section, factual, no schadenfreude. Several of the 2019 ten were
  acquired, pivoted, or wound down.
- VERIFY every claim in this section against a current source before publishing
  — corporate status changes and this is the part that ages fastest and is most
  embarrassing to get wrong.
- The interesting observation is structural: what it took to survive was rarely
  the chip.
-->

## What the 2019 survey missed entirely

<!--
- Things absent from the original list that turned out to matter: the software
  moat, inference economics, supply of HBM and advanced packaging, power and
  datacentre constraints, and the hyperscalers building in-house.
- This is the strongest section if written plainly — it is about what a survey
  of chips structurally cannot see.
-->

## Summary

<!--
- What you would tell someone writing the equivalent survey today.
- Resist making fresh ten-year predictions; if you make any, make them
  falsifiable, so the next revisit can be scored the same way this one was.
-->

## Links

- [New chips for machine intelligence]({filename}/mi-processors.md) — the 2019 survey
- [Machine learning challenges for computer architecture]({filename}/ml-challenges.md) — the 2016 predictions
- [Reducing memory use in deep neural networks]({filename}/reducing-memory-in-dnns.md)
- [New chips for machine intelligence (slides)]({{'MI-chips/new-chips-for-MI.pdf'|asset}}) — Bristol guest lecture, 2019
