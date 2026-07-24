# MCP Diagnostics

## Connection Testing

Test that the MCP server responds to the JSON-RPC 2.0 initialize handshake.

### STDIO Server Test
```bash
# Start the server and send initialize
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"diagnostics","version":"1.0.0"}}}' | npx -y @modelcontextprotocol/server-filesystem /tmp/mcp-test
```

### HTTP Server Test
```bash
curl -X POST https://mcp.example.com/mcp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $MCP_TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"diagnostics","version":"1.0.0"}}}'
```

### Using MCP Inspector
```bash
npx @modelcontextprotocol/inspector
# Opens a web UI to connect to any MCP server, list tools, and test invocations
```

## Tool Listing Validation

After initialize, verify the server exposes expected tools:

```bash
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' | npx -y @modelcontextprotocol/server-filesystem /tmp/mcp-test
```

**Expected output:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "tools": [
      {"name": "read_file", "description": "Read the contents of a file", "inputSchema": {...}},
      {"name": "write_file", "description": "Create or overwrite a file", "inputSchema": {...}}
    ]
  }
}
```

**Diagnostic checks:**
1. Response is valid JSON-RPC 2.0 (has `jsonrpc`, `id`, `result` or `error`)
2. `result.tools` is a non-empty array
3. Each tool has `name`, `description`, and `inputSchema`
4. Tool names match expected list from server documentation

## Resource URI Resolution

Verify resource URIs resolve correctly:

```bash
echo '{"jsonrpc":"2.0","id":3,"method":"resources/list","params":{}}' | npx -y @modelcontextprotocol/server-filesystem /tmp/mcp-test
```

**Common resource URI patterns:**
- Filesystem: `file:///path/to/file.txt`
- Database: `postgres://database/table/schema`
- API: `https://api.example.com/resource`
- Memory: `memory://entities/{id}`

## Common Failure Modes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| `ECONNREFUSED` | Server not running or wrong port | Check process, verify URL/port |
| `JSON parse error` | Server returned non-JSON (HTML error page, stack trace) | Check server logs, verify endpoint |
| `Method not found: initialize` | Not an MCP server — wrong endpoint | Verify URL points to MCP server, not a generic API |
| `Unsupported protocol version` | Version mismatch between client and server | Use matching protocol versions (prefer 2025-03-26) |
| `Tool not found` in tools/list | Server started without that capability | Check server arguments, environment, feature flags |
| `Permission denied` on tool call | Tool authorization blocked it | Check toolAuthorization config, adjust allow/deny |
| Orphaned process after shutdown | Server didn't handle SIGTERM | Add signal handler, use process supervisor |
