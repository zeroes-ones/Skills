# MCP Server Types

## Filesystem Server

Gives the agent read/write access to scoped directories.

- **Package:** `@modelcontextprotocol/server-filesystem`
- **Transport:** STDIO (local only — never expose filesystem over HTTP)
- **Tools:** `read_file`, `write_file`, `edit_file`, `list_directory`, `search_files`, `get_file_info`, `create_directory`, `move_file`
- **Security:** Scope to explicit directories. Require-approval for writes. Deny delete.

## Database Server (PostgreSQL)

Gives the agent SQL query access to a PostgreSQL database.

- **Package:** `@modelcontextprotocol/server-postgres`
- **Transport:** STDIO (local) or Streamable HTTP (remote)
- **Tools:** `execute_sql`, `list_tables`, `describe_table`
- **Security:** Use a read-only connection string by default. Require-approval for all write queries. Deny DDL. Limit connection pool size.

## Database Server (SQLite)

Gives the agent access to a local SQLite database file.

- **Package:** `@modelcontextprotocol/server-sqlite`
- **Transport:** STDIO (file must be local)
- **Tools:** `execute_sql`, `list_tables`, `describe_table`
- **Security:** Point to a specific `.db` file. Don't allow arbitrary file paths.

## API Gateway Server

Wraps external REST/GraphQL APIs as MCP tools. Custom implementation.

- **Transport:** Streamable HTTP (remote APIs) or STDIO (local proxy)
- **Tools:** Custom — map API endpoints to tool definitions
- **Security:** Handle API auth token management. Implement rate limiting. Sanitize API responses before passing to agent context.

## Memory / Knowledge Graph Server

Persistent memory across agent sessions using a knowledge graph.

- **Package:** `@modelcontextprotocol/server-memory`
- **Transport:** STDIO
- **Tools:** `create_entities`, `create_relations`, `search_nodes`, `open_nodes`, `add_observations`, `delete_entities`
- **Security:** Memory persists across sessions — sensitive data can leak. Implement session-scoped memory where possible.

## Web Search Server (Brave)

Gives the agent web search and content fetching capabilities.

- **Package:** `@modelcontextprotocol/server-brave-search`
- **Transport:** Streamable HTTP (Brave API is remote)
- **Tools:** `brave_web_search`, `brave_local_search`
- **Security:** Search results are untrusted content. Apply content filtering before passing to agent context. Require-approval to prevent automated search loops.

## Web Fetch Server

Fetches and processes web page content for the agent.

- **Package:** `@modelcontextprotocol/server-fetch`
- **Transport:** Streamable HTTP
- **Tools:** `fetch_url`
- **Security:** Fetched content is untrusted. Restrict domains via allowlist. Cap response size to prevent context overflow. Block internal IP ranges (SSRF prevention).
