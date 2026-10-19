---
title: "Terrain generator"
parent: Features
nav_order: 3
---
# Terrain generator

> A generator fills a new world from its seed. SuperVoxel ships two: **Layered Terrain** (hills, ridges, cliffs,
> overhangs, caves, rock layers, ore veins, surface rules, lakes and trees) and **Flat**. You can write your own.

## How do I...?
- **Get natural terrain:** set the world's **Generator** to **Layered Terrain**, then try a few **Seed** values.
- **Get a flat building plot:** set **Generator** to **Flat**.
- **Make more or fewer caves:** Layered Terrain > Caves > **Cave Amount** (0 = none, 1 = normal, 2 = many and wide).
- **Change what covers the ground:** edit **Surface Rules** (the first rule that matches a spot wins).
- **Write my own terrain:** subclass `USuperVoxelGenerator` in C++ (see the end of this page).

## Turn it on or off
**Generator** is a setting on the world. Leave it empty and the world is all air (useful if you fill it yourself).

## The 3 settings you'll use most

| Setting | Where | What it does | Default |
|---|---|---|---|
| Seed | World | Picks the layout. The same seed, size, block set and generator settings make the same world on every machine | 1 |
| Hill Height | Layered Terrain > Shape | How far hills rise and valleys sink, in meters | 8 |
| Water Level | Layered Terrain > Water | Lake surface as a fraction of world height (0 = no lakes) | 0.37 |

## Example
**Editor:** select the world, set Generator to Layered Terrain, change Seed. The viewport preview updates.

**C++: set it up at runtime**
```cpp
#include "SuperVoxelWorld.h"
#include "SuperVoxelTerrainGenerator.h"

USuperVoxelTerrainGenerator* Gen = NewObject<USuperVoxelTerrainGenerator>(World);
Gen->HillHeight = 14.f;
Gen->CaveAmount = 0.5f;
Gen->WaterLevel = 0.f;          // no lakes
World->Generator = Gen;
World->Seed = 1234;
World->Rebuild();
```

## The seed

| Setting or node | What it does |
|---|---|
| Seed | The layout. Default 1 |
| Random Seed | A new seed each time the world is generated at runtime (Begin Play or Rebuild). In multiplayer the server picks it and clients receive it. Default off |
| Get Seed | The seed in use (read it to show or share a random world) |
| Set Seed And Regenerate | Sets the seed and generates again. Runtime edits are dropped. Server or standalone only |

Loading a save and `Reset Edits` keep the current seed, even with Random Seed on.

```cpp
World->SetSeedAndRegenerate(98765);
```

## Meters, voxels and fractions
Layered Terrain mixes three units, as each setting's tooltip says:

- **meters** for sizes you'd measure (hill height, tunnel width, tree height), so the look holds when you change the
  voxel size;
- **fractions of world height** for levels (ground level, water level, altitudes);
- **voxels** for a few counts (floor thickness, cave floor clearance).

**Depth fraction** (used by stone layers and ores): 0 is the reference ground level and 1 is the top of the floor.

## Layered Terrain: all settings
**Shape**

| Setting | Default | What it does |
|---|---|---|
| Ground Level | 0.42 | Average ground height as a fraction of world height; also where depth fraction 0 starts |
| Hill Height | 8 m | How far hills rise and valleys sink from the ground level |
| Hill Scale | 28 m | Typical distance between hilltops |
| Ridge Amount | 0.6 | Strength of sharp ridges inside rocky regions (0 = none) |
| Cliff Amount | 0.5 | How strongly rocky regions step into shelves and cliffs (0 = smooth slopes) |
| Terrace Step | 2 m | Height of one cliff terrace |
| Overhang Strength | 0.6 | 3D noise that carves overhangs and builds outcrops (0 = plain heightmap) |
| Roughness | 0.5 | Fine detail: more hill octaves and small surface bumps |
| Warp Amount | 0.6 | Bends features so they don't follow the grid |
| Edge Rim | 6 m | Width of the band along the world's sides raised above the water level |

**Caves**

| Setting | Default | What it does |
|---|---|---|
| Cave Amount | 1 | 0 = none, 1 = normal, 2 = many and wide |
| Tunnel Scale | 28 m | Distance between tunnel bends |
| Tunnel Width | 2.5 m | Approximate tunnel width |
| Chamber Scale | 14 m | Size of cave chambers |
| Chamber Amount | 0.5 | How often chambers appear (0 = tunnels only) |
| Cave Surface Margin | 4 m | Caves fade out within this depth below the surface, so they rarely break through |
| Cave Entrances | 0.25 | Share of places where caves may open to the surface (0 = never) |
| Cave Floor Clearance | 4 voxels | No caves this close above the floor |

**Layers**

| Setting | Default | What it does |
|---|---|---|
| Bedrock Block | BaseRock | The floor block (make it indestructible in the block set) |
| Floor Thickness | 3 voxels | Floor thickness |
| Floor Unevenness | 2 voxels | Extra bumps on top of the floor |
| Fallback Stone | Granite | Rock where no layer matches, and the floor if the floor block is missing |
| Stone Layers | (list) | Rock types by depth band and region; at most 32 are used |
| Layer Region Size | 48 m | Size of the horizontal regions that pick different rock within a band |
| Layer Warp | 3 m | Waviness of the depth bands |
| Layer Blend | 0.03 | Raggedness of band edges |

A **stone layer** has: Block, Min Depth and Max Depth (depth fractions), and Region Weight (its share of the regions
within its depth range).

**Ores**

| Setting | Default | What it does |
|---|---|---|
| Ores | (list) | Ore vein types |
| Deep Band Start | 0.85 | Depth fraction where ores switch to their deep variant |

An **ore vein** has: Block; Deep Block (used in the deepest band; None = always Block); Min Depth and Max Depth;
Vein Size (about how many voxels, default 6); Frequency (veins per 1000 rock voxels in its range, default 0.1).

**Surface**

| Setting | Default | What it does |
|---|---|---|
| Surface Rules | (list) | Ordered; the first matching rule wins |
| Moisture Scale | 80 m | Size of wet and dry areas |
| Patch Scale | 6 m | Size of sand, gravel and clay patches |
| Shore Width | 2 m | Distance from a lake that counts as shore |
| Shore Height | 1 m | Height above the water that still counts as shore |

A **surface rule** says what covers the ground where all its conditions hold:

| Field | Default | What it does |
|---|---|---|
| Top Block | None | Block on the top voxel (None = bare rock) |
| Filler Block | None | Block under the top voxel (None = rock) |
| Filler Depth | 1 m | Depth of top plus filler |
| Min Altitude, Max Altitude | 0, 1 | Altitude range, as fractions of world height |
| Min Slope, Max Slope | 0°, 90° | Slope range (90 = no limit) |
| Water | Any | Any, Dry (not under water or on a shore), Shore, or Underwater (lake beds) |
| Min Moisture, Max Moisture | 0, 1 | Moisture range |
| Coverage | 1 | Applies where the shared patch value is at or below this. Rules share one patch value, so rules in a row with rising coverage split an area into patches |

**Water**

| Setting | Default | What it does |
|---|---|---|
| Fluid Block | Water | Fluid for lakes and underground pools |
| Water Level | 0.37 | Lake surface as a fraction of world height (0 = no lakes) |
| Underground Pools | on | Allow closed pools in large cave chambers |
| Underground Pool Attempts | 8 | Placement tries; most fail, which keeps pools rare |
| Underground Pool Depth | 0.75 m | Depth of underground and molten pools |
| Min Pool Voxels, Max Pool Voxels | 40, 8000 | Accepted pool sizes |
| Molten Pools | off | Pools of Molten Block in the deepest chambers (never next to water) |
| Molten Block | MoltenRock | The molten fluid |
| Molten Pool Attempts | 6 | Placement tries |
| Molten Max Height | 0.3 | Highest point for molten pools, as a fraction from the floor to the ground level |

**Trees**

| Setting | Default | What it does |
|---|---|---|
| Trees | on | Grow trees |
| Tree Density | 0.6 | Trees per 100 m² of suitable ground (approximate) |
| Tree Min Spacing | 4 m | Minimum distance between trunks |
| Max Tree Slope | 30° | Steepest ground a tree grows on |
| Tree Ground Blocks | (list) | Blocks trees may stand on |
| Tree Kinds | (list) | One is picked by weight among the kinds whose altitude and moisture fit |

A **tree kind** has: Log Block (the kind is skipped if missing); Leaves Block (None = bare trunk); Shape (Round, Tall
or Cone); trunk height 3.5–5.5 m; crown radius 1.75–2.75 m; Trunk Width 0.5 m; altitude and moisture ranges; and
Weight.

## Flat: all settings

| Setting | Default | What it does |
|---|---|---|
| Ground Height | 16 | Height of the ground in voxels |
| Surface Block | GrassTurf | The top layer |
| Fill Block | Loam | Under the surface |
| Fill Depth | 4 | Layers of Fill Block before stone starts |
| Stone Block | Granite | Below the fill |
| Bedrock Block | BaseRock | The bottom layer |

## Heightmap: all settings
The **Heightmap** generator (`USuperVoxelHeightmapGenerator`) builds terrain from a texture whose brightness is
height.

| Setting | Default | What it does |
|---|---|---|
| Heightmap | none | The texture |
| Height Min | 4 | Height of black, in voxels |
| Height Range | 48 | Voxels from black to white |
| Fit To World | on | Stretch the image over the world. Off: tile it at Voxels Per Pixel (unbounded worlds always tile) |
| Voxels Per Pixel | 1 | Scale when tiling |
| Top Block | GrassTurf | The top layer |
| Below Block, Below Depth | Loam, 3 | The layer under the top, and its depth |
| Stone Block | Granite | Below that |
| Bedrock Block | BaseRock | The bottom layer |
| Water Level | -1 | Water up to this height (-1 = no water) |
| Water Block, Shore Block | Water, Sand | The water, and the block at its edges |

**For packaged games the texture must be readable by the CPU:** Compression Settings = Grayscale or HDR, Mip Gen
Settings = NoMipmaps, Never Stream on. In the editor any texture works. 16-bit images keep slopes smooth.

## Write your own generator (C++)
Subclass `USuperVoxelGenerator` and override:

- `Prepare(const FSuperVoxelBlockRegistry& Blocks)`: runs on the game thread first. Turn block names into ids here, not
  per voxel.
- `Generate(const FSuperVoxelGenerationContext& Context) const`: fills `Context.Voxels` (all Air on entry). It may run on
  a worker thread, so it must only read your generator and write the grid. It must give the same result for the
  same seed, size and settings on every machine, because multiplayer clients and saves rebuild from the seed.
- `GetSpawnColumn(...)` (optional): the suggested player spawn column; the default is the world center.

```cpp
#include "SuperVoxelGenerator.h"
#include "SuperVoxelBlockRegistry.h"
#include "MyStripesGenerator.generated.h"

UCLASS(meta = (DisplayName = "Stripes"))
class UMyStripesGenerator : public USuperVoxelGenerator
{
	GENERATED_BODY()
public:
	virtual void Prepare(const FSuperVoxelBlockRegistry& Blocks) override
	{
		Stone = Blocks.FindId(TEXT("Granite"), true);
	}

	virtual void Generate(const FSuperVoxelGenerationContext& Context) const override
	{
		for (int32 Z = 0; Z < Context.SizeZ / 3; ++Z)
			for (int32 Y = 0; Y < Context.SizeY; ++Y)
				for (int32 X = 0; X < Context.SizeX; ++X)
					Context.Voxels[Context.Index(X, Y, Z)] = Stone;
	}

private:
	FSuperVoxelBlockId Stone = 0;
};
```
The **context** gives you SizeX/Y/Z, Seed, VoxelSize, the block registry, the voxel grid (index =
X + Y·SizeX + Z·SizeX·SizeY, Z is up) and an optional progress value (`SetProgress(0..1)`) for loading screens.

## Unbounded worlds
Flat and Layered Terrain both generate chunk by chunk for [unbounded worlds](streaming.md). Layered Terrain works
differently there: there are no world sides (Edge Rim doesn't apply), lakes are filled per column, underground and
molten pools are off, only lone voxels are cleaned up, and the shore distance is estimated. To support unbounded
worlds in your own generator, see [Unbounded worlds](streaming.md).

## Limits and performance
- Generation runs on worker threads when the world builds. `Get Last Generate Ms` reports how long it took.
- Layered Terrain needs at least 8 voxels per axis.

## Troubleshooting

| Message | Why | Fix |
|---|---|---|
| "Layered Terrain: block set has no X; those features are skipped." | A block the settings name isn't in the set | Add the block or change the setting |
| "Layered Terrain: none of the rock blocks exist in the block set; nothing generated." | No layer or fallback stone exists | Use the default block set or fix the names |
| "Layered Terrain: only the first 32 of N stone layers are used." | More than 32 layers | Remove some |
| "Layered Terrain: world AxBxC is too small (8 voxels per axis minimum)." | Tiny world | Make it bigger |
| "Layered Terrain: no block registry; call Prepare first." / "voxel buffer does not match the world size." | A custom caller skipped Prepare or passed a wrong buffer | Let the world run the generator, or call Prepare first |
| "Heightmap X: its pixel format can't be read at runtime. ..." | The texture isn't CPU-readable | Set Grayscale or HDR, NoMipmaps, Never Stream on |
| "Heightmap generator: X couldn't be read; the ground is flat." | The texture couldn't be read | Check the texture and its settings |
| Same seed, different world on another machine | Different block set or generator settings | Use the same assets everywhere |
| "SetSeedAndRegenerate: only the server can change the seed." | Called on a client | Call it on the server |
