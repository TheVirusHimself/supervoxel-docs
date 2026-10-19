---
title: "Performance"
nav_order: 9
---
# Performance

<!-- Status: draft (settings checked against 0f6bdf3; measured numbers come from the stress map) -->

## What costs what
- **Memory:** 2 bytes per voxel for the grid (a 256 × 256 × 96 world is about 12 MB), plus the meshes.
- **Building:** generation and meshing run on worker threads. Read `Get Last Generate Ms` and `Get Last Mesh Ms`.
- **Edits:** only the touched chunks rebuild, in the background (see [Background work](features/background-work.md)).

## Settings that matter
| Setting | Effect |
|---|---|
| World Size | Memory and build time grow with it |
| Chunk Size (32) | Smaller chunks rebuild faster after edits; larger ones mean fewer components |
| Async Meshing (on) | Keeps edits off the game thread |
| Max Chunk Uploads Per Frame (6) | Fewer = smoother frames, slower first build |
| Greedy Meshing (on) | Far fewer triangles in built areas |
| Ambient Occlusion (on) | Small meshing cost |
| Cast Shadows (on) | Turn off for big worlds if shadows cost too much |
| Affect Navigation (off) | Leave off: navmesh rebuilds on every edit are slow |
| Scatter Tile Size (32) | Bigger tiles: fewer components, slower updates after edits |
| Load Radius (9600, unbounded) | How much is generated and drawn around each player |
| Max Chunk Generations In Flight (24, unbounded) | Higher fills in faster but uses more worker threads |

## Measure it
Set the world's World Size to the size you need and read `Get Last Generate Ms`, `Get Last Mesh Ms` and
`Get Num Vertices`.

## Turn features off
Every feature is optional: pathfinding, scatter, collapse and the demo cost nothing when you don't use them.
