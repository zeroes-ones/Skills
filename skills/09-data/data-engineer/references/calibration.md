# Calibration — How to Know Your Level

<!-- STANDARD: 3min — honest self-assessment rubric -->

| You Know You're Stuck at L1 When... | You Know You've Reached L2 When... | You Know You're L3 When... |
|---|---|---|
| You can write a Spark job that works on your laptop but have no idea what happens when the input is 100× larger and the cluster has 3 spot instance terminations | You design pipelines with idempotency, dead letter queues, checkpointing, and backfill procedures — and you've tested all of them under failure conditions | A pipeline fails at 3 AM and from a single log line you can identify whether the fix needs to be in the code (retry logic), infrastructure (memory allocation), or data model (partition strategy) — and you're right 90% of the time |
| You process data in full-refresh mode because "incremental is too complicated" and don't understand why the warehouse bill doubled when the company tripled | You've implemented incremental processing with late-arriving data windows, merge strategies, and exactly-once semantics — and you can explain the trade-offs of each approach to a junior engineer | You can look at a data platform's monthly bill and identify the 3 pipelines responsible for 70% of the cost within 30 minutes, then propose changes that cut it by 40% without data loss |
| You don't know what a WAL or a checkpoint is — and you've never needed to because "Kafka just works" | You can recover a Kafka consumer group from a specific offset after an outage, and you've written a runbook that a junior engineer successfully executed without your help | You design the data platform for a 200-person engineering org — and 12 months later, 40 data producers and 60 data consumers are onboarded with zero data loss incidents |

**The Litmus Test:** Take your most critical production pipeline offline right now. Can you recover it with zero data loss and zero duplicate data within 30 minutes, without looking at documentation? If you reach for a runbook, your system isn't resilient enough. If the runbook is wrong, you find out during the incident.
