# Multi-Language Build Coordination

## The Polyglot Challenge

Multi-language builds involve different compilers, package managers, and build conventions. The build system must coordinate them.

## Language-Specific Rules (Bazel)

| Language | Rule Set | Example |
|----------|----------|---------|
| C/C++ | rules_cc (built-in) | cc_library, cc_binary, cc_test |
| Java | rules_java (built-in) | java_library, java_binary, java_test |
| Python | rules_python | py_library, py_binary, py_test |
| Go | rules_go | go_library, go_binary, go_test |
| Rust | rules_rust | rust_library, rust_binary, rust_test |
| JavaScript | rules_js | js_library, ts_project |
| Kotlin | rules_kotlin | kt_jvm_library, kt_jvm_binary |

## Protobuf Coordination

```python
# proto_library defines the schema
proto_library(
    name = "user_proto",
    srcs = ["user.proto"],
)

# Generate language-specific bindings
cc_proto_library(name = "user_cc_proto", deps = [":user_proto"])
java_proto_library(name = "user_java_proto", deps = [":user_proto"])
go_proto_library(name = "user_go_proto", proto = ":user_proto")

# Language libraries depend on their proto binding
cc_library(name = "user_service", deps = [":user_cc_proto"])
```

## Cross-Compilation

```bash
# Build for ARM64 from x86_64
bazel build //... --platforms=@platforms//cpu:arm64

# Define custom platform with specific toolchain
platform(
    name = "raspberry_pi",
    constraint_values = [
        "@platforms//cpu:arm64",
        "@platforms//os:linux",
    ],
)
```

## FFI (Foreign Function Interface)

For C/C++ libraries consumed by Python/Go/Rust:
```python
cc_library(
    name = "native_lib",
    srcs = ["lib.cc"],
    hdrs = ["lib.h"],
)

# Rust FFI binding
rust_library(
    name = "wrapper",
    deps = [":native_lib"],
    srcs = ["wrapper.rs"],
)
```
