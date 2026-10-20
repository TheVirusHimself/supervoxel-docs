---
title: "Install and upgrade"
nav_order: 4
---
# Install and upgrade

## Requirements

| | |
|---|---|
| Engine | Unreal Engine 5.8 |
| Platforms | Windows (Win64) is built and tested. Linux and Mac aren't verified yet (see the [Roadmap](roadmap.md)) |
| Graphics | Shader Model 5 or newer (the materials sample texture arrays). DirectX 11 or 12 at SM5 or SM6 works; verified on DirectX 12. Mobile (ES3.1) is untested |
| Engine plugins | Procedural Mesh Component, Enhanced Input (both ship with the engine; turned on automatically) |
| Third-party software | None |
| Known incompatibilities | None known |

## Install from Fab
SuperVoxel is coming soon to Fab. Once it's listed:

1. In the Epic Games Launcher, open your Fab library, find SuperVoxel and choose **Install to Engine** (5.8).
2. Open your project and tick SuperVoxel in Edit > Plugins, then restart the editor.

## Install into one project
1. Copy the `SuperVoxel` folder into your project's `Plugins` folder.
2. Open the project. The modules compile with it (C++ projects: regenerate project files first).
3. Check Edit > Plugins: SuperVoxel is enabled.

## The modules

| Module | Type | What it holds | Can I leave it out? |
|---|---|---|---|
| SuperVoxel | Runtime | The world actor, block sets, generators, meshing, editing, saves, multiplayer, scatter, the Blueprint library | No (the core) |
| SuperVoxelNavigation | Runtime | Pathfinding: the A* search, the async node, the path-follower component | Yes |
| SuperVoxelDemo | Runtime | Bumble, the walkers, the demo game modes and HUD, the block gallery | Yes |
| SuperVoxelEditor | Editor | The sculpt mode, the texture-array builder, the content commandlet | Editor only; not in packaged games |
| SuperVoxelLaylines | Runtime | Signal wiring: wires, switches, gates, timers, lamps, doors, displays ([Laylines](features/laylines.md)) | Optional module: does nothing until Enable Laylines is on |
| SuperVoxelFluids | Runtime | Flowing water and lava, emitters and drains ([Fluids](features/fluids.md)) | Optional module: does nothing until Enable Fluids is on |
| SuperVoxelFluidsEditor | Editor | Fluids editor support | Editor only |

SuperVoxel is one plugin: there are no separate Laylines or Fluids plugins to install.

**Optional modules: Laylines and Fluids.** Both are part of the SuperVoxel plugin and compile with it, but do nothing
until you turn them on in **Project Settings > Plugins > SuperVoxel > Optional Modules**:

- **Enable Laylines** (off by default): creates the Laylines world subsystem. Off, layline blocks are plain blocks.
  Applies to worlds that start after the change.
- **Enable Fluids** (off by default): lets Fluids components run. Off, fluid blocks stay where they are and SuperVoxel
  draws them. Applies at once.

From code: **Is / Set Laylines Enabled** and **Is / Set Fluids Enabled** (C++: `USuperVoxelSettings`). The Set calls
last for the run; the Project Settings switches are saved in `Config/DefaultGame.ini`.

**Per map:** a game mode or World Settings class that implements **SuperVoxel Optional Modules** (C++:
`ISuperVoxelOptionalModules`, `WantsLaylines` / `WantsFluids`) turns the modules on for the maps that use it, even
with the project switches off. **Is Laylines Enabled In** / **Is Fluids Enabled In** (World Context) answer for one
world. The demo game mode does this (its **Enable Laylines** / **Enable Fluids**, on by default), so the demo map works
out of the box. The Fluids materials (`/SuperVoxel/Fluids`, about 8 MB) are always cooked.

## Use it from C++
Add the modules you use to your module's `Build.cs`:
```csharp
PublicDependencyModuleNames.AddRange(new string[] { "SuperVoxel" });
// Pathfinding too:
PublicDependencyModuleNames.AddRange(new string[] { "SuperVoxelNavigation" });
// Laylines or Fluids from C++:
PublicDependencyModuleNames.AddRange(new string[] { "SuperVoxelLaylines", "SuperVoxelFluids" });
```

## Upgrade to a new version
- Saves, block names and assets stay compatible within 1.x. A change that needs a migration comes with a step in the
  [changelog](changelog.md).
1. Back up your project.
2. Read the [changelog](changelog.md) for the new version.
3. Update the plugin (from Fab, or replace the plugin folder), then open the project and let it rebuild.

**Upgrading from a pre-release** with separate Laylines and Fluids plugins: delete the old `Plugins/SuperVoxelLaylines`
and `Plugins/SuperVoxelFluids` folders, then turn on Enable Laylines / Enable Fluids in Project Settings if you used
them. Fluids content moved from `/SuperVoxelFluids/...` to `/SuperVoxel/Fluids/...`.

## Uninstall
1. Remove SuperVoxel worlds and components from your levels and Blueprints.
2. Untick SuperVoxel in Edit > Plugins (or delete the plugin folder from your project) and restart the editor.
