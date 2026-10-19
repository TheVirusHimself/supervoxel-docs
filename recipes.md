---
title: "Recipes"
nav_order: 3
---
# Recipes

<!-- Status: checked against e7f2c56 (headers; not compiled) -->

Copy-ready answers to common tasks. Each recipe gives the Blueprint nodes in order and the same thing in C++.
The C++ snippets assume `World` is your `ASuperVoxelWorld*` (from **Find Voxel World**) and that your module depends
on `"SuperVoxel"`.

## 1. Dig a tunnel
**Blueprint:** Trace From Camera → For Loop (0 to 10) → Make Sphere Brush (Dig, Center = Hit Location + Forward ×
Index × Voxel Size, Radius 2) → Apply Brush.
```cpp
const FSuperVoxelHit Hit = USuperVoxelLibrary::TraceFromCamera(this, World, 1500.f);
if (Hit.bHit)
{
	const FVector Forward = GetActorForwardVector();
	for (int32 i = 0; i < 10; ++i)
	{
		const FVector Center = Hit.Location + Forward * i * World->GetVoxelSize();
		World->ApplyBrush(USuperVoxelLibrary::MakeSphereBrush(ESuperVoxelBrushOp::Dig, Center, 2.f));
	}
}
```

## 2. Flatten a pad for building
**Blueprint:** Make Box Brush (Op = Flatten, Center, Half Extent = 6, 6, 4, Block = PackedPath) → Apply Brush.
Flatten removes solid voxels above the center's height and fills the empty ones below it.
```cpp
World->ApplyBrush(USuperVoxelLibrary::MakeBoxBrush(ESuperVoxelBrushOp::Flatten, Center, FVector(6, 6, 4), TEXT("PackedPath")));
```

## 3. Paint the ground with another block
**Blueprint:** Make Sphere Brush (Op = Paint, Center, Radius 3, Block = RedSand) → Apply Brush.
```cpp
World->ApplyBrush(USuperVoxelLibrary::MakeSphereBrush(ESuperVoxelBrushOp::Paint, Center, 3.f, TEXT("RedSand")));
```

## 4. Place a structure
**Blueprint:** Place Structure At (Template = ST_Cottage, Location, Rotation = 0..3).
```cpp
World->PlaceStructureAt(CottageTemplate, Location, /*Rotation*/ 1);
```
See [Structures and villages](features/structures.md).

## 5. Save on quit, load on start
**Blueprint:** on End Play: Save To Slot ("World1"). On Begin Play: Does Save Game Exist ("World1") → Load From Slot
("World1").
```cpp
#include "Kismet/GameplayStatics.h"

void AMyGameMode::BeginPlay()
{
	Super::BeginPlay();
	if (UGameplayStatics::DoesSaveGameExist(TEXT("World1"), 0))
	{
		World->LoadFromSlot(TEXT("World1"));
	}
}

void AMyGameMode::EndPlay(const EEndPlayReason::Type Reason)
{
	World->SaveToSlot(TEXT("World1"));
	Super::EndPlay(Reason);
}
```

## 6. A character that walks to a point
**Blueprint:** add a **Super Voxel Path Follower** component to your Character → Move To (World, Target). Bind **On
Arrived**.
```cpp
// Constructor:
Follower = CreateDefaultSubobject<USuperVoxelPathFollowerComponent>(TEXT("PathFollower"));
// Later:
Follower->MoveTo(World, Target);
```
Needs the `"SuperVoxelNavigation"` module. See [Pathfinding](features/pathfinding.md).

## 7. A cutaway toggle
**Blueprint:** on a key: Get Cutaway Height → if ≥ 0: Set Cutaway Height (-1), else Set Cutaway Height (your height).
```cpp
World->SetCutawayHeight(World->GetCutawayHeight() >= 0 ? -1 : 40);
```

## 8. Test multiplayer on one PC
No code: open the demo map (or yours), set Play > Net Mode to **Play As Listen Server** and Number of Players to
**2**, then press Play. Edits from either window show in both. See [Multiplayer](features/multiplayer.md).

## 9. Wait for the world before spawning the player
**Blueprint:** Is Ready → if false, Bind Event to **On World Built** → spawn at **Find Spawn Location**.
```cpp
if (World->IsReady())
{
	OnWorldReady();
}
else
{
	World->OnWorldBuilt.AddDynamic(this, &AMyGameMode::OnWorldReady); // OnWorldReady is a UFUNCTION()
}
```

## 10. A different world every play
Tick **Random Seed** on the world. Show or share the seed with **Get Seed**; replay one with **Set Seed And
Regenerate** (server or standalone).
```cpp
const int32 Seed = World->GetSeed();
World->SetSeedAndRegenerate(Seed); // same world again, edits dropped
```
