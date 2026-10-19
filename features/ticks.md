---
title: "Ticks"
parent: Features
nav_order: 23
---
# Ticks

> **Random ticks** visit voxels of chosen block types now and then, for grass spreading, crops growing or decay.
> **Scheduled ticks** call one voxel back after a delay, for timers, fuses and doors that close.

## How do I...?
- **Make grass spread:** turn on **Random Tick** for the grass block, give it a [behaviour](block-behaviors.md), and
  in **On Random Tick** turn a neighbouring soil voxel into grass.
- **Close a door after 3 seconds:** **Schedule Voxel Tick (Voxel, 3)**, then flip its state in **On Scheduled Tick**.

## Turn it on or off
- Random ticks run only for blocks with **Random Tick** on (block table, or **Set Block Random Tick** at runtime).
- Scheduled ticks run only when you schedule them.

## The 3 settings you'll use most

| Setting | Where | Default |
|---|---|---|
| Random Tick | Block table | off |
| Random Ticks Per Chunk Per Second | World > Ticks | 48 |
| Random Tick Radius | World > Ticks | 6400 cm (64 m) around players, streaming anchors, or the world |

## Example: a timed door
**Blueprint:** On Interact → Set Block State (open) → Schedule Voxel Tick (Voxel, 3). In the behaviour's On
Scheduled Tick → Set Block State (closed).

**C++:**
```cpp
World->ScheduleVoxelTick(Voxel, 3.f);   // scheduling again moves it
World->CancelVoxelTick(Voxel);          // or cancel it
```

## Blueprint nodes and C++ functions (on the world)

| Name | C++ | What it does |
|---|---|---|
| Schedule Voxel Tick | `void ScheduleVoxelTick(FIntVector Voxel, float Delay)` | Fires On Scheduled Tick and On Voxel Scheduled Tick once; scheduling again moves it |
| Cancel Voxel Tick | `void CancelVoxelTick(FIntVector Voxel)` | Cancels it |
| Set Block Random Tick | `bool SetBlockRandomTick(FName Block, bool bRandomTick)` | Turns the random tick on or off for a block at runtime |

## Events

| Event | Where | When it fires |
|---|---|---|
| On Voxel Random Tick | Server | The random tick picked a voxel whose block has Random Tick on (after its behaviour) |
| On Voxel Scheduled Tick | Server | A scheduled tick came due (after the block's behaviour) |

## Limits
- Ticks run on the server only.
- Scheduled ticks aren't saved.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| Random ticks never come | Random Tick is off for the block, or it's beyond Random Tick Radius | Turn it on; raise the radius |
| A scheduled tick is lost after loading | Scheduled ticks aren't saved | Schedule again after loading |
