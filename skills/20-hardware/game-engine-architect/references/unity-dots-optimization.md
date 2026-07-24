# Unity DOTS Optimization

## Burst Compiler
- `[BurstCompile(FloatPrecision.Low, FloatMode.Fast, OptimizeFor = OptimizeFor.Performance)]`
- `FloatPrecision.Low`: Enables FMA, approximate reciprocals (~15% speedup for physics)
- `FloatMode.Fast`: Enables subnormal flush-to-zero, associative math (~10% speedup)
- Avoid: managed objects, strings, delegates, `try/catch`, `throw` in Burst code

## Job System: IJobFor
```csharp
[BurstCompile]
struct UpdatePositions : IJobFor {
    [ReadOnly] public NativeArray<float3> Velocities;
    public NativeArray<float3> Positions;
    public float DeltaTime;
    public void Execute(int index) {
        Positions[index] += Velocities[index] * DeltaTime;
    }
}
// Schedule: job.Schedule(count, innerloopBatchCount: 64);
```

## IL2CPP AOT Compilation
- Strips unused code aggressively: use `[Preserve]` or `link.xml` for reflection-needed types
- Generics: `List<int>` and `List<float>` = separate AOT methods; reference types share generic instantiation
- `link.xml` preserves types needed by reflection

## Addressables Memory Streaming
```csharp
var handle = Addressables.LoadAssetAsync<GameObject>("Assets/Prefabs/Enemy.prefab");
handle.Completed += (op) => {
    if (op.Status == AsyncOperationStatus.Succeeded) Instantiate(op.Result);
};
// Release: Addressables.Release(handle);
```

## GPU Instancing vs SRP Batcher
- **GPU Instancing:** Same mesh + same material = 1 draw call for N instances. Best for >100 identical objects
- **SRP Batcher:** Different meshes + same shader variant = batched in SRP. Best for heterogeneous scenes
- **Rule:** GPU Instancing for identical objects, SRP Batcher for varied PBR props
