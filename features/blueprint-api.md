---
title: "Blueprint library and events"
parent: Features
nav_order: 17
---
# Blueprint library and events

> Helper nodes for the most common jobs, and the events you can bind to. Every node is listed in the
> [A to Z reference](../reference/api-index.md); this page covers the helpers and events.

## Helper nodes (`USuperVoxelLibrary`)

| Node | C++ | What it does |
|---|---|---|
| Find Voxel World | `FindVoxelWorld(WorldContextObject)` | The first voxel world in the level (or none) |
| Make Sphere Brush | `MakeSphereBrush(Op, Center, Radius = 2, Block = None, Strength = 1)` | A sphere brush at a world location (radius in voxels) |
| Make Box Brush | `MakeBoxBrush(Op, Center, HalfExtent, Block = None, Strength = 1)` | A box brush (half extent in voxels) |
| Trace From Camera | `TraceFromCamera(WorldContextObject, World, Distance = 1500, PlayerIndex = 0)` | Traces from a player's camera through the screen center |

## Converting between world and voxels (on the world)

| Node | C++ | What it does |
|---|---|---|
| World To Voxel | `WorldToVoxel(FVector WorldLocation)` | The voxel at a world location |
| Voxel To World | `VoxelToWorld(FIntVector Voxel, bool bBottomCenter = false)` | A voxel's center, or the middle of its bottom face (where feet stand) |
| Get Voxel Size | `GetVoxelSize()` | Voxel edge in world units |

## Events (on the world)

| Event | When it fires | Parameters |
|---|---|---|
| On World Built | Once the world is generated and every chunk is shown | none |
| On Voxels Changed | After voxels change: edits, loads, network | Min, Max: the changed box in voxels (inclusive) |
| On Chunk Meshed (C++ only) | A chunk got a new mesh | the chunk coordinate |

## Example: react to edits
**Blueprint:** Bind Event to On Voxels Changed → print Min and
Max

**C++:**
```cpp
// In your class: UFUNCTION() void HandleVoxelsChanged(FIntVector Min, FIntVector Max);
World->OnVoxelsChanged.AddDynamic(this, &AMyActor::HandleVoxelsChanged);

void AMyActor::HandleVoxelsChanged(FIntVector Min, FIntVector Max)
{
	// Update anything that stands on the voxels in this box.
}
```

## Other events

| Event | On | Page |
|---|---|---|
| On Found, On Failed | Find Voxel Path Async | [Pathfinding](pathfinding.md) |
| On Arrived, On Failed | Path Follower component | [Pathfinding](pathfinding.md) |
