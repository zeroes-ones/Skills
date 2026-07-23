# Scale Depth: Solo → Small → Medium → Enterprise

<!-- DEEP: 10+min -->

### Solo (1 person, 0-100 users)
- **What changes**: Simple dashboards in Metabase/Lightdash. Manual metric definitions in a shared doc. Spreadsheet-based board reporting. No semantic layer. No data freshness monitoring. Manual data exports.
- **What to skip**: dbt, LookML, formal semantic layer, governed self-serve, clinical analytics dashboards, pharma partner reporting, embedded analytics, data export compliance framework.
- **Coordination**: You build the dashboards and present the numbers. Document metric definitions somewhere accessible.

### Small Team (2-10 people, 100-10K users)
- **What changes**: dbt with basic testing. Looker/Metabase/Lightdash with shared dashboards. Formal board deck metrics with reconciliation. Basic clinical outcomes tracking. Data freshness monitoring with dbt source freshness. Star schema data models.
- **What to skip**: Full MetricFlow semantic layer, governed self-serve tiers, pharma partner RWE dashboards, white-label embedded analytics, SCD Type 2 history tracking, automated data export compliance.
- **Coordination**: BI engineer owns semantic layer. Data engineer ensures pipeline reliability. Weekly stakeholder review of key dashboards.

### Medium Team (10-50 people, 10K-1M users)
- **What changes**: Full dbt MetricFlow semantic layer. Governed self-serve with tiered dashboards. Automated board reporting with variance analysis. Clinical outcomes analytics with MCID thresholds. Pharma partner RWE dashboards with de-identification. SCD Type 2 for key dimensions. Incremental dbt models. Embedded analytics with SSO.
- **What to skip**: Real-time operational dashboards, multi-tenant embedded analytics, HIPAA-certified export pipeline, automated board deck generation, investor data room.
- **Coordination**: BI team (2-3 engineers). Monthly data governance review. Quarterly board report dry run. Clinical analytics reviewed by medical director.

### Enterprise (50+ people, 1M+ users)
- **What changes**: Multi-tier semantic layer across business domains. Full governed self-serve with certification workflow. Automated board deck generation. Real-time clinical outcomes monitoring. HIPAA-compliant pharma reporting pipeline. Full SCD history for regulatory audit trails. Real-time operational dashboards. Multi-tenant white-label embedded analytics. Automated data export compliance with audit.
- **What's full production**: SOC 2 + HIPAA certified BI platform. Investor data room with live metrics. Published data dictionary. Data certification program. Embedded analytics serving 10K+ external users. Real-time alerting on KPI degradation.
- **Coordination**: BI platform team. Data governance committee. Clinical informatics team. Investor relations coordinator. Quarterly board materials review.

### Transition Triggers
- **Solo → Small**: Board asks "what's our NRR?" and you can't produce it in <1 day. >3 people need dashboards.
- **Small → Medium**: CEO presents wrong number to investors. Pharma partner requires de-identified population analytics. >50 dashboard viewers.
- **Medium → Enterprise**: IPO or late-stage fundraising requires auditable metrics. Multiple external partners requiring embedded analytics. SOC 2/HIPAA certification required.
