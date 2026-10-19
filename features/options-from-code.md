---
title: "Changing options from code"
parent: Features
nav_order: 25
---

# Changing options from code

> Every option on the world, the generators, block sets, structures, structure volumes and the project settings can be
> read and changed from Blueprint and C++ while the game runs. Setting an option does the follow-up work for you:
> a rebuild, a re-mesh or a refresh.

## How do I...?
- **Change an option in Blueprint:** drag off the world (or generator, block set...) and use **Set** on the property.
  It calls the option's setter, which does the follow-up work.
- **Change one in C++:** call the setter function (for example `SetWorldSize`) instead of assigning the field.
- **Change a generator's own settings:** set them on the generator, then call **Request Rebuild**.
- **Change how a block looks or behaves at runtime:** **Get Block Definition**, change it, **Set Block Definition**.

## Example: a bigger world with another block set
**Blueprint:** Set World Size (512, 512, 128) → Set Block Set (your set).

**C++:**
```cpp
World->SetWorldSize(FIntVector(512, 512, 128)); // rebuilds, edits kept (server only)
World->SetBlockSet(MyBlockSet);                  // rebuilds, edits kept
World->SetGreedyMeshing(false);                  // re-meshes

// A generator's own settings: set them, then rebuild.
if (USuperVoxelHeightmapGenerator* Heightmap = Cast<USuperVoxelHeightmapGenerator>(World->Generator))
{
	Heightmap->HeightRange = 64;
	World->RequestRebuild();
}
```

## World options and what setting them does

| Option | Setter (C++) | What happens |
|---|---|---|
| Seed | `SetSeed` (the same as Set Seed And Regenerate) | Regenerates the world; **runtime edits are dropped** (a new seed is a new world). Server only |
| World Mode | `SetWorldMode` | Rebuilds, edits kept. Server only; clients follow |
| World Size | `SetWorldSize` (8 to 4096 per axis) | Rebuilds, edits kept. Server only |
| Voxel Size | `SetVoxelSize` | Rebuilds, edits kept. Server only |
| Chunk Size | `SetChunkSize` (8 to 64) | Rebuilds, edits kept |
| Block Set | `SetBlockSet` | Rebuilds, edits kept |
| Generator | `SetGenerator` (make one with Construct Object) | Rebuilds, edits kept |
| Structure Rules, Village Rules | `SetStructureRules`, `SetVillageRules` | Rebuilds, edits kept |
| Mesh Style | `SetMeshStyle` | Re-meshes every chunk (worker threads) |
| Ambient Occlusion, Greedy Meshing | `SetAmbientOcclusion`, `SetGreedyMeshing` | Re-meshes |
| Texture Tiling | `SetTextureTiling` | Material update only |
| Render Distance | `SetRenderDistance` | Per chunk, at once |
| Cast Shadows, Collision Profile, Affect Navigation | `SetCastShadows`, `SetCollisionProfile`, `SetAffectNavigation` | Applied to every chunk mesh; the navmesh refreshes |
| Editor Preview Radius, Build On Begin Play, Preview In Editor | (plain properties) | Read when the world builds |

**Request Rebuild** (`RequestRebuild()`) rebuilds from the current settings and keeps the edits. Use it after changing
a generator's own settings, or anything you set on an object directly.

## Block types at runtime

| Node | C++ | What it does |
|---|---|---|
| Get Block Definition | `bool GetBlockDefinition(FName Block, FSuperVoxelBlockDef& OutDef) const` | The whole definition as this world uses it |
| Set Block Definition | `bool SetBlockDefinition(FName Block, const FSuperVoxelBlockDef& Def)` | Replaces it at runtime on this machine: looks, hardness, falling, collision, light, ticks, health, drops, behaviour. Meshes, lights and materials update; the change survives rebuilds; the block asset isn't changed |

Set Block Random Tick and Set Block Behavior go through the same path.

## Project settings
**Get SuperVoxel Settings** (`USuperVoxelLibrary::GetSuperVoxelSettings()`) returns the project settings object; every
field can be changed. Changes apply to worlds built afterwards (or call Request Rebuild on a world). They aren't
written to the config file unless you save it.

## Multiplayer
- Seed, World Mode, World Size and Voxel Size replicate: set them on the server.
- Chunk Size, Block Set, Generator and the rules don't replicate: set them the same way on every machine.
- Set Block Definition is local: call it on every machine.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| Changing a generator setting does nothing | Generator settings aren't watched | Call Request Rebuild |
| My edits are gone after a seed change | A new seed drops runtime edits | Expected; other shaping setters keep them |
| A client looks different | Block Set, Generator or rules differ between machines | Set them the same way everywhere |
| Assigning a field in C++ has no effect | The field was set without its setter | Call the setter (for example `SetMeshStyle`) |
