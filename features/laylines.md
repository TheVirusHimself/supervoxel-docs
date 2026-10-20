---
title: "Laylines (signal wiring)"
parent: Features
nav_order: 26
---

# Laylines: signal wiring

> **Laylines** is an optional module of SuperVoxel that adds circuits built from blocks: wires carry a signal strength
> from 0 to 15 between switches, logic gates, timers and outputs. Build doors that open on a lever or a pressure
> plate, lights on clocks, counters and number screens, and game logic hooked to Blueprints.

## How do I...?
- **Open a door with a lever:** place a lever, a line of wire and a door; flip the lever with **Interact With Voxel**.
- **Run a wire along a floor or up a wall without using up blocks:** lay a [surface wire](#surface-wires).
- **Run my own Blueprint when a circuit fires:** end the circuit in a **Trigger** and bind **On Layline Signal
  Changed**.
- **See it working:** drop a **Laylines Demo** actor on flat ground.

## Turn it on or off
1. Turn on **Enable Laylines** in Project Settings > Plugins > SuperVoxel > Optional Modules (off by default). From
   code: **Set Laylines Enabled**. A world decides when it begins play; after changing the switch at runtime, call
   **Refresh Laylines Active**. Off, the Laylines subsystem is inert (Get returns null) and layline blocks are plain
   blocks. A game mode can turn it on for its maps instead (see
   [Install: the modules](../install-and-upgrade.md#the-modules)).
2. Give your world the layline blocks, either way:
   - add a Data Table of `SuperVoxelBlockDef` rows to your block set's **Tables** and fill it with **Fill Block
     Table** (Laylines library; C++: `ULaylinesBlocks::FillBlockTable` in `LaylinesBlocks.h`), or copy the rows into
     your own table under the same names. To run it in the editor, make an **Editor Utility Blueprint** (Content
     Browser > Add > Editor Utilities > Editor Utility Blueprint, parent Editor Utility Object), add a function marked
     **Call In Editor** that calls Fill Block Table with your table, then right-click the Blueprint > Run (or press
     the function's button). Save the table afterwards;
   - or call **Make Block Set With Laylines** (a copy of a block set plus the rows) and assign it to the world.

Nothing runs until a world's block set has the layline rows.

## The 3 settings you'll use most

| Setting | What it does | Default |
|---|---|---|
| Signal Decay | Wires fade with distance (for wire types left on Default) | on |
| Step Seconds | Reaction time of gates and outputs; also one "tick" for timers and emitters | 0.05 |
| Output Threshold | Lowest strength that turns lamps, doors and hatches on | 1 |

Project-wide settings are in Project Settings > Plugins > SuperVoxel Laylines.

## Example: place a gate from code
**Blueprint:** Get Laylines Subsystem → Place Layline (World, Voxel, Role = And, Facing = 0).

**C++:**
```cpp
#include "LaylinesSubsystem.h"

if (ULaylinesSubsystem* Laylines = ULaylinesSubsystem::Get(this))
{
	Laylines->PlaceLayline(World, FIntVector(10, 10, 20), ELaylineRole::And, /*Facing +X*/ 0);
}
```
Parts are also ordinary blocks: `Set Block (Voxel, "LaylineWire")` works too (**Get All Block Names** lists them).
Players use parts with **Interact With Voxel**.

## Parts
Strength runs from 0 to 15. Parts with a look per state (a lit wire, a timer's progress, an emitter's value, a
display's colour) swap between blocks of the same part, and their options go with them.

| Part | Blocks | What it does | Interact |
|---|---|---|---|
| Wire | LaylineWire, LaylineWireLit | Carries a signal and joins in all 6 directions; fades by Fade Per Voxel while decay is on for it | — |
| Cable | LaylineCable, LaylineCableLit | A second wire type that joins with wires; by default it never fades | — |
| Lever | LaylineLever, LaylineLeverOn | Sends its strength while on | Flips it |
| Button | LaylineButton, LaylineButtonOn | On for its pulse length | Presses it |
| Pressure plate | LaylinePlate, LaylinePlateOn | On while a pawn stands on it | — |
| Source | LaylineSource | Always sends its strength | — |
| Clock | LaylineClock | On and off by turns, each its half period | Cycles the clock presets |
| NOT, AND, OR, XOR, NAND, NOR | LaylineNot … LaylineNor | Output toward the front; inputs from whichever of back, left and right have a part next to them (NOT reads the back only) | — |
| Delay | LaylineDelay | Passes the back input on after 1 to 4 steps | Cycles the steps |
| Latch (SR) | LaylineLatch | Set from the back, reset from either side; remembers | — |
| Toggle (T) | LaylineToggle | Flips each time the back input turns on | — |
| Timer | LaylineTimer and its run blocks | A rising back input starts it; a side input resets it. **Pulse**: on for the duration. **Countdown**: fires when the time is up and stays on until reset. **Repeat** makes them cycle. The dial lights a quarter at a time; the time left saves | Cycles the timer presets |
| Number emitter | LaylineEmitter, LaylineEmitter1..15 | On a command (rising back input, interact, or **Emit**) outputs a value 0–15 toward the front. **Hold**, **Pulse** (for Pulse Ticks steps) or **Sequence** (steps through a list). A side input resets it | Next value, sent at once |
| Comparator | LaylineComparator | A is the back input, B the stronger side. Compare: A if A ≥ B. Subtract: A − B | Switches mode |
| Lamp | LaylineLamp, LaylineLampOn | Lit while its strongest neighbour reaches its threshold; gives real light | — |
| Door, Hatch | LaylineDoor/DoorOpen, LaylineHatch/HatchOpen | Open while powered; the open blocks don't collide | — |
| Display | LaylineDisplay, LaylineDisplay1..15 | A plain cube in one flat colour from the palette, picked by its signal. A wall of them makes a pixel screen | — |
| Trigger | LaylineTrigger | Holds its strength and fires **On Layline Signal Changed** when it changes (for example, to switch a [fluid emitter](fluids.md#emitters-and-drains)) | — |

**Facing:** a directional part outputs to its facing side (0 = +X, 1 = +Y, 2 = −X, 3 = −Y). Set it with Place Layline
or Set Facing. A part a player places faces where the player looks.

**Decay:** whether a wire fades is decided per wire: its own option (Set Wire Decay: On, Off or Default), otherwise
its type's setting (Wire Decay, Cable Decay), otherwise the project's Signal Decay. With decay off, a network carries
its strongest input at full strength along any length.

**Display colours:** a **Laylines Palette** data asset holds 16 colours, or gradient stops in gradient mode; empty
uses the built-in palette (dark, then blue through green and yellow to red). Display Zero Is Off shows level 0 as
black. Set Display Map picks which palette level each strength shows on one display (for example a red/green status
light). Notify Settings Changed re-tints every display at once.

**Any colour on any single display:** each display voxel carries its own colour through SuperVoxel's
[voxel tint](state-and-metadata.md#voxel-tint). **Set Display Palette** gives one display its own 16 colours (**Get
Display Palette** reads them back), and the colour saves, replicates and streams with the voxel.

## Surface wires
Wires can also lie on the faces of ordinary blocks instead of being blocks themselves: on floors, walls and ceilings,
on blocky faces and on smooth ground.

**Laying them** (server; clients see them through replication):

- **Place Surface Wire** (World, Host, Face, Cable): Host is the solid voxel, Face a unit axis pointing out of it, such
  as (0, 0, 1) for its top. The cell in front of the face must be open.
- **Place Surface Wire At Point** (a hit point and normal), **Trace And Place Surface Wire** (a ray, for players
  aiming), **Remove Surface Wire**.

```cpp
// A floor wire on top of voxel (10, 4, 19), and a cable up the side of the next one.
Laylines->PlaceSurfaceWire(World, FIntVector(10, 4, 19), FIntVector(0, 0, 1));
Laylines->PlaceSurfaceWire(World, FIntVector(11, 4, 20), FIntVector(-1, 0, 0), /*bCable*/ true);
```

**Shapes:** a surface wire joins the wires next to it and takes its shape from them: end, straight, corner, T or cross.
It joins along the same face of the next block, round an inner corner (up the wall the floor meets), and over an
outer edge (onto the block's next face), so a line can climb a step and come down the other side.

**Signal:** surface wires carry signal like wire blocks, with the same fading rules and an override per face (**Set /
Get Surface Wire Decay**); surface cables don't fade by default. They join wire blocks, and they power (and are powered
by) every part next to the cell they lie in, including the block they lie on: a lever or lamp standing beside a floor
wire is connected.

**Saving:** a surface wire is kept in its host block's metadata, so it saves, loads, streams and replicates. Digging the
host, or filling the cell in front of the wire, takes it away.

**Looks:** a flat pad with an arm toward each wire it joins, drawn in batches on every machine. On smooth ground it
sits on the drawn surface.

| Call | What it does |
|---|---|
| Has Surface Wire, Is Surface Cable | Whether a face has a wire, and whether it's a cable |
| Get Surface Signal | A surface wire's strength (0 to 15); Get Signal on the open cell gives the strongest wire in it |
| Get Surface Wire Shape | Its shape (None, Dot, End, Straight, Corner, Tee, Cross) and which of its face's 4 directions it connects to |
| Set / Get Surface Wire Decay | One surface wire's fading (Default: its type's setting) |

## Project settings (`ULaylinesSettings`)

| Setting | Default | What it does |
|---|---|---|
| Signal Decay | on | Wires fade with distance (wire types set to Default) |
| Fade Per Voxel | 1 | Strength a fading wire loses per voxel |
| Wire Decay / Cable Decay | Default / Off | Each wire type's override |
| Max Strength | 15 | What switches, sources, clocks and gates send |
| Max Updates Per Tick | 4096 | Wire voxels solved per frame per world |
| Max Network Size | 16384 | Largest network solved as one |
| Step Seconds | 0.05 | Reaction time; one "tick" for timers and emitters |
| Plate Checks Per Second | 10 | Pressure plate polling |
| Delay Step Seconds | 0.1 | One delay step |
| Button Pulse Seconds | 1 | Button on-time |
| Default Clock Period / Clock Presets | 10 / (5, 10, 20, 40) | Clock half period in tenths of a second, and the presets interact cycles |
| Default Timer Seconds / Mode / Repeat, Timer Presets | 5 / Pulse / off, (1, 2, 5, 10, 30) | New timers, and the presets interact cycles |
| Timer Progress Seconds | 0.5 | How often a running timer refreshes its look and saved time |
| Default Emitter Value / Mode / Pulse Ticks | 15 / Hold / 4 | New emitters |
| Output Threshold | 1 | Lowest strength that turns lamps, doors and hatches on |
| Palette, Display Zero Is Off, Display Emissive, Display Emissive Strength | built-in, on, on, 2 | Display colours |
| Surface Wire Width, Surface Wire Thickness | 0.18, 0.04 | Surface wire size, as a share of the voxel size |
| Surface Wire Color / Lit Color, Surface Cable Color / Lit Color | dark teal / bright teal, dark purple / light purple | Surface wire colours, off and lit |
| Surface Wire Material | the engine's basic material | Any material with a `Color` vector parameter |
| Surface Redraw Seconds | 0.05 | Batching interval for redrawing surface wires |

Change them at runtime by name with **Set Setting** / **Get Setting** (listed by **Get Setting Names**), or edit **Get
Laylines Settings** and call **Notify Settings Changed**. Either way **On Laylines Settings Changed** fires and every
network is solved again.

## Per-part options
Saved and replicated with the world. Each change fires **On Layline Option Changed** (World, Voxel, Option). Every
number option also works by name with **Set Block Option** / **Get Block Option** (listed by **Get Block Option
Names**).

| Option | Parts | Calls |
|---|---|---|
| Strength | lever, button, plate, source, clock, gates | Set/Get Strength |
| Decay | wire, cable | Set/Get Wire Decay, Wire Fades |
| Pulse | button | Set/Get Button Pulse (seconds) |
| Period | clock | Set/Get Clock Period (tenths) |
| Delay steps | delay | Set/Get Delay Steps |
| Facing | directional parts | Set/Get Facing |
| Subtract | comparator | Set/Get Comparator Subtract |
| Latch type | latch, toggle | Set/Get Latch Type |
| Duration, mode, repeat | timer | Set/Get Timer Duration (seconds), Set Timer Duration Ticks, Set/Get Timer Mode, Set/Get Timer Repeat; Start Timer, Reset Timer; Get Timer Remaining |
| Value, mode, pulse ticks, sequence | emitter | Set/Get Emitter Value, Mode, Pulse Ticks, Sequence; Emit, Reset Emitter; Get Emitter Output |
| Threshold, invert | lamp, door, hatch, trigger | Set/Get Output Threshold, Set/Get Output Inverted (on while not powered) |
| Map, Palette | display | Set/Get Display Map, Set/Get Display Palette; Get Display Level, Get Display Color |

**Reading a circuit:** Get Role, Get Signal, Is On. **Rescan** restarts clocks, timers and the like on demand (they
restart by themselves after a load or when a chunk streams in).

## How it runs
- **Server authoritative.** Every result is an ordinary block, state or metadata change on the server, so circuits
  replicate, save and load through SuperVoxel's own edit path, including switch positions, timers mid-count and
  emitter sequences.
- **No per-frame scans.** Only changed wire networks are solved, at most Max Updates Per Tick voxels a frame; the rest
  wait for the next frame.
- **Loops are safe.** Gates and outputs react one step later through scheduled ticks, so a loop oscillates at that
  pace instead of freezing the game.

## The demo
A **Laylines Demo** actor (`ALaylinesDemo`) on flat ground lays out seven small circuits when the world is built and runs
them on timers: an AND gate, a clock with a delay chain, a pressure-plate door, a button into a NOT gate, emitter-
driven display bars (a fading wire next to a non-fading cable), a button-started timer, and a lever's surface wire
along the floor, up and over a one-block step to a lamp.

## Limits
- Gate facing is horizontal only, and the textures don't show facing.
- A running timer's saved time left is refreshed every 0.5 s (Timer Progress Seconds).
- The part textures are drawn by code; displays are plain flat colour.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| No layline blocks to place | The world's block set has no layline rows | Fill Block Table, or Make Block Set With Laylines |
| Parts don't react | Enable Laylines is off, or was turned on after the world started | Turn it on, then call Refresh Laylines Active (or restart the level) |
| A long wire goes dark at the end | Signal decay | Use cable, or set the wire's decay to Off |
| A gate ignores its input | The input isn't at its back or sides, or the facing is wrong | Set Facing so the output points away from the inputs |
| A big circuit updates slowly | Max Updates Per Tick reached | Raise it, or split the network |
