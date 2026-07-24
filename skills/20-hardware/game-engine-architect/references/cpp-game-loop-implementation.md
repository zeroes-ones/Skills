# C++ Game Loop Implementation

## Robert Nystrom's Game Loop Pattern (Fixed Timestep)

```cpp
#include <chrono>

class GameLoop {
    using Clock = std::chrono::high_resolution_clock;
    using Duration = std::chrono::duration<double, std::milli>;

    static constexpr Duration FIXED_DT{16.6667};
    static constexpr int MAX_CATCHUP_FRAMES = 5;

    Duration lag{0.0};
    Clock::time_point previousTime;
    bool running = true;

public:
    void Run() {
        previousTime = Clock::now();
        while (running) {
            auto currentTime = Clock::now();
            Duration elapsed = currentTime - previousTime;
            previousTime = currentTime;
            if (elapsed > Duration{250.0}) elapsed = Duration{250.0};
            lag += elapsed;
            int steps = 0;
            while (lag >= FIXED_DT && steps < MAX_CATCHUP_FRAMES) {
                ProcessInput(FIXED_DT);
                FixedUpdate(FIXED_DT);
                lag -= FIXED_DT;
                ++steps;
            }
            double alpha = lag / FIXED_DT;
            Render(alpha);
        }
    }

private:
    void ProcessInput(Duration dt);
    void FixedUpdate(Duration dt);
    void Render(double alpha);
};
```

## Interpolation vs Extrapolation
- **Interpolation:** Render state between last 2 physics ticks. Adds latency but zero judder. Requires buffering previous+current state.
- **Extrapolation:** Predict next physics state from velocity. Zero added latency but overshoots on direction change.
- **Recommendation:** Interpolation always. Extrapolation only for remote players in multiplayer.

## Input Sampling
- Double-buffered input state: one buffer for capturing, one for reading.
- Sample ONCE per fixed update step, not per render frame.
- Use atomic swap for buffer index.

## Determinism Checklist
- Fixed-point math or IEEE 754 strict FP mode (no FMA contraction differences)
- Compiler: `/fp:strict` (MSVC), `-ffp-contract=off` (Clang/GCC)
- No `std::unordered_map` iteration (hash order differs between platforms)
- Seed random per tick, not per frame
