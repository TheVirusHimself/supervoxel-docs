---
title: "Glossary"
parent: Reference
nav_order: 4
---
# Glossary

| Term | Meaning |
|---|---|
| Air | The empty block. Every block set has it; it is never drawn. |
| Block | One type of material a voxel can hold, like Granite or Oak Planks. |
| Block behaviour | A Blueprint or C++ class that gives a block type its own logic (doors, chests, spreading grass). |
| Block id | The number a block gets when its block set loads. It can change between sessions, so saves use names. |
| Block kind | How a block is meshed: Smooth, Blocky or Fluid. |
| Block set | The data asset that lists a world's block types. |
| Blocky | A block kind with crisp cube faces. |
| Brush | A shape (sphere, box or cylinder) that digs, fills, paints or smooths many voxels at once. |
| Cave culling | Not drawing chunks the camera can't see into through open space. |
| Chunk | A box of voxels meshed together. Edits rebuild only the chunks they touch. |
| Collapse | Pieces left without support fall away after a dig. |
| Cutaway | A view that hides everything above a chosen height, so you can see inside. |
| Edit journal | The list of changes made on top of the generated world. Saves and multiplayer use it. |
| Face | The top, side or bottom of a block; each can have its own texture. |
| Fluid | A block kind that isn't solid and is drawn as flat surfaces, like water. |
| Generator | The rule that fills a new world from a seed. |
| Greedy meshing | Merging neighbouring faces of the same block into larger quads, so blocky areas use fewer triangles. |
| Mesh style | Whether a world meshes each block by its own kind, or forces every block smooth or blocky. |
| Metadata | Small key/value pairs stored on single voxels. |
| Opacity | Which material variant draws a block: Opaque, Masked (cut-out, like leaves) or Translucent (see-through). |
| Protection volume | A box where gameplay edits are refused. |
| Random tick | A visit, now and then, to voxels of block types that ask for it. |
| Render distance | How far away chunks are still drawn. |
| Scheduled tick | A call back to one voxel after a delay. |
| Seed | A number that picks the random layout. The same seed always gives the same world. |
| Smooth | A block kind for natural ground, smoothed with its smooth neighbours. |
| Spawn rule | A rule that scatters props (grass, rocks, trees) on chosen blocks. |
| State | A number from 0 to 255 kept with each voxel's block. |
| Structure template | A saved box of blocks (a house, a ruin) that can be stamped into a world. |
| Surface height | The height of the top solid voxel in a column. |
| Texture array | One texture asset holding many same-size textures, one per block face. |
| Vertex AO | Ambient occlusion baked into the mesh, so corners and caves look darker. |
| Village | A few house templates placed around a center and joined by paths. |
| Voxel | One cell of the world grid. |
| Voxel size | How big one voxel is in the level. |
