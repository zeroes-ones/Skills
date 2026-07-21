# Internal Developer Platform

> **Author:** Sandeep Kumar Penchala

Patterns for building Internal Developer Platforms (IDPs) that enable developer self-service, golden paths, and platform-as-a-product thinking. These patterns support the platform-engineer skill's mission of reducing cognitive load and accelerating delivery.

## IDP Architecture

### Build vs Buy vs Compose

```
Greenfield startup (< 20 engineers) → Buy: use existing tools individually; no IDP needed
Growing (20-100 engineers)           → Compose: Backstage/Port with curated plugins
Enterprise (100+ engineers)          → Build: Custom portal on Backstage/Port with deep integrations
```

### Core IDP Components

```
Internal Developer Platform
├── Developer Portal (Backstage / Port)
│   ├── Software Catalog (all services, APIs, resources)
│   ├── Software Templates (golden path scaffolder)
│   ├── TechDocs (documentation alongside code)
│   └── Plugins (CI/CD status, on-call, cost, SLOs)
├── CI/CD Pipeline (GitHub Actions / GitLab CI / Jenkins)
├── Infrastructure Orchestration (Terraform / Pulumi / Crossplane)
├── GitOps Delivery (ArgoCD / Flux)
├── Observability (Grafana / Datadog / Honeycomb)
├── Secrets Management (Vault / External Secrets)
└── Service Mesh (Istio / Linkerd / Cilium)
```

### Backstage Catalog Entity

```yaml
# catalog-info.yaml — registered in Backstage software catalog
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: order-service
  description: Order management microservice
  annotations:
    github.com/project-slug: myorg/order-service
    backstage.io/techdocs-ref: dir:.
    prometheus.io/alert: OrderServiceHighErrorRate
  tags: ["java", "spring-boot", "orders"]
  links:
    - url: https://order-service.prod.example.com/health
      title: Health Check
      icon: dashboard
spec:
  type: service
  lifecycle: production
  owner: team-checkout
  system: ecommerce-platform
  providesApis:
    - order-api
  dependsOn:
    - component:postgres-orders
    - component:payment-service
```

## Golden Path Templates

### Backstage Scaffolder Template

```yaml
# templates/service-template.yaml
apiVersion: scaffolder.backstage.io/v1beta3
kind: Template
metadata:
  name: spring-boot-service
  title: Spring Boot Microservice
  description: Golden path for creating a new Spring Boot service
spec:
  owner: platform-team
  type: service
  parameters:
    - title: Service Details
      required: ["name", "owner", "javaVersion"]
      properties:
        name:
          title: Service Name
          type: string
          pattern: '^[a-z][a-z0-9-]*$'
        owner:
          title: Owner Team
          type: string
          ui:field: OwnerPicker
        javaVersion:
          title: Java Version
          type: string
          enum: ["17", "21"]
          default: "21"
        includeDatabase:
          title: Include PostgreSQL?
          type: boolean
          default: true
  steps:
    - id: fetch-base
      action: fetch:template
      input:
        url: ./skeleton
        values:
          name: ${{ parameters.name }}
          javaVersion: ${{ parameters.javaVersion }}
    - id: publish
      action: publish:github
      input:
        repoUrl: github.com?owner=myorg&repo=${{ parameters.name }}
        defaultBranch: main
    - id: register
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps.publish.output.repoContentsUrl }}
        catalogInfoPath: /catalog-info.yaml
```

### What a Golden Path Template Provisions

```
Service template provisions:
  1. Repository with canonical structure
  2. Dockerfile (multi-stage, distroless)
  3. CI/CD pipeline (build → test → scan → deploy)
  4. Kubernetes manifests (Deployment, Service, HPA, PDB)
  5. Terraform module for infrastructure (DB, queue, bucket)
  6. Observability (dashboards, alerts, SLO definitions)
  7. Documentation skeleton (ADRs, runbooks, API docs)
  8. Catalog registration in Backstage/Port
```

## Developer Self-Service

### Provision with Terraform/Pulumi

```typescript
// Pulumi — self-service infrastructure as code
import * as aws from "@pulumi/aws";

export function createOrderServiceDatabase(name: string, env: string) {
  const db = new aws.rds.Instance(`${name}-db`, {
    engine: "postgres",
    engineVersion: "16",
    instanceClass: env === "prod" ? "db.t3.medium" : "db.t3.micro",
    allocatedStorage: 20,
    skipFinalSnapshot: env !== "prod",
    tags: { Name: name, Environment: env, CostCenter: "checkout" },
  });

  // Output connection details to Vault
  return {
    host: db.address,
    port: db.port,
    database: name.replace(/-/g, "_"),
  };
}
```

### Deploy with ArgoCD

```yaml
# ApplicationSet — auto-deploy every microservice in a directory
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: microservices
spec:
  generators:
    - git:
        repoURL: https://github.com/myorg/k8s-manifests
        revision: main
        directories:
          - path: apps/*
  template:
    metadata:
      name: '{{ path.basename }}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/k8s-manifests
        path: '{{ path }}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{ path.basename }}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
```

## Platform Maturity Model

| Level | Name | Developer Experience | Infrastructure |
|-------|------|---------------------|---------------|
| 0 | Ticket Ops | File a ticket; wait 3-14 days | Manual provisioning |
| 1 | Scripted | Run a script someone wrote; hope it works | Shell scripts, CloudFormation |
| 2 | Self-Service CI/CD | Push code; pipeline provisions infrastructure | Terraform in CI, basic templates |
| 3 | Platform with Guardrails | Scaffold from template; platform handles everything | Golden paths, policy enforcement |
| 4 | Fully Autonomous | Declare intent; platform figures out the how | Application model, auto-optimization |

### Transition Triggers

```
Level 0 → 1: Wait time > 1 week for infrastructure; engineers frustrated
Level 1 → 2: Scripts frequently break; no one maintains them
Level 2 → 3: Each team builds differently; security/compliance inconsistent
Level 3 → 4: Platform team becomes bottleneck for new capabilities
```

## Platform as a Product

### Developer NPS (Net Promoter Score)

```
Survey questions (quarterly):
  1. How likely are you to recommend our platform to a new team member? (0-10)
  2. How long did it take to go from idea to production on your last feature?
  3. What was the most frustrating part of your last deploy?
  4. What should the platform team stop doing, start doing, continue doing?

Targets:
  - NPS > 50 (Promoters - Detractors as %)
  - Time-to-production < 1 day for standard changes
  - On-call burden < 1 incident per service per week attributable to platform
```

### Platform SLAs

| Capability | SLA | Measurement |
|-----------|-----|-------------|
| Scaffold new service | < 5 min from template | Time from trigger to PR created |
| Deploy to staging | < 10 min from merge | CI pipeline duration |
| Deploy to production | < 30 min from merge | CI + ArgoCD sync time |
| Database provisioning | < 15 min | Terraform apply time |
| Secret availability | < 1 min after creation | Vault to K8s sync interval |

## Abstraction Layers

```
Full abstraction (PaaS-like):
  Developer writes: `platform.yaml` + code
  Platform handles: K8s, networking, DB, monitoring, secrets

Partial abstraction (guided K8s):
  Developer writes: `Deployment` + `Service` from template
  Platform handles: Networking policies, service mesh, cert management

Raw exposure (power users):
  Developer writes: Full K8s manifests
  Platform handles: Admission control, policy enforcement (OPA/Gatekeeper)

Rule: Start with full abstraction. Expose more as teams gain expertise.
       Never expose without guardrails (OPA policies, resource quotas).
```

## Platform Team Topology

```
Platform team anti-patterns:
  ❌ "Platform team builds everything" → Bottleneck; 3-month backlog
  ❌ "Platform team as ticket-takers" → Not scalable; no product mindset
  ❌ "Each team builds their own platform" → Fragmentation; no standards

Target topology (Thinnest Viable Platform):
  ✅ Platform team builds golden paths + guardrails
  ✅ Stream-aligned teams own their services end-to-end
  ✅ Platform team treats developers as customers
  ✅ Enablement over enforcement; self-service over gatekeeping

Staffing ratio: 1 platform engineer per 20-30 stream-aligned engineers
```

This IDP reference implements the platform-engineer skill's vision: treat the platform as a product, measure developer satisfaction, and build golden paths that make the right thing the easy thing.
