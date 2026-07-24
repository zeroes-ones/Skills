# Shallow Module Detection

## Detection Patterns

### 1. Pass-Through Module
**Signature:** Every public method is a single delegation call to another module. Zero transformation, zero validation, zero decision logic.
**Detection:** `grep -A2 "public " Module.java | grep -c "return .*\."` — if count equals public method count, it's a pass-through.
**Action:** Delete. Update callers to use the dependency directly.

### 2. Trivial Wrapper
**Signature:** Module wraps a library or external API with zero behavior added. Just renames methods or shuffles parameters.
**Detection:** Compare public methods to wrapped library's methods — if they're 1:1, it's a trivial wrapper.
**Action:** Delete, unless the wrapper serves as an anti-corruption layer for an unstable dependency.

### 3. Config Pass-Through
**Signature:** A class with 20+ fields, each with a public getter/setter. Zero behavior — just a data bucket with ceremony.
**Detection:** Count `getX()`/`setX()` pairs. If they constitute >80% of public methods and there are no behavior methods, it's a config pass-through.
**Action:** Replace with a plain data object, configuration record, or properties map.

### 4. Excessive Getters/Setters
**Signature:** Module exposes internal state through getters/setters rather than behavior methods. Callers pull data out, operate on it, push it back.
**Detection:** `grep -c "get\|set" Module.java | awk '$1 > 5'` — more than 5 getters/setters is a smell.
**Action:** Identify what callers do with the data. Add behavior methods that do it for them inside the module.

### 5. God Class Light
**Signature:** Module has 15+ public methods across unrelated concerns. High interface cost, but each method is thin.
**Detection:** Public method count > 15 AND average method length < 5 lines.
**Action:** Split along concern boundaries. Each split module should have depth > 1.0 independently.
