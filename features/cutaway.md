---
title: "Cutaway view"
parent: Features
nav_order: 9
---
# Cutaway view

<!-- Status: checked against 0f6bdf3 (headers) -->

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
- **Collision and traces still use the full world.** The one exception is the Visibility trace channel, which
  follows what's shown, so clicks land on what the player sees.

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
| Clicks pass through to hidden voxels | Your trace uses a channel other than Visibility | Trace on Visibility, or use `Trace Voxel` and compare with the cut height |
