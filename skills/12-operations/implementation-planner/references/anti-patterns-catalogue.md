# Anti-Pattern Catalogue

The recurring failure modes of planning, each with its detection signal.

## Horizontal slicing
**Signal:** slice 1 is "all the models". **Cost:** integration risk deferred to the final week.
**Fix:** one thin end-to-end slice first.

## Tasks as activities
**Signal:** tasks beginning with "work on", "look at", "handle". **Cost:** no demonstrable completion.
**Fix:** restate as a state change with criteria.

## Feature-based parallelism
**Signal:** two tasks in one wave, no collision surface recorded. **Cost:** merge crisis.
**Fix:** run the file/resource check.

## Implicit ordering
**Signal:** dependencies stated in the description but absent from `blocked_by`. **Cost:** rework when two people collide.
**Fix:** every dependency becomes an edge or is deleted.

## Foundation-as-a-layer
**Signal:** a sequence of same-kind tasks with no demo between them. **Cost:** nothing is demoable until everything is.
**Fix:** one foundation task with a named consumer.

## Missing forgotten work
**Signal:** a migration with no backfill task; a flag with no removal task. **Cost:** an unplanned second sprint.
**Fix:** walk Decision Tree 4 every time.

## No unblocked set
**Signal:** every task has an unresolved predecessor. **Cost:** the sprint stalls on day one.
**Fix:** find the frontier or re-slice.

## Silent re-slicing
**Signal:** a task quietly grows rather than being split. **Cost:** the wrong seam survives.
**Fix:** treat a blown-up task as data about a bad boundary.

## Failure modes summary
Each of the above is a documented failure mode with a detection signal — the catalogue exists so
the plan can be audited against known ways plans go wrong.
