# Simplify-Ignore: Code Block Protection

Protects specific code blocks from modification during `/code-simplify` operations.

## How It Works

1. **Marking blocks**: Wrap code you want to protect in special comment markers:

   ```
   // simplify-ignore-start
   func critical_legacy_code() { ... }
   // simplify-ignore-end

   ```

2. **Pre-hook protection**: When the agent reads files, the hook replaces protected block contents with `BLOCK_<N>_PROTECTED` placeholders, preventing the agent from seeing (and thus modifying) protected code.

3. **Language support**: Works with any language that supports line comments:
   - `// simplify-ignore-start` / `// simplify-ignore-end` — JavaScript, TypeScript, Go, Rust, Java, C, C++
   - `# simplify-ignore-start` / `# simplify-ignore-end` — Python, Ruby, Shell, YAML
   - `-- simplify-ignore-start` / `-- simplify-ignore-end` — SQL, Lua, Haskell

## When to Use

- Legacy code paths that work but are fragile
- Certified/audited compliance code that cannot be changed
- Performance-critical sections where "simplification" might break optimizations
- Vendor SDK wrappers with known quirks
- Auto-generated code that should not be manually edited
