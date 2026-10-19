---
title: "Structures and villages"
parent: Features
nav_order: 12
---
# Structures and villages

> A structure template is a saved box of blocks, such as a cottage, a hut, a tower or a ruin, that you can stamp into
> the world, rotated or mirrored. Rules can scatter structures and villages over a new world from its seed, and you
> can place them yourself from Blueprint or C++.

## How do I...?
- **Place a cottage where I click:** `Place Structure At (Template, Location)`.
- **Build a village:** `Spawn Village (Rule, Location)`.
- **Add ruins to every new world:** add a **Structure Rule** to the world's **Structure Rules**.
- **Make my own structure:** build it in a world, then capture it with a **SuperVoxel Structure Capture** actor
  (below).

## Turn it on or off
Off unless you use it. With the world's **Structure Rules** and **Village Rules** empty (the default), nothing is
added at generation. The placement nodes do nothing until you call them.

## The 3 settings you'll use most

| Setting | What it does | Default |
|---|---|---|
| Rotation | Quarter turns around the vertical axis (0-3) | 0 |
| Air | **Clear**: the template's air hollows out the world (a house's rooms in a hillside). **Keep World**: the template's air leaves the world as it is (a ruin among the hills) | Clear |
| Anchor To Surface | Move the anchor to the ground surface at the target column | on |

## Samples
`/SuperVoxel/Structures/ST_Cottage`, `ST_Hut`, `ST_Tower` and `ST_Ruin`.

## Example: place a cottage where the player looks
**Blueprint:** Trace From Camera → Place Structure At (Template =
ST_Cottage, Location = Hit Location, Rotation = 1)

**C++:**
```cpp
#include "SuperVoxelWorld.h"
#include "SuperVoxelLibrary.h"
#include "SuperVoxelStructure.h"

const FSuperVoxelHit Hit = USuperVoxelLibrary::TraceFromCamera(this, World, 3000.f);
if (Hit.bHit)
{
	World->PlaceStructureAt(CottageTemplate, Hit.Location, /*Rotation*/ 1); // CottageTemplate: a UPROPERTY set to ST_Cottage
}
```

**C++: full control with a placement**
```cpp
FSuperVoxelStructurePlacement Place;
Place.Template = TowerTemplate;
Place.Voxel = World->WorldToVoxel(Location);
Place.Rotation = 2;
Place.bMirror = true;
Place.Air = ESuperVoxelStructureAir::KeepWorld;
const int32 Changed = World->PlaceStructure(Place);
```

## Make your own structure
1. Build it in a voxel world: sculpt it in the editor, or dig and place in game.
2. Place a **SuperVoxel Structure Capture** actor over it and size its box. The box snaps to whole voxels.
3. Set **Asset Path** (for example `/Game/Structures/ST_MyHouse`) and **Anchor At**: X and Y as a share of the
   footprint (0.5 = middle), Z in voxels from the bottom.
4. Press **Capture To Asset**. The asset is created, or overwritten.

From code, `Capture Structure (Min, Max)` copies a box of voxels into a new template. It isn't saved to disk; save
it with the capture actor in the editor.

## All settings
**Template (`USuperVoxelStructureTemplate`)**

| Setting | Default | What it does |
|---|---|---|
| Size | 0, 0, 0 | Size in voxels |
| Anchor | bottom middle | The template voxel placed at the target voxel |
| Palette | | Block names used by the template (stored by name, so it survives block set changes) |
| Foundation Depth | 0 | Layers below the anchor that are always placed, even where the ground falls away |
| Foundation Block | StonyLoam | Fills under the footprint down to the ground on uneven surfaces (None = leave gaps) |
| Entrance | 0, 0, 0 | The door, where village paths connect |

**Placement (`FSuperVoxelStructurePlacement`)**

| Setting | Default | What it does |
|---|---|---|
| Template | | The template to stamp |
| Voxel | 0, 0, 0 | World voxel the anchor goes to |
| Rotation | 0 | Quarter turns (0-3) |
| Mirror | off | Mirror along the template's X axis before rotating |
| Air | Clear | Clear or Keep World (see above) |
| Anchor To Surface | on | Stand it on the ground at the target column |
| Keep Indestructible | on | Leave indestructible blocks (the world floor) untouched |

**Structure rule (`FSuperVoxelStructureRule`)**, on the world's **Structure Rules**

| Setting | Default | What it does |
|---|---|---|
| Templates | | One is picked per spawn, evenly |
| On Blocks | empty | Surface blocks it may stand on (empty = any solid ground that isn't liquid) |
| Spacing | 48 m | At most one per square cell of this size (also the minimum spacing) |
| Chance | 0.35 | Chance that a cell gets one |
| Max Slope | 3 voxels | Most height difference across the footprint (rejects steep spots) |
| Air | Clear | Clear or Keep World |
| Salt | 1 | Mixed into the seed so rules don't line up with each other |

**Village rule (`FSuperVoxelVillageRule`)**, on the world's **Village Rules** or passed to Spawn Village

| Setting | Default | What it does |
|---|---|---|
| Houses | | House templates |
| Min Houses, Max Houses | 3, 6 | How many houses |
| Radius | 18 m | How far houses spread from the center |
| Path Block | PackedPath | Block of the paths between the doors and the center |
| Spacing | 0 | At generation: at most one village per square cell of this size (0 = never at generation; Spawn Village only) |
| Chance | 0.5 | Chance that a cell gets one |
| Max Slope | 3 voxels | Most height difference across a house footprint |
| On Blocks | empty | Surface blocks houses stand on (empty = any dry ground) |
| Salt | 7 | Mixed into the seed |

## Blueprint nodes and C++ functions (on the world)

| Name | Blueprint | C++ | What it does |
|---|---|---|---|
| Place Structure | yes | `int32 PlaceStructure(const FSuperVoxelStructurePlacement&)` | Stamps a template. Returns voxels changed (0 on a client, which asks the server) |
| Place Structure At | yes | `int32 PlaceStructureAt(Template, Location, Rotation = 0, bMirror = false, Air = Clear)` | Stamps a template at a world location, on the ground |
| Spawn Village | yes | `int32 SpawnVillage(const FSuperVoxelVillageRule&, FVector Location, int32 VillageSeed = 0)` | Builds a village. Returns the number of houses (0 on a client) |
| Capture Structure | yes | `USuperVoxelStructureTemplate* CaptureStructure(FIntVector Min, FIntVector Max, UObject* Outer = nullptr)` | Copies a box (inclusive) into a new, unsaved template |
| Get Num Solid Voxels | yes (on a template) | `int32 GetNumSolidVoxels() const` | Solid voxels in a template |

## Limits
- Rules (spawned at generation) run in bounded worlds only. Place Structure and Spawn Village work in unbounded
  worlds too.
- A village is one cluster with straight paths.
- On a client, Place Structure and Spawn Village ask the server and return 0; the change arrives a moment later.

## Troubleshooting

| Message or problem | Why | Fix |
|---|---|---|
| "Structure capture: no built SuperVoxel world in this level." | No world, or it isn't built | Turn on Preview In Editor and let the world build |
| "Structure capture: the box is outside the world." | The capture box doesn't overlap the world | Move it over the world |
| "Structure capture: couldn't save X." | The asset path is invalid or read-only | Use a long package path like `/Game/Structures/ST_MyHouse` |
| A structure floats on a slope | Foundation Block is None | Set a Foundation Block |
| No structures appear | Rules empty, Chance 0, or the ground is too steep (Max Slope) | Check the rule |
