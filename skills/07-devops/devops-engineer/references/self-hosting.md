# Self-Hosting Breakeven Calculator

```
Monthly cost to self-host = (server_cost + backup_cost + monitoring_cost) + 
                           (engineer_salary / 12 × ops_time_fraction × team_size)

Example: Self-hosting PostgreSQL
Server: r6i.xlarge = $190/month
Backup + monitoring: $50/month
Ops time: 25% of 1 engineer @ $200K/year = $4,167/month
TOTAL: $4,407/month

RDS equivalent: db.r6i.xlarge Multi-AZ = $780/month
Savings: $3,627/month by using managed.

Self-hosting only wins when:
- You need 10+ dedicated servers → bulk hardware savings > engineer cost
- You have < 1% ops overhead (automated everything, zero-touch)
- You need features no cloud provider offers
```
