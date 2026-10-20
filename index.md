---
title: "Home"
nav_order: 1
permalink: /
---
# SuperVoxel user guide

SuperVoxel builds editable voxel worlds in Unreal Engine 5.8: smooth natural ground and crisp blocks in the same
world, with data-driven block types, brushes, saves, multiplayer edits and pathfinding.

Seller: Onur C Ozdemir. Version: 1.0. Platform: Windows (Win64). **Coming soon to Fab.**

## First aid

| Problem | Quick fix |
|---|---|
| The world doesn't show | Check the world's Block Set and Generator, and that the build finished ([Settings](features/settings.md)) |
| The player falls through | Spawn after **On World Built** ([Background work](features/background-work.md)) |
| Things pass through the terrain | Check the world's Collision Profile (default BlockAll) ([Settings](features/settings.md)) |
| Blocks look plain grey | Press **Rebuild Texture Arrays** on the block set ([Materials](features/materials.md)) |
| Nothing digs | On a client, edits go through the server; brush sizes are in voxels ([Editing](features/editing.md)) |

More in [Troubleshooting and errors](reference/errors.md).

**In the editor:** Help > SuperVoxel Documentation opens this guide, and the Documentation row in the Details panel
opens the page for what you've selected.

## Start here
- [Quick start (5 minutes)](quick-start.md): an editable world in your level.
- [Recipes](recipes.md): ten copy-ready tasks.
- [Coming from another voxel tool](coming-from-other-tools.md)
- [Roadmap](roadmap.md): ideas for after 1.0, not promises
- [Install and upgrade](install-and-upgrade.md)
- [Concepts](concepts.md): voxels, chunks, blocks and how a world is built.
- [Glossary](glossary.md)

## How do I...?

| I want to... | Go to |
|---|---|
| Put a world in my level | [Quick start](quick-start.md) |
| Change how the terrain is generated | [Terrain generator](features/generator.md) |
| Add my own block type | [Block set and block types](features/block-set.md) |
| Use my own textures | [Materials and textures](features/materials.md) |
| Dig, fill or paint at runtime | [Editing](features/editing.md) |
| Sculpt in the editor | [Editor tools](features/editor-tools.md) |
| Save and load the player's changes | [Save and load](features/save-load.md) |
| Make characters walk on the voxels | [Pathfinding](features/pathfinding.md) |
| See inside caves and buildings | [Cutaway view](features/cutaway.md) |
| Make unsupported pieces fall | [Collapse](features/collapse.md) |
| Place houses, ruins or villages | [Structures and villages](features/structures.md) |
| Stop drawing hidden caves, or limit the draw distance | [Cave culling and render distance](features/culling.md) |
| Make an endless world | [Unbounded worlds](features/streaming.md) |
| Edit in multiplayer | [Multiplayer](features/multiplayer.md) |
| Scatter grass, rocks or trees on the ground | [Surface spawn rules](features/spawn-rules.md) |
| React when voxels change | [Blueprint library and events](features/blueprint-api.md), [Block behaviours](features/block-behaviors.md) |
| Colour single blocks (signs, pixel walls) | [Voxel tint](features/state-and-metadata.md#voxel-tint) |
| Make doors, chests and levers | [Block behaviours](features/block-behaviors.md), [Voxel state and metadata](features/state-and-metadata.md) |
| Mine blocks with hits and drops | [Damage and drops](features/damage-and-drops.md) |
| Find blocks, the ground, or copy and paste areas | [Queries and regions](features/queries.md) |
| Make grass spread or timers fire | [Ticks](features/ticks.md) |
| Make lamps light the world | [Light blocks](features/lights.md) |
| Change any option while the game runs | [Changing options from code](features/options-from-code.md) |
| Build circuits: levers, gates, timers, lamps, doors | [Laylines](features/laylines.md) (optional module) |
| Make water and lava flow, with springs and drains | [Fluids](features/fluids.md) (optional module) |
| Stop players editing an area | [Editing: protection volumes](features/editing.md#protection-volumes) |
| Choose what can break, or make a world read-only | [Destruction settings](features/destruction.md) |
| Make it run faster | [Performance](performance.md) |
| Try the demo character | [Example character: Bumble](bumble.md) |
| Fix a problem | [Troubleshooting and errors](reference/errors.md), [FAQ](faq.md) |

## Features
Every feature can be turned off. Features you don't use cost nothing.

| Feature |
|---|
| [Block set and block types](features/block-set.md) |
| [Settings (voxel size, textures, tiling)](features/settings.md) |
| [Terrain generator](features/generator.md) |
| [Meshing: smooth, blocky, mesh style, greedy, ambient occlusion](features/meshing.md) |
| [Materials and textures](features/materials.md) |
| [Editing (brushes, traces)](features/editing.md) |
| [Background meshing and collision](features/background-work.md) |
| [Save and load](features/save-load.md) |
| [Cutaway view](features/cutaway.md) |
| [Collapse](features/collapse.md) |
| [Structures and villages](features/structures.md) |
| [Cave culling and render distance](features/culling.md) |
| [Unbounded worlds](features/streaming.md) |
| [Pathfinding](features/pathfinding.md) |
| [Multiplayer](features/multiplayer.md) |
| [Surface spawn rules](features/spawn-rules.md) |
| [Editor tools](features/editor-tools.md) |
| [Blueprint library and events](features/blueprint-api.md) |
| [Voxel state and metadata](features/state-and-metadata.md) |
| [Queries and regions](features/queries.md) |
| [Block behaviours](features/block-behaviors.md) |
| [Damage and drops](features/damage-and-drops.md) |
| [Ticks](features/ticks.md) |
| [Light blocks](features/lights.md) |
| [Changing options from code](features/options-from-code.md) |
| [Destruction settings](features/destruction.md) |
| [Laylines: signal wiring (optional module)](features/laylines.md) |
| [Fluids: flowing water and lava (optional module)](features/fluids.md) |

## Reference
- [Blueprint nodes and C++ functions (A to Z)](reference/api-index.md)
- [Console variables](reference/console-variables.md)
- [Troubleshooting and errors](reference/errors.md)
- [Performance](performance.md)

## Help
- [FAQ](faq.md)
- [Support and updates](support.md)
- [Changelog](changelog.md)
