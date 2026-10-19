---
title: "Queries and regions"
parent: Features
nav_order: 20
---
# Queries and regions

> Ask the world questions (where's the nearest ore, how much stone is in this box, where's the ground) and copy and
> paste boxes of voxels. The nodes are in the **SuperVoxel query library** (`USuperVoxelQueryLibrary`).

## How do I...?
- **Find the nearest iron ore:** `Find Nearest Block (World, Location, "IronOre", 64)`.
- **Find the ground under a tree:** `Find Surface` with the leaves and logs in **Pass Through**.
- **Spawn things on the ground:** `Sample Surface` gives transforms turned to the slope.
- **Copy a building and paste it elsewhere:** `Copy Voxel Region`, then `Paste Voxel Region`.

## Turn it on or off
Nothing runs until you call a node.

## The 3 nodes you'll use most

| Node | What it gives |
|---|---|
| Find Blocks In Sphere | Voxels of the given blocks (empty list: any solid), nearest first |
| Find Surface | Up or down a column to the ground |
| Paste Voxel Region | Pastes a copied box as one edit |

## Example: count the ore in an area
**Blueprint:** Count Blocks In Box (World, Min, Max, Blocks = [IronOre, DeepIronOre]).

**C++:**
```cpp
#include "SuperVoxelQueries.h"

const int32 Iron = USuperVoxelQueryLibrary::CountBlocksInBox(World, Min, Max, { TEXT("IronOre") });

FIntVector Ore;
if (USuperVoxelQueryLibrary::FindNearestBlock(World, GetActorLocation(), TEXT("IronOre"), 64, Ore))
{
	// Ore is the voxel.
}
```

## Queries

| Node | C++ | What it gives |
|---|---|---|
| Find Blocks In Box | `FindBlocksInBox(World, Min, Max, Blocks, MaxResults = 1000)` | Voxels of the given blocks (empty: any solid), nearest first |
| Find Blocks In Sphere | `FindBlocksInSphere(World, Center, Radius, Blocks, MaxResults = 1000)` | The same in a sphere |
| Count Blocks In Box | `CountBlocksInBox(World, Min, Max, Blocks)` | How many |
| Count Block Types In Box | `CountBlockTypesInBox(World, Min, Max)` | A map of block to count |
| Find Nearest Block | `FindNearestBlock(World, Location, Block, MaxDistance, OutVoxel)` | The nearest voxel of one block type |
| Find Surface | `FindSurface(World, From, bSearchUp, MaxDistance, OutVoxel, PassThrough)` | The ground up or down a column. Pass Through lists blocks to treat as air (leaves, plants) |
| Is Area Editable | `IsAreaEditable(World, Min, Max)` | Inside the world and not in a [protection volume](editing.md#protection-volumes) |
| Sample Surface | `SampleSurface(World, Min, Max, OnBlocks, Spacing = 2, MaxSlope = 40, Jitter = 0.5, Seed = 0)` | Ground points every N columns (jittered, repeatable by seed, filtered by block and slope), as transforms turned to the slope; for spawning things or feeding PCG |

## Regions: copy and paste
- **Copy Voxel Region** (`CopyVoxelRegion(World, Min, Max)`) copies a box: blocks by name, states and metadata.
- **Paste Voxel Region** (`PasteVoxelRegion(World, Region, Origin, Mask, QuarterTurns, bMirror, Replace)`) pastes it
  as one gameplay edit, saved and replicated. Paste on the server.
- **Get Turned Region Size** (`GetTurnedRegionSize(Region, QuarterTurns)`) gives the size after turning.

| Mask | What it does |
|---|---|
| All | Every voxel of the region, air included: the box becomes exactly the copy |
| Skip Air | Only the copy's solid voxels; where it has air, the world keeps what it has |
| Only Into Air | Only into the world's air; nothing already there is replaced |
| Replace Listed | Only over world voxels whose block is in the Replace list |

## Limits
- One query reads at most 16 million voxels. A bigger box is clipped, with a warning.

## Troubleshooting

| Message or problem | Why | Fix |
|---|---|---|
| "SuperVoxel query: the box is larger than N voxels; only its lower part is read." | Over 16 million voxels | Query smaller boxes |
| "Paste Voxel Region: paste on the server (clients see it through replication)." | Called on a client | Paste on the server |
| Find Surface stops at a treetop | Leaves count as ground | Add them to Pass Through |
