---
title: "Destruction settings"
parent: Features
nav_order: 27
---

# Destruction settings

> Decide what players can break. Three levels: **per block type** (which blocks can be dug, damaged, collapse, wash
> away or survive blasts), **per area** (protection volumes), and **per world** (a master switch that makes the whole
> world read-only to gameplay).

## How do I...?
- **Make a block that can't be dug:** untick its **Can Be Dug** in the block table.
- **Make a whole world read-only** (a hub, a showcase map): untick the world's **Destructible**, or call
  **Set Destructible (false)** on the server.
- **Protect only a village or a spawn area:** place a [protection volume](editing.md#protection-volumes).
- **Turn destruction off in every world of the project:** untick Project Settings > Plugins > SuperVoxel >
  **Terrain Destructible**.

## The 3 settings you'll use most

| Setting | Where | What it does | Default |
|---|---|---|---|
| Can Be Dug | Block table | Gameplay edits may remove or replace this block | on |
| Destructible | World | Gameplay may change this world at all | on |
| Indestructible | Block table | Every protection at once (the world's floor) | off (on for BaseRock) |

## Per block type (block table, Destruction)

| Setting | Default | What it does |
|---|---|---|
| Can Be Dug | on | Gameplay edits (Set Block, brushes, Break Voxel, pasting) may remove or replace it. Editor sculpting always can |
| Can Be Damaged | on | [Damage Voxel](damage-and-drops.md) wears it down. Breaking it also needs Can Be Dug |
| Affected By Collapse | on | Falls or breaks off when unsupported ([collapse](collapse.md), and Falls blocks). Off: it holds itself and what rests on it, and anchors pieces like the floor does |
| Fluid Can Destroy | off | Flowing fluid washes it away (plants, torches); used by [Fluids](fluids.md) |
| Explosion Proof | off | Blasts don't destroy it. Read by your explosion code |
| Indestructible | off | All of the above protections at once: never dug, damaged, collapsed or blasted |

**In the shipped table:** BaseRock (the world's floor) is fully protected. Vine Mat, Root Tangle, Fungal Mat, Glow
Fungus, Ember Bed, Oil Lamp Block and Paper Lantern Block wash away in flowing fluid.

## Per world: the master switch
- **Destructible** on the world (`bDestructible`, default on). Off: the world is read-only to gameplay. Set Block,
  brushes, Break Voxel, Damage Voxel and pasting do nothing, and nothing collapses.
- **Still works when it's off:** editor sculpting, saves and loads. Metadata and tints can still change.
- Set it on the server; it's replicated.
- **Terrain Destructible** in Project Settings (default on) does the same for every world in the project.
- **Is Destructible** tells you whether gameplay can change a world: its own switch and the project's together.

## Example: a read-only lobby
**Blueprint:** on Begin Play (server): Find Voxel World → Set Destructible (false).

**C++:**
```cpp
#include "SuperVoxelWorld.h"
#include "SuperVoxelLibrary.h"

void AMyLobbyGameMode::BeginPlay()
{
	Super::BeginPlay();
	if (ASuperVoxelWorld* World = USuperVoxelLibrary::FindVoxelWorld(this))
	{
		World->SetDestructible(false); // replicated to clients
	}
}
```

**C++: make one block type undiggable at runtime**
```cpp
FSuperVoxelBlockDef Def;
if (World->GetBlockDefinition(TEXT("Obsidian"), Def))
{
	Def.bCanBeDug = false;
	World->SetBlockDefinition(TEXT("Obsidian"), Def); // on this machine: call it on every machine
}
```

## Per area: protection volumes
A **SuperVoxel Protection Volume** refuses gameplay edits inside its box. See
[Editing: protection volumes](editing.md#protection-volumes).

## Blueprint nodes and C++ functions

| Name | C++ | What it does |
|---|---|---|
| Set Destructible | `void SetDestructible(bool bOn)` (on the world) | The world's master switch (server; replicated) |
| Is Destructible | `bool IsDestructible() const` (on the world) | Whether gameplay can change this world |
| Get / Set Block Definition | see [Changing options from code](options-from-code.md) | Change a block's Destruction settings at runtime |
| Is Voxel Protected | `bool IsVoxelProtected(FIntVector Voxel) const` | Whether a protection volume covers a voxel |

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| Nothing digs anywhere | The world's Destructible or the project's Terrain Destructible is off | Turn them on |
| One block won't break | Can Be Dug is off, or it's Indestructible | Check the block table |
| Damage does nothing but digging works | Can Be Damaged is off | Turn it on |
| A block floats after a dig | Affected By Collapse is off | Expected; turn it on if it should fall |
