---
title: "Troubleshooting and errors"
parent: Reference
nav_order: 2
---
# Troubleshooting and errors

<!-- Status: checked against e7f2c56 (every warning and error in the source) -->

SuperVoxel writes to the log category **LogSuperVoxel** (content building uses **LogSuperVoxelContent**). Open Window >
Output Log and filter by the category. `X`, `N` and `%s` stand for names or numbers filled in at runtime.

## Messages

| Message | What it means | Fix |
|---|---|---|
| `<World>: no block set (and no default block set in Project Settings > SuperVoxel); the world will be empty.` | No block set anywhere | Set Block Set on the world, or the project default |
| `<World>: the level's baked edits can't be used (<reason>); they're ignored.` | The editor sculpting saved in the level doesn't fit the world any more | Restore the old settings (e.g. World Size) or sculpt again |
| `ApplyBrush on a client needs a USuperVoxelNetComponent on the player controller (the server adds one).` | A client edit with no net component | Have the world in the level when players log in |
| `SetBlock on a client needs a USuperVoxelNetComponent on the player controller (the server adds one).` | Same, for Set Block | Same |
| `<player>: client edit request rejected: <reason> (further rejections log at Verbose)` | The server refused a client's edit: rate limit, edit distance, or no world | See [Multiplayer](../features/multiplayer.md) |
| `SetBlock: unknown block 'X'` | No such block in the set | Check the row name (no spaces) |
| `Unknown block 'X', using Air` | A name in a save or setting isn't in the set | Add the block, or fix the name |
| `Too many block types; 'X' ignored (limit 4096)` | The block set has more than 4096 types | Remove rows |
| `LoadEdits: only the server can load edits.` | Load called on a client | Load on the server |
| `LoadEdits: not SuperVoxel edit data` | The bytes aren't a SuperVoxel save | Pass the bytes from Save Edits |
| `LoadEdits: saved by a newer SuperVoxel version` | Save from a later version | Update the plugin |
| `LoadEdits: saved for a world of a different size` | World Size changed | Use the same size, or Load From Slot |
| `LoadEdits: corrupt edit data` | The data is damaged | Use another save |
| `Layered Terrain: block set has no X; those features are skipped.` | A block named in the generator's settings is missing | Add it, or change the setting |
| `Layered Terrain: none of the rock blocks exist in the block set; nothing generated.` | No stone layer or fallback stone exists | Fix the names or use the default block set |
| `Layered Terrain: only the first 32 of N stone layers are used.` | Over 32 stone layers | Remove some |
| `Layered Terrain: world AxBxC is too small (8 voxels per axis minimum).` | Tiny world | Make it bigger |
| `Layered Terrain: no block registry; call Prepare first.` | Custom code ran Generate without Prepare | Call Prepare first |
| `Layered Terrain: voxel buffer does not match the world size.` | Custom code passed a wrong buffer | Pass a grid of SizeX × SizeY × SizeZ |
| `Bumble needs Enhanced Input (Project Settings > Input > Default Input Component Class = EnhancedInputComponent).` | The project uses the old input component | Change the setting |
| `Can't read <file>` (LogSuperVoxelContent) | The content builder can't find a source file | Check the plugin's `Data` folder |
| `Build the default content first (DT_SuperVoxelBlocks is missing).` (LogSuperVoxelContent) | A content step ran before the block table existed | Run `-run=SuperVoxelBuildContent` without options first |
| `SetSeedAndRegenerate: only the server can change the seed.` | Called on a client | Call it on the server |
| `Structure capture: no built SuperVoxel world in this level.` | No world, or not built yet | Let the world build (Preview In Editor on) |
| `Structure capture: the box is outside the world.` | The capture box doesn't overlap the world | Move the box over the world |
| `Structure capture: couldn't save X.` | Bad or read-only asset path | Use a path like `/Game/Structures/ST_MyHouse` |

## Common problems

| Problem | Fix |
|---|---|
| The world is empty | Check the block set and the generator ([Settings](../features/settings.md)) |
| The world appears late | It builds on worker threads; wait for On World Built ([Background work](../features/background-work.md)) |
| Edits don't show for other players | Edits must go through the server; see [Multiplayer](../features/multiplayer.md) |
| A new block is grey | Press Rebuild Texture Arrays ([Materials](../features/materials.md)) |
| Agents can't find a path | Raise Region Margin or Max Expansions ([Pathfinding](../features/pathfinding.md)) |
