# "Is REST Overkill?" Decision Tree

```
Need real-time bidirectional streaming?
├── YES → WebSocket/SSE. REST is wrong here.
└── NO → Multiple client types (web, mobile, third-party)?
    ├── NO and only 1-2 clients, simple CRUD → JSON-RPC is fine. REST adds ceremony.
    └── YES → Do clients need flexible, nested queries (avoid over-fetching)?
        ├── YES → GraphQL. REST N+1 problems will kill you.
        └── NO → Is this internal service-to-service?
            ├── YES → gRPC. Better performance, strongly typed, streaming.
            └── NO → REST. Use REST. It's the right choice.
```

### When to Use Simple JSON-RPC Instead of REST
```
POST /rpc  { "method": "createOrder", "params": {...}, "id": 1 }
```

| Scenario | REST | JSON-RPC |
|----------|------|----------|
| Internal microservices (2-5 services) | ❌ Overkill | ✅ Simple, fast |
| Single client (your own frontend) | ❌ Overkill | ✅ Sufficient |
| Actions/commands > resources | ❌ Verb-mapping pain | ✅ Natural |
| Small team (< 5 eng) | ❌ Too much ceremony | ✅ Ship faster |
| Public API or > 3 clients | ✅ Standard, cacheable | ❌ Not standard |
