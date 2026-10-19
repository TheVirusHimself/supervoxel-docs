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

## Building in code without your build falling mid-way
Separate Set Block and brush calls are each checked for collapse right away. If you build piece by piece from code,
for example an arch from its top down or a floor before its pillars, a half-built part can fall before its support is
placed. Wrap the build in **Begin Defer Collapse** and **End Defer Collapse**: nothing collapses or falls in between,
and End runs one collapse and falling-block check over everything dug meanwhile.

- Calls nest: the check runs at the outermost End. **Is Collapse Deferred** tells you whether you're inside one.
- One brush, structure or Apply Changes call is already checked once, after the whole batch. You only need this for a
  build made of many separate calls.
- In Blueprint, always pair each Begin with an End, including on early exits.

**Blueprint:** Begin Defer Collapse → your Set Block / Apply Brush calls → End Defer Collapse.

**C++:** `FSuperVoxelDeferCollapse` is the same as a scope; the check runs when it ends.
```cpp
#include "SuperVoxelWorld.h"

void BuildBridge(ASuperVoxelWorld* World, FIntVector Start, int32 Length)
{
	FSuperVoxelDeferCollapse Defer(World); // nothing falls until this scope ends
	for (int32 X = 0; X < Length; ++X)
	{
		World->SetBlock(Start + FIntVector(X, 0, 0), TEXT("OakPlanks")); // the deck first...
	}
	World->SetBlock(Start + FIntVector(0, 0, -1), TEXT("OakLog"));          // ...then its supports
	World->SetBlock(Start + FIntVector(Length - 1, 0, -1), TEXT("OakLog"));
} // one collapse check here, with the bridge complete
```

## Blueprint nodes and C++ functions

| Name | Blueprint | C++ | What it does |
|---|---|---|---|
| Collapse After Dig | property | `bool bCollapseAfterDig` | Turns automatic collapse on |
| Begin Defer Collapse, End Defer Collapse | yes | `void BeginDeferCollapse()`, `void EndDeferCollapse()` | Nothing collapses or falls in between; End runs one check. Nests |
| Is Collapse Deferred | yes | `bool IsCollapseDeferred() const` | Whether a Begin is still open |
| (C++ scope) | no | `FSuperVoxelDeferCollapse(ASuperVoxelWorld*)` | Begin when made, End when it goes out of scope |
| (C++ only) | no | `int32 CollapseUnsupported(TConstArrayView<FIntVector> Seeds, int32 MaxPieceSize = 20000)` | Lets unsupported pieces touching Seeds fall. Returns the number of voxels that fell |

## Limits and performance
- Very large pieces (over Max Piece Size) are left standing, so one dig can't drop half the map.
- Indestructible blocks never move.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| Nothing falls | Collapse After Dig is off, or the piece still touches the floor or an indestructible block | Turn it on; check the piece is really cut off |
| A part falls while my code is still building it | Each separate call is checked at once | Wrap the build in Begin/End Defer Collapse (C++: `FSuperVoxelDeferCollapse`) |
| A huge overhang stays up | It's bigger than Max Piece Size | Expected; call `CollapseUnsupported` with a larger limit if you want it to fall |
