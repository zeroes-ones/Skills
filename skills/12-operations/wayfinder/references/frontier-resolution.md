# Frontier Resolution

## What Is the Frontier?

The frontier is the set of investigation tickets whose dependencies are all resolved (status: done). These are the only tickets ready to be worked on.

## Computing the Frontier

```
frontier = []
for ticket in all_tickets:
    if ticket.status in [pending] and all_dependencies_done(ticket):
        frontier.append(ticket)
```

## Frontier Selection Strategy

When the frontier has more than 3 tickets (the session cap):

1. **BLOCKING first:** These gate implementation — resolve them before anything else
2. **ORDERING next:** These gate other investigations — resolving them expands the frontier
3. **INDEPENDENT last:** These can wait — use as fill tasks when blocked on others

Within the same classification, prefer:
- Tickets with the most dependents (unblocks more work)
- Tickets that have been pending longest
- Tickets whose method is fastest (quick wins expand frontier faster)

## Frontier Starvation

When frontier is empty but tickets remain:
- **All remaining tickets are blocked:** The dependency chain hasn't been worked through. Check if any dependencies can be relaxed.
- **Incorrect dependency specification:** Some edges may be wrong — re-evaluate whether ticket B truly requires ticket A.
- **External blocker:** Something outside the DAG is blocking (waiting for access, data, decision). Document as BLOCKED.

## Parallel Investigation

With 3 active slots:
- Slot 1: Highest priority BLOCKING ticket
- Slot 2: Next BLOCKING or highest ORDERING ticket
- Slot 3: INDEPENDENT fill ticket (something that can be worked on while slots 1-2 may have wait times)

This ensures at least 1 ticket is always making progress even if 1-2 hit temporary blocks.

## Frontier Dashboard

Query to run at session start:
```bash
echo "=== Frontier Tickets ==="
for t in tickets/*.md; do
  deps=$(grep "Depends on:" "$t" | sed 's/.*: //')
  status=$(grep "status:" "$t" | sed 's/.*: //')
  if [ "$status" = "pending" ]; then
    all_done=true
    for dep in $deps; do
      dep_status=$(grep "status:" "tickets/${dep}.md" 2>/dev/null | sed 's/.*: //')
      [ "$dep_status" != "done" ] && all_done=false
    done
    $all_done && echo "  READY: $(basename $t .md)"
  fi
done
```
