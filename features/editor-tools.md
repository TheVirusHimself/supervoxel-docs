---
title: "Editor tools"
parent: Features
nav_order: 16
---
# Editor tools

> See the world in the editor without pressing Play, and sculpt it in the viewport with the SuperVoxel mode: dig,
> fill, paint, smooth and flatten, with undo. Edits made in the editor are saved with the level.

## How do I...?
- **See the world without Play:** it previews automatically while **Preview In Editor** is on (the default). It
  rebuilds when you change settings.
- **Sculpt:** switch the editor mode to **SuperVoxel**, pick the **Sculpt** tool, then click and drag on the world.
- **Undo a stroke:** Ctrl+Z. Each stroke is one undo step.
- **Rebuild all plugin content:** run the `SuperVoxelBuildContent` commandlet (below).

## Turn it on or off
- **Preview:** untick **Preview In Editor** on the world.
- **The editor module** (SuperVoxelEditor) is editor-only and never ships in a packaged game.

## The 3 settings you'll use most (Sculpt tool)

| Setting | What it does | Default |
|---|---|---|
| Operation | Dig, Fill, Paint, Smooth, or Flatten (to the height where the stroke began) | Dig |
| Radius | Brush radius in voxels (0.5–48) | 3 |
| Block | Block for Fill, Paint and Flatten (a drop-down of the world's blocks) | Granite |

## Sculpt tool: all settings

| Setting | Default | What it does |
|---|---|---|
| Operation | Dig | What a stroke does |
| Shape | Sphere | Sphere, Box or Cylinder |
| Block | Granite | Block for Fill, Paint and Flatten |
| Radius | 3 | In voxels |
| Strength | 1 | Share of the covered voxels each stamp changes (0.05–1). Lower = rough, gradual edits |
| Stamps Per Second | 12 | Stamps while dragging (1–60) |

## How editor edits are kept
- Sculpt strokes are stored in the level as the world's **baked edits** and replayed after generation, every time the
  world builds (in the editor and in game).
- Runtime edits come on top of them. `Reset Edits` goes back to the generated world **plus** the baked edits.
- If you change a setting that makes the baked edits not fit (for example World Size), they can be ignored; the log
  says so.

## Regenerate the plugin's content (command line)
Every plugin asset is built from code and data, so it can be rebuilt:
```
UnrealEditor-Cmd.exe YourProject.uproject -run=SuperVoxelBuildContent [-Resolution=256] [-NoMaps]
```

| Option | What it does |
|---|---|
| -Resolution=N | Texture-array slice size |
| -NoMaps | Skip the demo maps |

It rebuilds the block table from `Data/SuperVoxelBlocks.csv`, the default block set, its texture arrays, the materials and
the demo maps.

## Help in the editor
- **Help > SuperVoxel Documentation** opens this guide.
- A **Documentation** row at the top of the Details panel opens the matching page for the SuperVoxel World, block
  sets, the scatter component, structure volumes and templates, the path follower, the net component, and Project
  Settings > SuperVoxel.
- The sculpt mode's **Guide** button opens this page.
- In the Plugins window, SuperVoxel's **Documentation** link opens the guide, and **Support** writes to the support
  email.
- From C++: `SuperVoxel::DocsURL` is the guide's address, and `SuperVoxel::DocsPage("features/streaming")` gives a
  page's address.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| The world doesn't show in the editor | Preview In Editor is off, or no block set | Turn it on; set a block set |
| Sculpting does nothing | No SuperVoxel world under the cursor | Point at the world |
| My sculpting vanished | The baked edits no longer fit the world (see the log) | Restore the old size, or sculpt again |
| The commandlet logs "Can't read ..." | A source file is missing | Check `Data/SuperVoxelBlocks.csv` exists in the plugin |
