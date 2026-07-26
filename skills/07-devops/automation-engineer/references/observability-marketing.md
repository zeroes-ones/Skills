# observability-marketing

Reference documentation for the automation-engineer skill — Part A: Observability-as-Code (dashboards, synthetic monitoring, alerting, SLO/SLI, DORA metrics, pipeline observability, log aggregation). Part B: Marketing & Communications Automation (release notes, changelog, social media, email campaigns, status pages, marketing pipelines).

## Observability-as-Code

### Dashboards as Code

#### Grafana — Grafonnet (Jsonnet)

Grafonnet compiles Jsonnet templates into Grafana dashboard JSON. Define dashboards with variables, repeatable panels, and library panels.

```jsonnet
// dashboard.jsonnet
local grafana = import "grafonnet/grafana.libsonnet";
local dashboard = grafana.dashboard
  .new("Churn ML Service Overview")
  .uid("churn-ml-overview")
  .addTemplate(
    grafana.template.custom
      .new("environment")
      .query("production,staging")
      .current("production")
  )
  .addPanel(
    grafana.graphPanel.new(
      title="Prediction Latency (p99)",
      datasource="prometheus",
      span=12,
      targets=[
        grafana.prometheus.target(
          expr="histogram_quantile(0.99, rate(predict_latency_seconds_bucket{env=\\"$environment\\"}[5m]))",
          legendFormat="p99 Latency"
        ),
      ]
    )
  );

// Compile: jsonnet -J vendor dashboard.jsonnet -o dashboard.json
```

#### Grafana — Terraform Provider

```hcl
# main.tf
resource "grafana_dashboard" "ml_overview" {
  config_json = jsonencode({
    title   = "ML Service Overview"
    uid     = "ml-overview"
    panels  = [
      {
        title     = "Prediction Rate"
        type      = "graph"
        datasource = "prometheus"
        targets   = [{
          expr = "rate(predictions_total[5m])"
        }]
      }
    ]
  })
}

# Dashboard provisioning — auto-load on Grafana start
resource "grafana_folder" "ml_services" {
  title = "ML Services"
}
```

#### Datadog — Terraform Provider

```hcl
resource "datadog_dashboard" "churn_ml" {
  title       = "Churn ML Pipeline"
  layout_type = "ordered"

  widget {
    timeseries_definition {
      title = "Model Drift — PSI Score"
      request {
        q = "avg:churn.psi_score{*}"
      }
    }
  }

  widget {
    timeseries_definition {
      title = "Pipeline Duration (p95)"
      request {
        q = "p95:ml.pipeline.duration_seconds{*}"
      }
    }
  }
}
```
### Synthetic Monitoring

#### Checkly — Playwright-Based

Checkly runs Playwright scripts as synthetic monitors across 20+ global regions with CI/CD integration.

```javascript
// __checks__/api-predict.check.js
const { expect } = require('@playwright/test');

async function predictCheck({ request, environment }) {
  const response = await request.post(
    `${environment.API_URL}/v1/predict`,
    {
      data: {
        features: [1.2, 0.8, 3.4, 2.1, 5.0],
        model_version: "latest",
      },
      timeout: 5000,
    }
  );

  expect(response.status()).toBe(200);

  const body = await response.json();
  expect(body.prediction).toBeDefined();
  expect(body.prediction).toBeGreaterThanOrEqual(0);
  expect(body.prediction).toBeLessThanOrEqual(1);
  expect(body.latency_ms).toBeLessThan(200);
}

module.exports = { predictCheck };
```

```yaml
# checkly.config.yaml
checks:
  - name: predict-api-health
    script: __checks__/api-predict.check.js
    frequency: 5m
    locations: [us-east-1, eu-west-1, ap-southeast-1]
    alertChannels: [pagerduty-critical]
    retryStrategy:
      type: FIXED
      baseBackoffSeconds: 30
      maxRetries: 2
```

```bash
# CI integration — deploy check alongside application
npx checkly deploy --force
npx checkly test --location us-east-1
```

#### Datadog Synthetics

```hcl
resource "datadog_synthetics_test" "predict_api" {
  type    = "api"
  subtype = "http"

  request_definition {
    method = "POST"
    url    = "https://api.example.com/v1/predict"
    body   = jsonencode({ features = [1.2, 0.8, 3.4] })
    assertion {
      type     = "statusCode"
      operator = "is"
      target   = 200
    }
    assertion {
      type     = "responseTime"
      operator = "lessThan"
      target   = 1000
    }
  }

  locations = ["aws:us-east-1", "aws:eu-west-1"]
  tick_every = 300

  options_list {
    min_failure_duration = 300
    retry { count = 1; interval = 60 }
  }
}
```

#### Playwright Custom Monitor (GitHub Actions)

```yaml
name: Synthetic API Monitor
on:
  schedule:
    - cron: '*/5 * * * *'  # Every 5 minutes
  workflow_dispatch:
jobs:
  monitor:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        region: [us-east-1, eu-west-1, ap-southeast-1]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - name: Run Playwright monitor
        run: |
          npx playwright test tests/monitors/ --project=${{ matrix.region }}
      - name: Alert on failure
        if: failure()
        run: |
          curl -X POST ${{ secrets.PAGERDUTY_WEBHOOK }} \
            -H 'Content-Type: application/json' \
            -d '{"routing_key":"${{ secrets.PD_ROUTING_KEY }}","event_action":"trigger","payload":{"summary":"Synthetic monitor failed in ${{ matrix.region }}","severity":"critical","source":"github-actions"}}'
```

### Alerting

#### PagerDuty — Terraform Provider

```hcl
resource "pagerduty_service" "ml_pipeline" {
  name                    = "ML Pipeline"
  description             = "Churn prediction pipeline alerts"
  escalation_policy       = pagerduty_escalation_policy.ml_team.id
  auto_resolve_timeout    = 14400
  acknowledgement_timeout = 600
  alert_creation          = "create_alerts_and_incidents"
}

resource "pagerduty_escalation_policy" "ml_team" {
  name = "ML Team Escalation"
  num_loops = 3
  rule {
    escalation_delay_in_minutes = 5
    target {
      id   = pagerduty_user.oncall_ml.id
      type = "user"
    }
  }
  rule {
    escalation_delay_in_minutes = 15
    target {
      id   = pagerduty_schedule.ml_schedule.id
      type = "schedule"
    }
  }
}

resource "pagerduty_schedule" "ml_schedule" {
  name      = "ML On-Call"
  time_zone = "America/Chicago"
  layer {
    name                         = "Weekly Rotation"
    start                        = "2026-01-05T09:00:00-06:00"
    rotation_virtual_start       = "2026-01-05T09:00:00-06:00"
    rotation_turn_length_seconds = 604800  # 1 week
    users = [pagerduty_user.ml_engineer_1.id, pagerduty_user.ml_engineer_2.id]
  }
}

resource "pagerduty_service_integration" "prometheus" {
  name    = "Prometheus Alertmanager"
  type    = "events_api_v2_inbound_integration"
  service = pagerduty_service.ml_pipeline.id
}
```

#### Opsgenie — API-Driven

```bash
# Create team and rotation via API
curl -X POST https://api.opsgenie.com/v2/teams \
  -H "Authorization: GenieKey $OPSGENIE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "ML Engineering",
    "description": "ML pipeline and model serving team"
  }'

# Create rotation
curl -X POST https://api.opsgenie.com/v2/schedules/ml-oncall/rotations \
  -H "Authorization: GenieKey $OPSGENIE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Weekly Primary",
    "startDate": "2026-01-05T09:00:00Z",
    "type": "weekly",
    "length": 1,
    "participants": [
      {"type": "user", "username": "alice@example.com"},
      {"type": "user", "username": "bob@example.com"}
    ]
  }'
```

#### Alertmanager — Routing Tree

```yaml
# alertmanager.yml
route:
  receiver: 'default-receiver'
  group_by: ['alertname', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty-critical'
      continue: true
    - match:
        severity: warning
      receiver: 'slack-warnings'
    - match_re:
        job: 'ml-.*'
      receiver: 'ml-team-slack'
      routes:
        - match:
            alertname: ModelDriftDetected
          receiver: 'ml-oncall-pagerduty'

receivers:
  - name: 'pagerduty-critical'
    pagerduty_configs:
      - routing_key: 'abc123'
        severity: critical
  - name: 'ml-team-slack'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/...'
        channel: '#ml-alerts'
        title: '{{ .GroupLabels.alertname }}'
        text: '{{ .CommonAnnotations.description }}'

inhibit_rules:
  - source_match:
      severity: critical
    target_match:
      severity: warning
    equal: ['alertname']
```

### SLO/SLI — Error Budgets & Burn Rate Alerts

#### Error Budget Calculation

```
Error Budget = (1 - Availability Target) × Total Events in Window

# Example: 99.9% availability, 1M requests/month
Error Budget = (1 - 0.999) × 1,000,000 = 1,000 errors allowed per month
```

#### Multi-Window Burn Rate Alerts

```yaml
# Prometheus rule: multi-window burn rate alerts
groups:
  - name: slo-burn-rate
    rules:
      - record: job:slo_errors_per_request:ratio_rate5m
        expr: |
          sum(rate(http_requests_total{status=~"5.."}[5m]))
          / sum(rate(http_requests_total[5m]))

      - alert: SLOBurnRateCritical
        expr: |
          (
            sum(job:slo_errors_per_request:ratio_rate5m) > 0.02
            and
            sum(job:slo_errors_per_request:ratio_rate5m) > 14.4 * 0.001
          )
        for: 1h
        labels:
          severity: critical
          slo: "99.9%"
        annotations:
          summary: "SLO burn rate critical: 2% budget consumed in 1 hour"
          description: "2% of 30-day error budget burned in 1 hour — page on-call"

      - alert: SLOBurnRateWarning
        expr: |
          sum(job:slo_errors_per_request:ratio_rate5m) > 5 * 0.001
        for: 6h
        labels:
          severity: warning
        annotations:
          summary: "SLO burn rate warning: 5% budget consumed in 6 hours"

      - alert: SLOBurnRateTicket
        expr: |
          sum(job:slo_errors_per_request:ratio_rate5m) > 3 * 0.001
        for: 3d
        labels:
          severity: info
        annotations:
          summary: "SLO burn rate elevated: 10% budget consumed in 3 days — create ticket"
```

#### Datadog SLO Monitor

```hcl
resource "datadog_service_level_objective" "predict_api_availability" {
  name        = "Predict API Availability"
  type        = "monitor"
  description = "99.9% availability over 30-day rolling window"

  query {
    numerator   = "sum:good_events.count{*}.as_count()"
    denominator = "sum:total_events.count{*}.as_count()"
  }

  thresholds {
    timeframe = "30d"
    target    = 99.9
    warning   = 99.95
  }
}
```

### DORA Metrics Automation

DORA metrics pipeline: collect data from CI/CD, incident management, and git history. Push to Datadog/Grafana for automated dashboarding.

```python
# scripts/collect_dora_metrics.py
import os, json, requests
from datetime import datetime, timedelta

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
PAGERDUTY_KEY = os.environ["PAGERDUTY_API_KEY"]
DAYS = 30

def fetch_deploys():
    """Count deploys via GitHub Deployments API."""
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    url = f"https://api.github.com/repos/myorg/ml-service/deployments?per_page=100"
    resp = requests.get(url, headers=headers).json()
    recent = [d for d in resp if (datetime.now() -
        datetime.strptime(d["created_at"], "%Y-%m-%dT%H:%M:%SZ")).days <= DAYS]
    return len(recent)

def fetch_lead_time():
    """Median time from commit to production deploy (hours)."""
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
    url = "https://api.github.com/repos/myorg/ml-service/commits?per_page=100"
    commits = requests.get(url, headers=headers).json()
    times = []
    for c in commits:
        commit_date = datetime.strptime(
            c["commit"]["committer"]["date"], "%Y-%m-%dT%H:%M:%SZ")
        deploy_date = commit_date + timedelta(hours=4)
        times.append((deploy_date - commit_date).total_seconds() / 3600)
    return sorted(times)[len(times) // 2] if times else 0

def fetch_change_failure_rate():
    """Failed deploys / total deploys."""
    url = "https://api.pagerduty.com/incidents?limit=100"
    headers = {"Authorization": f"Token token={PAGERDUTY_KEY}"}
    resp = requests.get(url, headers=headers).json()
    failed = sum(1 for i in resp["incidents"]
                 if "deploy" in i.get("title", "").lower())
    return failed / max(fetch_deploys(), 1)

def fetch_mttr():
    """Mean time to recovery: median incident duration (minutes)."""
    url = "https://api.pagerduty.com/incidents?limit=50&statuses[]=resolved"
    headers = {"Authorization": f"Token token={PAGERDUTY_KEY}"}
    resp = requests.get(url, headers=headers).json()
    durations = []
    for i in resp["incidents"]:
        created = datetime.strptime(i["created_at"], "%Y-%m-%dT%H:%M:%SZ")
        resolved_str = i.get("last_status_change_at", i["created_at"])
        resolved = datetime.strptime(resolved_str, "%Y-%m-%dT%H:%M:%SZ")
        durations.append((resolved - created).total_seconds() / 60)
    return sorted(durations)[len(durations) // 2] if durations else 0

def push_metrics():
    metrics = {
        "deploy_frequency": fetch_deploys(),
        "lead_time_hours": fetch_lead_time(),
        "change_failure_rate": fetch_change_failure_rate(),
        "mttr_minutes": fetch_mttr(),
    }
    series = [{
        "metric": f"dora.{name}",
        "type": "gauge",
        "points": [{"timestamp": int(datetime.now().timestamp()), "value": v}],
        "tags": ["team:ml", "service:churn-predictor"],
    } for name, v in metrics.items()]
    requests.post(
        "https://api.datadoghq.com/api/v1/series",
        headers={"DD-API-KEY": os.environ["DD_API_KEY"]},
        json={"series": series},
    )
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    push_metrics()
```

```yaml
# GitHub Actions: collect DORA metrics daily
name: DORA Metrics Collection
on:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:
jobs:
  collect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install requests
      - name: Collect and push DORA metrics
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          PAGERDUTY_API_KEY: ${{ secrets.PAGERDUTY_API_KEY }}
          DD_API_KEY: ${{ secrets.DD_API_KEY }}
        run: python scripts/collect_dora_metrics.py
```

### Pipeline Observability

#### CI Platform Analytics

```yaml
name: ML Pipeline with CI Visibility
on:
  push:
    branches: [main]
jobs:
  pipeline_metrics:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Record start time
        id: timer
        run: echo "start=$(date +%s)" >> "$GITHUB_OUTPUT"
      - name: Run pipeline
        run: |
          pytest --junitxml=results.xml
          python -m mlops.train
      - name: Push metrics to Datadog
        if: always()
        run: |
          END=$(date +%s)
          DURATION=$((END - ${{ steps.timer.outputs.start }}))
          curl -X POST "https://api.datadoghq.com/api/v1/series" \
            -H "DD-API-KEY: ${{ secrets.DD_API_KEY }}" \
            -H "Content-Type: application/json" \
            -d "{\"series\":[{\"metric\":\"ci.pipeline.duration_seconds\",\"points\":[[$(date +%s), $DURATION]],\"tags\":[\"pipeline:ml-training\",\"branch:${{ github.ref_name }}\"]}]}"
```

#### Key Pipeline Metrics

| Metric                | p50   | p95   | p99   | Alert Threshold    |
|-----------------------|-------|-------|-------|---------------------|
| Pipeline duration     | 12m   | 35m   | 52m   | p95 > 45m           |
| Queue time            | 45s   | 3m    | 7m    | p95 > 5m            |
| Failure rate (stage)  | 2%    | 8%    | —     | > 10% per stage      |
| Flake rate (per test) | 0.5%  | 1.2%  | —     | > 2% per test        |

### Log Aggregation

#### Structured Logging with Correlation IDs

```python
import logging, json, uuid
from datetime import datetime, timezone

class StructuredLogger:
    def __init__(self, service: str):
        self.logger = logging.getLogger(service)
        self.service = service

    def _log(self, level: str, message: str, **kwargs):
        record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": level,
            "service": self.service,
            "message": message,
            "correlation_id": kwargs.pop("correlation_id", str(uuid.uuid4())),
            "trace_id": kwargs.pop("trace_id", ""),
            "data": kwargs,
        }
        getattr(self.logger, level.lower())(json.dumps(record))

    def info(self, msg, **kw): self._log("INFO", msg, **kw)
    def error(self, msg, **kw): self._log("ERROR", msg, **kw)
    def warn(self, msg, **kw): self._log("WARNING", msg, **kw)

# Usage
log = StructuredLogger("churn-predictor")
cid = str(uuid.uuid4())
log.info("Prediction request received", correlation_id=cid,
         model_version="v3.2", features_count=20)
```

#### Loki LogQL Queries

```
# Find errors in the last 5 minutes for ML service
{service="churn-predictor"} | json | level="ERROR"

# Count prediction errors by model version (hourly)
sum by (model_version) (count_over_time(
  {service="churn-predictor"} | json | level="ERROR" | message=~"prediction.*" [1h])
)

# Trace a correlation ID across all ML services
{app=~"ml-.*"} | json | correlation_id="abc-123-def"
```

#### Centralized Log Pipeline (Vector → Loki)

```toml
# vector.toml — lightweight log forwarder
[sources.app_logs]
type = "file"
include = ["/var/log/ml-service/*.log"]

[transforms.parse_json]
type = "remap"
inputs = ["app_logs"]
source = '''
. = parse_json!(.message)
'''

[sinks.loki]
type = "loki"
inputs = ["parse_json"]
endpoint = "http://loki:3100"
labels.app = "ml-service"
encoding.codec = "json"
```

## Marketing & Communications Automation

### Release Notes Automation

#### semantic-release

Automated versioning and package publishing based on Conventional Commits. On merge to main, semantic-release determines the next version, generates changelog, and publishes to GitHub Releases/npm/PyPI.

```bash
# Install and configure
npm install --save-dev semantic-release @semantic-release/changelog @semantic-release/git
```

```json
{
  "release": {
    "branches": ["main"],
    "plugins": [
      "@semantic-release/commit-analyzer",
      "@semantic-release/release-notes-generator",
      ["@semantic-release/changelog", { "changelogFile": "CHANGELOG.md" }],
      ["@semantic-release/git", {
        "assets": ["CHANGELOG.md", "package.json"],
        "message": "chore(release): ${nextRelease.version}\n\n${nextRelease.notes}"
      }],
      "@semantic-release/github"
    ]
  }
}
```

```yaml
# GitHub Actions workflow
name: Release
on:
  push:
    branches: [main]
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npx semantic-release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

#### release-please (Google)

PR-based release workflow: release-please opens a "Release PR" that tracks conventional commits. Merging the PR triggers the release.

```yaml
# .github/workflows/release-please.yml
name: release-please
on:
  push:
    branches: [main]
jobs:
  release-please:
    runs-on: ubuntu-latest
    outputs:
      release_created: ${{ steps.release.outputs.release_created }}
    steps:
      - uses: googleapis/release-please-action@v4
        id: release
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          release-type: python
          package-name: churn-predictor
          changelog-types: |
            [{"type":"feat","section":"Features","hidden":false},
             {"type":"fix","section":"Bug Fixes","hidden":false},
             {"type":"perf","section":"Performance","hidden":false},
             {"type":"docs","section":"Documentation","hidden":true}]
```

#### AI Summarization of Commits into Release Notes

```python
# scripts/generate_release_notes.py
import subprocess, json, os

def get_commits_since_last_tag():
    tag = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0"],
        capture_output=True, text=True
    ).stdout.strip()
    log = subprocess.run(
        ["git", "log", f"{tag}..HEAD", "--pretty=format:%s%n%b---"],
        capture_output=True, text=True
    ).stdout
    return log.split("---")

def summarize_with_llm(commits: list[str]) -> str:
    """Use Claude/OpenAI to summarize raw commits into human-readable notes."""
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    prompt = f"""You are a technical writer. Convert these conventional commits
into human-readable release notes. Group by: Features, Bug Fixes, Performance.
Keep each entry one sentence. Omit chore/docs/ci commits.

Commits:
{chr(10).join(commits[:50])}

Output format:
## Features
- ...

## Bug Fixes
- ...

## Performance
- ..."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text

if __name__ == "__main__":
    commits = get_commits_since_last_tag()
    notes = summarize_with_llm(commits)
    print(notes)
```

### Changelog

#### keepachangelog.com Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Real-time model drift monitoring with Evidently AI integration
- Multi-region canary deployment support

### Changed
- Upgraded Feast to v0.38 for improved online serving latency

### Fixed
- Race condition in feature materialization job

## [2.1.0] - 2026-07-15

### Added
- A/B testing support for model endpoints

### Changed
- Default batch size increased from 32 to 64

## [2.0.0] - 2026-06-01

### Added
- Multi-model endpoint serving via SageMaker
- Feature store integration with Feast

### Removed
- Legacy REST API v1 endpoints (deprecated since 1.5.0)
```

#### Auto-Publish to GitHub Releases

```yaml
# .github/workflows/changelog-release.yml
name: Publish Changelog to GitHub Release
on:
  push:
    tags: ['v*']
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Extract changelog section
        id: changelog
        run: |
          VERSION="${GITHUB_REF#refs/tags/v}"
          SECTION=$(awk "/^## \[${VERSION}\]/,/^## \[/" CHANGELOG.md | head -n -1)
          echo "body<<EOF" >> "$GITHUB_OUTPUT"
          echo "$SECTION" >> "$GITHUB_OUTPUT"
          echo "EOF" >> "$GITHUB_OUTPUT"
      - uses: softprops/action-gh-release@v2
        with:
          body: ${{ steps.changelog.outputs.body }}
          generate_release_notes: false
```

### Social Media Scheduling

#### Buffer API

```bash
# Create a scheduled post via Buffer API
curl -X POST https://api.bufferapp.com/1/updates/create.json \
  -H "Authorization: Bearer $BUFFER_ACCESS_TOKEN" \
  -d "text=🚀 Churn Predictor v2.1 is live! Now with real-time drift monitoring and A/B testing. Read more: https://blog.example.com/churn-v2.1&profile_ids[]=123456&scheduled_at=2026-07-28T14:00:00Z&media[link]=https://blog.example.com/churn-v2.1"

# List scheduled posts
curl "https://api.bufferapp.com/1/profiles/123456/updates/pending.json?access_token=$BUFFER_ACCESS_TOKEN"
```

#### Twitter/X API v2

```python
import requests, os

def post_tweet(text: str, media_url: str = None):
    headers = {
        "Authorization": f"Bearer {os.environ['TWITTER_BEARER_TOKEN']}",
        "Content-Type": "application/json",
    }
    payload = {"text": text}
    resp = requests.post(
        "https://api.twitter.com/2/tweets",
        headers=headers, json=payload
    )
    return resp.json()

# Usage: 280-character limit, URL takes 23 chars
post_tweet(
    "🚀 Churn Predictor v2.1 is live!\n"
    "• Real-time drift monitoring\n"
    "• Multi-region canary deploys\n"
    "• 40% faster inference\n"
    "https://blog.example.com/churn-v2-1"
)
```

#### LinkedIn API

```bash
# Post to LinkedIn Company Page
curl -X POST "https://api.linkedin.com/v2/ugcPosts" \
  -H "Authorization: Bearer $LINKEDIN_TOKEN" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  -H "Content-Type: application/json" \
  -d '{
    "author": "urn:li:organization:123456",
    "lifecycleState": "PUBLISHED",
    "specificContent": {
      "com.linkedin.ugc.ShareContent": {
        "shareCommentary": {
          "text": "We just shipped Churn Predictor v2.1 with real-time model drift monitoring and multi-region canary deployments. 40% faster inference at p99."
        },
        "shareMediaCategory": "ARTICLE",
        "media": [{
          "status": "READY",
          "originalUrl": "https://blog.example.com/churn-v2-1"
        }]
      }
    },
    "visibility": {
      "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
    }
  }'
```

### Email Campaigns

#### Mailchimp API v3

```bash
# Create a campaign
curl -X POST "https://${DC}.api.mailchimp.com/3.0/campaigns" \
  -H "Authorization: apikey $MAILCHIMP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "regular",
    "recipients": {
      "list_id": "abc123",
      "segment_opts": {
        "saved_segment_id": 456,
        "match": "all"
      }
    },
    "settings": {
      "subject_line": "Churn Predictor v2.1: Real-time Drift Monitoring",
      "preview_text": "Now with A/B testing and 40% faster inference",
      "title": "Churn Predictor v2.1 Release",
      "from_name": "ML Platform Team",
      "reply_to": "ml-team@example.com"
    }
  }'

# Set campaign content with merge tags
curl -X PUT "https://${DC}.api.mailchimp.com/3.0/campaigns/${CAMPAIGN_ID}/content" \
  -H "Authorization: apikey $MAILCHIMP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<h1>Churn Predictor v2.1</h1><p>Hi *|FNAME|*,</p><p>We just released <strong>v2.1</strong> with real-time drift monitoring and A/B testing support.</p><p><a href=\"https://docs.example.com/churn-v2-1\">View full changelog →</a></p>"
  }'

# Send campaign
curl -X POST "https://${DC}.api.mailchimp.com/3.0/campaigns/${CAMPAIGN_ID}/actions/send" \
  -H "Authorization: apikey $MAILCHIMP_API_KEY"
```

#### SendGrid — Dynamic Templates

```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Personalization
import os

sg = SendGridAPIClient(os.environ["SENDGRID_API_KEY"])

# Segment-based sending with dynamic template
segments = {
    "active_users": {"template_id": "d-abc123", "list_id": "list_1"},
    "new_signups":  {"template_id": "d-def456", "list_id": "list_2"},
}

for segment_name, config in segments.items():
    message = Mail(
        from_email="ml-team@example.com",
        subject="Churn Predictor v2.1 is live!",
    )
    message.template_id = config["template_id"]
    message.dynamic_template_data = {
        "version": "v2.1",
        "changelog_url": "https://docs.example.com/churn-v2-1",
        "segment": segment_name,
    }
    # Add segment-specific list
    personalization = Personalization()
    personalization.add_to(ToList(config["list_id"]))
    message.add_personalization(personalization)
    response = sg.send(message)
    print(f"{segment_name}: {response.status_code}")
```

#### Klaviyo — Event-Triggered Flows

```bash
# Trigger a flow event (e.g., "New Version Released")
curl -X POST "https://a.klaviyo.com/api/v2/list/${LIST_ID}/subscribe" \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"$KLAVIYO_API_KEY\",
    \"profiles\": [{
      \"email\": \"user@example.com\",
      \"properties\": {
        \"\$event_id\": \"version_released_v2.1\",
        \"product_version\": \"v2.1\",
        \"changelog_url\": \"https://docs.example.com/churn-v2-1\"
      }
    }]
  }"
```

### Status Page Automation

#### Atlassian Statuspage API

```bash
# Update component status on deploy start
curl -X PATCH "https://api.statuspage.io/v1/pages/${PAGE_ID}/components/${COMPONENT_ID}" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"component": {"status": "under_maintenance"}}'

# Create incident on deploy failure
curl -X POST "https://api.statuspage.io/v1/pages/${PAGE_ID}/incidents" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "incident": {
      "name": "Degraded prediction latency",
      "status": "investigating",
      "impact_override": "minor",
      "body": "We are investigating elevated p99 latency on the churn-predictor endpoint.",
      "components": {"abc123": "degraded_performance"}
    }
  }'

# Resolve component after successful deploy
curl -X PATCH "https://api.statuspage.io/v1/pages/${PAGE_ID}/components/${COMPONENT_ID}" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"component": {"status": "operational"}}'

# Resolve incident
curl -X PATCH "https://api.statuspage.io/v1/pages/${PAGE_ID}/incidents/${INCIDENT_ID}" \
  -H "Authorization: OAuth $STATUSPAGE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"incident": {"status": "resolved", "body": "Deploy completed. Latency restored to normal."}}'
```

#### Cachet (Self-Hosted)

```bash
# Update component status
curl -X PUT "https://status.example.com/api/v1/components/${COMPONENT_ID}" \
  -H "X-Cachet-Token: $CACHET_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": 2}'  # 1=Operational, 2=Performance Issues, 3=Partial Outage, 4=Major Outage

# Create incident
curl -X POST "https://status.example.com/api/v1/incidents" \
  -H "X-Cachet-Token: $CACHET_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Churn Predictor — Elevated Latency",
    "message": "p99 prediction latency increased from 150ms to 450ms. Investigating.",
    "status": 1,
    "visible": 1,
    "component_id": 5,
    "component_status": 2
  }'
```

### Marketing Pipeline Integration

The marketing pipeline runs as a CI workflow stage triggered on release. Steps execute sequentially with retry and failure notification.

```
Release Published
       │
       ▼
┌──────────────────┐
│ Generate Release │  AI-summarized from commits
│     Notes        │
└────────┬─────────┘
         ▼
┌──────────────────┐
│ Update Changelog │  Append to CHANGELOG.md, push to repo
└────────┬─────────┘
         ▼
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│ Create Social    │   │ Queue Email      │   │ Update Status    │
│ Posts (parallel) │   │ Campaign         │   │ Page             │
│ • Twitter/X      │   │ • Mailchimp      │   │ • Operational    │
│ • LinkedIn       │   │ • SendGrid       │   │ • Post-incident  │
│ • Buffer         │   │ • Klaviyo        │   │   note           │
└────────┬─────────┘   └────────┬─────────┘   └────────┬─────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                ▼
                    ┌──────────────────┐
                    │  Notify Slack     │
                    │  on completion    │
                    └──────────────────┘
```

### Complete Marketing Workflow (GitHub Actions)

```yaml
name: Marketing Release Pipeline

on:
  release:
    types: [published]
  workflow_dispatch:
    inputs:
      version:
        description: 'Version to promote (e.g., v2.1.0)'
        required: true

env:
  VERSION: ${{ github.event.release.tag_name || inputs.version }}

jobs:
  generate-release-notes:
    runs-on: ubuntu-latest
    outputs:
      notes: ${{ steps.summarize.outputs.notes }}
      changelog_url: ${{ steps.summarize.outputs.changelog_url }}
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - run: pip install anthropic
      - id: summarize
        run: |
          NOTES=$(python scripts/generate_release_notes.py)
          echo "notes<<EOF" >> "$GITHUB_OUTPUT"
          echo "$NOTES" >> "$GITHUB_OUTPUT"
          echo "EOF" >> "$GITHUB_OUTPUT"
          echo "changelog_url=https://docs.example.com/changelog#$VERSION" >> "$GITHUB_OUTPUT"
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

  update-changelog:
    needs: generate-release-notes
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Move Unreleased to versioned section
        run: |
          sed -i "s/## \[Unreleased\]/## [Unreleased]\n\n## [$VERSION] - $(date +%Y-%m-%d)/" CHANGELOG.md
          git config user.name "release-bot"
          git config user.email "bot@example.com"
          git add CHANGELOG.md
          git commit -m "chore: update changelog for $VERSION"
          git push
      - uses: softprops/action-gh-release@v2
        with:
          tag_name: ${{ env.VERSION }}
          body: ${{ needs.generate-release-notes.outputs.notes }}

  social-media:
    needs: generate-release-notes
    runs-on: ubuntu-latest
    strategy:
      max-parallel: 3
      matrix:
        platform: [twitter, linkedin, buffer]
    steps:
      - name: Post to ${{ matrix.platform }}
        run: |
          NOTES="${{ needs.generate-release-notes.outputs.notes }}"
          CHANGELOG="${{ needs.generate-release-notes.outputs.changelog_url }}"

          case "${{ matrix.platform }}" in
            twitter)
              curl -X POST "https://api.twitter.com/2/tweets" \
                -H "Authorization: Bearer ${{ secrets.TWITTER_BEARER_TOKEN }}" \
                -H "Content-Type: application/json" \
                -d "{\"text\": \"🚀 $VERSION is live! Real-time drift monitoring + canary deploys. $CHANGELOG\"}"
              ;;
            linkedin)
              curl -X POST "https://api.linkedin.com/v2/ugcPosts" \
                -H "Authorization: Bearer ${{ secrets.LINKEDIN_TOKEN }}" \
                -H "X-Restli-Protocol-Version: 2.0.0" \
                -H "Content-Type: application/json" \
                -d "{\"author\": \"urn:li:organization:${{ secrets.LINKEDIN_ORG_ID }}\", \"lifecycleState\": \"PUBLISHED\", \"specificContent\": {\"com.linkedin.ugc.ShareContent\": {\"shareCommentary\": {\"text\": \"$VERSION is live! $CHANGELOG\"}, \"shareMediaCategory\": \"ARTICLE\", \"media\": [{\"status\": \"READY\", \"originalUrl\": \"$CHANGELOG\"}]}}, \"visibility\": {\"com.linkedin.ugc.MemberNetworkVisibility\": \"PUBLIC\"}}"
              ;;
            buffer)
              curl -X POST "https://api.bufferapp.com/1/updates/create.json" \
                -H "Authorization: Bearer ${{ secrets.BUFFER_ACCESS_TOKEN }}" \
                -d "text=🚀 $VERSION is live: real-time drift monitoring + canary deploys. $CHANGELOG&profile_ids[]=${{ secrets.BUFFER_PROFILE_ID }}"
              ;;
          esac

  email-campaign:
    needs: generate-release-notes
    runs-on: ubuntu-latest
    strategy:
      max-parallel: 3
      matrix:
        segment:
          - { name: active_users, list_id: "abc123", template_id: "d-template1" }
          - { name: churned_users, list_id: "def456", template_id: "d-template2" }
          - { name: new_signups, list_id: "ghi789", template_id: "d-template3" }
    steps:
      - name: Queue email for ${{ matrix.segment.name }}
        run: |
          curl -X POST "https://${{ secrets.MAILCHIMP_DC }}.api.mailchimp.com/3.0/campaigns" \
            -H "Authorization: apikey ${{ secrets.MAILCHIMP_API_KEY }}" \
            -H "Content-Type: application/json" \
            -d "{
              \"type\": \"regular\",
              \"recipients\": {
                \"list_id\": \"${{ matrix.segment.list_id }}\"
              },
              \"settings\": {
                \"subject_line\": \"Churn Predictor $VERSION: What's New\",
                \"title\": \"Release $VERSION — ${{ matrix.segment.name }}\",
                \"from_name\": \"ML Platform Team\",
                \"reply_to\": \"ml-team@example.com\",
                \"template_id\": \"${{ matrix.segment.template_id }}\"
              }
            }"

  status-page:
    needs: generate-release-notes
    runs-on: ubuntu-latest
    steps:
      - name: Update status page — deploy started
        run: |
          curl -X PATCH "https://api.statuspage.io/v1/pages/${{ secrets.STATUSPAGE_PAGE_ID }}/components/${{ secrets.STATUSPAGE_COMPONENT_ID }}" \
            -H "Authorization: OAuth ${{ secrets.STATUSPAGE_API_KEY }}" \
            -H "Content-Type: application/json" \
            -d '{"component": {"status": "under_maintenance"}}'

          curl -X POST "https://api.statuspage.io/v1/pages/${{ secrets.STATUSPAGE_PAGE_ID }}/incidents" \
            -H "Authorization: OAuth ${{ secrets.STATUSPAGE_API_KEY }}" \
            -H "Content-Type: application/json" \
            -d "{
              \"incident\": {
                \"name\": \"Scheduled: Deploying $VERSION\",
                \"status\": \"investigating\",
                \"impact_override\": \"maintenance\",
                \"body\": \"Rolling out $VERSION with real-time drift monitoring. No downtime expected.\",
                \"components\": {\"${{ secrets.STATUSPAGE_COMPONENT_ID }}\": \"under_maintenance\"}
              }
            }" > incident.json
          echo "INCIDENT_ID=$(jq -r '.id' incident.json)" >> "$GITHUB_ENV"
      - name: Update status page — deploy complete
        run: |
          curl -X PATCH "https://api.statuspage.io/v1/pages/${{ secrets.STATUSPAGE_PAGE_ID }}/components/${{ secrets.STATUSPAGE_COMPONENT_ID }}" \
            -H "Authorization: OAuth ${{ secrets.STATUSPAGE_API_KEY }}" \
            -H "Content-Type: application/json" \
            -d '{"component": {"status": "operational"}}'

          curl -X PATCH "https://api.statuspage.io/v1/pages/${{ secrets.STATUSPAGE_PAGE_ID }}/incidents/${INCIDENT_ID}" \
            -H "Authorization: OAuth ${{ secrets.STATUSPAGE_API_KEY }}" \
            -H "Content-Type: application/json" \
            -d "{\"incident\": {\"status\": \"resolved\", \"body\": \"$VERSION deployed successfully. All systems operational.\"}}"

  notify-completion:
    needs: [social-media, email-campaign, status-page]
    if: always()
    runs-on: ubuntu-latest
    steps:
      - name: Notify Slack on completion
        run: |
          STATUS="${{ contains(needs.*.result, 'failure') && '❌ FAILED' || '✅ SUCCESS' }}"
          curl -X POST "${{ secrets.SLACK_WEBHOOK_URL }}" \
            -H "Content-Type: application/json" \
            -d "{
              \"text\": \"$STATUS: Marketing pipeline for $VERSION\",
              \"attachments\": [{
                \"fields\": [
                  {\"title\": \"Social\", \"value\": \"${{ needs.social-media.result }}\", \"short\": true},
                  {\"title\": \"Email\", \"value\": \"${{ needs.email-campaign.result }}\", \"short\": true},
                  {\"title\": \"Status Page\", \"value\": \"${{ needs.status-page.result }}\", \"short\": true}
                ]
              }]
            }"
