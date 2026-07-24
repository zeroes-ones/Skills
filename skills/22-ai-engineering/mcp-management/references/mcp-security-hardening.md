# MCP Security Hardening

## Tool Poisoning Defense

Tool poisoning occurs when an MCP server exposes a tool with a benign name that performs malicious actions. Defense requires source code audit and runtime verification.

**Prevention checklist:**
1. Audit MCP server source code before installation
2. Prefer official `@modelcontextprotocol/*` packages
3. Review the full tool list (names + descriptions) before connecting
4. Monitor tool invocation patterns for anomalies
5. Pin MCP server versions, don't auto-update

## Resource Isolation

MCP resources (files, database rows, API responses) flow into the LLM context window. Untrusted resources are prompt injection vectors.

**Hardening pattern:**
```json
{
  "resourcePolicy": {
    "defaultAction": "deny",
    "allowedUriPatterns": [
      "file:///home/user/project/docs/**",
      "postgres://readonly/**"
    ],
    "contentFilter": {
      "stripHiddenInstructions": true,
      "maxResourceSize": 1048576
    }
  }
}
```

- Apply URI pattern whitelisting for all resource access
- Filter resource content for hidden instruction patterns (e.g., `[IGNORE PREVIOUS]`)
- Cap resource size to prevent context window overflow attacks

## OAuth 2.0 for HTTP Transport

Every Streamable HTTP MCP server exposed beyond localhost must use authentication.

```json
{
  "auth": {
    "type": "oauth2",
    "clientId": "${env:MCP_CLIENT_ID}",
    "clientSecret": "${env:MCP_CLIENT_SECRET}",
    "tokenUrl": "https://auth.example.com/oauth/token",
    "scopes": ["mcp:read", "mcp:write"]
  }
}
```

- Never hardcode tokens — use `${env:VAR}` references
- Rotate tokens on a schedule (max 90-day lifetime)
- Use separate tokens per server, not shared credentials

## Filesystem Sandboxing

```json
{
  "name": "filesystem",
  "transport": "stdio",
  "command": "npx",
  "args": ["-y", "@modelcontextprotocol/server-filesystem",
    "/home/user/project/src",
    "/home/user/project/config"
  ],
  "toolAuthorization": {
    "write_file": "require-approval",
    "edit_file": "require-approval",
    "read_file": "allow",
    "list_directory": "allow",
    "search_files": "allow",
    "delete_file": "deny"
  }
}
```

- Never expose `/`, `~`, or system directories
- Require approval for writes, deny destructive operations
