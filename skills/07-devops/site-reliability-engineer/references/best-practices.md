# Best Practices

<!-- STANDARD: 3min -- rules extracted from production experience -->
- **Hope is not a strategy**: every critical user journey needs an SLI. If you can't measure it, you can't manage it.
- **SLOs are a decision-making tool, not a report card**: use error budgets to decide when to ship features vs. invest in reliability — not to punish teams.
- **100% is the wrong target**: 100% reliability costs exponentially more and prevents innovation. Users don't notice the difference between 99.99% and 99.999% on a mobile connection.
- **Automate toil until it hurts (and then automate some more)**: every manual step is a future incident. SREs should spend > 50% of time on engineering work, not operations.
- **Blameless is not consequence-free**: postmortems should be blameless in tone but rigorous in action items. "Blameless" means "we all want to fix the system," not "nobody is accountable."
- **Alert on symptoms, not causes**: alert on "user-facing error rate > 1%" not "CPU > 80%." The latter is a <!-- DEEP: 10+min -->
debugging signal, not a user-impact signal.
- **Every alert must require human action**: if an alert fires and you can ignore it, it's noise — tune the threshold or remove it. Alert fatigue kills response times.
- **Runbooks before alerts**: never create an alert without a linked runbook. "Page first, figure it out later" is how SEV1s become SEV0s.
- **Capacity is a reliability concern**: running out of capacity is a self-inflicted outage. Plan for 2x peak and have elastic scaling as backup.
- **SRE is cultural, not a job title**: reliability is everyone's responsibility. SRE provides the framework, tooling, and expertise — but service owners own their SLOs.
