# Index Strategy Patterns

## Index Types

| Type | Use Case | Example |
|------|----------|---------|
| **B-tree** (default) | Equality + range, sorting | `CREATE INDEX idx_email ON users(email)` |
| **Hash** | Equality only (no range/sort) | `CREATE INDEX idx_token ON sessions USING hash(token)` |
| **Partial** | Subset of rows | `CREATE INDEX idx_active ON orders(status) WHERE status = 'active'` |
| **Covering** | Includes all queried columns | `CREATE INDEX idx_cover ON orders(user_id) INCLUDE (total, created_at)` |
| **GIN** | Full-text search, arrays, JSONB | `CREATE INDEX idx_fts ON posts USING gin(to_tsvector('english', body))` |
| **GiST** | Geometric, full-text | `CREATE INDEX idx_geo ON locations USING gist(coordinates)` |
| **BRIN** | Large tables, physical correlation | `CREATE INDEX idx_brin ON events USING brin(created_at)` |

## Index Rules

### Always Index
1. **Primary keys** (automatic)
2. **Foreign keys** — prevents full table scans on JOINs
3. **Columns in WHERE clauses** of frequent queries
4. **Columns in ORDER BY** — avoids filesort
5. **Columns in GROUP BY** — avoids temporary tables

### Never Index
1. **Low-cardinality columns** — boolean, status with 3 values (use partial index instead)
2. **Very wide columns** — TEXT/BLOB unless using expression index
3. **Columns never queried** — adds write overhead with no read benefit
4. **Tables with heavy writes and few reads** — each index slows writes

### Composite Index Strategy

**Column order matters**:
```sql
-- For: WHERE status = 'active' AND created_at > '2024-01-01' ORDER BY created_at
CREATE INDEX idx_status_created ON orders(status, created_at);
-- status first (equality), created_at second (range/sort)
```

**Rule**: Equality columns first, range/sort columns last.

### Index Maintenance
- `REINDEX` — rebuild bloated indexes
- Monitor unused indexes: `pg_stat_user_indexes.idx_scan = 0`
- Monitor duplicate indexes: overlapping left-prefix composites
- `VACUUM ANALYZE` — keep statistics current for query planner

### When NOT to Create an Index
- The table is small (< 10K rows)
- The column is rarely queried
- Write performance is more critical than read performance
- A similar composite index already covers the use case
