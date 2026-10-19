---
title: "Background meshing and collision"
parent: Features
nav_order: 7
---
# Background meshing and collision

<!-- Status: checked against 0f6bdf3 (headers) -->

> The world is generated and meshed on worker threads, edits are meshed in the background, and chunk meshes are
> handed to the renderer a few per frame, so building and digging don't hitch.

## Turn it on or off
| Setting (world > Building) | What it does | Default |
|---|---|---|
| Async Meshing | Build meshes for edits on worker threads (a frame or two later). Off = rebuild on the game thread at once | on |
| Max Chunk Uploads Per Frame | Most chunk meshes handed to the renderer per frame (the first build uses four times as many) | 6 |
| Build On Begin Play | Generate and build when play begins | on |

Turn **Async Meshing** off only if you need an edit's mesh in the same frame (for example in a test).

## How do I...?
- **Show a loading bar:** read `Get Build Progress` (0 to 1) until `Is Ready` is true, or bind **On World Built**.
- **Wait for the world before spawning players:** bind **On World Built**, then use `Find Spawn Location`.

## Example: wait for the world
**Blueprint:** Bind Event to On World Built → spawn the
player at Find Spawn Location

**C++:**
```cpp
void AMyGameMode::BeginPlay()
{
	Super::BeginPlay();
	if (ASuperVoxelWorld* World = USuperVoxelLibrary::FindVoxelWorld(this))
	{
		if (World->IsReady())
		{
			OnWorldReady();
		}
		else
		{
			World->OnWorldBuilt.AddDynamic(this, &AMyGameMode::OnWorldReady); // OnWorldReady is a UFUNCTION()
		}
	}
}
```

## Blueprint nodes and C++ functions
| Name | Blueprint | C++ | What it does |
|---|---|---|---|
| Is Ready | yes | `bool IsReady() const` | Generated and every chunk shown |
| Get Build Progress | yes | `float GetBuildProgress() const` | 0..1 while building, 1 when ready |
| Find Spawn Location | yes | `FVector FindSpawnLocation() const` | A dry standing spot near the generator's spawn column, or the world center |
| Get Last Generate Ms | yes | `float GetLastGenerateMs() const` | Milliseconds the last full generation took (worker time) |
| Get Last Mesh Ms | yes | `float GetLastMeshMs() const` | Milliseconds the last full meshing pass took (worker time) |

## Events
| Event | When it fires |
|---|---|
| On World Built | Once the world is generated and every chunk is shown |

## Limits
- After an edit, the old mesh stays until the new one is ready, a frame or two later.
- A rebuild while a build is running waits for it to finish first.

## Troubleshooting
| Problem | Why | Fix |
|---|---|---|
| The world appears a moment after Play | It builds on worker threads | Expected; show a loading screen with Get Build Progress |
| Players fall through at start | They spawned before the world was ready | Spawn on On World Built |
