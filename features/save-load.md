---
title: "Save and load"
parent: Features
nav_order: 8
---
# Save and load

<!-- Status: checked against 0f6bdf3 (headers) -->

> A world is its seed plus the list of changes made to it (the edit journal). Saving stores only the changes, so saves
> stay small. Loading rebuilds the world from the seed and replays them.

## How do I...?
- **Save to a slot:** `Save To Slot ("Slot1")`. **Load it:** `Load From Slot ("Slot1")`.
- **Put the edits in my own save game:** `Save Edits` gives you a byte array; store it, then pass it to `Load Edits`
  later.
- **Go back to the generated world:** `Reset Edits`.

## Turn it on or off
Nothing is saved unless you call a save node. Edits made in the editor are always saved with the level.

## The 3 nodes you'll use most

| Node | What it does |
|---|---|
| Save To Slot | Saves seed, size and edits to a save-game slot |
| Load From Slot | Loads them and rebuilds |
| Get Num Edits | How many voxels have changed since generation |

## Example
**Blueprint:** key F5 → Save To Slot; key F9 → Load From Slot

**C++:**
```cpp
#include "SuperVoxelWorld.h"

void AMyGameMode::SaveWorld(ASuperVoxelWorld* World)
{
	World->SaveToSlot(TEXT("World1"));
}

void AMyGameMode::LoadWorld(ASuperVoxelWorld* World)
{
	if (!World->LoadFromSlot(TEXT("World1")))
	{
		// No slot yet, or it doesn't fit this world: see the log.
	}
}
```

## What's in a save
- **Save To Slot** writes a `USuperVoxelSaveGame`: the seed, the world size and the edits.
- **Save Edits** returns only the edits, as bytes. They record **block names, not ids**, so a save still loads after
  you add or reorder block types.
- The edits don't include the seed. If you store them yourself, store the seed and world size too.
- **Two kinds of edits:**
  - *baked edits*: made in the editor with the sculpt mode, saved with the level;
  - *runtime edits*: made while playing. These are what Save Edits and Save To Slot store.

## Blueprint nodes and C++ functions

| Name | Blueprint | C++ | What it does |
|---|---|---|---|
| Save Edits | yes | `TArray<uint8> SaveEdits() const` | The runtime edits as bytes |
| Load Edits | yes | `bool LoadEdits(const TArray<uint8>& Data)` | Replaces the runtime edits and updates the world. False if the data doesn't fit this world |
| Save To Slot | yes | `bool SaveToSlot(const FString& SlotName, int32 UserIndex = 0)` | Seed, size and edits to a slot |
| Load From Slot | yes | `bool LoadFromSlot(const FString& SlotName, int32 UserIndex = 0)` | Loads a slot written by Save To Slot and rebuilds |
| Reset Edits | yes | `void ResetEdits()` | Forgets the runtime edits and sets the world back to as generated (plus baked edits) |
| Get Num Edits | yes | `int32 GetNumEdits() const` | Voxels changed since generation |

## No rebuild on load or reset
`Load Edits` and `Reset Edits` (same seed and world size) don't rebuild the world. It stays on screen, the voxels
that differ are set as one batch of edits, and edits made meanwhile are kept. In multiplayer, clients get the change
like any edit.

- `Get Num Edits` changes at once; the voxels change a moment later, because the generated world is rebuilt on a
  worker thread first. With **Async Meshing** off, it all happens before the call returns.
- `Load From Slot` with a different seed or size, `Set Seed And Regenerate`, and unbounded worlds still do a full
  rebuild.

## Limits
- Loading happens on the server (or in a standalone game). In multiplayer the server loads and clients receive the
  result.
- Load Edits fails if the data was saved for a world of a different size, or by a newer plugin version. Saves from
  older versions of the edit format still load.
- **Unbounded worlds:** edits are stored by position, including edits to chunks that aren't loaded; they're applied
  when the chunk loads ([Unbounded worlds](streaming.md)).
- An edit naming a block that no longer exists loads as Air.
- Load Edits, Load From Slot and Reset Edits keep the seed they load or already have, even with Random Seed on.

## Troubleshooting

| Message or problem | Why | Fix |
|---|---|---|
| "LoadEdits: only the server can load edits." | Called on a client | Load on the server |
| "LoadEdits: saved for a world of a different size" | The world size changed since the save | Use the same World Size, or use Load From Slot (it restores the size) |
| "LoadEdits: saved by a newer SuperVoxel version" | The save is from a later version | Update the plugin |
| "LoadEdits: not SuperVoxel edit data" / "corrupt edit data" | The bytes aren't a SuperVoxel save, or are damaged | Check what you passed in |
| "Unknown block 'X', using Air" | The save names a block the set no longer has | Add the block back, or accept Air |
| "the level's baked edits can't be used (...); they're ignored." | The level's editor edits don't fit the world any more | Usually after a big settings change; sculpt again |
