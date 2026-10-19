---
title: "Damage and drops"
parent: Features
nav_order: 22
---
# Block health, damage and drops

> Blocks can take several hits before they break, and drop an item (or spawn an actor, such as a pickup) when they do.
> Damage heals after a while.

## How do I...?
- **Mine with a pickaxe:** call **Damage Voxel (Voxel, 25, Self)** on each swing.
- **Show cracks:** bind **On Voxel Damaged** and use its Health Fraction.
- **Give items:** bind **On Voxel Broken** on the server and add Drop Item × Drop Count to the player's inventory.

## Turn it on or off
Nothing runs until you call Damage Voxel or Break Voxel. Plain `Apply Brush` digging doesn't use health.

## The 3 settings you'll use most

| Setting | Where | What it does | Default |
|---|---|---|---|
| Max Health | Block table | Hit points of one voxel (0: Hardness × Health Per Hardness) | 0 |
| Drop Item | Block table | What it drops (None: the block's own name) | None |
| Damage Heal Seconds | World | Seconds after its last hit before a damaged voxel heals (0: never) | 10 |

## Example: hit what the player looks at
**Blueprint:** Trace From Camera → Damage Voxel (Hit Voxel, 25, Self) → if the result is 0, it broke.

**C++:**
```cpp
const FSuperVoxelHit Hit = USuperVoxelLibrary::TraceFromCamera(this, World, 500.f);
if (Hit.bHit)
{
	const float Left = World->DamageVoxel(Hit.Voxel, 25.f, this); // 0 = broke, -1 = can't be damaged
}
```

## Block table columns

| Column | Default | What it does |
|---|---|---|
| Max Health | 0 | Hit points; 0 = Hardness × the world's Health Per Hardness |
| Drop Item | None | Item name it drops (None: the block's name) |
| Drop Count | 1 | How many |
| Drop Chance | 1 | Chance (0..1) to drop |
| Drop Actor | none | An actor spawned where it breaks, e.g. a pickup |

## World settings (world > Damage)

| Setting | Default | What it does |
|---|---|---|
| Health Per Hardness | 100 | Hit points per point of Hardness, for blocks whose Max Health is 0 |
| Damage Heal Seconds | 10 | Seconds after the last hit before a damaged voxel heals completely (0: never) |

## Blueprint nodes and C++ functions (on the world)

| Name | C++ | What it does |
|---|---|---|
| Damage Voxel | `float DamageVoxel(FIntVector Voxel, float Amount, AActor* ByActor)` | Returns the health left: 0 if it broke, -1 if it can't be damaged (air, fluid, indestructible, protected). On a client it asks the server |
| Break Voxel | `bool BreakVoxel(FIntVector Voxel, AActor* ByActor, bool bDrop = true)` | Breaks at once, with or without the drop. Server only |
| Get Voxel Health Fraction | `float GetVoxelHealthFraction(FIntVector Voxel) const` | 1 when whole (also for air), down to 0 |
| Get Block Max Health | `float GetBlockMaxHealth(FName Block) const` | Hit points of one voxel of a block |

## Events

| Event | Where | Parameters |
|---|---|---|
| On Voxel Damaged | Every machine | Voxel, Health Fraction, Instigator (for crack effects) |
| On Voxel Broken | Server | Voxel, Block, Instigator, Drop Item, Drop Count (Drop Count 0: nothing) |

**C++: give the drop to the player**
```cpp
// In your class: UFUNCTION() void HandleVoxelBroken(FIntVector Voxel, FName Block, AActor* Instigator, FName DropItem, int32 DropCount);
World->OnVoxelBroken.AddDynamic(this, &AMyGameMode::HandleVoxelBroken); // on the server

void AMyGameMode::HandleVoxelBroken(FIntVector Voxel, FName Block, AActor* Instigator, FName DropItem, int32 DropCount)
{
	// Add DropCount x DropItem to Instigator's inventory (DropCount 0: nothing dropped).
}
```

A block's [behaviour](block-behaviors.md) also gets On Damaged and On Broken (return false for no drop).

## Limits
- A voxel whose block changes forgets its damage.
- Indestructible and [protected](editing.md#protection-volumes) voxels can't be damaged.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| Damage Voxel returns -1 | Air, fluid, indestructible or protected | Expected |
| Cracks reset | Damage Heal Seconds passed | Raise it, or set 0 to never heal |
| No drop | Drop Chance, or a behaviour's On Broken returned false | Check the row and the behaviour |
