---
title: "Surface spawn rules"
parent: Features
nav_order: 15
---
# Surface spawn rules (scatter)

> Scatter meshes such as grass, flowers, pebbles and bushes on the world's open-sky surface. Placement comes from the
> world seed, so every machine shows the same props without replicating them, and props update where the ground is
> edited.

## Turn it on or off
Add a **Super Voxel Scatter** component (`USuperVoxelScatterComponent`) to the voxel world, or to any actor with **World** set.
Remove the component, or leave **Rules** empty, and nothing runs.

## The 3 settings you'll use most

| Setting | What it does | Default |
|---|---|---|
| Mesh | The static mesh to scatter | none |
| On Blocks | Surface blocks it grows on (empty = any solid block) | empty |
| Density | Instances per square meter | 0.2 |

## Example: grass on turf
**Blueprint/editor:** select the world, Add Component > Super Voxel Scatter, add a rule, set Mesh and add `GrassTurf` to On
Blocks.
**C++:**
```cpp
#include "SuperVoxelScatterComponent.h"

USuperVoxelScatterComponent* Scatter = NewObject<USuperVoxelScatterComponent>(World);
FSuperVoxelScatterRule Grass;
Grass.Mesh = GrassMesh;                 // your UStaticMesh*
Grass.OnBlocks = { TEXT("GrassTurf") };
Grass.Density = 1.5f;
Grass.MaxSlope = 35.f;
Scatter->Rules.Add(Grass);
Scatter->RegisterComponent();           // it binds to its owner world and places the props
```

## All settings
**Component**

| Setting | Type | Default | What it does |
|---|---|---|---|
| Rules | array | empty | One rule per kind of prop |
| World | voxel world | the owner | The world to scatter on; empty = the owner, if it's a voxel world |
| Tile Size | int 8..128 | 32 | Columns of this many voxels share one instance component per rule |
| Update Budget Ms | float ≥ 0 | 2 | Most milliseconds per frame spent updating props, nearest tiles first; 0 = no limit |
| Hide Above Cutaway | bool | on | Hide props on ground the [cutaway](cutaway.md) slices off; they come back when the cut moves away |

**Rule (`FSuperVoxelScatterRule`)**

| Setting | Type | Default | What it does |
|---|---|---|---|
| Mesh | Static Mesh | none | What to place |
| Material | Material | none | Optional material for every slot of the mesh |
| On Blocks | names | empty | Surface blocks it grows on (empty = any solid block) |
| Density | float ≥ 0 | 0.2 | Instances per square meter |
| Max Slope | degrees 0..90 | 30 | Steepest ground it stands on |
| Scale Range | 2D vector | 0.8, 1.2 | Uniform scale range |
| Scale Multiplier | vector | 1, 1, 1 | Extra non-uniform scale (multiplies the uniform one) |
| Align To Surface | bool | false | Lean with the ground instead of standing upright |
| Sink | float | 4 | Sinks into the ground, in world units (hides the bottom edge on slopes) |
| Cull Distance | float ≥ 0 | 12000 | Beyond this distance instances aren't drawn (0 = always drawn) |
| Collision | bool | false | Instances have collision |
| Cast Shadows | bool | true | Instances cast shadows |

## Blueprint nodes and C++ functions

| Name | Blueprint | C++ | What it does |
|---|---|---|---|
| Rebuild All | yes | `void RebuildAll()` | Rebuilds every prop. Only needed after changing Rules |
| Flush Updates | yes | `void FlushUpdates()` | Applies every pending edit and cutaway update now, ignoring Update Budget Ms |
| Has Pending Updates | yes | `bool HasPendingUpdates() const` | True while tiles or columns still wait for their props |
| Mark All Tiles Dirty | yes | `void MarkAllTilesDirty()` | Re-checks every column with ground over the next ticks (after changing a rule in place) |
| Get Num Instances In Column | yes | `int32 GetNumInstancesInColumn(int32 X, int32 Y) const` | Props standing on one column, over every rule |
| Get Last Update Stats | yes | `void GetLastUpdateStats(int32& ColumnsChecked, int32& ColumnsChanged, float& Milliseconds) const` | The last update's cost |
| Get Num Instances | yes | `int32 GetNumInstances() const` | Props placed |

## Saves, loads and streaming
Props come from the voxels plus the seed, so they follow saves, loads and streaming with nothing to save: a dug column
stays bare after a load, and refilled ground grows the same props again.

Rules, World, Tile Size and Hide Above Cutaway can be changed from code at runtime; the props rebuild.

## How it updates
- **Edits update props in place.** After any change (Set Block, Apply Brush, collapse, structures, network edits),
  only the edited columns plus one around them are checked.
- A column's props change only if its ground block, the heights around it or the cutaway changed. A prop goes when
  its ground block is removed or is no longer the surface. Props elsewhere never change.
- Placement stays the same for the same seed, on every machine.
- Re-meshing (changing the mesh style, ambient occlusion or greedy meshing) doesn't touch props. A world rebuild (a
  load or a reset) compares columns instead of clearing everything.
- Cost: a one-voxel dig checks 9 columns, in about 0.02–0.08 ms in the demo.

## Limits and performance
- Each rule gets one hierarchical instanced mesh component per tile. Bigger tiles mean fewer components but slower
  updates after an edit.
- Props sit on the open-sky surface only, not in caves.
- Collision is off by default; turn it on only for props players should bump into.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| Props vanish when the cutaway is on | Hide Above Cutaway | Expected; untick it to keep them |
| No props appear | Empty rules, no Mesh, or On Blocks names don't match the surface | Check the names against the block set |
| Props float after a dig | Updates are spread over frames (Update Budget Ms) | Call Flush Updates if you need them at once |
| A rule changed in place has no effect | Existing props aren't re-checked | Call Mark All Tiles Dirty, or Rebuild All |
| Props on steep cliffs | Max Slope is too high | Lower it |
