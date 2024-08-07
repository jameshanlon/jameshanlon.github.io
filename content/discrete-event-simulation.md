---
Title: Discrete-event simulation
Date: 2024-08-07
Category: notes
Tags: computing
Summary: Building a simple discrete-event simulation in C++
Status: published
---

{% import 'post-macros.html' as macros %}

Discrete event simulation (DES) is a methodology for modelling dynamic systems
as a sequence of events in time. There are plenty of places to read about DES,
but in this note I want to outline how it works and can be simply implement,
recognising several subtulties. DES is widely used in different areas where
analytical solutions are difficult. I am focussing on its use in modelling
clocked computer systems.

In a DES, each event is scheduled to occur at a particular point in time and
represents a change in the state of the system and the possible generation of
more future events. Because there are no state changes between events, the
simulation jumps through time from one event to the next. These variable time
steps are in contrast with a discrete-event scheme with fixed timesteps. Fixed
timesteps are particularly suited to digital systems with clocked logic, where
each time increment corresponds to cycle. Fixed-time simulation has the
drawback that all time steps are evaluated regardless of whether anything
happens. However, DES can be harder to parallelise because of the need to
maintain a centralised event list.

The main components of a DES are:

- A **state** (or set of states) representing the components of the system.
- **Events**, that can update the system state and create new future events.
- A **clock**, that records the simulation time.
- A **list of future events** (the event list). This is most often implemented
  as a priority queue with events queued in chronological order, soonest at
  the front.

An outline of the DES algorithm is as follows:

- Create one or more initial events and add them to the event list.
- While the event list not empty:
  * Choose a next event with the earliest time.
  * Advance simulation clock to time of event.
  * Execute the event.
    - State updates are committed immediately.
    - New events are added to the event queue.

Simulation proceeds until there are no more events to process, or a maximum
time is reached.

During the simulation the following must be ensured:

- For events that occur at the same time, it must be possible to execute them
  in any order, without affecting the correctness of the simulation. In other
  words, the outcome of the simulation must not depend on any ordering of
  simultaneous events.

- Care must be taken to not create duplicate events. For example, if a
  component of the system is servicing some kind of input queue, when an item
  is added to the queue a corresponding 'service' event must be created, but only
  when the queue is empty. As such, delegation of responsibility for event
  creation must be clear.

For modelling of a synchronsied system, it can be useful to subdivide each time
step into several phases. For example, two phases can be used to separate
actions of producing...

C++ example

Parallelisation

```python
foo
```

xxx

    #!python
    # Code goes here ...

## References / further reading

- [GitHub repository](https://github.com/jameshanlon/discrete-event-simulator)
- [Discrete-event simulation](https://en.wikipedia.org/wiki/Discrete-event_simulation), Wikipedia.
- [List of DES software](https://en.wikipedia.org/wiki/List_of_discrete_event_simulation_software), Wikipedia.
- [Introduction to discrete event simulation](https://www.cs.cmu.edu/~music/cmsip/readings/intro-discrete-event-sim.html), CMU lecture notes.
- [Distributed discrete event simulation](https://dl.acm.org/doi/pdf/10.1145/6462.6485)
