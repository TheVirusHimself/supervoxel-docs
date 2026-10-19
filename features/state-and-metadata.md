---
title: "Voxel state and metadata"
parent: Features
nav_order: 19
---
# Voxel state and metadata

> Every voxel can carry a small number (its **state**, 0–255) and a few key/value pairs (its **metadata**), for things
> like a door being open, an owner, a timer or an inventory id. Both are saved, loaded and replicated with the edits.

## How do I...?
- **Mark a door open:** `Set Block State (Voxel, 1)`; read it back with `Get Block State`.
- **Store who placed a block:** `Set Voxel Meta (Voxel, "Owner", PlayerName)`.
- **Keep a number on a voxel:** `Set Voxel Meta Int` and `Get Voxel Meta Int` (with a default).

## Turn it on or off
Nothing to turn on. Voxels have state 0 and no metadata until you set them.

## The 3 nodes you'll use most

| Node | What it does |
|---|---|
| Set Block With State | Sets a voxel's block and its state together |
| Set Voxel Meta | Sets one metadata value on a voxel |
| Get Voxel Meta | Reads one value (false if the voxel doesn't have it) |

## Example: a door that remembers it's open
**Blueprint:** On interact → Get Block State (Voxel) → if 0: Set Block State (Voxel, 1), else Set Block State
(Voxel, 0).

**C++:**
```cpp
const uint8 Open = World->GetBlockState(Voxel) == 0 ? 1 : 0;
World->SetBlockState(Voxel, Open);
World->SetVoxelMeta(Voxel, TEXT("LastUser"), GetName());
```

## State
- A number from 0 to 255 kept with the voxel's block.
- Changing a voxel's block sets its state to what the change gives (0 by default).
- **Bits 0 to 4 are reserved** for block rotation (see the [Roadmap](../roadmap.md); only for blocks that opt in). Use bits 5 to 7
  for your game.

## Metadata
- Key/value pairs on single voxels. Values are text; the Int nodes store and read whole numbers.
- **Changing a voxel's block clears its metadata.** Falling blocks, collapse and region pastes carry it along.
- Works in bounded and unbounded worlds.

## Voxel tint
Colour single voxels of a block (signs, pixel walls, dyed blocks): tick **Tintable** on the block in the block table,
then set a tint per voxel.

- The tint multiplies the block's colour and glow, so a white or light texture gives flat colours.
- It's set on the server, and saved and replicated like metadata (under the key `SV.Tint`). A new block starts
  untinted.
- Blocky faces only; 8 bits per channel.

```cpp
World->SetVoxelTint(Voxel, FLinearColor(0.9f, 0.2f, 0.2f)); // red
FLinearColor Tint;
const bool bTinted = World->GetVoxelTint(Voxel, Tint);      // false (and white) if none
World->ClearVoxelTint(Voxel);
```

## Blueprint nodes and C++ functions (on the world)

| Name | C++ | What it does |
|---|---|---|
| Set Block With State | `bool SetBlockWithState(FIntVector Voxel, FName Block, uint8 State)` | Block and state together |
| Set Block State | `bool SetBlockState(FIntVector Voxel, uint8 State)` | Changes the state, keeps the block. On a client this asks the server |
| Get Block State | `uint8 GetBlockState(FIntVector Voxel) const` | The state |
| Set Voxel Meta | `bool SetVoxelMeta(FIntVector Voxel, FName Key, const FString& Value)` | Sets one value |
| Get Voxel Meta | `bool GetVoxelMeta(FIntVector Voxel, FName Key, FString& Value) const` | Reads one value |
| Set Voxel Meta Int | `bool SetVoxelMetaInt(FIntVector Voxel, FName Key, int32 Value)` | Stores a whole number |
| Get Voxel Meta Int | `int32 GetVoxelMetaInt(FIntVector Voxel, FName Key, int32 Default = 0) const` | Reads it (Default if missing or not a number) |
| Remove Voxel Meta | `bool RemoveVoxelMeta(FIntVector Voxel, FName Key)` | Removes one value |
| Clear Voxel Meta | `bool ClearVoxelMeta(FIntVector Voxel)` | Removes all of a voxel's metadata |
| Get Voxel Meta Keys | `TArray<FName> GetVoxelMetaKeys(FIntVector Voxel) const` | The keys a voxel has |
| Set Voxel Tint | `bool SetVoxelTint(FIntVector Voxel, FLinearColor Tint)` | Colours one voxel of a tintable block |
| Get Voxel Tint | `bool GetVoxelTint(FIntVector Voxel, FLinearColor& Tint) const` | Its tint (false and white if none) |
| Clear Voxel Tint | `bool ClearVoxelTint(FIntVector Voxel)` | Removes the tint |

## Events

| Event | When it fires |
|---|---|
| On Voxel Meta Changed | A voxel's metadata changed: set, removed, cleared by a block change, loaded, or from the network (parameter: the voxel) |

## Limits
- 32 keys per voxel, keys up to 64 characters, values up to 1024 characters.
- On a client, metadata changes go to the server.
- Saves from earlier versions still load.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| Metadata vanished | The voxel's block changed, which clears it | Set it again after changing the block |
| State bits change unexpectedly | Bits 0–4 are reserved for rotation | Use bits 5–7 |
