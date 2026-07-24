# Multi-Server MCP Routing

## Namespace Prefix Strategy

When multiple MCP servers expose tools with the same name, apply namespace prefixes to disambiguate.

**Pattern:** `{namespace}{separator}{tool_name}`

```json
{
  "routing": {
    "collisionResolution": "namespace-prefix",
    "separator": "__",
    "servers": {
      "filesystem": { "namespace": "fs", "priority": 1 },
      "database": { "namespace": "db", "priority": 2 },
      "memory": { "namespace": "mem", "priority": 3 }
    }
  }
}
```

**Resulting tool names:**
- `fs__read_file`, `fs__write_file`, `fs__list_directory`
- `db__execute_sql`, `db__list_tables`, `db__describe_table`
- `mem__create_entities`, `mem__search_nodes`, `mem__add_observations`

## Collision Detection Algorithm

```
1. For each server, fetch tools/list
2. Build a map: tool_name → [server_names]
3. Any tool_name with len([server_names]) > 1 is a collision
4. If collisions exist, prefixing is mandatory
5. If no collisions, prefixing is optional but recommended for clarity
```

## Priority Ordering for Ambiguous Resolution

When the agent invokes a tool without a prefix and multiple servers could handle it:

```
Priority 1 (highest) → checked first
Priority 2 → checked if priority 1 doesn't have the tool
Priority 3 (lowest) → fallback
```

**Rule:** The agent SHOULD use prefixed tool names. Priority-based resolution is a fallback for unprefixed invocations and SHOULD produce a warning.

## Collision Report Example

```
COLLISION DETECTED: tool "search" exposed by 3 servers
  → filesystem (priority 1): search_files — searches local filesystem
  → memory (priority 3): search_nodes — searches knowledge graph
  → web-search (priority 4): brave_web_search — searches the web

RECOMMENDED: Use prefixed names: fs__search_files, mem__search_nodes, web__brave_web_search
```

## Cross-Platform Notes

- **Claude Code:** Supports namespace prefixes natively via `claude_desktop_config.json`
- **Codex:** Uses `codex.yaml` with `mcp.servers[].prefix` field
- **Cursor:** `.cursor/mcp.json` with `namespace` key per server
- **Gemini CLI:** `.gemini/config.json` with `mcpServers[].toolPrefix`
- **Copilot CLI:** Uses `mcp-config.json` with same schema as above
