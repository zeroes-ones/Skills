# Cross-Agent MCP Patterns

## Claude Code (Anthropic)

- **Config:** `claude_desktop_config.json`
- **Transport:** STDIO, Streamable HTTP
- **Namespace:** Automatic — uses server key as prefix
- **Auth:** Environment variables via `${VAR}` syntax
- **Management:** `/mcp` command for status and reload
- **Permissions:** `/permissions` command, tool-level allow/deny
- **Docs:** https://docs.anthropic.com/en/docs/claude-code/mcp

## Codex (OpenAI)

- **Config:** `codex.yaml` in project root or `~/.codex/config.yaml`
- **Transport:** STDIO, HTTP
- **Namespace:** `mcp.servers[].prefix` field
- **Auth:** Environment variables, `.env` file support
- **Management:** `codex mcp list`, `codex mcp reload`
- **Permissions:** Per-server `approval` field: `auto`, `always-ask`, `never`

## Cursor

- **Config:** `.cursor/mcp.json` in project root
- **Transport:** STDIO, Streamable HTTP
- **Namespace:** `namespace` key per server entry
- **Auth:** `${env:VAR}` syntax, `.cursor/.env` file
- **Management:** Cursor Settings → MCP tab, or command palette "MCP: Restart Servers"
- **Permissions:** Tool-level in MCP settings UI

## Gemini CLI (Google)

- **Config:** `.gemini/config.json` in project root
- **Transport:** STDIO, Streamable HTTP
- **Namespace:** `mcpServers[].toolPrefix`
- **Auth:** `${env:VAR}`, Google Cloud Secret Manager integration
- **Management:** `gemini mcp status`, `gemini mcp restart`
- **Permissions:** `gemini mcp permissions` interactive mode

## Copilot CLI (GitHub)

- **Config:** `mcp-config.json` (project-level or `~/.copilot/`)
- **Transport:** STDIO, Streamable HTTP
- **Namespace:** `namespace` field per server
- **Auth:** `${env:VAR}`, GitHub token inheritance for GitHub-owned MCP servers
- **Management:** `copilot mcp list`, `copilot mcp connect`
- **Permissions:** Tool authorization per server in config

## Portability Checklist

When designing an MCP configuration for multi-agent portability:

1. Use `mcp-config.json` as the canonical file name
2. Include a `$schema` reference for cross-platform validation
3. Use `${env:VAR}` syntax for all secrets (universally supported)
4. Prefer STDIO transport for maximum compatibility
5. Document platform-specific deviations in comments
6. Test the same config on all target platforms before declaring "portable"
7. Keep server implementations platform-agnostic (no agent-specific code)
