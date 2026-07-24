# MCP Config Schema (mcp-config.json)

## JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "MCP Configuration",
  "type": "object",
  "required": ["mcpServers"],
  "properties": {
    "mcpServers": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "required": ["transport"],
        "properties": {
          "transport": {
            "enum": ["stdio", "streamable-http", "sse"]
          },
          "command": { "type": "string" },
          "args": { "type": "array", "items": { "type": "string" } },
          "env": { "type": "object" },
          "url": { "type": "string", "format": "uri" },
          "sseUrl": { "type": "string", "format": "uri" },
          "auth": {
            "type": "object",
            "properties": {
              "type": { "enum": ["bearer", "oauth2", "mtls"] },
              "token": { "type": "string" },
              "clientId": { "type": "string" },
              "clientSecret": { "type": "string" },
              "tokenUrl": { "type": "string" }
            }
          },
          "toolAuthorization": {
            "type": "object",
            "additionalProperties": {
              "enum": ["allow", "deny", "require-approval"]
            }
          },
          "resourcePolicy": {
            "type": "object",
            "properties": {
              "defaultAction": { "enum": ["allow", "deny"] },
              "allowedUriPatterns": {
                "type": "array",
                "items": { "type": "string" }
              }
            }
          },
          "namespace": { "type": "string" },
          "priority": { "type": "integer", "minimum": 1 }
        }
      }
    }
  }
}
```

## Complete Example Configuration

```json
{
  "mcpServers": {
    "filesystem": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/project"],
      "toolAuthorization": {
        "read_file": "allow",
        "write_file": "require-approval",
        "list_directory": "allow",
        "search_files": "allow",
        "delete_file": "deny"
      },
      "resourcePolicy": {
        "defaultAction": "deny",
        "allowedUriPatterns": ["file:///home/user/project/**"]
      },
      "namespace": "fs",
      "priority": 1
    },
    "database": {
      "transport": "streamable-http",
      "url": "https://db-mcp.internal.example.com/mcp",
      "auth": {
        "type": "bearer",
        "token": "${env:DB_MCP_TOKEN}"
      },
      "toolAuthorization": {
        "execute_sql": "require-approval",
        "list_tables": "allow",
        "describe_table": "allow"
      },
      "namespace": "db",
      "priority": 2
    }
  },
  "routing": {
    "collisionResolution": "namespace-prefix",
    "separator": "__"
  },
  "security": {
    "denyByDefault": true,
    "auditLogging": true,
    "requireHealthCheck": true
  }
}
```

## Validation Rules

1. `transport: "stdio"` requires `command` and optionally `args`, `env`
2. `transport: "streamable-http"` requires `url` and `auth` (unless localhost)
3. `transport: "sse"` is deprecated — warn but allow for legacy
4. `toolAuthorization` keys must match actual tool names from server
5. `namespace` must be unique across all servers
6. `priority` must be unique — no two servers at same priority
7. Environment variable references (`${env:VAR}`) must resolve at runtime
