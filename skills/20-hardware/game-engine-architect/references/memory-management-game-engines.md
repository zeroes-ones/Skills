# Memory Management for Game Engines

## Object Pool Pattern
```cpp
template<typename T>
class ObjectPool {
    std::vector<T> pool;
    std::vector<size_t> freeList;
    size_t capacity;
public:
    ObjectPool(size_t size) : capacity(size) {
        pool.resize(capacity);
        freeList.reserve(capacity);
        for (size_t i = 0; i < capacity; ++i) freeList.push_back(i);
    }
    
    T* Acquire() {
        if (freeList.empty()) return nullptr;  // Pool exhausted
        size_t idx = freeList.back();
        freeList.pop_back();
        return &pool[idx];
    }
    
    void Release(T* obj) {
        size_t idx = obj - pool.data();
        freeList.push_back(idx);
        obj->~T();  // Call destructor but keep memory
    }
};
```
- **Sizing:** `peak_count * 1.5` headroom. Log warning at 80% utilization

## Arena/Linear Allocator
```cpp
class LinearAllocator {
    uint8_t* buffer;
    size_t size;
    size_t offset{0};
public:
    LinearAllocator(size_t sz) : buffer(new uint8_t[sz]), size(sz) {}
    
    void* Allocate(size_t sz, size_t alignment = 16) {
        size_t aligned = (offset + alignment - 1) & ~(alignment - 1);
        if (aligned + sz > size) return nullptr;
        void* ptr = buffer + aligned;
        offset = aligned + sz;
        return ptr;
    }
    
    void Reset() { offset = 0; }  // Per-frame reset
};
```
- **Use case:** Per-frame scratch allocations (transforms, visibility results, command lists)
- **Reset at frame boundary.** Never free individual allocations

## Console Memory Budgets
| Subsystem | PS5 (16GB) | Xbox Series X (16GB) | Xbox Series S (10GB) |
|-----------|------------|---------------------|---------------------|
| OS Reserve | 2.5 GB | 2.5 GB | 2.0 GB |
| Audio | 512 MB | 512 MB | 384 MB |
| Render Targets | 2 GB | 2 GB | 1 GB |
| Textures (streaming) | 3 GB | 3 GB | 1.5 GB |
| Geometry (static) | 1 GB | 1 GB | 512 MB |
| Animation/Physics | 512 MB | 512 MB | 256 MB |
| Gameplay/UI | 512 MB | 512 MB | 256 MB |
| **Game Total** | **~8 GB** | **~8 GB** | **~4 GB** |

- **Budget rule:** Never exceed 85% of budget. Reserve 15% for fragmentation + peak spikes
- **Streaming pool:** Double-buffered texture streaming. Unload far LODs before loading near

## Avoid Common STL Allocation Pitfalls
- `std::vector::push_back()` amortized O(1) but reallocates. Use `reserve()` or pool allocator
- `std::map` / `std::unordered_map`: node-based allocation per element. Use `flat_map` or `robin_hood` hash
- `std::string`: SSO (Small String Optimization) up to 15 chars. Use `FixedString` for longer strings
- `std::function`: heap allocates for captures > 16 bytes. Use function pointers or templates
