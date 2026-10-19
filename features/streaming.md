---
title: "Unbounded worlds"
parent: Features
nav_order: 18
---
# Unbounded worlds (streaming)
{: .no_toc }

> An unbounded world is endless in X and Y. Chunks are generated and drawn around the players (and any actors you
> add as anchors) and dropped again when everyone moves away. Edits are kept even while their chunks are unloaded.
> It's opt-in: worlds are bounded unless you set World Mode to Unbounded.

## How do I...?
- **Make an endless world:** set the world's **World Mode** to **Unbounded**. **World Size Z** is the height.
- **Keep the ground loaded around an NPC or a vehicle:** `Add Streaming Anchor (Actor)`.
- **Spawn only once the ground is there:** wait until `Is Area Ready (Location)` is true.

## Turn it on or off
**World Mode** on the world: **Bounded** (the default, a box of World Size voxels) or **Unbounded**. While Bounded,
none of the streaming work runs.

## The 3 settings you'll use most

| Setting | What it does | Default |
|---|---|---|
| World Mode | Bounded or Unbounded | Bounded |
| Load Radius | Chunks within this distance of a player or anchor are generated and drawn (world units) | 9600 |
| Stream Around Players | Stream around every player pawn (the server: all players; a client: its own) | on |

## Example: an NPC that keeps the world loaded around it
**Blueprint:** Begin Play → Find Voxel World → Add Streaming Anchor
(Self); End Play → Remove Streaming Anchor (Self)

**C++:**
```cpp
#include "SuperVoxelWorld.h"
#include "SuperVoxelLibrary.h"

void AMyNpc::BeginPlay()
{
	Super::BeginPlay();
	if (ASuperVoxelWorld* World = USuperVoxelLibrary::FindVoxelWorld(this))
	{
		World->AddStreamingAnchor(this);
	}
}
```

## All settings (world > Streaming)

| Setting | Default | What it does |
|---|---|---|
| World Mode | Bounded | Bounded (a box) or Unbounded (endless in X and Y; World Size Z is the height) |
| Load Radius | 9600 | Distance around players and anchors that is generated and drawn (world units, min 500) |
| Unload Margin | 3200 | Chunks are dropped once farther than Load Radius plus this, so edges don't flicker |
| Max Chunk Generations In Flight | 24 | Chunks generated at once on worker threads (1–256) |
| Stream Around Players | on | Stream around player pawns |
| Editor Preview Radius | 4800 | In the editor viewport: preview radius around the world actor |

## Blueprint nodes and C++ functions (on the world)

| Name | Blueprint | C++ | What it does |
|---|---|---|---|
| Add Streaming Anchor | yes | `void AddStreamingAnchor(AActor* Anchor)` | Also stream around this actor |
| Remove Streaming Anchor | yes | `void RemoveStreamingAnchor(AActor* Anchor)` | Stop streaming around it |
| Is Area Ready | yes | `bool IsAreaReady(FVector Location) const` | The ground around a location is generated and meshed (bounded worlds: the world is built). A column counts as in range when any part of it is within Load Radius |
| Is Voxel Loaded | yes | `bool IsVoxelLoaded(FIntVector Voxel) const` | The voxel's data is in memory (always true inside a built bounded world) |
| Get Num Loaded Chunks | yes | `int32 GetNumLoadedChunks() const` | Chunks in memory |

## Events (C++ only)

| Event | When it fires |
|---|---|
| `OnChunkLoaded` | A chunk was generated (or regenerated) and its edits applied (parameter: the chunk coordinate) |
| `OnChunkUnloaded` | A chunk was dropped from memory; its edits stay in the journal |

## How the other features work in an unbounded world
- **Generators:** the generator must support chunk generation. Flat and Layered Terrain do. A few Layered Terrain
  features work differently or not at all: no world sides, lakes filled per column, no underground or molten pools,
  only lone voxels cleaned up, shore distance estimated. See [Terrain generator](generator.md).
- **Saves:** edits are saved by position, including edits to chunks that aren't loaded; they're applied when the
  chunk loads. See [Save and load](save-load.md).
- **Multiplayer:** each client asks the server for the edits of the chunks it loads, and the server sends live edits
  only for chunks that player has loaded. A chunk's edits are sent in one go, not paged (see Limits). See
  [Multiplayer](multiplayer.md).
- **Pathfinding:** a goal in chunks that aren't loaded gives a partial path as close as the loaded ground allows. See
  [Pathfinding](pathfinding.md).
- **Structures:** Place Structure and Spawn Village work anywhere. Structure and village **rules** (spawned at
  generation) work in bounded worlds only.

## Write a generator for unbounded worlds (C++)
Override two more functions on your `USuperVoxelGenerator`:

- `SupportsChunkGeneration()`: return true.
- `GenerateChunk(const FSuperVoxelChunkGenerationContext& Context) const`: fill one chunk. It may run on any thread,
  many chunks at once. Chunks must join seamlessly, so a voxel's block may depend only on its world position, the
  seed and your settings, never on other chunks.

The chunk context gives you `Origin` (the chunk's lowest voxel corner; X and Y may be negative), `Size` (voxels per
axis), `WorldHeight`, `Seed`, `VoxelSize`, the block registry and the chunk's voxels (index = X + Y·Size.X +
Z·Size.X·Size.Y, chunk-local, all Air on entry).

## Limits and performance
- No distance detail levels (LOD): every loaded chunk is meshed at full detail. Load Radius sets the cost.
- Height up to 65535 voxels. X and Y within about ±8.3 million voxels of the origin; far from the origin the finest
  terrain detail slowly coarsens.
- Cave culling and render distance work as in bounded worlds ([Culling](culling.md)).
- **Unbounded worlds with multiplayer:** a chunk's edits are sent to a player in one go (in messages of 1,500
  changes, with all of the chunk's metadata in the last one), not paged like bounded worlds. Chunks with very large
  edit or metadata histories (tens of thousands of edits, or thousands of metadata entries, in the chunks one player
  loads at once) can exceed the engine's message size. Bounded worlds have no such limit.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| A custom generator gives an empty unbounded world | It doesn't implement chunk generation | Add `SupportsChunkGeneration` and `GenerateChunk`, or use Flat or Layered Terrain |
| Holes at the edge of view | Load Radius is smaller than the view | Raise Load Radius, or set a Render Distance below it |
| The player falls at the start | Spawned before the ground loaded | Wait for `Is Area Ready` at the spawn point |
| An NPC far from players walks into nothing | No chunks are loaded around it | `Add Streaming Anchor` on the NPC |
