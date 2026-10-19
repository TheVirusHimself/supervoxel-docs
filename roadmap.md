---
title: "Roadmap"
nav_order: 13
---
# Roadmap

> Ideas we're looking at for after 1.0. **These are not promises:** none of them ships in 1.0, plans change, and
> nothing here has a date. Everything the guide describes elsewhere is in 1.0. Owners get every future update free.

## Platforms
- **Linux and Mac verification.** The code is platform-neutral, but only Windows (Win64) is built and tested for 1.0.

## Looks
- **Higher-resolution textures** (512 px), possibly as an optional pack. 1.0 ships 256 px texture arrays, and you can
  set your own Texture Resolution and rebuild the arrays.
- **Real block thumbnails in the palette** of the example character.
- **Level of detail** for distant chunks.
- **Biome blending** at biome borders.

## Blocks and editing
- **Block rotation and shape variants** (stairs, slabs). Bits 0 to 4 of the voxel state byte are reserved for this,
  for blocks that opt in.
- **A mesh voxelizer** (turn a static mesh into voxels).
- **Physics debris** from digging and collapse.

## Engine and tools
- **A memory allocator comparison** for chunk data, kept only if it measures faster.
- **A native PCG node.** In 1.0, surface sampling feeds PCG from Blueprint or C++ (see [Queries](features/queries.md)).

Have a request? Write to [ocozdemir@gmail.com](mailto:ocozdemir@gmail.com); see [Support](support.md).
