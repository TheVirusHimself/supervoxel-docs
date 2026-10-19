---
title: "Concepts"
nav_order: 5
has_children: true
---
# Concepts

Read this once; the rest of the manual uses these ideas.

- **The world is a box of voxels.** Each voxel holds one block type, or Air. The world has a fixed size in voxels
  (default 256 × 256 × 96). Z is up. [Unbounded worlds](features/streaming.md), endless in X and Y and loaded around
  the players, are coming.
- **Voxel size** is how big one voxel is in the level (default 50 cm).
- **Chunks.** The world is meshed in chunks (default 32 voxels on each edge), so an edit only rebuilds the chunks it
  touches.
- **Block types** come from a [block set](features/block-set.md). Each block has a kind:
  - **Smooth**: natural ground, smoothed into its smooth neighbours;
  - **Blocky**: crisp cube faces that never smooth into the ground;
  - **Fluid**: not solid, drawn as flat surfaces.
- **Smooth and blocky in one chunk:** a brick wall can stand in a smooth hillside with no seam.
- **Generation** fills the box from a seed and a [generator](features/generator.md). The same seed, size, block set
  and generator settings always give the same world, on every machine.
- **Edits** are changes on top of the generated world. Editor sculpting is saved with the level (baked edits);
  changes made while playing are runtime edits. A save is the seed plus the runtime edits.
- **Block names, not numbers.** Each block gets an id when its block set loads (Air is always 0). Ids can change
  between sessions, so saves store names.
- **Limits in version 1.0:** water doesn't flow, there are no distance detail levels (LOD), and Win64 is the only
  verified platform.
- **Everything heavy runs in the background:** generation, meshing and collision happen on worker threads.

