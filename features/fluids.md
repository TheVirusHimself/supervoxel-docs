---
title: "Fluids (flowing water and lava)"
parent: Features
nav_order: 28
---

# Fluids: flowing water and lava

> **SuperVoxel Fluids** is an optional plugin that makes fluid blocks flow: they fall, spread, drain, level out and
> react (lava meets water and turns to stone). Choose **Block** mode for classic blocky water with endless sources, or
> **Dynamic** mode for water that keeps its volume and can be emptied. Openings set in any surface work as springs
> and drains.

## How do I...?
- **Make water flow in my world:** add the **SuperVoxel Fluids** component to the world actor, or call **Enable
  Fluids**.
- **Get water that empties when drained:** set the fluid's mode to **Dynamic**.
- **Add a spring in a cave wall:** call **Add Emitter On Face**, or place a **SuperVoxel Fluid Emitter** actor against
  the wall.
- **Add a sink:** add a drain with **Instant** on (**Add Drain On Face**, or the emitter actor with **Drain** ticked).
- **Stop plants from blocking water:** tick **Fluid Can Destroy** on them in the block table (see
  [Destruction settings](destruction.md)), or list them in **Washable Blocks**.
- **See it working:** drop a **SuperVoxel Fluid Demo** actor into a level with a world.

## Turn it on or off
1. Enable **SuperVoxel Fluids** in Edit > Plugins (it needs SuperVoxel).
2. Turn it on for a world, either way:
   - add the **SuperVoxel Fluids** component to the world actor;
   - or call **Enable Fluids (World)** (Blueprint or C++). It adds the component with the default Water and Molten
     Rock rows, or returns the one already there.

Without the component, fluid blocks stay where they are. To pause flow, untick **Simulate**: fluids stay as they are
and queries still work.

## The 3 settings you'll use most

| Setting | Where | What it does | Default |
|---|---|---|---|
| Mode | Fluid type row (or Project Settings > Plugins > SuperVoxel Fluids > Default Mode) | Block (classic, endless sources) or Dynamic (keeps its volume) | Block |
| Viscosity | Fluid type row | Seconds between flow steps: higher is thicker and slower | Water 0.15, Molten Rock 0.9 |
| Spread Distance | Fluid type row | How far a flow reaches over flat ground (Block), and how far it looks for an edge to pour over | Water 7, Molten Rock 3 |

## Two modes

| | Block (default) | Dynamic |
|---|---|---|
| Idea | Classic blocky liquid | Every part is kept: water can be emptied |
| Sources | Still voxels (placed or generated) are endless sources | None; springs and emitters add fluid, drains take it |
| Levels | One step lower per voxel away from a source, up to Spread Distance | 1 to 16 parts per voxel |
| Behaviour | Falls first, then runs toward the nearest drop; recedes when nothing feeds it | Falls, spreads and evens out; fills dug holes; optional Pressure (a U-tube levels) and evaporation |
| Look (Auto) | Stepped: flat tops, one height per voxel | Rounded: one smooth surface with rounded edges |

**Set the mode:**

- for the whole project: Project Settings > Plugins > SuperVoxel Fluids > **Default Mode**;
- for one fluid: untick its row's **Use Project Default Mode** and pick **Mode**;
- at runtime: **Set Fluid Mode (Fluid, Mode)**; **Get Fluid Mode** reads it.

Switching converts the fluid's voxels over the next frames. Block to Dynamic makes them full. Dynamic to Block turns
full voxels into sources and rounds the rest to Block levels. The look follows the mode. Call Set Fluid Mode the same
way on clients so they draw the same look.

## Example: turn fluids on and add a spring
**Blueprint:** on Begin Play (server): Find Voxel World → Enable Fluids → Add Emitter On Face (Host, Face = (1, 0, 0),
Fluid = Water).

**C++:** add `"SuperVoxelFluids"` to your module's dependencies.
```cpp
#include "SuperVoxelWorld.h"
#include "SuperVoxelLibrary.h"
#include "SuperVoxelFluidLibrary.h"
#include "SuperVoxelFluidComponent.h"

void AMyGameMode::BeginPlay()
{
	Super::BeginPlay();
	ASuperVoxelWorld* World = USuperVoxelLibrary::FindVoxelWorld(this);
	if (USuperVoxelFluidComponent* Fluids = USuperVoxelFluidLibrary::EnableFluids(World))
	{
		Fluids->SetFluidMode(TEXT("Water"), ESuperVoxelFluidMode::Dynamic);
		// A spring on the +X face of a wall voxel: 16 parts a second is one voxel a second.
		Fluids->AddEmitterOnFace(FIntVector(20, 12, 30), FIntVector(1, 0, 0), TEXT("Water"), 16.f);
	}
}
```

## Fluid types (one row per fluid block)
Set them in the component's **Fluid Types**. Rows ship for Water and Molten Rock. Add a row for any block whose Kind is
Fluid in the block table (Salt Water, Swamp Water...). Rows naming blocks the world doesn't have are skipped.

| Setting | Default (Water / Molten Rock) | What it does |
|---|---|---|
| Block | | The fluid block this row drives |
| Use Project Default Mode | on | Use the project's Default Mode instead of Mode |
| Mode | Block | This fluid's own mode |
| Look | Auto | How the surface is drawn: Auto (Block draws Stepped, Dynamic draws Rounded), Stepped, Smooth or Rounded |
| Viscosity | 0.15 / 0.9 | Seconds between flow steps |
| Flow Rate | 1 / 0.5 | Dynamic: share (0.05 to 1) of a level difference that moves per step |
| Spread Distance | 7 / 3 | 1 to 15. Block: how far a flow reaches over flat ground. Both: how far it looks for an edge |
| Min Layer | 1 / 4 | Dynamic: a layer this thin (in sixteenths) stays put as a puddle |
| Max Fall Per Step | 2 / 1 | Voxels a falling voxel drops per step through open air |
| Pressure | off | Dynamic: connected bodies even out through submerged passages |
| Evaporates | off | Dynamic: thin layers dry up a part at a time |
| Evaporation Seconds | 20 | Seconds per part lost |
| Evaporate At Or Below | 2 | Layers this thin (sixteenths) or thinner evaporate |
| Sources Multiply | off | Block: a flowing voxel resting on something, with two or more still neighbours, becomes a new source |

## Reactions
**Reactions** are rows checked in order where a fluid touches a block; the first that applies wins. Every reaction
fires **On Fluid Reaction (Voxel, Fluid, Touching, Result)** on the server.

| Field | What it does |
|---|---|
| Fluid | The fluid whose voxels are checked |
| Touching | The neighbour: another fluid or any block |
| Result | What appears (None: Air) |
| Target | This Cell (the fluid voxel) or Touching Cell (the neighbour) becomes the result |
| Condition | Any, Still Only or Flowing Only |
| Side | Any, Above, Below or Sides |
| Chance | 0 to 1 each check; below 1 the voxel stays awake until it happens |

**By default:** still Molten Rock touching Water turns to Obsidian; flowing Molten Rock touching Water turns to Basalt.

**Washing away:** fluids flow into blocks marked **Fluid Can Destroy** in the block table, and blocks listed in
**Washable Blocks**, replacing them with no drop. **Wash Non-Colliding** adds every block that doesn't collide.
Indestructible blocks are never washed away.

## Emitters and drains
An emitter or drain is an opening set into a solid voxel's surface: any of its six faces, or smooth ground at any
angle. It faces the surface normal and is drawn as a dark hole (a decal), optionally with a grate. One per voxel.

- **Emitter:** puts out fluid along the normal, up to Reach voxels out. A wall emitter jets out and falls, a ceiling
  one drips, a floor one wells up.
  - Block mode: an endless source.
  - Dynamic mode: Parts Per Second (16 = one voxel a second), stopping after Max Parts if set.
- **Drain:** takes in the fluid in front of it at Parts Per Second, or everything at once each step with **Instant** (a
  sink). **Fluid Filter** limits it to one fluid. Both modes flow toward active drains, so a pool drains to empty.
  **On Fluid Drained (Drain, Fluid, Parts)** tells you what it took, so you can pipe it elsewhere.
- **Saving:** kept as the host voxel's metadata, so it saves and replicates. Digging or changing the host removes it.
- **Switching:** **Set Emitter Active** / **Set Drain Active**, from code, Blueprint, or a
  [Laylines](laylines.md) trigger's event.

**Placing them:**

- from code: Add Emitter, Add Emitter On Face, Add Emitter At Point, Trace And Add Emitter, Add Drain On Face, Add Drain
  At Point (use a line-trace hit for the At Point calls);
- in the level: place a **SuperVoxel Fluid Emitter** actor with its arrow pointing out of the surface (tick
  **Drain** in its Emitter settings for a drain). It looks up to Search Voxels behind itself for the surface;
- scattered over the world by **Emitter Rules** (springs in cave walls, drips from ceilings).

| Emitter setting | Default | What it does |
|---|---|---|
| Fluid | Water | The fluid it puts out |
| Parts Per Second | 8 (16 for drains added by code) | Dynamic: sixteenths per second. Block: any rate above 0 is a source |
| Max Parts | 0 | Dynamic: stops after this many parts (0: never) |
| Reach | 1 | 1 to 8 voxels out along the normal |
| Hole Size | 0.4 | Width of the opening, in voxels |
| Active | on | On or off |
| Drain | off | A drain instead of an emitter |
| Fluid Filter | None | Drains: only this fluid (None: any) |
| Instant | off | Drains: take everything in reach each step |
| Grate | off | Draw a grate over the opening |

| Emitter rule setting | Default | What it does |
|---|---|---|
| Emitter | | What each emitter is like (its host, normal and point are filled in per surface) |
| Surface | Walls | Any, Walls, Ceilings or Floors |
| Host Blocks | empty (any solid block) | Blocks that can carry one |
| Chance | 0.002 | Chance a candidate surface gets one |
| Max Per Chunk | 2 | At most this many per chunk |
| Min Depth | 0 | Only this many voxels or more below the ground surface (caves); 0: anywhere |
| Seed | 1 | Same seed, same emitters on every machine and every reload |

Simple springs and drains without an opening are also available: **Set Spring** (Dynamic: a fluid voxel that refills
itself) and **Set Drain** (a solid voxel that takes fluid from the voxel above it).

## Component settings

| Setting | Default | What it does |
|---|---|---|
| Simulate | on | Run the simulation (server or standalone) |
| Tick Automatically | on | Step from the component's tick; off: call Step yourself |
| Resume Saved Flow | on | After a build or load, carry on flow that was still moving |
| Displace On Fill | on | Dynamic: a block placed or fallen into fluid pushes its parts into nearby room |
| Wash Non-Colliding | off | Also wash away every block that doesn't collide |
| Fluid Types, Reactions, Washable Blocks | Water and Molten Rock; lava meets water | See above |
| Max Cell Updates Per Frame | 4096 | Most fluid voxels updated per frame |
| Max Changes Per Frame | 2048 | Most voxel changes written per frame; 256 suits multiplayer |
| Max Milliseconds Per Frame | 2 | Most game-thread time per frame |
| Max Pressure Search, Max Pressure Searches Per Frame | 256, 8 | Limits for Pressure levelling |
| Simulation Radius | 0 | Fluids farther than this (cm) from every player pause; 0: no limit |
| Use Fluid Material | on | Draw fluids with the plugin's liquid material (on every machine) |
| Fluid Material | the plugin's | Your own material for the fluid mesh section |
| Rounded Blur | 0.35 | Rounded look: how much each voxel's fill mixes with its side neighbours' (rounds free edges; 0 = none) |
| Rounded Min Thickness | 0.55 | Rounded look: the thinnest a layer is drawn, as a share of a voxel (0.5 to 1), so thin films still show |
| Rounded Smoothing Seconds | 0.25 | Rounded look: how long the surface takes to follow a change, so flowing water doesn't shimmer |
| Rounded Remesh Seconds | 0.1 | Rounded look: at most one new mesh per chunk this often |
| Max Rounded Meshes Per Frame | 4 | Rounded look: most chunk meshes started per frame (built on worker threads) |
| Emitter Rules | empty | Scatter rules (see above) |
| Show Emitter Holes, Hole Material | on, the plugin's | The opening decals |
| Target World | the owner | The world to simulate |

Every setting can be changed from C++ or Blueprint at any time. After changing rows in place, or the project settings,
call **Notify Data Changed** (the setters do it for you).

## Blueprint nodes and C++ functions
All on the component (`USuperVoxelFluidComponent`) unless noted.

| Group | Functions |
|---|---|
| Turn on | Enable Fluids, Get Fluids (`USuperVoxelFluidLibrary`) |
| Editing | Add Fluid (Parts 1 to 16, Still), Remove Fluid, Set Spring, Set Drain, Wake Voxel, Wake Area, Wake All, Step |
| Reading (any machine) | Get Fluid Parts, Get Fluid Level (0 to 1), Get Fluid Name, Is Fluid Still, Get Fluid Surface Height, Get Flow Direction |
| Data | Set/Get/Remove Fluid Type, Set Fluid Mode, Get Fluid Mode, Set Reactions, Set Washable Blocks, Notify Data Changed, Get Default Fluid Types, Get Default Reactions |
| Emitters | Add Emitter, Add Emitter On Face, Add Emitter At Point, Trace And Add Emitter, Add Drain On Face, Add Drain At Point, Remove Emitter, Set Emitter Active, Set Drain Active, Get Emitter, Get Emitters, Get Emitter Output |
| Look | Set Fluid Look, Get Fluid Look, Set Use Fluid Material, Set Fluid Material, Get Fluid Material Instance, Set Rounded Blur, Set Rounded Min Thickness, Get Surface Meshes |
| Stats | Get Num Active Cells, Get Num Parked Cells, Get Last Frame Ms, Get Last Frame Breakdown (Housekeeping, Openings, Cells, Apply Edits), Get Last Frame Updates, Get Last Frame Changes, Get Total Parts (bounded worlds), Is Simulating |
| Events | On Fluid Reaction, On Fluid Drained (server) |
| Project settings | Get SuperVoxel Fluid Settings (Default Mode) |

On a client, Add Fluid and Add Emitter ask the server.

## The look
- The plugin's liquid material (`M_SuperVoxelFluids_Liquid`) draws ripples on water tops, streaks and foam on falling
  water, and crust with glowing cracks on any fluid whose block gives light. Its parameters: Normal Strength, Waterfall
  Speed, Foam Strength, Lava Glow Strength (through Get Fluid Material Instance).
- **The plugin draws every fluid** in its own meshes, and the world draws none (the world's
  [fluid surface](meshing.md#fluid-surfaces) is set to Hidden). So when only fluid changes, chunk meshes aren't
  rebuilt. Collision, traces and queries work as before.
- **Look per fluid type**, set with the row's **Look** or **Set Fluid Look** (the same way on every machine):

  | Look | What it draws |
  |---|---|
  | Auto (default) | Stepped in Block mode, Rounded in Dynamic mode |
  | Stepped | Flat tops, one height per voxel: the classic blocky look |
  | Smooth | Levels with each top corner averaged with its neighbours |
  | Rounded | One smooth surface through the fill levels: rounded free edges, beads where it drips, no seams, eased over time |

- **Resting pools are flat.** A Rounded pool's surface sits at its fill level, and only free edges round off, so
  water lies flat against stone walls with no dome or rim.

## The demo
A **SuperVoxel Fluid Demo** actor (`ASuperVoxelFluidDemo`) builds, when play begins: a stone pool, a waterfall from a
ledge channel, lava running into a water basin (Basalt and Obsidian), Block and Dynamic side by side (Water as an
endless source, Salt Water as a tank that empties), a cliff spring, a ceiling drip, and a grated drain that switches
every 8 seconds while a spring refills its basin.

## How it runs
- **Only moving fluid costs time.** Settled bodies sleep; an edit next to fluid wakes it, so digging a lake shore lets
  the water run in.
- **Budgeted.** A big flood slows down instead of hitching the frame. Each fluid steps at its own viscosity.
- **Ordinary edits.** Every change is a gameplay edit, so protection volumes and Can Edit Voxel apply.
- **Saves and multiplayer.** Levels live in the voxel state byte (bits 0 to 4; bits 5 to 7 stay yours). Saves need
  nothing extra, and flow saved mid-run carries on after loading. Only the server (or standalone) simulates; clients
  receive ordinary edits. Set the same fluid types on every machine.
- **Unbounded worlds.** Fluid pauses at unloaded chunks and carries on when they load.

## Limits
- One emitter or drain per voxel.
- Get Total Parts reads the whole world, so it is for tests and tools, and returns -1 in unbounded worlds.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| Water doesn't move | No fluids component, Simulate is off, or the fluid has no row | Add the component (Enable Fluids), tick Simulate, add a row |
| Water flows on the server only | Clients don't simulate; they get edits | Expected. Check the world replicates |
| A lake never empties | Block mode: still voxels are endless sources | Use Dynamic mode, or remove the sources |
| Water stops at a plant | The plant isn't washable | Tick Fluid Can Destroy, or add it to Washable Blocks |
| A big flood is slow | The per-frame budget | Raise Max Cell Updates and Max Milliseconds, or set Simulation Radius |
| An emitter vanished | Its host voxel was dug or changed | Add it again on a solid voxel |
| Lag in multiplayer during floods | Many changes per frame | Lower Max Changes Per Frame (256) |
