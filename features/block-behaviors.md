---
title: "Block behaviours"
parent: Features
nav_order: 21
---
# Block behaviours and events

> Give a block type its own logic: a door that opens, a chest, a lever, ore that drops gems, grass that spreads. Make a
> Blueprint of **SuperVoxel Block Behavior**, override the events you need, and pick it for the block.

## How do I...?
- **Make a door:** a behaviour whose **On Interact** flips the voxel's [state](state-and-metadata.md); call
  **Interact With Voxel** from your character.
- **React to any change in the world:** bind the world's **On Blocks Changed**.
- **Credit an edit to a player:** **Set Edit Instigator (Actor)** before you edit.

## Turn it on or off
A block has a behaviour when its table row's **Behavior** column names one, or after **Set Block Behavior (Block,
Class)** at runtime. Blocks without one cost nothing.

## The 3 events you'll use most

| Event | When it runs |
|---|---|
| On Interact | Someone used **Interact With Voxel** on it (return true if handled) |
| On Placed | A voxel became this block |
| On Broken | Damage broke it (return false for no drop) |

## Example: a lever
**Blueprint:** create a Blueprint class from **SuperVoxel Block Behavior** → override **On Interact**: Get Block
State → Set Block State (the other value) → return true. In the block table, set the lever block's **Behavior** to
it. From your character: Trace From Camera → **Interact With Voxel (Hit Voxel, Self)**.

**C++** (from your character):
```cpp
const FSuperVoxelHit Hit = USuperVoxelLibrary::TraceFromCamera(this, World, 400.f);
if (Hit.bHit)
{
	World->InteractWithVoxel(Hit.Voxel, this);
}
```

## How it works
- **One instance per block type and world** handles every voxel of that type. Keep per-voxel data in the voxel's
  state or metadata, not in the behaviour.
- Events run **on the server** for gameplay edits, not for loads, resets or editor sculpting.

## Behaviour events (`USuperVoxelBlockBehavior`)

| Event | Parameters | Notes |
|---|---|---|
| On Placed | World, Voxel, Previous Block, Instigator | A voxel became this block |
| On Removed | World, Voxel, New Block, Instigator | A voxel stopped being this block |
| On Interact | World, Voxel, Instigator | Return true if handled |
| On Neighbor Changed | World, Voxel, Neighbor | A voxel next to it changed |
| On Damaged | World, Voxel, Amount, Health Left, Instigator | See [Damage and drops](damage-and-drops.md) |
| On Broken | World, Voxel, Instigator | Return false for no drop |
| On Random Tick | World, Voxel | See [Ticks](ticks.md) |
| On Scheduled Tick | World, Voxel | See [Ticks](ticks.md) |

## World nodes and events

| Name | C++ | What it does |
|---|---|---|
| Interact With Voxel | `bool InteractWithVoxel(FIntVector Voxel, AActor* ByActor)` | For doors, chests and levers. On a client it asks the server |
| Set Edit Instigator | `void SetEditInstigator(AActor* ByActor)` | Credits the edits you make in this frame. Network requests credit the player's pawn |
| Get Edit Instigator | `AActor* GetEditInstigator() const` | |
| Set Block Behavior | `bool SetBlockBehavior(FName Block, TSubclassOf<USuperVoxelBlockBehavior> Behavior)` | Gives a block a behaviour at runtime (none removes it) |
| On Blocks Changed (event) | `OnBlocksChanged` | Every voxel an edit changed (old and new block, new state) plus the instigator, on every machine. Bind it only if you need it |
| On Voxel Interact (event) | `OnVoxelInteract` | On the server, after Interact With Voxel (and the block's behaviour) |

## Limits and performance
- On Blocks Changed fires for every edit on every machine; keep handlers light.
- Behaviours don't run for loads, resets or editor sculpting.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| An event never fires | It ran on a client, or the change came from a load or sculpting | Events run on the server, for gameplay edits |
| Two voxels share a value | Data kept in the behaviour object | Use state or metadata per voxel |
