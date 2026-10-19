---
title: "Cave culling and render distance"
parent: Features
nav_order: 11
---
# Cave culling and render distance

<!-- Status: checked against e7f2c56 (headers; not yet run in the editor) -->

> Cave culling skips drawing chunks the camera can't see into through open space, such as sealed caves behind rock
> or the underground below a closed surface. Render distance skips chunks beyond a set distance. Collision isn't
> affected by either.

## Turn it on or off

| Setting (world > Rendering) | What it does | Default |
|---|---|---|
| Cave Culling | Hide chunks the camera can't see into | on |
| Render Distance | Chunks farther than this (world units) aren't drawn; 0 = no limit | 0 |

Frustum culling (not drawing what's behind the camera) is the engine's, and it's always on.

## The settings

| Setting | What it does | Default |
|---|---|---|
| Cave Culling | Turns cave culling on or off | on |
| Render Distance | Draw distance in world units (0 = unlimited) | 0 |
| Set Render Distance (node) | Changes the distance at runtime on every chunk | |

## Example
**Blueprint:** Set Render Distance (8000) for 80 m

**C++:**
```cpp
World->SetRenderDistance(8000.f); // 80 m
World->bCaveCulling = false;      // e.g. for a top-down camera
```

## How it works
Each chunk records which of its faces are joined by open space inside it. Each frame, starting from the camera's
chunk, it flood-fills through those openings; chunks it can't reach are hidden.

## When it's off by itself
- While a [cutaway](cutaway.md) is shown.
- In the editor viewport.

## Blueprint nodes and C++ functions

| Name | Blueprint | C++ | What it does |
|---|---|---|---|
| Cave Culling | property | `bool bCaveCulling` | On or off |
| Render Distance | property | `float RenderDistance` | Draw distance |
| Set Render Distance | yes | `void SetRenderDistance(float Distance)` | Changes it at runtime |
| Get Num Cave Culled Chunks | yes | `int32 GetNumCaveCulledChunks() const` | Chunks hidden this frame |

## Limits
- It uses the first local player's camera only. In split-screen it culls for the first player.
- Chunks are coarse, so some hidden chunks may still be drawn.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| Chunks pop in when a cave opens | They become visible once the camera can see in | Expected |
| Split-screen players see holes | Only the first player's camera is used | Turn Cave Culling off for split-screen |
| Distant terrain is missing | Render Distance is set | Raise it, or set 0 |
