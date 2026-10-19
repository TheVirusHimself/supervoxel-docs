---
title: "Multiplayer"
parent: Features
nav_order: 14
---
# Multiplayer

> The server owns every edit. Clients send their edits to the server, the server applies them and replicates them to
> everyone as an ordered stream, and players who join late receive the whole edit history.

## How do I...?
- **Try it now:** open `/SuperVoxel/Demo/Maps/SuperVoxelDemo`, set Play > Net Mode to *Play As Listen Server* and Number of Players to 2, and
  press Play. Edits from either player appear for both.
- **Use it in my game:** nothing extra. Call `Apply Brush` or `Set Block` on any machine; on a client the call goes to
  the server.
- **Limit what players can do:** set **Max Edit Distance** and **Max Requests Per Second** on the net component, and
  `CanEditVoxel` on the world.

## Turn it on or off
It's on whenever the world is in a networked game. In a standalone game nothing is sent. The world actor replicates
its seed, size and voxel size, so every machine generates the same world, then replays the edits.

## The 3 settings you'll use most

| Setting | Where | What it does | Default |
|---|---|---|---|
| Max Edit Distance | Super Voxel Net Component | Farthest a player's pawn may be from an edit, in world units (0 = no limit). Checked on the server | 0 |
| Max Requests Per Second | Super Voxel Net Component | Most edit requests a player may send per second (0 = no limit); extras are dropped | 30 |
| Can Edit Voxel | World (C++) | Your own yes/no for each gameplay edit, on the server | not set |

## How it works
1. A client calls `Apply Brush` or `Set Block`. It goes through the player's **Super Voxel Net Component**
   (`ServerApplyBrush` / `ServerSetBlock`).
2. The server checks the distance and rate limits and `CanEditVoxel`, then applies the edit.
3. The server sends the changes to every client as batches in an ordered stream. Older batches are folded into later
   ones, so the stream stays compact.
4. A late joiner gets the world's seed and size, generates the same world, then applies the whole stream.
   The history is sent to each player in pages, a few per tick, so it can be any size: players join late into worlds
   with tens of thousands of edits. A rebuild on the server starts a new history.

**Unbounded worlds** ([Unbounded worlds](streaming.md)): each client asks the server for the edits of the chunks it
loads, and the server sends live edits only for chunks that player has loaded.

**The net component is added for you:** when a SuperVoxel world is in the level, the server adds one to every player
controller as players log in.

## Example: set the limits
**Blueprint:** on the server, Get Component by Class (Super Voxel
Net Component) on the player controller → set Max Edit Distance

**C++:**
```cpp
#include "SuperVoxelNet.h"

void AMyGameMode::PostLogin(APlayerController* NewPlayer)
{
	Super::PostLogin(NewPlayer);
	if (USuperVoxelNetComponent* Net = NewPlayer->FindComponentByClass<USuperVoxelNetComponent>())
	{
		Net->MaxEditDistance = 1200.f;
		Net->MaxRequestsPerSecond = 15.f;
	}
}
```
The component may be added after your `PostLogin` runs. If `FindComponentByClass` returns null, set the limits a
moment later, for example on the next tick.

## Blueprint nodes and C++ functions

| Name | Blueprint | C++ | What it does |
|---|---|---|---|
| Max Edit Distance | property | `float MaxEditDistance` | Distance limit (server) |
| Max Requests Per Second | property | `float MaxRequestsPerSecond` | Rate limit (server) |
| (C++ only) | no | `ServerApplyBrush(World, Brush)` / `ServerSetBlock(World, Voxel, Block)` | The server calls behind Apply Brush and Set Block on a client |
| (C++ only) | no | `USuperVoxelNetComponent::FindLocal(UWorld*)` | The local player's component, on a client |

## Testing in the editor
Play In Editor with several players (one process) works for client edits.

## Limits
- Loading saves is server-only (`Load Edits`, `Load From Slot`, `Reset Edits`).
- Props from [Surface spawn rules](spawn-rules.md) aren't replicated: every machine places the same ones from the seed.
- On a client, `Apply Brush` returns 0 because the change arrives from the server a moment later.

## Troubleshooting

| Problem | Why | Fix |
|---|---|---|
| "ApplyBrush on a client needs a USuperVoxelNetComponent..." | The player controller has no net component | Make sure the world is in the level when players log in; the server adds it then |
| "client edit request rejected: <reason> (further rejections log at Verbose)" | The server refused a client edit (rate limit, edit distance, no world); the first one is a Warning, later ones Verbose | Check the reason; raise the limit if needed |
| Edits from far away are ignored | Max Edit Distance | Raise it, or set 0 for no limit |
| Fast repeated edits drop out | Max Requests Per Second | Raise it, or batch edits into one brush |
| A client's world looks different | Different block set or generator settings on the client | Ship the same assets; seed, size and voxel size are replicated |
