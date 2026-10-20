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

## Demo stations
Around the spawn point, one station per feature: each has something to try and a floating sign with a title, one to
three lines with the keys to press, and **See:** the guide page to read. The keys on a sign follow your device
(keyboard or gamepad). Signs face the camera and fade with distance.

The stations: digging, damage and drops, smooth and blocky, structures, cutaway and caves, collapse, lights, ticks and
falling blocks, walkers, props, [Laylines](features/laylines.md) and [Fluids](features/fluids.md) (each when its plugin
is enabled), and multiplayer.

- **Hide or show the signs:** F10, or the help menu's station signs row (pad: Menu).
- **Edit the text:** the rows are in `DT_SuperVoxelDemoStations` (row structure `SuperVoxelDemoStationRow`): Title,
  Body, Guide Page, Kind (what the station builds), Order, Ring Scale (how far out it sits) and Enabled. In Body, a key
  in braces such as `{Dig}` or `{Camera}` shows as that key for the device in use.
- **Leave them out:** untick **Spawn Stations** on the demo game mode (`ASuperVoxelDemoGameMode`), or start with
  `-SuperVoxelNoStations`. Skip single stations with `-SuperVoxelStationsSkip=Id,Id` (row names). **Stations Class**
  swaps in your own subclass.
- **The stations actor** (`ASuperVoxelDemoStations`): Station Table, Ring Radius (2600), Fade Start / Fade End (2200 /
  3600), Sign Scale (0.9), Show Signs (Set Show Signs, Toggle Signs), Get Station Sites, Get Station Ids.

## Cameras
Bumble's cameras and controls are demo code to copy from, not a SuperVoxel feature.

Bumble has two cameras: **over the shoulder** (the default) and **first person**. **Y** switches between them (pad:
right stick click), and the HUD always shows the key beside the hotbar.

- In first person, Bumble is hidden from its own player only; other players still see it, and the target highlight
  still works.
- **From code:** Camera Mode (`EBumbleCameraMode`: Over Shoulder, First Person), Set Camera Mode, Toggle Camera Mode,
  First Person Eye Offset (22, 0, 72).
- **Rebind the switch:** Set Camera Toggle Keys (Keyboard Key, Gamepad Key; pass an empty key to keep one as it is).
  Get Camera Toggle Label returns the key's label for the device in use ("Y", "RS click").

## Controls

| Input | Action |
|---|---|
| WASD, mouse | Move, look |
| Space | Jump |
| Shift | Run |
| Left mouse (hold) | Dig: harder blocks take longer |
| Right mouse | Place |
| Wheel or 1–9 | Pick a hotbar slot (9 slots) |
| E | Use the block you aim at (a lever, a button) if it does something; otherwise open or close the block palette |
| Y | Switch camera: over the shoulder or first person |
| G / H | Cycle the slot through every block |
| Q | Swap shoulder |
| Ctrl | Aim |
| [ ] | Brush size |
| B | Brush shape |
| F | Fly (Space / Alt for up / down) |
| Z / X / C | Cutaway down / up / off |
| F6 / F7 | Save / load |
| = | UI scale: 75 / 100 / 125 / 150% |
| . (period) | Build the feature showcase in front of Bumble |
| Home | Open this page in the online guide |
| Tab | Show or hide help |
| F10 | Show or hide the station signs |

**Commands**

| Key | Action |
|---|---|
| 0 | Build an overhang |
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

## Gamepad
Every action works on a gamepad, and the HUD shows pad labels while a pad is in use.

| Button | Action |
|---|---|
| Left stick, right stick | Move, look |
| A | Jump |
| B | Fly down |
| X | Fly |
| Y | Use the block you aim at, otherwise the block palette |
| RT, LT | Dig, place |
| LB, RB | Pick a block |
| Left stick click | Run |
| Right stick click | Switch camera |
| D-pad up, down | Cutaway down, up |
| D-pad left, right | Brush size |
| Menu | Help menu: the d-pad picks a setting, A changes it, B closes |

**Hold View for tools:**

| Button (with View held) | Action |
|---|---|
| A | Feature showcase |
| B | Call the walkers |
| X | Brush shape |
| Y | Place a cottage |
| LB, RB | Cycle the slot through every block |
| D-pad up, down | Build a village, build an overhang |
| D-pad left, right | Cutaway off, aim |
| LT, RT | Save, load |
| Left stick click | Props on or off |
| Right stick click | Swap shoulder |
| Menu | Open the online guide |

Walker paths and the station signs are in the help menu (Menu). Both sticks have a 0.2 dead zone, and the right
stick looks without inverting.

The demo keys stay clear of the editor's own debug keys. **Esc** ends Play in the editor, so it doesn't close menus:
use E (palette), Tab (help) and Enter (search).

**In the palette:** the d-pad moves, A fills the current slot, LB / RB pick the slot, LT / RT change tab, B closes.

## The feature showcase
Press **.** (or call **Stamp Showcase** from Blueprint) to build a small showcase in front of Bumble:

- a sand pile on a plank beam: dig the beam and the sand falls (the block set needs **Falls** on for sand);
- two [light blocks](features/lights.md);
- a glow fungus that spreads one block per [scheduled tick](features/ticks.md), eight times.

## The block palette
Press **E** (pad: **Y**) to open the palette, a compact panel with:

- **category tabs** (pad: LT / RT; keyboard: [ and ] while the palette is open);
- a **search box**: press **/** to type, Enter to finish;
- a **recent** row of the blocks you used last;
- a **grid** of blocks, with each block's name in a tooltip.

Click a block to put it in the current hotbar slot, or drag it onto any slot. **E** closes it; the mouse cursor is free
while it's open. On a pad: the d-pad moves, A fills the slot, LB / RB pick the slot, B closes.

## How it works
- **Built from cubes:** no skeletal mesh. Each part is a static mesh cube with its own colour.
- **Procedural animation** (`UBumbleAnimComponent`): bobbing, a hat that wobbles behind the motion, limbs that swing
  with speed, a jump stretch, a landing squash, and dig and place swings.
- **Over-the-shoulder camera** (and a [first-person one](#cameras)): a spring arm (`UBumbleSpringArm`) with a shoulder offset you can swap, and a closer
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
These are part of the demo character (the SuperVoxelDemo module), not the SuperVoxel API.


| Node | What it does |
|---|---|
| Start Digging | Starts digging what the crosshair is on, as if the dig button were held (local player) |
| Stop Digging | Lets go of the dig button |
| Interact With Target | Uses the block under the crosshair (Interact With Voxel) if its block has a behaviour; returns whether it did something |
| Set Help Visible | Shows or hides the help panel |
| Set Camera Mode, Toggle Camera Mode | Over the shoulder or first person |
| Set Camera Toggle Keys, Get Camera Toggle Label | Rebinds the camera switch; its label as the HUD shows it |
| Set Palette Open | Opens or closes the block palette (frees the mouse cursor while open) |
| Stamp Showcase | Builds the feature showcase (Base voxel, Direction) |
| Set Using Gamepad, Is Using Gamepad | Switches the HUD labels and menus between gamepad and keyboard (Bumble also detects it from input) |
| Set Menu Open, Is Menu Open | Opens or closes the help menu |
| Move Menu Cursor | Moves the menu highlight (Y), or the palette cursor (X across, Y by rows) |
| Get Palette Blocks, Get Palette Categories | The blocks and the category tabs the palette shows |
| Set Palette Tab, Set Palette Search | Picks a tab, or filters by text |
| Assign Block To Slot | Puts a block in a hotbar slot |
| Get Recent Blocks | The recent row |
| Activate Menu Item, Get Menu Cursor | Does what a settings row does (the same as its keyboard key); the highlighted row |
| Set Body Color, Set Leg Color, Set Head Color, Set Hat Color, Set Hat Band Color | Change a look colour at runtime and repaint (Apply Look) |

**HUD scale:** the demo HUD (`ASuperVoxelDemoHUD`) has **UI Scale** (0.5 to 2; Set UI Scale). The = key or the help
menu's UI scale row cycles 75, 100, 125 and 150%.

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
