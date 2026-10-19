---
title: "Light blocks"
parent: Features
nav_order: 24
---
# Light blocks

> Blocks can give off real light: lamps, crystals, lava. The light-giving voxels nearest the camera get point lights
> from a small pool, so a world full of lamps stays cheap.

## Turn it on or off
- A block gives light when its **Light Intensity** (block table) is above 0. The 12 blocks in the Light category do
  by default.
- **Voxel Lights** on the world (on by default). Off: light blocks only glow.

## The 3 settings you'll use most

| Setting | Where | Default |
|---|---|---|
| Light Intensity | Block table | 0 (candelas; 0 = no light) |
| Max Voxel Lights | World > Lights | 24 |
| Voxel Light Distance | World > Lights | 5000 cm (50 m) |

## Example
**Block table:** set a block's Light Intensity to 800, Light Color to warm orange and Light Radius to 600.

**C++: tune it at runtime**
```cpp
World->MaxVoxelLights = 48;
World->bVoxelLightShadows = false; // shadows are costly with many lights
```

## Block table columns

| Column | Default | What it does |
|---|---|---|
| Light Intensity | 0 | Candelas; 0 = gives no light |
| Light Color | white | The light's colour |
| Light Radius | 1000 | Reach in cm |

## World settings (world > Lights)

| Setting | Default | What it does |
|---|---|---|
| Voxel Lights | on | Light blocks get real point lights near the camera. Off: they only glow |
| Max Voxel Lights | 24 | Most point lights at once (0–256); the light blocks nearest the camera get them |
| Voxel Light Distance | 5000 | Light blocks farther than this (cm) get no light |
| Voxel Light Shadows | off | The lights cast shadows (costly with many lights) |

## Blueprint nodes

| Name | C++ | What it reports |
|---|---|---|
| Get Num Light Emitters | `int32 GetNumLightEmitters() const` | Light-giving voxels in the loaded world |
| Get Num Active Voxel Lights | `int32 GetNumActiveVoxelLights() const` | Point lights lit right now |

## Limits
- Light blocks above the [cutaway](cutaway.md) are hidden, and give no light.
- Only the nearest Max Voxel Lights emitters are lit; the rest glow without light.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| Far lamps are dark | Beyond Voxel Light Distance, or over Max Voxel Lights | Raise the setting |
| Frame rate drops near many lamps | Shadows are on | Turn Voxel Light Shadows off |
