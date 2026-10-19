---
title: "Editing"
parent: Features
nav_order: 6
---
# Editing

> Change the world while playing: set one voxel, or dig, fill, paint, smooth and flatten many at once with a brush.
> Traces tell you which voxel is under the cursor.

## How do I...?
- **Dig where the player looks:** trace from the camera, then apply a Dig brush at the hit (example below).
- **Place a block:** trace, then call `Set Block` on the hit's **Adjacent** voxel (the empty one in front of the face).
- **Read a voxel:** `Get Block At` (its name) or `Get Block Id At` (its number).
- **Stop players editing some voxels:** set `CanEditVoxel` in C++ (see "Allow or refuse edits" below).

## Turn it on or off
Editing is always available on the world, and nothing runs until you call it. To stop players editing, don't call
the edit nodes, or refuse edits with `CanEditVoxel`.

## The 3 settings you'll use most

| Setting | What it does | Default |
|---|---|---|
| Brush **Op** | Dig, Fill, Paint, Smooth or Flatten | Dig |
| Brush **Extent** | Radius (sphere, cylinder) or half size (box), in voxels | 3, 3, 3 |
| Brush **Block** | The block placed by Fill, Paint and Flatten | None |

## Example: dig where the player looks, place with the other button
**Blueprint:** Find Voxel World → Trace From Camera → Branch on
bHit → Make Sphere Brush (Dig) → Apply Brush

**C++:**
```cpp
#include "SuperVoxelWorld.h"
#include "SuperVoxelLibrary.h"

void AMyCharacter::Dig()
{
	ASuperVoxelWorld* World = USuperVoxelLibrary::FindVoxelWorld(this);
	if (!World) return;

	const FSuperVoxelHit Hit = USuperVoxelLibrary::TraceFromCamera(this, World, 1500.f);
	if (Hit.bHit)
	{
		World->ApplyBrush(USuperVoxelLibrary::MakeSphereBrush(ESuperVoxelBrushOp::Dig, Hit.Location, 2.f));
	}
}

void AMyCharacter::Place()
{
	ASuperVoxelWorld* World = USuperVoxelLibrary::FindVoxelWorld(this);
	if (!World) return;

	const FSuperVoxelHit Hit = USuperVoxelLibrary::TraceFromCamera(this, World, 1500.f);
	if (Hit.bHit)
	{
		World->SetBlock(Hit.Adjacent, TEXT("OakPlanks"));
	}
}
```
Your module needs `"SuperVoxel"` in its `Build.cs` dependencies.

## Brushes
A brush (`FSuperVoxelBrush`) is one area edit.

| Field | Type | Default | What it does |
|---|---|---|---|
| Shape | `ESuperVoxelBrushShape` | Sphere | Sphere, Box or Cylinder |
| Op | `ESuperVoxelBrushOp` | Dig | What it does (see below) |
| Center | Vector | 0, 0, 0 | The center, in world space |
| Extent | Vector | 3, 3, 3 | Radius (sphere, cylinder) or half extent on each axis (box), **in voxels** |
| Block | Name | None | Block placed by Fill, Paint and Flatten |
| Strength | Float 0..1 | 1 | Share of the covered voxels affected. 1 = all; lower gives a rough, scattered edit |

| Op | What it does |
|---|---|
| Dig | Removes solid voxels. Indestructible blocks stay. |
| Fill | Fills empty voxels with the brush block. |
| Paint | Replaces the block of solid voxels, keeping the shape. |
| Smooth | Evens out bumps: removes lone solid voxels and fills lone holes, by neighbour count. |
| Flatten | Removes solid voxels above the brush center's height and fills empty ones below it. |

## Traces
`Trace Voxel (Start, End, Hit Fluids, Include Cut Away)` finds the first solid voxel along a line, in world space.
Liquids are passed through unless **Hit Fluids** is on. Voxels hidden by the [cutaway](cutaway.md) are skipped unless
**Include Cut Away** (advanced) is on, so it hits what's drawn: use it for cursors, not physics. `Trace From Camera` does the same from a player's camera through the screen
center.

The result is an `FSuperVoxelHit`:

| Field | What it is |
|---|---|
| bHit | Something was hit |
| Voxel | The solid voxel that was hit |
| Adjacent | The empty voxel in front of the hit face: where a placed block goes |
| FaceNormal | Unit axis of the hit face, pointing out of the voxel |
| Location | The world point where the ray entered the voxel |
| BlockId | Block id of the hit voxel |

## Blueprint nodes and C++ functions

| Name | Blueprint | C++ | What it does |
|---|---|---|---|
| Set Block | yes | `ASuperVoxelWorld::SetBlock(FIntVector Voxel, FName Block)` | Sets one voxel. None or "Air" digs it. True if it changed (on a client: if the request was sent). |
| Apply Brush | yes | `ASuperVoxelWorld::ApplyBrush(const FSuperVoxelBrush&)` | Applies a brush. Returns the number of voxels changed (0 on a client, which asks the server). |
| Trace Voxel | yes | `ASuperVoxelWorld::TraceVoxel(Start, End, bHitFluids = false, bIncludeCutAway = false)` | First solid voxel along a segment |
| Trace From Camera | yes | `USuperVoxelLibrary::TraceFromCamera(WorldContext, World, Distance = 1500, PlayerIndex = 0)` | A trace through the screen center |
| Make Sphere Brush | yes | `USuperVoxelLibrary::MakeSphereBrush(Op, Center, Radius = 2, Block = None, Strength = 1)` | A sphere brush |
| Make Box Brush | yes | `USuperVoxelLibrary::MakeBoxBrush(Op, Center, HalfExtent, Block = None, Strength = 1)` | A box brush |
| Get Block At | yes | `GetBlockAt(FIntVector Voxel)` | Block name of a voxel (Air outside the world) |
| Get Block Id At | yes | `GetBlockIdAt(FIntVector Voxel)` | Block id of a voxel |
| Is Voxel Solid | yes | `IsVoxelSolid(FIntVector Voxel)` | Whether the voxel is solid |
| Get Surface Height | yes | `GetSurfaceHeight(int32 X, int32 Y)` | First air voxel above the highest solid one in a column; -1 for an empty column |
| (C++ only) | no | `ComputeBrush(const FSuperVoxelBrush&, TArray<FSuperVoxelChange>&)` | The changes a brush would make, without making them |
| (C++ only) | no | `ApplyChanges(Changes, ESuperVoxelEditSource, OutPrevious = nullptr)` | The low-level edit that every other edit goes through |

## Allow or refuse edits (C++)
`ASuperVoxelWorld::CanEditVoxel` is a function you can set on the server. It's asked about every gameplay edit;
return false to keep the voxel as it is.
```cpp
World->CanEditVoxel = [](const FIntVector& Voxel, FSuperVoxelBlockId OldBlock, FSuperVoxelBlockId NewBlock)
{
	return Voxel.Z > 4; // keep the bottom layers
};
```
It's only asked about gameplay edits, not loads, network replays or editor sculpting.

## Events

| Event | When it fires | Parameters |
|---|---|---|
| On Voxels Changed | After voxels change (edits, loads, network) | Min, Max: the changed box in voxels (inclusive) |

## Protection volumes
For which block types can break, and a switch that makes a whole world read-only, see
[Destruction settings](destruction.md).

Place a **SuperVoxel Protection Volume** (`ASuperVoxelProtectionVolume`) and size its box. Gameplay edits inside it
are refused: players, brushes, network requests, metadata, damage and falling blocks. Collapse treats it as support
and never drops a piece into it. Editor sculpting and loads still work.

| Setting or node | What it does |
|---|---|
| Protect (on the volume) | Whether edits inside are refused (default on; can change at runtime) |
| Is Voxel Protected (on the world) | `bool IsVoxelProtected(FIntVector Voxel) const`: whether a volume protects a voxel |
| Is Area Editable (query) | Whether a box is inside the world and not protected ([Queries](queries.md)) |

## Characters on edited ground
Characters (any `ACharacter`, including AI and walkers) standing on ground that's dug away fall. Nothing to set up.
**Known issue:** a character resting still far from the edge of a dug pit can stay hovering until it moves.

## Limits and performance
- Edits are batched: the touched chunks rebuild a frame or two later on worker threads (see
  [Background meshing and collision](background-work.md)).
- **Block hardness** is stored for your game code; brushes ignore it.
- **Indestructible** blocks are never removed by digging, brushes or collapse.
- In multiplayer, a client's edit goes to the server first. See [Multiplayer](multiplayer.md).

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| "SetBlock: unknown block 'X'" in the log | No block with that name in the world's block set | Check the name (row names have no spaces, e.g. `OakPlanks`) |
| Apply Brush returns 0 on a client | Clients send the edit to the server, which applies it | Expected; the change arrives a moment later |
| "...needs a USuperVoxelNetComponent on the player controller" | A client edit with no net component | The server adds one to every player automatically; check the world is in the level when players join |
| Dig does nothing at the bottom | The floor block is indestructible | Expected |
| The brush is far too big | Extent is in voxels, not world units | Use small numbers (2-5) |
