---
title: "Quick start"
nav_order: 2
---
# Quick start (5 minutes)

By the end you'll have a generated world in your level and you'll dig into it while playing.

**You need:** Unreal Engine 5.8 on Windows. See the [requirements](install-and-upgrade.md#requirements).

1. **Install the plugin.** Copy the `SuperVoxel` folder into your project's `Plugins` folder (or install it from
   Fab) and open the project. Check that it's enabled in Edit > Plugins.
2. **Add a world.** Drag a **Super Voxel World** actor into your level. It shows in the viewport right away (flat
   ground by default).
3. **Pick a generator.** In the Details panel, set **Generator** to **Layered Terrain**. Try a few **Seed** values
   and watch the preview change.
4. **Press Play.** The world builds on worker threads and appears a moment later.
5. **Dig.** Open `/SuperVoxel/Demo/Maps/SuperVoxelDemo` and play as Bumble (left mouse digs, right mouse
   places). The signs around the spawn show one feature each; see [Demo stations](bumble.md#demo-stations). Or add the two nodes below to your own character.


## Dig where you look (your own character)
**Blueprint:** on your dig input: **Find Voxel World** → **Trace From Camera** → if **bHit**: **Make Sphere Brush**
(Op = Dig, Center = Hit Location, Radius = 2) → **Apply Brush**.

**C++:**
```cpp
#include "SuperVoxelWorld.h"
#include "SuperVoxelLibrary.h"

ASuperVoxelWorld* World = USuperVoxelLibrary::FindVoxelWorld(this);
const FSuperVoxelHit Hit = USuperVoxelLibrary::TraceFromCamera(this, World, 1500.f);
if (World && Hit.bHit)
{
	World->ApplyBrush(USuperVoxelLibrary::MakeSphereBrush(ESuperVoxelBrushOp::Dig, Hit.Location, 2.f));
}
```
Add `"SuperVoxel"` to your module's `Build.cs` dependencies.

## Next steps
- Change hills, caves and water: [Terrain generator](features/generator.md)
- Add your own blocks: [Block set](features/block-set.md)
- Save the player's changes: [Save and load](features/save-load.md)
- Sculpt in the editor: [Editor tools](features/editor-tools.md)
