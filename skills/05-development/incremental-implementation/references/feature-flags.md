# Feature Flags in Incremental Delivery

A flag is what makes an incomplete slice safe to ship.

## The lifecycle

1. **Create the flag, default off.** Ship it before the code that uses it.
2. **Build behind the flag.** Each slice lands dark.
3. **Enable progressively.** Internal → canary → percentage → all.
4. **Remove the flag.** A flag that outlives its rollout is debt, not safety.

## Rules

- **The default must be safe.** Off, or the last-known-good behaviour.
- **One flag, one purpose.** Reusing a flag couples unrelated rollouts.
- **The flag removal is a task.** Schedule it when the flag is created, not when someone remembers.
- **Both paths must be tested.** The off path is production until the rollout completes.

## Failure modes of flags

- **Flag never removed.** Dead branches accumulate and every reader must reason about both paths.
- **Unsafe default.** A flag defaulting on ships the change before anyone intended it.
- **Untested off path.** The flag is flipped off in an incident and the old path is broken.
- **Flag used as a permission system.** Coupling release control to authorization is a security smell.
- **Rollout without an owner.** Nobody knows whether it is safe to enable further.
