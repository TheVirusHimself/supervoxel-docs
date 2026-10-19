---
title: "Settings"
parent: Features
nav_order: 2
---
# Settings

> Project-wide defaults live in Project Settings > Plugins > SuperVoxel. Each world can override them in its Details
> panel.

## How do I...?
- **Make voxels bigger or smaller:** set the world's **Voxel Size** (cm), or the project's **Default Voxel Size**.
- **Make textures repeat less often:** raise **Texture Tiling** (world units per repeat).
- **Make the world bigger:** the world's **World Size** (in voxels).

## The 3 settings you'll use most

| Setting | Where | Default |
|---|---|---|
| World Size | World | 256 × 256 × 96 voxels |
| Voxel Size | World (0 = project default) / Project | 50 cm |
| Seed | World | 1 |

Every option here can also be changed while the game runs: see [Changing options from code](options-from-code.md).

## Project settings (`USuperVoxelSettings`)
Find them under Project Settings > Plugins > SuperVoxel. Tip: if Project Settings opens filtered ("All results
have been filtered"), click **All** next to the General chip.


| Setting | Default | What it does |
|---|---|---|
| Default Voxel Size | 50 | Voxel edge in cm for worlds that don't set their own |
| Default Texture Tiling | 200 | World units per texture repeat, for worlds that don't set their own |
| Default Mesh Style | Per Block | Per Block, Smooth or Blocky, for worlds left on Project Default ([Meshing](meshing.md)) |
| Default Block Set | `/SuperVoxel/Blocks/BS_SuperVoxelDefault` | For worlds that don't set their own |
| Default Opaque / Masked / Translucent / Fluid Material | `/SuperVoxel/Materials/M_SuperVoxel_*` | Used when a block set leaves its own empty |

## World settings (`ASuperVoxelWorld`)
**SuperVoxel**

| Setting | Default | What it does |
|---|---|---|
| Seed | 1 | Generation seed. The same seed, size, block set and generator settings give the same world on every machine |
| Random Seed | off | Pick a new seed each time the world is generated at runtime (Begin Play, Rebuild); the server picks it in multiplayer |
| World Mode | Bounded | Bounded (a box) or Unbounded (endless in X and Y). See [Unbounded worlds](streaming.md) |
| World Size | 256, 256, 96 | Size in voxels (8–4096 per axis). In an unbounded world only Z (the height) counts |
| Voxel Size | 0 | Voxel edge in cm. 0 or less = project default |
| Chunk Size | 32 | Chunk edge in voxels (8–64). Smaller chunks rebuild faster after edits; larger ones mean fewer components |
| Block Set | empty | The block types. Empty = project default |
| Generator | empty | Fills the world. Empty = all air. See [Terrain generator](generator.md) |

**Building**

| Setting | Default | What it does |
|---|---|---|
| Build On Begin Play | on | Generate and build when play begins |
| Preview In Editor | on | Show the world in the editor viewport (rebuilt when settings change) |
| Async Meshing | on | Build meshes for edits on worker threads. Off = rebuild on the game thread at once |
| Max Chunk Uploads Per Frame | 6 | Most chunk meshes handed to the renderer per frame (the first build uses four times as many) |

**Editing:** Collapse After Dig (off). See [Collapse](collapse.md).

**Streaming:** Load Radius, Unload Margin, Max Chunk Generations In Flight, Stream Around Players, Editor Preview
Radius. See [Unbounded worlds](streaming.md).

**Structures:** Structure Rules and Village Rules (both empty).

**Destruction:** Destructible (on; replicated) and the project's Terrain Destructible (on). See
[Destruction settings](destruction.md).

**Damage:** Health Per Hardness (100), Damage Heal Seconds (10). See [Damage and drops](damage-and-drops.md).

**Ticks:** Random Ticks Per Chunk Per Second (48), Random Tick Radius (6400). See [Ticks](ticks.md).

**Lights:** Voxel Lights (on), Max Voxel Lights (24), Voxel Light Distance (5000), Voxel Light Shadows (off). See
[Light blocks](lights.md). See [Structures and villages](structures.md).

**Rendering**

| Setting | Default | What it does |
|---|---|---|
| Ambient Occlusion | on | Bake ambient occlusion into the mesh |
| Greedy Meshing | on | Merge equal block faces into larger quads |
| Texture Tiling | 0 | World units per texture repeat. 0 or less = project default |
| Cast Shadows | on | Chunk meshes cast shadows |
| Mesh Style | Project Default | Per Block, Smooth or Blocky ([Meshing](meshing.md)) |
| Cave Culling | on | Don't draw chunks the camera can't see into ([Culling](culling.md)) |
| Render Distance | 0 | Don't draw chunks beyond this distance; 0 = no limit ([Culling](culling.md)) |

**Collision**

| Setting | Default | What it does |
|---|---|---|
| Collision Profile | BlockAll | Collision profile of the chunk meshes |
| Affect Navigation | off | Chunks affect the engine navmesh. Off by default because navmesh rebuilds on every edit are slow; use [Pathfinding](pathfinding.md), or see its navmesh section |

## Blueprint nodes and C++ functions

| Name | Blueprint | C++ | What it does |
|---|---|---|---|
| Get Voxel Size | yes | `float GetVoxelSize() const` | The effective voxel size (the world's, or the project default) |
| Get Texture Tiling | yes | `float GetTextureTiling() const` | The effective tiling |
| Rebuild | yes | `void Rebuild(bool bAsync = true)` | Regenerates from the seed, replays edits and rebuilds every chunk |

## Limits
- Changing World Size or Voxel Size regenerates the world.
- Memory grows with World Size: 2 bytes per voxel for the grid, plus the meshes.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| A setting seems to do nothing | It's 0 on the world, so the project default is used | Set a value above 0 on the world, or change the project setting |
| The world is empty | No block set anywhere, or no generator | See [Block set](block-set.md) and [Generator](generator.md) |
