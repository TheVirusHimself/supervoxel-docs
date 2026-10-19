---
title: "Example character"
nav_order: 7
---
# Example character: Bumble

Bumble is the demo's playable character: a blocky little figure built from cubes in code, with a huge head, a tiny
body, stubby legs, noodle arms and a crooked top hat. It walks, runs, jumps, digs and places blocks through the
SuperVoxel editing API, in single player and multiplayer, so it doubles as a working example to copy from.

## Play as Bumble
Open `/SuperVoxel/Demo/Maps/SuperVoxelDemo` (the one demo map) and press Play. For multiplayer, set Play > Net Mode
to *Play As Listen Server* with 2 players.

## Controls

| Input | Action |
|---|---|
| WASD, mouse | Move, look |
| Space | Jump |
| Shift | Run |
| Left mouse (hold) | Dig: harder blocks take longer |
| Right mouse | Place |
| Wheel or 1–9 | Pick a hotbar slot (9 slots) |
| E | Open or close the block palette |
| G / H | Cycle the slot through every block |
| Q | Swap shoulder |
| Ctrl | Aim |
| [ ] | Brush size |
| B | Brush shape |
| F | Fly (Space / Alt for up / down) |
| Z / X / C | Cutaway down / up / off |
| F5 / F9 | Save / load |
| . (period) | Build the feature showcase in front of Bumble |
| F1 | Open this page in the online guide |
| Tab | Show or hide help |

**Commands**

| Key | Action |
|---|---|
| Y | Build an overhang |
| U | Place a cottage |
| L | Build a village |
| T | Call the walkers |
| J | Copy the seed |
| R | New random seed |

**Toggles** (the help panel shows each one's state)

| Key | Toggles |
|---|---|
| K | Collapse |
| M | Mesh style |
| O | Ambient occlusion |
| I | Greedy meshing |
| P | Props (scatter) |
| N | Cave culling |
| , (comma) | Render distance: unlimited / 40 m / 80 m |
| V | Walker paths |

The controls are built in code with Enhanced Input; no input assets are needed.

## The feature showcase
Press **.** (or call **Stamp Showcase** from Blueprint) to build a small showcase in front of Bumble:

- a sand pile on a plank beam: dig the beam and the sand falls (the block set needs **Falls** on for sand);
- two [light blocks](features/lights.md);
- a glow fungus that spreads one block per [scheduled tick](features/ticks.md), eight times.

## The block palette
Press **E** to open the palette: every block, grouped by category, with its hardness and kind when you hover over it.
Click a block to put it in the current hotbar slot; the wheel scrolls, and **E** closes it. The mouse cursor is free
while it's open.

## How it works
- **Built from cubes:** no skeletal mesh. Each part is a static mesh cube with its own colour.
- **Procedural animation** (`UBumbleAnimComponent`): bobbing, a hat that wobbles behind the motion, limbs that swing
  with speed, a jump stretch, a landing squash, and dig and place swings.
- **Over-the-shoulder camera:** a spring arm (`UBumbleSpringArm`) with a shoulder offset you can swap, and a closer
  view while aiming. When something blocks the camera it moves in at once, then eases back out (Return Speed, default
  5; 0 snaps back like a plain spring arm). While dig is held, Bumble keeps facing the way the camera looks.
- **Aiming:** each frame Bumble traces from the camera. A ghost outline shows the voxel a dig will remove, or where a
  placed block will go.
- **Digging takes time:** hold the dig button. A block breaks after its **Hardness** × **Dig Seconds Per Hardness**
  (default 0.3 s per point; 0 = instant). Indestructible blocks never break. A crack overlay grows on the block and a
  progress bar shows under the crosshair.
- **Digging uses block damage** (**Dig With Damage**, on by default): Bumble digs through `Damage Voxel`
  ([Damage and drops](features/damage-and-drops.md)), so every player sees the crack, and what the block drops (its
  Drop Item, or the block itself) goes into Bumble's **Bag**, shown under the hotbar. Turn it off for a local timer and
  `Set Block` instead. Brushes bigger than one voxel always use the timer.
- **Target highlight:** a thin slab marks the aimed face, and a see-through ghost of the selected block shows where it
  would go. With a brush larger than 1, a ghost of the brush size shows instead.
- **Help panel (Tab):** shows the live state of collapse, mesh style, ambient occlusion, greedy meshing, props,
  cutaway, cave culling, render distance, walker paths, target highlight and flying.
- **Multiplayer:** each player spawns on a ring around the spawn point, in join order.
- **Editing:** dig and place call the editing API (`Apply Brush` and `Set Block`), so in multiplayer they go through
  the server like any other edit.

## Settings (`ABumbleCharacter`)

| Setting | Default | What it does |
|---|---|---|
| Body Color | mustard | Body colour |
| Leg Color | teal | Leg colour |
| Head Color | light tan | Head colour |
| Hat Color | dark plum | Hat colour |
| Hat Band Color | teal | Hat band colour |
| Hotbar | (list) | Blocks on the hotbar (1–9) |
| Brush Size | 1 | Brush radius in voxels (1 = a single voxel) |
| Dig With Damage | on | Dig through Damage Voxel, with shared cracks and drops into the Bag. Off: a local timer and Set Block |
| Dig Seconds Per Hardness | 0.3 | Seconds of digging per point of block Hardness while the button is held; 0 = every block breaks at the first swing |
| Show Target Highlight | on | Show the face under the crosshair and a ghost of the block about to be placed |
| Brush Shape | Sphere | Shape for digging and placing |
| Reach | 700 | Farthest edit from Bumble's head, in world units |
| Shoulder Offset | 65 | Sideways camera offset |
| Arm Length | 340 | Camera distance |
| Aim Arm Length | 170 | Camera distance while aiming |

**Animation (`UBumbleAnimComponent`)**

| Setting | Default | What it does |
|---|---|---|
| Run Speed | 450 | Ground speed at which the walk becomes a run (bigger swings, forward lean) |
| Stride Length | 110 | Distance covered per full stride, in world units |
| Swing Duration | 0.34 | Seconds a dig or place swing takes |
| Swing Hit Time | 0.45 | Share of the swing (0..1) at which the tool hits: when the edit happens |

## Blueprint nodes on Bumble

| Node | What it does |
|---|---|
| Start Digging | Starts digging what the crosshair is on, as if the dig button were held (local player) |
| Stop Digging | Lets go of the dig button |
| Set Palette Open | Opens or closes the block palette (frees the mouse cursor while open) |
| Stamp Showcase | Builds the feature showcase (Base voxel, Direction) |
| Set Body Color, Set Leg Color, Set Head Color, Set Hat Color, Set Hat Band Color | Change a look colour at runtime and repaint (Apply Look) |

## Use Bumble in your own level
Set Bumble (`ABumbleCharacter`) as the default pawn class in your game mode, or use the demo game mode
(`ASuperVoxelDemoGameMode`). Bumble finds the first voxel world in the level and waits for it to be built.

## Leave Bumble out
Bumble lives in the **SuperVoxelDemo** module. Your game doesn't need it.

## Make your own character from it
Copy these three ideas:

1. **Aim:** `Trace From Camera` (or `Trace Voxel`) every frame; keep the hit.
2. **Show the target:** draw a box at `Voxel To World (Hit.Voxel)` for digging, or at `Hit.Adjacent` for placing.
3. **Edit:** `Apply Brush` with a Dig brush at the hit, or `Set Block (Hit.Adjacent, Block)`.
See [Editing](features/editing.md) for the full example.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| "Bumble needs Enhanced Input (Project Settings > Input > Default Input Component Class = EnhancedInputComponent)." | Your project uses the old input component | Set Default Input Component Class to EnhancedInputComponent |
| Bumble falls at the start | The world isn't built yet | Bumble waits for the world; if you spawn it yourself, spawn after On World Built |
| Can't dig far away | Reach | Raise Reach |
