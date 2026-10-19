---
title: "Meshing"
parent: Features
nav_order: 4
---
# Meshing: smooth, blocky, greedy and ambient occlusion

> Each chunk becomes one mesh. Smooth blocks become rounded natural ground, Blocky blocks become crisp cubes, and both
> sit in the same chunk with no seam. Equal block faces are merged into larger quads (greedy meshing), and ambient
> occlusion is baked into the mesh.

## Turn it on or off

| Part | Setting (world > Rendering) | Default |
|---|---|---|
| Greedy meshing | Greedy Meshing | on |
| Baked ambient occlusion | Ambient Occlusion | on |
| Shadows | Cast Shadows | on |

## Mesh style: per block, all smooth or all cubes

| Style | What it does |
|---|---|
| Per Block | Each block's own **Kind** (Smooth or Blocky) in the block table: smooth ground and crisp blocks side by side |
| Smooth | Every opaque block is smoothed |
| Blocky | Every block is a crisp cube |
| Project Default | Use Project Settings > Plugins > SuperVoxel > **Default Mesh Style** (itself Per Block by default) |

Set it on the world (**Mesh Style**, default Project Default) or at runtime with `Set Mesh Style`. Masked,
translucent and liquid blocks are always cubes or flat surfaces, whatever the style.

```cpp
World->SetMeshStyle(ESuperVoxelMeshStyle::Blocky);   // re-meshes every chunk on worker threads
const ESuperVoxelMeshStyle Used = World->GetEffectiveMeshStyle(); // Project Default resolved
```
Changing the style re-meshes every chunk, which costs about as much as the first meshing pass.

## How it looks
- **Smooth ground:** surface nets. Where up to three smooth block types meet, their textures blend at each vertex.
  Smooth ground and blocks are each closed solids: smooth ground runs on under a block instead of bending up to it,
  so there are no cracks where they meet (on slopes, in caves, under overhangs, at chunk borders). Where the ground
  rounds off next to a block, you see the block's side in a small groove. That's expected.
- **Hidden faces:** no face is made between two opaque voxels, across chunk borders too, so buried blocks cost no
  triangles.
- **Blocky blocks:** crisp faces. Buried faces aren't drawn, and with greedy meshing, neighbouring equal faces merge
  into larger quads, so walls and floors use far fewer triangles.
- **Separate sections** for masked (cut-out), translucent and liquid blocks, each with its own material.
- **Ambient occlusion:** creases, corners and caves are darker. It works with Lumen.

## Change it at runtime

| Node | C++ | What it does |
|---|---|---|
| Set Mesh Style | `SetMeshStyle(ESuperVoxelMeshStyle)` | Changes the style and re-meshes |
| Get Effective Mesh Style | `GetEffectiveMeshStyle()` | The style in use, Project Default resolved |
| Set Meshing Options | `SetMeshingOptions(bool bAmbientOcclusion, bool bGreedyMeshing)` | Turns AO or greedy meshing on or off and re-meshes |
| Remesh All | `RemeshAll()` | Re-meshes every chunk, on worker threads |

## Example
Tick or untick Greedy Meshing and Ambient Occlusion on the world. The editor preview rebuilds.
AO on and off side by side

## Fluid surfaces
How a fluid block's surface is drawn, set per fluid block at runtime (for fluid simulations):

| Style | What it draws |
|---|---|
| Flat (default) | A flat surface a little below the voxel top; the voxel's state is ignored |
| Levels | Each voxel's surface at its own level, read from its state byte: stepped |
| Smooth Levels | Levels averaged at each corner over the voxels sharing it: a smooth surface |

```cpp
World->SetFluidSurface(TEXT("Water"), ESuperVoxelFluidSurface::SmoothLevels);
```
**Set Fluid Surface** and **Get Fluid Surface** work on this machine only (set it the same way on every machine); the
style is kept across rebuilds.

## Stats (Blueprint and C++)

| Name | C++ | What it reports |
|---|---|---|
| Get Num Chunks With Mesh | `GetNumChunksWithMesh()` | Chunks that have a mesh |
| Get Num Vertices | `GetNumVertices()` | Total vertices |
| Get Last Mesh Ms | `GetLastMeshMs()` | Milliseconds the last full meshing pass took (worker time) |
| Get Num Culled Faces | `GetNumCulledFaces()` | Block faces never drawn because a neighbour hides them |
| Get Num Merged Faces | `GetNumMergedFaces()` | Visible faces merged away by greedy meshing |

## Events

| Event | When it fires |
|---|---|
| On Chunk Meshed (C++ only) | A chunk got a new mesh (parameter: the chunk coordinate) |

## Limits and performance
- Chunk Size (default 32) sets how much rebuilds after an edit: smaller chunks rebuild faster, larger chunks mean
  fewer components.
- Runtime voxel meshes don't use Nanite.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| A block I wanted as a cube is rounded | Its Kind is Smooth, or Mesh Style is Smooth | Set Kind = Blocky, or Mesh Style = Per Block or Blocky |
| Too many triangles in built areas | Greedy Meshing is off | Turn it on |
| Caves look flat | Ambient Occlusion is off | Turn it on |
