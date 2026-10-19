---
title: "Nodes and functions A to Z"
parent: Reference
nav_order: 1
---
# Blueprint nodes and C++ functions (A to Z)

**On** says where the node lives: the world (`ASuperVoxelWorld`), the library (`USuperVoxelLibrary`), navigation
(`USuperVoxelPathfindingLibrary`), the path follower, the scatter component or the block set.

| Name | On | Page |
|---|---|---|
| Add Streaming Anchor | World | [Unbounded worlds](../features/streaming.md) |
| Apply Brush | World | [Editing](../features/editing.md) |
| Capture Structure | World | [Structures](../features/structures.md) |
| Capture To Asset (button) | Structure Capture actor | [Structures](../features/structures.md) |
| Cave Culling (property) | World | [Culling](../features/culling.md) |
| Collapse After Dig (property) | World | [Collapse](../features/collapse.md) |
| CollapseUnsupported (C++) | World | [Collapse](../features/collapse.md) |
| ComputeBrush (C++) | World | [Editing](../features/editing.md) |
| Copy Voxel Region, Paste Voxel Region, Get Turned Region Size | Query library | [Queries](../features/queries.md) |
| Count Blocks In Box, Count Block Types In Box | Query library | [Queries](../features/queries.md) |
| Damage Voxel, Break Voxel | World | [Damage and drops](../features/damage-and-drops.md) |
| Draw Voxel Path | Navigation | [Pathfinding](../features/pathfinding.md) |
| Fill Block Table, Make Block Set With Laylines | Laylines library | [Laylines](../features/laylines.md) |
| Find Blocks In Box, Find Blocks In Sphere | Query library | [Queries](../features/queries.md) |
| Find Nearest Block | Query library | [Queries](../features/queries.md) |
| Find Spawn Location | World | [Background work](../features/background-work.md) |
| Find Surface | Query library | [Queries](../features/queries.md) |
| Find Voxel Path | Navigation | [Pathfinding](../features/pathfinding.md) |
| Find Voxel Path Async | Navigation (async node) | [Pathfinding](../features/pathfinding.md) |
| Find Voxel World | Library | [Blueprint library](../features/blueprint-api.md) |
| Flush Updates | Scatter | [Spawn rules](../features/spawn-rules.md) |
| Get All Block Names | World | [Block set](../features/block-set.md) |
| Get Block At | World | [Editing](../features/editing.md) |
| Get Block Def | World | [Block set](../features/block-set.md) |
| Get Block Definition, Set Block Definition | World | [Options from code](../features/options-from-code.md) |
| Get Block Id | World | [Block set](../features/block-set.md) |
| Get Block Id At | World | [Editing](../features/editing.md) |
| Get Block Name | World | [Block set](../features/block-set.md) |
| Get Build Progress | World | [Background work](../features/background-work.md) |
| Get Cutaway Height | World | [Cutaway](../features/cutaway.md) |
| Get Effective Mesh Style | World | [Meshing](../features/meshing.md) |
| Get Last Generate Ms | World | [Background work](../features/background-work.md) |
| Get Last Mesh Ms | World | [Meshing](../features/meshing.md) |
| Get Last Update Stats | Scatter | [Spawn rules](../features/spawn-rules.md) |
| Get Num Cave Culled Chunks | World | [Culling](../features/culling.md) |
| Get Num Chunks With Mesh | World | [Meshing](../features/meshing.md) |
| Get Num Culled Faces | World | [Meshing](../features/meshing.md) |
| Get Num Edits | World | [Save and load](../features/save-load.md) |
| Get Num Instances | Scatter | [Spawn rules](../features/spawn-rules.md) |
| Get Num Instances In Column | Scatter | [Spawn rules](../features/spawn-rules.md) |
| Get Num Light Emitters, Get Num Active Voxel Lights | World | [Light blocks](../features/lights.md) |
| Get Num Loaded Chunks | World | [Unbounded worlds](../features/streaming.md) |
| Get Num Merged Faces | World | [Meshing](../features/meshing.md) |
| Get Num Solid Voxels | Structure template | [Structures](../features/structures.md) |
| Get Num Vertices | World | [Meshing](../features/meshing.md) |
| Get Path Points | Path follower | [Pathfinding](../features/pathfinding.md) |
| Get Seed | World | [Generator](../features/generator.md) |
| Get SuperVoxel Settings | Library | [Options from code](../features/options-from-code.md) |
| Get Surface Height | World | [Editing](../features/editing.md) |
| Get Texture Tiling | World | [Settings](../features/settings.md) |
| Get Voxel Health Fraction, Get Block Max Health | World | [Damage and drops](../features/damage-and-drops.md) |
| Get Voxel Size | World | [Settings](../features/settings.md) |
| Interact With Voxel | World | [Block behaviours](../features/block-behaviors.md) |
| Is Area Editable | Query library | [Queries](../features/queries.md) |
| Is Area Ready | World | [Unbounded worlds](../features/streaming.md) |
| Is Moving | Path follower | [Pathfinding](../features/pathfinding.md) |
| Is Ready | World | [Background work](../features/background-work.md) |
| Is Standable At | Navigation | [Pathfinding](../features/pathfinding.md) |
| Is Voxel Loaded | World | [Unbounded worlds](../features/streaming.md) |
| Is Voxel Protected | World | [Editing](../features/editing.md) |
| Is Voxel Solid | World | [Editing](../features/editing.md) |
| Load Edits | World | [Save and load](../features/save-load.md) |
| Load From Slot | World | [Save and load](../features/save-load.md) |
| Make Box Brush | Library | [Editing](../features/editing.md) |
| Make Sphere Brush | Library | [Editing](../features/editing.md) |
| Move To | Path follower | [Pathfinding](../features/pathfinding.md) |
| On Arrived, On Failed (events) | Path follower | [Pathfinding](../features/pathfinding.md) |
| On Blocks Changed, On Voxel Interact (events) | World | [Block behaviours](../features/block-behaviors.md) |
| On Chunk Loaded, On Chunk Unloaded (C++ events) | World | [Unbounded worlds](../features/streaming.md) |
| On Chunk Meshed (C++ event) | World | [Meshing](../features/meshing.md) |
| On Found, On Failed (events) | Find Voxel Path Async | [Pathfinding](../features/pathfinding.md) |
| On Layline Signal Changed, On Layline Option Changed, On Laylines Settings Changed (events) | Laylines | [Laylines](../features/laylines.md) |
| On Partial (event) | Find Voxel Path Async | [Pathfinding](../features/pathfinding.md) |
| On Voxel Damaged, On Voxel Broken (events) | World | [Damage and drops](../features/damage-and-drops.md) |
| On Voxel Meta Changed (event) | World | [State and metadata](../features/state-and-metadata.md) |
| On Voxel Random Tick, On Voxel Scheduled Tick (events) | World | [Ticks](../features/ticks.md) |
| On Voxels Changed (event) | World | [Blueprint library](../features/blueprint-api.md) |
| On World Built (event) | World | [Background work](../features/background-work.md) |
| Place Layline, Emit, Rescan, Get Signal, Is On, Get Role | Laylines subsystem | [Laylines](../features/laylines.md) |
| Place Structure | World | [Structures](../features/structures.md) |
| Place Structure At | World | [Structures](../features/structures.md) |
| Random Seed (property) | World | [Generator](../features/generator.md) |
| Rebuild | World | [Settings](../features/settings.md) |
| Rebuild All | Scatter | [Spawn rules](../features/spawn-rules.md) |
| RebuildTextureArrays (button) | Block set | [Materials](../features/materials.md) |
| Remesh All | World | [Meshing](../features/meshing.md) |
| Remove Streaming Anchor | World | [Unbounded worlds](../features/streaming.md) |
| Remove Voxel Meta, Clear Voxel Meta, Get Voxel Meta Keys | World | [State and metadata](../features/state-and-metadata.md) |
| Request Rebuild | World | [Options from code](../features/options-from-code.md) |
| Reset Edits | World | [Save and load](../features/save-load.md) |
| Sample Surface | Query library | [Queries](../features/queries.md) |
| Save Edits | World | [Save and load](../features/save-load.md) |
| Save To Slot | World | [Save and load](../features/save-load.md) |
| Schedule Voxel Tick, Cancel Voxel Tick, Set Block Random Tick | World | [Ticks](../features/ticks.md) |
| Set Ambient Occlusion, Set Greedy Meshing, Set Texture Tiling | World | [Options from code](../features/options-from-code.md) |
| Set Block | World | [Editing](../features/editing.md) |
| Set Block Behavior | World | [Block behaviours](../features/block-behaviors.md) |
| Set Block Material Params | World | [Materials](../features/materials.md) |
| Set Block Option, Get Block Option, Get Block Option Names (and the per-part Set/Get calls) | Laylines subsystem | [Laylines](../features/laylines.md) |
| Set Block Set, Set Generator, Set Structure Rules, Set Village Rules | World | [Options from code](../features/options-from-code.md) |
| Set Block With State, Set Block State, Get Block State | World | [State and metadata](../features/state-and-metadata.md) |
| Set Cast Shadows, Set Collision Profile, Set Affect Navigation | World | [Options from code](../features/options-from-code.md) |
| Set Cutaway Height | World | [Cutaway](../features/cutaway.md) |
| Set Edit Instigator, Get Edit Instigator | World | [Block behaviours](../features/block-behaviors.md) |
| Set Mesh Style | World | [Meshing](../features/meshing.md) |
| Set Meshing Options | World | [Meshing](../features/meshing.md) |
| Set Render Distance | World | [Culling](../features/culling.md) |
| Set Seed | World | [Generator](../features/generator.md) |
| Set Seed And Regenerate | World | [Generator](../features/generator.md) |
| Set Setting, Get Setting, Get Setting Names, Get Laylines Settings, Notify Settings Changed | Laylines subsystem | [Laylines](../features/laylines.md) |
| Set Voxel Meta, Get Voxel Meta, Set Voxel Meta Int, Get Voxel Meta Int | World | [State and metadata](../features/state-and-metadata.md) |
| Set World Mode, Set World Size, Set Voxel Size, Set Chunk Size | World | [Options from code](../features/options-from-code.md) |
| Spawn Village | World | [Structures](../features/structures.md) |
| Start Digging, Stop Digging, Set Palette Open | Bumble | [Example character](../bumble.md) |
| Stop | Path follower | [Pathfinding](../features/pathfinding.md) |
| Trace From Camera | Library | [Editing](../features/editing.md) |
| Trace Voxel | World | [Editing](../features/editing.md) |
| Voxel To World | World | [Blueprint library](../features/blueprint-api.md) |
| World Mode (property) | World | [Unbounded worlds](../features/streaming.md) |
| World To Voxel | World | [Blueprint library](../features/blueprint-api.md) |

**C++ only:** `CanEditVoxel` and `ApplyChanges` (world, [Editing](../features/editing.md));
`USuperVoxelGenerator` ([Generator](../features/generator.md)); `FSuperVoxelPathfinder` and `FSuperVoxelNavGrid`
([Pathfinding](../features/pathfinding.md)); `USuperVoxelNetComponent` ([Multiplayer](../features/multiplayer.md)).
