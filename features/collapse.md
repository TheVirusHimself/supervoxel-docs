---
title: "Collapse"
parent: Features
nav_order: 10
---
# Collapse

> When a dig leaves a piece with no support, it falls straight down until it lands.

## Turn it on or off
On the world: **Collapse After Dig** (`bCollapseAfterDig`). It's **off** by default. While it's off, nothing extra
runs after digs.

## The settings

| Setting | Where | What it does | Default |
|---|---|---|---|
| Collapse After Dig | World > SuperVoxel > Editing | After digs, pieces that lost all support fall | Off |
| Max Piece Size | C++ `CollapseUnsupported` | Pieces larger than this (in voxels) stay standing | 20000 |

## What counts as supported
A solid piece is supported while it still connects to the world's floor or to an indestructible block. A piece that
connects to neither falls straight down until it lands.

## Example
**Blueprint:** tick **Collapse After Dig** on the world. That's all: every dig checks for unsupported pieces.

**C++** (run it yourself, for example after your own edits):
```cpp
#include "SuperVoxelWorld.h"

// Voxels you just emptied; pieces touching them are checked.
TArray<FIntVector> Emptied = { FIntVector(10, 12, 20) };
const int32 Fell = World->CollapseUnsupported(Emptied);           // MaxPieceSize defaults to 20000
```

## Blueprint nodes and C++ functions

| Name | Blueprint | C++ | What it does |
|---|---|---|---|
| Collapse After Dig | property | `bool bCollapseAfterDig` | Turns automatic collapse on |
| (C++ only) | no | `int32 CollapseUnsupported(TConstArrayView<FIntVector> Seeds, int32 MaxPieceSize = 20000)` | Lets unsupported pieces touching Seeds fall. Returns the number of voxels that fell |

## Limits and performance
- Very large pieces (over Max Piece Size) are left standing, so one dig can't drop half the map.
- Indestructible blocks never move.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| Nothing falls | Collapse After Dig is off, or the piece still touches the floor or an indestructible block | Turn it on; check the piece is really cut off |
| A huge overhang stays up | It's bigger than Max Piece Size | Expected; call `CollapseUnsupported` with a larger limit if you want it to fall |
