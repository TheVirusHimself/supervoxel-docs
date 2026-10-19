---
title: "Block set and block types"
parent: Features
nav_order: 1
---
# Block set and block types

> A block set is a data asset that lists the block types a world can use. The block types live in tables, one row per
> block. Add a row to add a block, with no code.

## How do I...?
- **Use the 450 shipped blocks:** do nothing. Worlds use the default block set, `/SuperVoxel/Blocks/BS_SuperVoxelDefault`.
- **Add a block:** add a row to a block table (a DataTable with row type **SuperVoxelBlockDef**, or `Data/SuperVoxelBlocks.csv`),
  then press **RebuildTextureArrays** on the block set.
- **Override a shipped block:** make your own table with a row of the same name and list it *after* the default table
  in the block set's **Tables**. Later rows win.
- **Use my own textures:** see [Materials and textures](materials.md).

## Turn it on or off
Every world needs a block set. If a world's **Block Set** is empty it uses the project default (Project Settings >
Plugins > SuperVoxel > Default Block Set). If neither is set, the world is empty and the log says so.

## The 3 settings you'll use most

| Setting | What it does | Default |
|---|---|---|
| Kind | Smooth (natural ground), Blocky (crisp cubes) or Fluid (liquid) | Smooth |
| Base Color | The main colour, also used for the generated placeholder texture | grey |
| Opacity | Opaque, Masked (cut-out, like leaves) or Translucent (see-through) | Opaque |

## Example: add a block
Don't edit the shipped `BS_SuperVoxelDefault` or its table: a plugin update overwrites them. Make your own:

1. **Your block table:** in the Content Browser, Add > Miscellaneous > Data Table, row structure
   **SuperVoxelBlockDef**. Add a row named `MossyGranite`; set Kind = Smooth, Category = Stone, Base Color and
   Secondary Color, Pattern = Speckle.
2. **Your block set:** Add > Miscellaneous > Data Asset, class **SuperVoxelBlockSet**. In its **Tables**, add the
   shipped `DT_SuperVoxelBlocks` first, then your table (later rows win).
3. Press **RebuildTextureArrays** (Textures section) on your block set.
4. **Use your set:** set the world's **Block Set** to it, or make it the project default (Project Settings > Plugins >
   SuperVoxel > Default Block Set).
5. Use the block: `Set Block (Voxel, "MossyGranite")`, or pick it in the sculpt mode.

**Using a CSV instead:** a DataTable imported from a CSV doesn't follow later edits to the file by itself. After
changing the CSV, right-click the table > Reimport, then press RebuildTextureArrays again.


**C++: read a block's definition**
```cpp
FSuperVoxelBlockDef Def;
if (World->GetBlockDef(TEXT("Granite"), Def))
{
	UE_LOG(LogTemp, Log, TEXT("%s: hardness %.1f"), *Def.DisplayName.ToString(), Def.Hardness);
}
```

## The shipped catalog
450 blocks in 17 categories: Worked Stone (60), Wood (54), Ore (50), Plant (38), Soil (34), Stone (32), Masonry (24),
Glass (22), Metal (21), Fantasy (20), Concrete (16), Cloth (16), Tile (16), Fired Clay (16), Light (12), Liquid (10),
Gem (9). Of these, 125 are Smooth, 315 Blocky and 10 Fluid; 391 are Opaque, 22 Masked and 37 Translucent.

Block names are the row names, written without spaces: `Granite`, `OakPlanks`, `GrassTurf`, `ClearGlass`.
The full list is the block table, `Data/SuperVoxelBlocks.csv`, in the plugin.

## All block settings (`FSuperVoxelBlockDef`)
**Block**

| Setting | Type | Default | What it does |
|---|---|---|---|
| (Row name) | name | | The block's id in code and saves, e.g. `OakPlanks` |
| Display Name | text | | Name shown to players |
| Category | name | | Free grouping for menus and filters ("Stone", "Soil"...) |
| Kind | Smooth / Blocky / Fluid | Smooth | How it's meshed |
| Opacity | Opaque / Masked / Translucent | Opaque | Which material variant draws it |
| Hardness | float ≥ 0 | 1 | Relative effort to dig. Your game decides what it means; brushes ignore it |
| Indestructible | bool | false | Every protection at once: never dug, damaged, collapsed or blasted (the world's floor). For each protection on its own, see [Destruction settings](destruction.md) |
| Hidden | bool | false | Solid but not drawn: something else renders it |
| Move Speed | float ≥ 0 | 1 | Walk speed multiplier on top of this block (pathfinding reads it). 0 = can't stand on it |
| Tags | Gameplay Tags | | Free tags for your game ("Ore", "Flammable"...) |

**Look** (used for the generated placeholder texture)

| Setting | Type | Default | What it does |
|---|---|---|---|
| Base Color | colour (sRGB) | grey | Main colour |
| Secondary Color | colour (sRGB) | dark grey | Grain, mortar, flecks, veins... |
| Pattern | enum | Noise | Noise, Speckle, Strata, Grain, Planks, Bricks, Tiles, Ore Flecks, Crystal, Weave, Ripple, Leaves, Metal, Glass, Cobble, Solid |
| Top Color | colour (sRGB) | alpha 0 | Top face colour if it differs (turf, log ends). Alpha 0 = same as Base Color |

**Material** (can be changed at runtime, see [Materials](materials.md))

| Setting | Type | Default | What it does |
|---|---|---|---|
| Tint | colour (sRGB) | white | Multiplies the texture colour |
| Roughness | 0..1 | 0.85 | |
| Metallic | 0..1 | 0 | |
| Emissive Color | colour (linear) | black | Emitted light colour, times Emissive Strength |
| Emissive Strength | float ≥ 0 | 0 | Glow strength |
| Tiling Scale | float ≥ 0.01 | 1 | Texture repeats relative to the world's tiling (2 = twice as dense) |
| Opacity Value | 0..1 | 1 | Opacity of translucent blocks |

**Textures:** Top, Side and Bottom, each with Base Color, Normal and Packed maps. See [Materials](materials.md).

**Gameplay**

| Setting | Type | Default | What it does |
|---|---|---|---|
| Falls | bool | off | Drops straight down when nothing holds it up (checked whenever a voxel next to it changes); columns come down together and stop on solid ground. On in the default table for Sand, Red Sand, Black Sand, White Sand and Gravel |
| Collides | bool | on | Off: characters and physics pass through it (plants, cobwebs, decorations). It's still drawn, still hides what's behind it, and Trace Voxel still hits it; pathfinding walks through it. Blocky blocks only; smooth ground always collides |
| Behavior | class | none | A [block behaviour](block-behaviors.md) |
| Random Tick | bool | off | Gets random ticks ([Ticks](ticks.md)) |
| Tintable | bool | off | Voxels of this block can be coloured one by one ([Voxel tint](state-and-metadata.md#voxel-tint)) |
| Max Health, Drop Item, Drop Count, Drop Chance, Drop Actor | | 0, None, 1, 1, none | See [Damage and drops](damage-and-drops.md) |
| Light Intensity, Light Color, Light Radius | | 0, white, 1000 | See [Light blocks](lights.md) |

## Block set settings (`USuperVoxelBlockSet`)

| Setting | Default | What it does |
|---|---|---|
| Tables | | Block tables (row structure SuperVoxelBlockDef). Later rows with the same name override earlier ones |
| Opaque / Masked / Translucent / Fluid Material | empty | Materials per variant. Empty = the project defaults |
| Texture Resolution | 256 | Pixel size of each texture-array slice (16–4096). Rebuild the arrays after changing it |
| Source Texture Folder | empty | Optional folder of images used before the placeholders (editor only) |
| RebuildTextureArrays | button | Rebuilds the arrays from the block textures, the source folder and placeholders (editor only) |

## Blueprint nodes and C++ functions

| Name | Blueprint | C++ (on `ASuperVoxelWorld`) | What it does |
|---|---|---|---|
| Get Block Id | yes | `GetBlockId(FName Block)` | Name to id |
| Get Block Name | yes | `GetBlockName(int32 BlockId)` | Id to name |
| Get All Block Names | yes | `GetAllBlockNames()` | Every block name (Air excluded), in id order |
| Get Block Def | yes | `GetBlockDef(FName Block, FSuperVoxelBlockDef& OutDef)` | The block's settings (false if it doesn't exist) |

## Limits
- Up to 4096 block types per set (block ids are 16-bit). Id 0 is always Air.
- **Ids can change** when the set changes, so store names. Saves already do.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| "no block set (and no default block set in Project Settings > SuperVoxel); the world will be empty." | Neither the world nor the project names a block set | Set one on the world, or restore the project default |
| "Too many block types; 'X' ignored (limit 4096)" | Over the limit | Remove unused rows |
| "Unknown block 'X', using Air" | A name (in a save or setting) isn't in the set | Fix the name or add the block |
| A new block looks plain grey | Texture arrays not rebuilt | Press RebuildTextureArrays |
