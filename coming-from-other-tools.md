---
title: "Coming from another voxel tool"
parent: Concepts
nav_order: 1
---
# Coming from another voxel tool

<!-- Status: draft -->

If you've used other voxel or terrain tools, this table maps the ideas you know to this guide's terms.

| You may know it as | Here it's called | Where to read |
|---|---|---|
| Voxel volume, voxel world, terrain actor | The voxel **world** actor | [Concepts](concepts.md) |
| Voxel graph, noise graph, world generator | A **generator** (Layered Terrain, Flat, or your own C++ class) | [Terrain generator](features/generator.md) |
| Material layers, terrain layers, voxel materials | **Block types** in a **block set** (a table), drawn from texture arrays | [Block set](features/block-set.md), [Materials](features/materials.md) |
| Stamp, sculpt tool, edit tool | A **brush** (Dig, Fill, Paint, Smooth, Flatten) | [Editing](features/editing.md) |
| Prefab, schematic, stamp asset | A **structure template** | [Structures and villages](features/structures.md) |
| Foliage spawner, scatter graph | **Surface spawn rules** (the scatter component) | [Spawn rules](features/spawn-rules.md) |
| Marching cubes, dual contouring, smooth mesher | **Smooth** blocks (surface nets) | [Meshing](features/meshing.md) |
| Cubic mesher, block mesher | **Blocky** blocks (greedy meshed) | [Meshing](features/meshing.md) |
| Navmesh on voxels | Voxel **pathfinding** (no navmesh rebuild) | [Pathfinding](features/pathfinding.md) |
| Edit history, voxel save, diff | The **edit journal** (seed plus runtime edits) | [Save and load](features/save-load.md) |
| Section view, x-ray, slice | The **cutaway** view | [Cutaway](features/cutaway.md) |
| Occlusion culling for caves | **Cave culling** | [Culling](features/culling.md) |
| Infinite terrain, world streaming | An **unbounded** world (coming) | [Unbounded worlds](features/streaming.md) |

## What works differently
- **Bounded worlds:** a world is a box with a fixed size. Unbounded, streamed worlds are coming.
- **One world, two looks:** smooth ground and crisp blocks live in the same chunk, with no second system.
- **Names, not ids:** saves store block names, so you can add and reorder block types safely.
- **Static water:** fluid blocks don't flow.
