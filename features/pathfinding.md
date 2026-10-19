---
title: "Pathfinding"
parent: Features
nav_order: 13
---
# Pathfinding

> Finds walkable paths across the voxel world for agents of any size. It reads the voxels directly, so paths follow
> digs and builds with no navmesh rebuild.

## How do I...?
- **Make a character walk somewhere:** add a **Super Voxel Path Follower** component and call `Move To`.
- **Get a path without blocking the game:** use the **Find Voxel Path Async** node.
- **Check if a spot is walkable:** `Is Standable At`.

## Turn it on or off
Pathfinding lives in its own module, **SuperVoxelNavigation**. Leave the module out (or don't call it) and nothing
runs. The world's chunks don't affect the engine navmesh by default (`bAffectNavigation` is off), because rebuilding
a navmesh on every edit is slow.

## The 3 settings you'll use most

| Setting | What it does | Default |
|---|---|---|
| Agent **Radius** | Voxels on each side of the center column the body covers (0 = one voxel wide, 1 = three wide) | 0 |
| Agent **Height** | Voxels of headroom the body needs | 4 |
| Agent **Max Step Up** | Highest step it walks up, in voxels | 1 |

## Example: walk a character to a clicked point
**Blueprint:** Get Super Voxel Path Follower → Move To (World, Hit
Location); bind On Arrived

**C++:**
```cpp
#include "SuperVoxelPathfindingLibrary.h"
#include "SuperVoxelLibrary.h"

// In the constructor of an ACharacter subclass:
Follower = CreateDefaultSubobject<USuperVoxelPathFollowerComponent>(TEXT("PathFollower"));

// Later:
void AMyWalker::GoTo(const FVector& Target)
{
	ASuperVoxelWorld* World = USuperVoxelLibrary::FindVoxelWorld(this);
	Follower->MoveTo(World, Target);
}
```
Add `"SuperVoxelNavigation"` (and `"SuperVoxel"`) to your module's `Build.cs` dependencies.

**Async search from C++:**
```cpp
FSuperVoxelPathOptions Options;
Options.Agent.Height = 4;
USuperVoxelFindPathAsync::FindPathAsync(World, Start, Goal, Options,
	[](bool bFound, const TArray<FVector>& Points)
	{
		// Runs on the game thread. Points are world-space, at feet height.
	});
```

## How it works
- A path node is a voxel the agent's feet can occupy: solid ground below, and enough clear space around and above.
- Steps go to the 8 neighbouring columns, up to **Max Step Up** voxels up or **Max Drop** down. Diagonals never cut
  corners.
- Slow ground costs more: blocks with a low **Move Speed** (in the block table) are avoided when there's a faster way.
  A block with Move Speed 0 can't be stood on.
- With **Can Wade**, agents may walk through one voxel of liquid at half speed. Deeper liquid is never walkable.
- **Straighten** replaces the cell path with turning points wherever a straight walk is clear.
- Start and goal are snapped to the nearest standable voxel first.

## All settings
**Agent shape (`FSuperVoxelAgentShape`)**

| Setting | Type | Default | What it does |
|---|---|---|---|
| Radius | int 0..4 | 0 | Voxels on each side of the center column (0 = one wide, 1 = three wide) |
| Height | int 1..32 | 4 | Voxels of headroom needed |
| Max Step Up | int 0..8 | 1 | Highest step walked up |
| Max Drop | int 0..32 | 3 | Deepest drop walked down |
| Can Wade | bool | true | May wade through one voxel of liquid, at half speed |

**Search options (`FSuperVoxelPathOptions`)**

| Setting | Type | Default | What it does |
|---|---|---|---|
| Agent | Agent shape | see above | The walker |
| Max Expansions | int (min 100) | 30000 | Search budget: cells looked at before giving up |
| Heuristic Weight | float 1..3 | 1.25 | Above 1 trades path quality for speed |
| Straighten | bool | true | Turning points instead of every cell |
| Allow Diagonal | bool | true | Diagonal steps (never cutting corners) |
| Region Margin | int (min 4) | 48 | Async searches look this many voxels beyond the box around start and goal |
| Allow Partial | bool | true | When the goal can't be reached, return a path to the reachable spot closest to it |

**Path follower (`USuperVoxelPathFollowerComponent`)**

| Setting | Type | Default | What it does |
|---|---|---|---|
| Path Options | Search options | defaults | How it searches |
| Acceptance Radius | float | 30 | Distance at which a path point counts as reached (world units, horizontal) |
| Speed Scale | float 0..1 | 1 | Movement input scale (1 = full speed) |
| Draw Path | bool | false | Draws the current path |
| Retry When Voxels Change | bool | true | After a failure, try again when voxels near it change (say someone digs a ramp) |

The follower steers its Character owner with movement input, jumps up ledges higher than the character can step, and
finds a new path when the voxels along the way change.

- When there's no way to the goal from where it stands (trapped in a pit, say), it fires **On Failed** once and stops
  instead of wandering back and forth on partial paths.
- A walker stuck for 3 seconds asks for a cell-by-cell path next.
- Straightened paths keep a little clearance from drops and walls, so walkers don't clip corners.

## Using Unreal's navmesh instead
To use the engine navmesh instead of (or as well as) voxel pathfinding:

1. turn on the world's **Affect Navigation**;
2. set Project Settings > Navigation Mesh > Runtime Generation to **Dynamic**.

Edits then rebuild the navmesh tiles they touch. With Affect Navigation on, chunk collision is cooked as soon as a
chunk is meshed (a little game-thread time per edited chunk), so the navmesh sees the new ground at once.

## Blueprint nodes and C++ functions

| Name | Blueprint | C++ | What it does |
|---|---|---|---|
| Find Voxel Path | yes | `USuperVoxelPathfindingLibrary::FindVoxelPath(World, Start, Goal, Options, OutPoints, Result)` | Game-thread search; world-space points at feet height, and the result (below) |
| Find Voxel Path Async | yes (async node: On Found, On Partial, On Failed) | `USuperVoxelFindPathAsync::FindVoxelPathAsync(...)`; native `FindPathAsync(..., OnDone)` | Searches a copy of the region on a worker thread |
| Is Standable At | yes | `USuperVoxelPathfindingLibrary::IsStandableAt(World, Location, Agent)` | Whether the agent can stand there |
| Draw Voxel Path | yes | `USuperVoxelPathfindingLibrary::DrawVoxelPath(WorldContext, Points, Color, Duration = 2)` | Debug lines |
| Move To | yes | `USuperVoxelPathFollowerComponent::MoveTo(World, Goal)` | Walk the owner to a location |
| Stop | yes | `USuperVoxelPathFollowerComponent::Stop()` | Stop walking |
| Is Moving | yes | `IsMoving()` | |
| Get Path Points | yes | `GetPathPoints()` | The current path |
| (C++ only) | no | `FSuperVoxelPathfinder` | The search itself: `FindPath`, `IsStandable`, `FindNearestStandable`, `CanWalkStraight`, `Straighten`, `GroundSpeed` |
| (C++ only) | no | `FSuperVoxelNavGrid::FromWorld` / `CopyRegion` | The voxels a search reads: the live world (game thread) or a copy (any thread) |

**Custom costs (C++):** on an `FSuperVoxelPathfinder`, set `ExtraCost` (extra cost to enter a cell, ≥ 0) and
`IsBlocked` (cells that must not be entered), and call `SetReservedCells` for cells other walkers hold (paths pass
them at a cost; default 8).

## Path results (`ESuperVoxelPathResult`)

| Result | Meaning |
|---|---|
| Found | A full path to the goal |
| Partial | No full path, but a path to the reachable spot closest to the goal; try again from there, or later |
| Target Not Loaded | The goal's chunks aren't loaded (unbounded worlds): the path leads as close as the loaded ground allows |
| No Path | No way at all: the start isn't standable, or nothing is reachable |

The path follower walks partial paths and searches again when it gets there. It notices a trench dug anywhere
across its route and finds a way around; if the trench cuts the way completely, it walks to the edge and stops (On
Failed, or a partial path).

## Events

| Event | On | When it fires |
|---|---|---|
| On Found | Find Voxel Path Async | A path was found (Points) |
| On Partial | Find Voxel Path Async | Only a partial path (Points lead as close to the goal as possible) |
| On Failed | Find Voxel Path Async | No path |
| On Arrived | Path Follower | Reached the goal |
| On Failed | Path Follower | Gave up |

## Limits and performance
- **Find Voxel Path** runs on the game thread; use the async node for long searches.
- An async search copies only the region around start and goal (plus Region Margin). A path that must detour further
  out isn't found; raise Region Margin.
- Max Expansions caps the work. Raise it for very long paths.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| No path between two clear points | The detour leaves the copied region, or Max Expansions ran out | Raise Region Margin or Max Expansions |
| Agents won't climb a one-voxel step | Max Step Up is 0 | Set it to 1 or more |
| Agents walk into walls | Radius is too small for the character | Raise Radius |
| Agents avoid some ground | That block's Move Speed is low or 0 | Change Move Speed in the block table |
