# Build Rules and Extensibility

## Starlark: Bazel's Extension Language

Starlark is a subset of Python designed for build rule definition. It is deterministic, hermetic, and parallel-safe.

```python
# my_rule.bzl
def _my_rule_impl(ctx):
    # ctx.attr: user-specified attributes
    # ctx.file: output file handle
    # ctx.actions: build actions (run, write, expand_template)

    output = ctx.actions.declare_file(ctx.attr.name + ".txt")
    ctx.actions.write(
        output = output,
        content = "Hello, {}!".format(ctx.attr.greeting),
    )
    return [DefaultInfo(files = depset([output]))]

my_rule = rule(
    implementation = _my_rule_impl,
    attrs = {
        "greeting": attr.string(default = "World"),
    },
)
```

## Providers: Passing Information Between Rules

```python
# Define a provider (typed struct for rule outputs)
ColorInfo = provider(fields = ["color", "shape"])

def _producer_impl(ctx):
    return [ColorInfo(color = "red", shape = "circle")]

def _consumer_impl(ctx):
    # Access provider from dependency
    info = ctx.attr.dep[ColorInfo]
    # Use info.color, info.shape
```

## Custom Toolchains

```python
# Define a toolchain type
my_toolchain_type = toolchain_type(name = "my_toolchain_type")

# Register toolchain implementations
toolchain(
    name = "my_toolchain_linux",
    toolchain_type = ":my_toolchain_type",
    exec_compatible_with = ["@platforms//os:linux"],
    target_compatible_with = ["@platforms//os:linux"],
    toolchain = ":my_tool_linux",
)
```

## When to Write a Custom Rule vs Macro

- **Macro** (function in .bzl): combines existing rules. No new behavior. Simpler, easier to test.
- **Custom rule**: defines new build actions. Needed when you need to run tools, generate files, or define new providers.

Rule of thumb: Start with a macro. Graduate to a custom rule only when macros can't express the behavior.
