# MCP Transport Configurations

## STDIO Transport (Local Process)

Used when the MCP server runs on the same machine as the agent. The agent spawns the server as a child process and communicates over stdin/stdout with JSON-RPC 2.0.

```json
{
  "servers": [{
    "name": "filesystem",
    "transport": "stdio",
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"],
    "env": {
      "HOME": "${env:HOME}"
    }
  }]
}
```

**When to use:** Local filesystem access, SQLite databases, local tools, CLI wrappers.
**Security:** Process runs as the same user as the agent. Scope directories, never expose root.

## Streamable HTTP Transport (Remote)

The MCP server exposes an HTTP endpoint. Client sends JSON-RPC 2.0 requests via POST. Optional SSE endpoint for server-to-client streaming.

```json
{
  "servers": [{
    "name": "database",
    "transport": "streamable-http",
    "url": "https://mcp.internal.example.com/mcp",
    "auth": {
      "type": "bearer",
      "token": "${env:MCP_DB_TOKEN}"
    },
    "headers": {
      "X-Request-ID": "${uuid}"
    }
  }]
}
```

**When to use:** Remote services, shared infrastructure, multi-tenant deployments.
**Security:** Always use OAuth 2.0 bearer tokens or mTLS. Never expose without auth.

## Streamable HTTP + SSE (Streaming)

Same as Streamable HTTP but with a parallel SSE connection for server-initiated events.

```json
{
  "servers": [{
    "name": "long-running-task",
    "transport": "streamable-http",
    "url": "https://mcp.internal.example.com/mcp",
    "sseUrl": "https://mcp.internal.example.com/mcp/sse",
    "auth": {
      "type": "bearer",
      "token": "${env:MCP_TASK_TOKEN}"
    }
  }]
}
```

**When to use:** Long-running tools, progress updates, real-time notifications.
**Security:** SSE connection needs same auth as the main HTTP endpoint.
