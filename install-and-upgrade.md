---
title: "Install and upgrade"
nav_order: 4
---
# Install and upgrade

<!-- Status: draft (module facts checked against 0f6bdf3; Fab install steps added once the listing exists) -->

## Requirements

| | |
|---|---|
| Engine | Unreal Engine 5.8 |
| Platforms | Windows (Win64) is built and tested. Linux and Mac are planned, not supported yet |
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
| SuperVoxelEditor | Editor | The sculpt mode, the texture-array builder, the content commandlet, automation tests | Editor only; not in packaged games |

## Use it from C++
Add the modules you use to your module's `Build.cs`:
```csharp
PublicDependencyModuleNames.AddRange(new string[] { "SuperVoxel" });
// Pathfinding too:
PublicDependencyModuleNames.AddRange(new string[] { "SuperVoxelNavigation" });
```

## Upgrade to a new version
- Saves, block names and assets stay compatible within 1.x. A change that needs a migration comes with a step in the
  [changelog](changelog.md).
1. Back up your project.
2. Read the [changelog](changelog.md) for the new version.
3. Update the plugin (from Fab, or replace the plugin folder), then open the project and let it rebuild.

## Uninstall
1. Remove SuperVoxel worlds and components from your levels and Blueprints.
2. Untick SuperVoxel in Edit > Plugins (or delete the plugin folder from your project) and restart the editor.
