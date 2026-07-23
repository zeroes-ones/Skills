# Vendor Due Diligence Checklist

1. Does this vendor touch PHI in ANY way? (logs, IP, email, name?)
2. Do they offer a BAA? → If NO, can you de-identify before sending?
3. Does their BAA cover ALL sub-processors they use?
4. What is their breach notification SLA? (HIPAA requires ≤60 days; contract should require ≤30)
5. What happens to PHI on contract termination? (must be returned or destroyed)
```

### Phase 5: Patient Data Deletion (~3 hours)

```python
# app/services/data_deletion.py
# Implement cascading deletion that covers: primary DB, backups, logs, caches, search indexes

async def execute_deletion_request(db: AsyncSession, user_id: UUID, scope: str):
    """
    HIPAA right to request deletion + state law requirements.
    scope: 'full' | 'partial' | 'anonymize'
    """
    if scope == "full":
        # 1. Soft-delete in primary DB (preserve audit trail)
        await db.execute("UPDATE profiles SET deleted_at = now() WHERE user_id = :uid", {"uid": user_id})
        await db.execute("UPDATE users SET deleted_at = now() WHERE id = :uid", {"uid": user_id})

        # 2. Hard-delete from caches
        await redis.delete(f"user:{user_id}:*")
        await redis.delete(f"session:{user_id}:*")

        # 3. Queue deletion from search indexes
        await celery.send_task("search.delete_user", args=[str(user_id)])

        # 4. Queue deletion from backups (next backup cycle excludes soft-deleted)
        await celery.send_task("backup.exclude_user", args=[str(user_id)])

        # 5. Log the deletion request
        await audit_service.log_disclosure(db, user_id=user_id, action="deletion_requested")

        # 6. Queue 30-day verification (did cascading deletion complete?)
        await celery.send_task("compliance.verify_deletion", args=[str(user_id)],
                               countdown=30 * 86400)  # 30 days

    elif scope == "anonymize":
        # Replace PHI with synthetic data, preserve analytics value
        await db.execute("""
            UPDATE profiles SET
                first_name = CONCAT('Deleted_User_', SUBSTR(gen_random_uuid()::text, 1, 8)),
                last_name = '',
                email = NULL,
                phone = NULL,
                date_of_birth = NULL,
                address = NULL
            WHERE user_id = :uid
        """, {"uid": user_id})
    else:
        raise ValueError(f"Unknown deletion scope: {scope}")
```

### Phase 6: Breach Notification Pipeline (~2 hours)

```python
# app/services/breach_notification.py
from datetime import datetime, timedelta

class BreachResponse:
    """HIPAA breach notification: 60-day clock from discovery."""

    def assess_notification_requirement(self, incident: dict) -> str:
        """
        4-factor risk assessment per 45 CFR § 164.402.
        Returns: 'notify' | 'no_notify' | 'escalate_to_legal'
        """
        score = 0
        # Factor 1: Nature and extent of PHI
        if any(k in str(incident.get('data_types', [])) for k in ['diagnosis', 'treatment', 'hiv', 'mental_health']):
            score += 3  # clinical data = high risk
        elif any(k in str(incident.get('data_types', [])) for k in ['name', 'email']):
            score += 1  # demographic only = lower risk

        # Factor 2: Who received it
        if incident.get('recipient_is_covered_entity'):
            score -= 2  # another covered entity under BAA
        if incident.get('publicly_posted'):
            score += 3  # public exposure

        # Factor 3: Was PHI actually acquired?
        if incident.get('confirmed_exfiltration'):
            score += 3
        if incident.get('viewed_only'):
            score += 1

        # Factor 4: Mitigation
        if incident.get('data_encrypted'):
            score -= 3  # encrypted data = low probability of compromise

        if score <= 2:
            return 'no_notify'  # Low probability — document and move on
        elif score <= 5:
            return 'notify'  # Notify individuals and HHS
        else:
            return 'escalate_to_legal'  # High severity, potential media notification

    async def send_notifications(self, incident: dict, affected_count: int):
        """Execute notification pipeline."""
        # 1. Notify individuals within 60 days
        # 2. Notify HHS (simultaneously if >500 affected, annually if <500)
        # 3. Notify media if >500 affected in a single state/jurisdiction
        # 4. Log all notification attempts (required for compliance audit)

        for user in incident.get('affected_users', []):
            await self.notify_individual(user, incident)

        if affected_count > 500:
            await self.notify_hhs_immediate(incident, affected_count)
            await self.notify_prominent_media(incident, affected_count)
        else:
            await self.schedule_hhs_annual_report(incident, affected_count)
```
