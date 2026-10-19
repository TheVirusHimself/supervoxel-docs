---
title: "Cutaway view"
parent: Features
nav_order: 9
---
# Cutaway view

> Hide everything above a chosen height to look inside caves, mines and buildings. It only changes what's drawn.

## Turn it on or off
- **On:** `Set Cutaway Height (Z)` with a voxel height.
- **Off:** `Set Cutaway Height (-1)`. Off is the default, and it costs nothing while off.

## The settings

| Node | What it does | Default |
|---|---|---|
| Set Cutaway Height | Hides everything above voxel height Z; -1 = off | -1 (off) |
| Get Cutaway Height | The current height, or -1 | |

## Example: step the cut down and up
**Blueprint:** key Z → Get Cutaway Height − 1 → Set Cutaway Height

**C++:**
```cpp
#include "SuperVoxelWorld.h"

void AMyPlayerController::CutawayDown(ASuperVoxelWorld* World)
{
	const int32 Current = World->GetCutawayHeight();
	const int32 Start = World->WorldSize.Z - 1;
	World->SetCutawayHeight(FMath::Max(0, (Current < 0 ? Start : Current) - 1));
}

void AMyPlayerController::CutawayOff(ASuperVoxelWorld* World)
{
	World->SetCutawayHeight(-1);
}
```

## How it works
- Chunks the cut passes through get a second, display-only mesh drawn up to the cut.
- **Collision still uses the full world:** characters stand on hidden voxels. The cut slices themselves have no
  collision.
- **Trace Voxel skips hidden voxels**, so it hits what's drawn. Its Include Cut Away option (advanced) traces through
  them too. Use it for cursors, not physics line traces.

## Blueprint nodes and C++ functions

| Name | Blueprint | C++ |
|---|---|---|
| Set Cutaway Height | yes | `void SetCutawayHeight(int32 Z)` |
| Get Cutaway Height | yes | `int32 GetCutawayHeight() const` |

## Limits and performance
- Changing the height doesn't stall the game: the slice is meshed in the background and appears a few frames later.
  Until then each chunk keeps its previous look.
- Cost in the demo: the worst frame after a step is about 30–40 ms.
- Characters still collide with hidden voxels.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| A character walks on something invisible | Collision ignores the cutaway | Expected: it's a view, not an edit |
| Clicks hit hidden voxels | Your own physics trace sees the full world | Use `Trace Voxel`, which skips what the cutaway hides |
