---
title: "Materials and textures"
parent: Features
nav_order: 5
---
# Materials and textures

> Every block is drawn from texture arrays (one slice per block face) by four master materials: opaque, masked,
> translucent and fluid. Each block's tint, roughness, metallic, glow and tiling come from a small parameter texture,
> so you can change a block's look at runtime without new materials.

## How do I...?
- **Use my own textures for a block:** set the block's Top, Side or Bottom textures in its table row, or drop images
  in the block set's Source Texture Folder. Then press **RebuildTextureArrays**.
- **Make a block glow:** set Emissive Color and Emissive Strength in its row, or call `Set Block Material Params` at
  runtime.
- **Change a block's look while playing:** `Set Block Material Params` (example below).
- **Use my own material:** set the block set's Opaque/Masked/Translucent/Fluid Material to your material or an
  instance of the master material.

## Turn it on or off
The materials always draw the world. The parts you choose are which textures each block uses (yours, images from a
folder, or generated placeholders) and which material each variant uses.

## The 3 settings you'll use most

| Setting | Where | Default |
|---|---|---|
| Texture Resolution | Block set | 256 px per slice |
| Texture Tiling | World (0 = project default 200) | 200 world units per repeat |
| Tint | Block row | white |

## Where a block face's texture comes from
When you press **RebuildTextureArrays**, each block face uses the first of these that exists:

1. the textures set in the block's table row (Top, Side, Bottom);
2. an image in the block set's **Source Texture Folder**, named `<Block>_<Top|Side|Bottom>_<BaseColor|Normal|Packed>.png`
   (Side alone covers every face; missing Normal and Packed maps are derived from Base Color);
3. a generated placeholder, made from the row's Base Color, Secondary Color, Top Color and Pattern.

**Faces:** Top is used for up-facing surfaces (empty = Side). Side is used for walls and slopes, and for every face
when Top and Bottom are empty. Bottom is used for down-facing surfaces (empty = Top if set, else Side).

**Maps per face**

| Map | What it holds |
|---|---|
| Base Color | sRGB colour, no baked lighting |
| Normal | Tangent-space normal map (DirectX convention, as Unreal imports it) |
| Packed | Linear: R = ambient occlusion, G = roughness, B = metallic, A = height (0.5 = base level, used to blend blocks) |

All slices share one size, the block set's **Texture Resolution**. Textures are resized to it.

## Example: make a block glow at runtime
**Blueprint:** Set Block Material Params (Block = "GlowingQuartz",
Emissive Strength = 8)

**C++:**
```cpp
World->SetBlockMaterialParams(TEXT("Granite"),
	FLinearColor(1.f, 0.9f, 0.9f),   // Tint
	0.6f,                            // Roughness
	0.f,                             // Metallic
	FLinearColor::Black,             // Emissive colour
	0.f,                             // Emissive strength
	1.f);                            // Tiling scale
```
The change applies to every world using this block set **on this machine**. It isn't replicated or saved, so in
multiplayer call it on every machine.

## Materials

| Asset | Used for |
|---|---|
| `/SuperVoxel/Materials/M_SuperVoxel_Opaque` | Opaque blocks |
| `/SuperVoxel/Materials/M_SuperVoxel_Masked` | Cut-out blocks: leaves, grates, plants |
| `/SuperVoxel/Materials/M_SuperVoxel_Translucent` | See-through blocks: glass, ice |
| `/SuperVoxel/Materials/M_SuperVoxel_Fluid` | Liquids |

A block set's own material fields override these; empty fields fall back to the project defaults.

## Blueprint nodes and C++ functions

| Name | Blueprint | C++ | What it does |
|---|---|---|---|
| Set Block Material Params | yes | `ASuperVoxelWorld::SetBlockMaterialParams(Block, Tint, Roughness, Metallic, EmissiveColor, EmissiveStrength, TilingScale)` | Changes how a block is drawn at runtime |
| RebuildTextureArrays | button on the block set | `USuperVoxelBlockSet::RebuildTextureArrays()` (editor) | Rebuilds the arrays |
| (command line) | | `-run=SuperVoxelBuildContent [-Resolution=256] [-NoMaps]` | Rebuilds all plugin content, including the arrays (see [Editor tools](editor-tools.md)) |

## Limits and performance
- One draw section per variant per chunk, so many block types cost no extra draw calls.
- Higher Texture Resolution means more texture memory (4 maps × slices × resolution²).
- The placeholder textures are made by the plugin's own code; no external or AI art.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| My texture doesn't show | Arrays not rebuilt, or a wrong file name in the source folder | RebuildTextureArrays; check `<Block>_<Face>_<Map>.png` |
| Textures look blurry | Texture Resolution is low | Raise it on the block set and rebuild |
| Textures repeat too often or too rarely | Tiling | Change Texture Tiling on the world, or Tiling Scale per block |
| A runtime colour change shows only for me | `Set Block Material Params` is local | Call it on every machine |
