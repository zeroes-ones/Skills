# Build System Taxonomy

## Task-Based Build Systems

Task-based systems define WHAT to do, not WHAT artifacts to produce. The build author specifies commands to execute.

| System | Language Focus | Strengths | Weaknesses |
|--------|---------------|-----------|------------|
| Make | C/C++ (historically) | Universal, simple model, battle-tested | Manual dependency tracking, non-hermetic by default |
| Ninja | Any (assembly-level) | Extremely fast, designed as build output target | Not human-writable, requires generator |
| Just | Polyglot | Modern command runner, simple syntax | No built-in caching, limited dependency tracking |
| Task | Polyglot | YAML-based, cross-platform | Young ecosystem, limited integrations |

Task-based systems scale DOWN well (personal projects, small teams). They fail at scale because dependency correctness is the author's responsibility.

## Artifact-Based Build Systems

Artifact-based systems define WHAT artifacts to produce and their dependencies. The build system derives the execution plan.

| System | Creator | Language Support | Key Differentiator |
|--------|---------|-----------------|-------------------|
| Bazel | Google | C++, Java, Python, Go, Rust, JS, +20 more | Largest ecosystem, Google-scale proven, Bzlmod |
| Buck2 | Meta | C++, Java, Python, Rust, OCaml | Rust daemon performance, materialized file system |
| Pants | Toolchain Labs/Community | Python, Java, Scala, Go, Shell | Simpler than Bazel, strong Python support |
| Please | Thought Machine | Go, Python, Java, C++ | Simpler mental model, fast to adopt |

Artifact-based systems scale UP (50+ engineers, monorepos, multi-language). They cost more at small scale due to learning curve and maintenance overhead.

## Convention-Based Build Systems

Convention-based systems derive the build graph from project structure conventions.

| System | Language | Convention |
|--------|----------|------------|
| Cargo | Rust | Cargo.toml defines crate, src/ layout |
| Go build | Go | go.mod + package directory structure |
| Maven | Java (JVM) | pom.xml + src/main/java layout |
| Gradle | Java, Kotlin, Groovy | build.gradle + convention plugins |

Convention-based systems work within their language ecosystem. They struggle with cross-language builds — exactly where artifact-based systems excel.
