---
Title: Thoughts on a Python processor 
Date: 2023-06-30
Category: notes
Tags: computing, computer-architecture
Summary: A rationale and strawman for a processor to accelerate Python workloads. 
Status: published
---

{% import 'post-macros.html' as macros %}

I have spent some time recently thinking about how hardware can be architected
and optimised to better support high-level dynamic languages such as Python.
There appears to be a significant gap between these domains, which is a huge
opportunity for new hardware innovation.

Dynamic languages have become hugely popular becuase they are easy to use. Ease
of use is a critical factor in the development of new application areas and
technologies, allowing developers to move quickly and widening participation to
people without expertise in low-level programming. Although there can be
significant performance overheads, this can be an acceptable price to pay. In
AI for example, the state-of-the art is constantly evolving and the vast
majority of models are built and developed using Python.
