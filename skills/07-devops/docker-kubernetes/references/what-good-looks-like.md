# What Good Looks Like — Full Quality Standard

Containers are minimal, pinned by SHA256 digest, and run as non-root with all Linux security capabilities dropped. Kubernetes manifests are templated, versioned in Git, and deployed via GitOps — the cluster state always matches the repo. Resources have appropriate requests and limits, and the cluster auto-scales horizontally and vertically without human intervention. Health probes are configured correctly, and PodDisruptionBudgets ensure zero downtime during voluntary disruptions. The cluster self-heals from node failures, and every workload survives a random pod deletion without dropping a single request.

> This is the full aspirational quality standard. The compressed version in SKILL.md is optimized for model token budgets.
