# Physics Engine Integration

## PhysX 5 (NVIDIA)
- **Rigid bodies:** `PxRigidDynamic` / `PxRigidStatic`. Set `PxRigidBodyFlag::eENABLE_CCD` for fast-moving objects
- **Collision detection:** Broadphase (AABB tree) → narrowphase (GJK/EPA). `PxSceneDesc::kineic-pruning` for CCD
- **Solver:** Position-based dynamics. Iteration count: 4 (quality), 2 (performance), 1 (mobile)
- **Scene queries:** `PxScene::raycast()`, `sweep()`, `overlap()`. Use `PxQueryFilterData` for layer filtering
- **Determinism:** `PxSceneDesc::eENABLE_PCM` + `eENABLE_STABILIZATION`. Still not 100% cross-platform deterministic

## Chaos Physics (Unreal Engine 5)
- **Physics asset:** `UPhysicsAsset` with `UBodySetup` per bone. Collision primitives: sphere/capsule/box/convex
- **Solver:** `UChaosSolverSettings`. Iterations: 8 (default), 4 (60 FPS console)
- **CCD:** `UChaosSolverSettings::bUseCCD`. Swept collision for bullets, fast projectiles
- **Destruction:** `UGeometryCollection` with fracture levels. Chaos destruction solver
- **Vehicles:** `UChaosWheeledVehicleMovementComponent` (replaces PhysX vehicles)

## Unity Physics (DOTS)
- **Stateless:** `PhysicsWorld` built fresh each frame from `PhysicsCollider` + `PhysicsVelocity` components
- **Collision layers:** `CollisionFilter` with `BelongsTo` / `CollidesWith` bitmasks
- **Solver iteration count:** `PhysicsStep.SolverIterationCount` (default: 4). Increase for stacking stability
- **CCD:** `PhysicsVelocity.Angular` with `PhysicsExclude.CCD` filter
- **Deterministic:** Same inputs = same results on same platform. Not guaranteed across platforms (float FP modes)

## Physics Budget per Frame
- **Physics tickrate:** 60Hz (16.67ms). Can be lower: 30Hz for mobile
- **Solver iteration budget:** 4 iterations × N contacts. Monitor contact manifold count
- **CCD cost:** 2-5x more expensive than discrete. Enable only for player character + projectiles
- **Wake/sleep:** Disable sleep for moving platforms, rotating objects. Use for static geometry
