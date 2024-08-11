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
recognising several subtleties. DES is widely used in different areas where
analytical solutions are difficult. I am focusing on its use in modelling
clocked computer systems.

In a DES, each event is scheduled to occur at a particular point in time and
represents a change in the state of the system and the possible generation of
more future events. Because there are no state changes between events, the
simulation jumps through time from one event to the next. These variable time
steps are in contrast with a discrete-event scheme with fixed timesteps. Fixed
timesteps are particularly suited to digital systems with clocked logic, where
each time increment corresponds to clock cycle. Fixed-time simulation has the
drawback that all time steps are evaluated regardless of whether anything
happens, although it is easier to reason about since everything proceeds in
lockstep. DES is inherently more flexible but can be harder to parallelise
because of the need to maintain a centralised event list.

The main components of a DES are:

- A **state** (or set of states) representing the components of the system.
- **Events**, that occur atomically at a particular instant and can update
  the system state and create new future events.
- A **clock**, that records the simulation time.
- A **list of future events** (the *event list*). This is most often implemented
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

1. For events that occur at the same time, it must be possible to execute them
   in any order, without affecting the behaviour of the simulation. In other
   words, the outcome of the simulation must not depend on any ordering of
   simultaneous events.

2. Care must be taken to not create duplicate events. For example, if a
  component of the system is servicing some kind of input queue, when an item
  is added to the queue a corresponding 'service' event must be created, but only
  when the queue is empty. As such, delegation of responsibility for event
  creation must be clear.

To avoid violating point 1 above, each time step can be divided into several
phases to impose an ordering of events. A simple case is to divide each
timestep into two phases: a *read* phase where system state can be read and a
*write* phase where system state can be updated. By separating access in this
way, there can be no dependencies between the serialisation of reads and writes
as the events are fetched from the queue. As an example, consider a set of
nodes connected in a ring topology and they pass a token around in a fixed
direction.

{{ macros.imagenothumb('discrete-event-simulation/DES-ring.png',
                       caption="DES of a ring of nodes that exchange a token with events for transmit and receive, separated by different phases within a simulation timestep.") }}

In simulating this system, receiving always occurs after a previous write has
committed. This avoids a dependent receive from ever being scheduled before a
transmit.

Extending this concept of phases, a timestep can be divided into an arbitrary
number of sub phases to model more complex behaviours. This is how the
SystemVerliog execution semantics are defined, with a set of stateful processes
that respond to changes on their inputs to product outputs. Every change in
state of a net or variable causes processes sensitive to them to be evaluated
and there may be many steps of evaluation to produce a final output for the
time step. The timestep is divided into a fixed set of ordered regions in order
to provide predictable interactions with a design.

Using the above example of a ring of nodes passing a token, I will walk through some Rust
code that implements a DES of the system. The main component is a `Simulator`
object that maintains the event queue and the system state:

``` Rust
struct Simulator {
    max_cycles: usize,
    current_time: usize,
    event_queue: BinaryHeap<Event>,
    state: State,
}
```

The main simulation loop pops events off of the queue and dispatches them to a
handler function:

```
fn run(&mut self) {
        while let Some(event) = self.event_queue.pop() {
            if self.max_cycles > 0 && self.current_time >= self.max_cycles {
                break;
            }
            self.current_time = event.time;
            self.handle_event(event);
        }
    }
```

The event handler function implements the behaviour for each event:

```
fn handle_event(&mut self, event: Event) {
        match event.event_type {
            EventType::Transmit => {
                // Deactivate.
                self.state.nodes[event.node_id].active = false;
                println!("Node {} inactive", event.node_id);
                // Schedule receive at next node.
                let recv_event = Event {
                    event_type: EventType::Receive,
                    time: self.current_time + 1,
                    node_id: self.state.next_node(event.node_id),
                };
                self.schedule_event(recv_event);
            }
            EventType::Receive => {
                // Activate.
                self.state.nodes[event.node_id].active = true;
                println!("Node {} active", event.node_id);
                // Schedule transmit.
                let send_event = Event {
                    event_type: EventType::Transmit,
                    time: self.next_timestep(self.current_time),
                    node_id: event.node_id,
                };
                self.schedule_event(send_event);
            }
        }
    }
```

The complete source code can be found in [this repository]().

.. Parallelisation strategies

## Summary

Blah

## References / further reading

- [GitHub repository](https://github.com/jameshanlon/discrete-event-simulator)
- [Discrete-event simulation](https://en.wikipedia.org/wiki/Discrete-event_simulation), Wikipedia.
- [List of DES software](https://en.wikipedia.org/wiki/List_of_discrete_event_simulation_software), Wikipedia.
- [Introduction to discrete event simulation](https://www.cs.cmu.edu/~music/cmsip/readings/intro-discrete-event-sim.html), CMU lecture notes.
- [Distributed discrete event simulation](https://dl.acm.org/doi/pdf/10.1145/6462.6485), Jayadev Misra (1986).
- [Parallel discrete event simulation](https://dl.acm.org/doi/10.1145/84537.84545), Richard M. Fujimoto (1990).
- Principles and Practices of Interconnection Networks, Chapter 24, William Dally, Brian Towles (2004).
- [1800-2017 SystemVerilog LRM](https://ieeexplore.ieee.org/document/8299595),  section 4 'Scheduling semantics'.
