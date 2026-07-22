# C4 Model Guide

author: Sandeep Kumar Penchala

## Overview

The C4 model is a hierarchical set of diagrams for describing software architecture at four levels of abstraction: **Context**, **Container**, **Component**, and **Code**. Created by Simon Brown, it solves the problem of architecture diagrams that are either too high-level (boxes and lines with no detail) or too low-level (UML class diagrams that only developers understand). C4 gives each audience exactly the level of detail they need.

## When to Use Each Level

| Level | Audience | Purpose | Detail |
|-------|----------|---------|--------|
| **System Context** | Everyone (business, execs, devs) | "What does this system do, and who uses it?" | System as single box, external actors, high-level interactions |
| **Container** | Technical leadership, ops, devs | "What are the deployable runtime units?" | Web apps, services, databases, message brokers, file systems |
| **Component** | Senior devs, architects within a team | "How is this container structured internally?" | Modules, packages, key classes, their responsibilities and interfaces |
| **Code** | Developers working on the codebase | "How is this component implemented?" | Class diagrams, ERDs, function signatures — usually auto-generated |

## Level 1: System Context Diagram

### Purpose
Show the system as a single box in the center, surrounded by its users (personas) and external systems it depends on. The goal is answering: *What is this system? Who uses it? What does it depend on externally?*

### What to Include
- **System**: One box representing the entire system being designed. Label it with the system name.
- **Actors** (people): Roles like Customer, Admin, Support Agent. Use stick figures or person icons.
- **External Systems**: Third-party APIs (Stripe, SendGrid, Auth0), partner systems, legacy monoliths. Use different-colored boxes.
- **Relationships**: Labeled arrows showing intent, not protocol. "Views orders" not "HTTP GET /orders". "Sends payment" not "POSTs to Stripe API".

### Example: E-Commerce Platform

```
┌─────────────┐          ┌─────────────────┐          ┌─────────────┐
│   Customer   │─────────▶│                 │◀─────────│    Admin     │
└─────────────┘  Browses │  E-Commerce     │  Manages └─────────────┘
                  Orders   │  Platform       │  Inventory
┌─────────────┐  Pays     │                 │          ┌─────────────┐
│   Payment    │◀────────│                 │─────────▶│  Warehouse   │
│   Gateway    │          └─────────────────┘  Ships   │   System     │
└─────────────┘                    │                    └─────────────┘
                                   │ Sends
                                   ▼
                          ┌─────────────────┐
                          │   Email Service │
                          │   (SendGrid)    │
                          └─────────────────┘
```

### Anti-Patterns
- Adding technology choices (Kubernetes, AWS, PostgreSQL) — that belongs in Container level.
- Showing internal components or databases — too much detail.
- Omitting the human actors — the system exists for people, show them.
- Using protocol-specific labels (REST, gRPC, HTTPS) — use intent-based labels.

## Level 2: Container Diagram

### Purpose
Show the high-level technology choices and how major runtime units communicate. A "container" is anything that executes code or stores data: a web application, a mobile app, a database, a file system, a message broker, a serverless function, a cron job.

### What to Include
- **Containers**: Each is a separately deployable/runnable unit. Name describes its role: "Web Application", "Order Service", "Product Database", "Redis Cache".
- **Technology**: Under each container name, specify the tech: "React SPA", "Go + Gin", "PostgreSQL 16", "Redis 7".
- **Communication**: Label arrows with protocol and intent: "JSON/HTTPS [REST]", "gRPC [protobuf]", "Binary/TCP [Redis Protocol]".
- **Boundary**: A dashed box around the entire system to separate internal from external.

### Example: E-Commerce Containers

```
┌──────────────────────────────────────────────────────────────────┐
│  E-Commerce Platform                                              │
│                                                                   │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐      │
│  │   Web App    │────▶│  API Gateway │────▶│ Order Service│      │
│  │   React SPA  │     │  Nginx/Kong  │     │  Go + Gin    │      │
│  └──────────────┘     └──────┬───────┘     └──────┬───────┘      │
│                              │                     │              │
│                              ▼                     ▼              │
│                      ┌──────────────┐     ┌──────────────┐       │
│                      │  Auth Service│     │ Order DB     │       │
│                      │  Python+Fast │     │ PostgreSQL   │       │
│                      └──────┬───────┘     └──────────────┘       │
│                             │                                     │
│                             ▼                                     │
│                     ┌──────────────┐     ┌──────────────┐        │
│                     │  Redis Cache │     │  Message      │        │
│                     │  Sessions    │     │  Broker (RMQ) │        │
│                     └──────────────┘     └──────┬───────┘        │
│                                                  │                │
└──────────────────────────────────────────────────┼────────────────┘
                                                   │
                                                   ▼
                                           ┌──────────────┐
                                           │ Email Worker │
                                           │ Python+Celery│
                                           └──────────────┘
```

### Key Decisions to Document
- **Why this database?** PostgreSQL for orders (ACID), MongoDB for product catalog (flexible schema), Redis for sessions (low-latency, TTL).
- **Why this communication?** REST for Web↔API (browser-native), gRPC for internal services (performance, contracts), RabbitMQ for async (reliable delivery, DLQ).
- **Why separate containers?** Auth is a separate container for security isolation. Order Service scales independently.

### Anti-Patterns
- Showing load balancers, firewalls, CDN edges — that's deployment infra, not architecture. Show them only if architecturally significant.
- Too many containers at once — aim for 5-15 containers. If more, split into multiple diagrams.
- Missing data stores — every stateful container needs its data store shown.

## Level 3: Component Diagram

### Purpose
Zoom into a single container and show its internal components: modules, controllers, services, repositories, event handlers. This is the level where team-level architecture decisions live.

### What to Include
- **Components**: Logical groupings of functionality within a container. In Spring: `@Service`, `@Repository`, `@Controller`. In FastAPI: routers, services, repositories. In Go: packages.
- **Responsibilities**: A one-line description of what each component does and what it owns.
- **Interfaces**: The API (method signatures, message contracts, event schemas) each component exposes.
- **Dependencies**: Which components call which, via what mechanism (direct call, event, dependency injection).

### Example: Order Service Components

```
┌────────────────────────────────────────────────────────────────┐
│  Order Service Container (Go + Gin)                             │
│                                                                 │
│  ┌──────────────────┐    ┌──────────────────┐                  │
│  │  OrderHandler    │───▶│  OrderService    │                  │
│  │  (HTTP handlers) │    │  (Business logic)│                  │
│  │  CreateOrder     │    │  ValidateOrder   │                  │
│  │  GetOrder        │    │  CalculateTax    │                  │
│  │  CancelOrder     │    │  ReserveStock    │                  │
│  └──────────────────┘    └────────┬─────────┘                  │
│                                   │                             │
│                    ┌──────────────┼──────────────┐              │
│                    ▼              ▼              ▼              │
│  ┌──────────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │ OrderRepository  │ │ StockClient  │ │ TaxCalculator│       │
│  │ (DB access)      │ │ (gRPC to     │ │ (Strategy     │       │
│  │ Insert,Find,     │ │  Inventory)  │ │  pattern:     │       │
│  │ Update           │ │              │ │  per region)  │       │
│  └────────┬─────────┘ └──────┬───────┘ └──────────────┘       │
│           │                  │                                   │
│           ▼                  ▼                                   │
│  ┌──────────────────┐ ┌──────────────┐                          │
│  │ OrderDB          │ │ Inventory    │                          │
│  │ PostgreSQL       │ │ Service gRPC │                          │
│  └──────────────────┘ └──────────────┘                          │
│                                                                 │
│  ┌──────────────────┐                                           │
│  │ OrderEventPub    │───▶ RabbitMQ Exchange "order.events"      │
│  │ Publish:         │                                           │
│  │ order.created    │                                           │
│  │ order.cancelled  │                                           │
│  └──────────────────┘                                           │
└────────────────────────────────────────────────────────────────┘
```

### Component Design Principles
1. **Single Responsibility**: Each component has one reason to change. `OrderService` orchestrates, not calculates tax.
2. **Interface Segregation**: Components depend on interfaces, not implementations. `StockClient` interface means you can swap implementations.
3. **Dependency Inversion**: High-level modules (OrderService) don't depend on low-level (OrderRepository). Both depend on abstractions.
4. **Ports & Adapters**: External interactions (DB, gRPC, MQ) go through adapter components. Business logic never imports database drivers directly.

## Level 4: Code Diagram

### Purpose
Show the implementation details of a single component: classes, interfaces, functions, database tables. This level is rarely drawn manually — use IDE tooling or documentation generators.

### What to Include (Auto-Generated)
- **UML Class Diagrams**: For complex domain models with inheritance and composition.
- **Entity-Relationship Diagrams**: For database schemas (use SchemaSpy, pgModeler, DBeaver export).
- **Sequence Diagrams**: For complex interactions between objects (PlantUML from code annotations).
- **Package Diagrams**: For module dependencies in large codebases.

### Automation
Use tools, not manual drawing:
- **Java**: Structurizr DSL with `@Component` annotations, auto-generate from code.
- **Python**: `pydeps` for import graphs, `pyreverse` (pylint) for class diagrams.
- **Go**: `go-callvis` for call graphs, `goda` for dependency analysis.
- **TypeScript**: `dependency-cruiser` for module dependency graphs, `madge` for circular dependency detection.

## Diagram Notation

### Standard C4 Shapes
- **Person**: Rounded rectangle, light blue background. Represents a human user.
- **System**: Rounded rectangle, dark blue background. An external or internal system.
- **Container**: Rectangle, different colors per technology (blue=app, green=data, orange=messaging).
- **Component**: Rectangle with component icon.
- **Relationship**: Solid line with arrow, labeled. Dashed line for async/event-based.

### Tooling Options
| Tool | Best For | Learning Curve | Output |
|------|----------|---------------|--------|
| **Structurizr DSL** | Code-first diagrams, version control | Medium | Diagrams + ADRs |
| **PlantUML** | Text-based, CI/CD integration | Low | PNG/SVG from text |
| **Mermaid.js** | Markdown-native, GitHub rendering | Low | SVG in README |
| **draw.io** | Quick sketches, non-technical sharing | Lowest | PNG/XML |
| **Lucidchart** | Team collaboration, templates | Lowest | Cloud-hosted |
| **IcePanel** | C4-native, interactive, team | Low | Interactive web |
| **Ilograph** | Interactive, zoomable architecture | Low | Interactive web |

### Structurizr DSL Example (Recommended for version-controlled architecture)

```
workspace {
    model {
        customer = person "Customer"
        admin = person "Administrator"
        
        ecommerce = softwareSystem "E-Commerce Platform" {
            webapp = container "Web Application" "React SPA"
            api = container "API Gateway" "Nginx + Kong"
            ordersvc = container "Order Service" "Go + Gin"
            orderdb = container "Order Database" "PostgreSQL 16"
        }
        
        payment = softwareSystem "Payment Gateway" "Stripe"
        
        customer -> webapp "Browses products, places orders"
        admin -> webapp "Manages inventory"
        webapp -> api "Makes API calls" "JSON/HTTPS"
        api -> ordersvc "Routes requests" "JSON/HTTPS"
        ordersvc -> orderdb "Reads/writes orders" "SQL/TCP"
        ordersvc -> payment "Processes payments" "JSON/HTTPS"
    }
    
    views {
        systemContext ecommerce {
            include *
        }
        
        container ecommerce {
            include *
        }
    }
}
```

## C4 + ADR Integration

Every C4 diagram should be accompanied by Architecture Decision Records that explain why the structure looks the way it does:

- **Context Diagram → ADR-001**: Why this system boundary? What was the scope decision?
- **Container Diagram → ADR-002-005**: Why PostgreSQL over MongoDB? Why gRPC over REST for internal calls? Why separate Auth service?
- **Component Diagram → ADR-006-010**: Why strategy pattern for tax calculation? Why event-driven for order status changes?

Link diagrams to ADRs by filename convention: `adr/004-postgresql-for-orders.md` references `diagrams/container-level.puml`.

## Review Checklist

- [ ] Context diagram shows all external actors and systems — nothing internal leaked
- [ ] Container diagram shows all deployable units with technology choices — no infrastructure detail (load balancers, VPCs, subnets)
- [ ] Component diagram for complex containers only — don't diagram CRUD wrappers
- [ ] Every arrow has a meaningful label (intent, not protocol at Context level)
- [ ] Diagrams stored as text (PlantUML/Structurizr DSL) in version control, not binary images
- [ ] Each diagram has a corresponding ADR explaining key decisions visible in the diagram
- [ ] Diagrams are renderable in CI/CD pipeline (auto-generate PNG/SVG on commit)
