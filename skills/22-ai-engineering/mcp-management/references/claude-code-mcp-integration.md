# Claude Code MCP Integration

## Configuration File: `claude_desktop_config.json`

Located at:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/projects"]
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost/mydb"]
    },
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "${BRAVE_API_KEY}"
      }
    }
  }
}
```

## Claude Code-Specific Patterns

1. **No namespace prefixing built-in** — Claude Code registers tools by server name automatically. If two servers expose `search`, Claude Code prefixes them as `filesystem__search` and `brave-search__search` using the server key as the namespace.

2. **Tool approval is global, not per-server** — Claude Code's `/permissions` command sets allow/deny per tool name, not per server. Use unique tool names or rely on the automatic server-name prefixing.

3. **Reload config without restart** — Use `/mcp` command in Claude Code to reload MCP server configurations without restarting the application.

4. **Environment variable resolution** — Claude Code resolves `${VAR}` syntax in config at server startup. Variables must be set in the shell that launched Claude Code.

5. **STDIO process management** — Claude Code manages server processes automatically: spawns on first use, keeps alive during session, terminates on app close. No manual process management needed.

## Testing MCP in Claude Code

```
/mcp              # List all connected MCP servers and their status
/mcp reload       # Reload MCP configuration
/permissions      # View and edit tool permission settings
```

## Common Claude Code MCP Issues

- **Server not appearing:** Check JSON syntax in `claude_desktop_config.json`. Trailing commas break JSON.
- **BRAVE_API_KEY not found:** Set `export BRAVE_API_KEY=...` in your shell profile, then restart Claude Code.
- **Tool not available:** Run `/mcp` to verify the server is connected and tools are registered.
- **Permission denied repeatedly:** Use `/permissions` to set the tool to "Allow" permanently.
