---
name: native-module-integration
description: Integrating native C++, Rust, Swift, and C# libraries into Electron, Tauri, and .NET desktop applications — N-API, FFI, prebuilds, cross-platform compilation, and graceful degradation patterns.
author: Sandeep Kumar Penchala
---

# Native Module Integration

Desktop applications often require native code for performance-critical operations (image processing, cryptography, audio/video encoding) or OS-specific APIs not exposed by the framework. This reference covers native module integration across Electron, Tauri, and .NET.

---

## 1. Integration Strategy Decision

```
                    ┌──────────────────────────────────────┐
                    │ START: Native code integration?       │
                    └──────────────────┬───────────────────┘
                                       │
          ┌────────────────────────────▼────────────────────────────┐
          │ What kind of native code?                                │
          └──┬──────────────┬──────────────┬──────────────┬─────────┘
             │              │              │              │
        Existing C/C++  New Rust lib  Swift/ObjC    C#/.NET lib
             │              │              │              │
             ▼              ▼              ▼              ▼
    ┌──────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────┐
    │ N-API/C++    │ │ Tauri      │ │ Electron   │ │ .NET     │
    │ addon OR FFI │ │ command    │ │ native     │ │ P/Invoke │
    │              │ │ (direct)   │ │ addon OR   │ │ OR COM   │
    │              │ │ OR N-API   │ │ child proc │ │ interop  │
    └──────────────┘ └────────────┘ └────────────┘ └──────────┘
```

## 2. Electron: N-API (Node-API)

### 2.1 Why N-API

N-API is the stable ABI for native addons. Unlike `nan` (Native Abstractions for Node.js), N-API addons are **binary-compatible across Node.js and Electron versions.** An addon compiled for Node.js 18 works on Electron 28 without recompilation.

### 2.2 C++ Addon with N-API

```cpp
// native/image-processor.cpp
#include <napi.h>
#include <vips/vips8>

Napi::Value ProcessImage(const Napi::CallbackInfo& info) {
  Napi::Env env = info.Env();

  // Validate arguments
  if (info.Length() < 2) {
    Napi::TypeError::New(env, "Expected (inputPath: string, outputPath: string)")
      .ThrowAsJavaScriptException();
    return env.Null();
  }

  std::string inputPath = info[0].As<Napi::String>().Utf8Value();
  std::string outputPath = info[1].As<Napi::String>().Utf8Value();

  try {
    vips::VImage image = vips::VImage::new_from_file(inputPath.c_str());
    image = image.resize(0.5); // 50% resize

    // Convert to sRGB and save as JPEG
    image.colourspace(VIPS_INTERPRETATION_sRGB)
         .jpegsave(outputPath.c_str());

    return Napi::Boolean::New(env, true);
  } catch (const std::exception& e) {
    Napi::Error::New(env, e.what()).ThrowAsJavaScriptException();
    return env.Null();
  }
}

Napi::Object Init(Napi::Env env, Napi::Object exports) {
  exports.Set("processImage", Napi::Function::New(env, ProcessImage));
  return exports;
}

NODE_API_MODULE(image_processor, Init)
```

### 2.3 Binding Configuration

```json
// binding.gyp
{
  "targets": [{
    "target_name": "image_processor",
    "sources": ["native/image-processor.cpp"],
    "include_dirs": [
      "<!@(node -p \"require('node-addon-api').include\")",
      "/usr/local/include/vips"
    ],
    "libraries": ["-lvips"],
    "defines": ["NAPI_DISABLE_CPP_EXCEPTIONS"],
    "cflags!": ["-fno-exceptions"],
    "cflags_cc!": ["-fno-exceptions"],
    "conditions": [
      ["OS=='mac'", {
        "xcode_settings": {
          "GCC_ENABLE_CPP_EXCEPTIONS": "YES",
          "MACOSX_DEPLOYMENT_TARGET": "10.15"
        }
      }]
    ]
  }]
}
```

### 2.4 Prebuilds for Cross-Platform Distribution

```json
// package.json
{
  "scripts": {
    "prebuild": "prebuildify --napi --strip",
    "prebuild:win": "prebuildify --napi --strip --platform=win32 --arch=x64",
    "prebuild:mac": "prebuildify --napi --strip --platform=darwin --arch=x64",
    "prebuild:mac-arm": "prebuildify --napi --strip --platform=darwin --arch=arm64",
    "prebuild:linux": "prebuildify --napi --strip --platform=linux --arch=x64"
  },
  "binary": {
    "napi_versions": [8]
  }
}
```

### 2.5 Graceful Degradation

```typescript
// renderer/src/native-bridge.ts
let imageProcessor: { processImage: (input: string, output: string) => boolean } | null = null;

try {
  imageProcessor = require('image-processor');
} catch (err) {
  console.warn('Native image processor not available, using WASM fallback');
}

export async function processImage(inputPath: string, outputPath: string): Promise<boolean> {
  if (imageProcessor) {
    return imageProcessor.processImage(inputPath, outputPath);
  }
  // Fallback to WASM implementation
  const wasmModule = await import('./image-processor.wasm');
  return wasmModule.processImage(inputPath, outputPath);
}
```

## 3. Electron: FFI (Foreign Function Interface)

For calling existing system libraries without writing C++:

```typescript
// Using koffi (modern FFI, no compilation needed)
import koffi from 'koffi';

// Load system library
const libc = koffi.load('libc.so.6'); // Linux
// const libc = koffi.load('msvcrt.dll'); // Windows
// const libc = koffi.load('/usr/lib/libSystem.B.dylib'); // macOS

// Define function signature
const getpid = libc.func('int getpid()');

// Call native function
console.log('PID:', getpid());

// Complex example: call ImageMagick via FFI
const libMagick = process.platform === 'win32'
  ? koffi.load('CORE_RL_MagickCore_.dll')
  : process.platform === 'darwin'
    ? koffi.load('/usr/local/lib/libMagickCore-7.Q16HDRI.dylib')
    : koffi.load('libMagickCore-7.Q16HDRI.so');

// Warning: FFI bypasses type safety. Validate ALL inputs and outputs.
```

## 4. Electron: Child Process Isolation

For native code that might crash or has memory leaks:

```typescript
// main.ts — spawn a child process for native processing
import { fork } from 'child_process';
import { join } from 'path';

ipcMain.handle('native:processLargeFile', async (_event, filePath: string) => {
  return new Promise((resolve, reject) => {
    const worker = fork(join(__dirname, 'native-worker.js'));

    worker.on('message', (result) => {
      worker.kill();
      resolve(result);
    });

    worker.on('error', (err) => {
      worker.kill();
      reject(err);
    });

    // Kill if takes too long
    setTimeout(() => {
      worker.kill();
      reject(new Error('Native processing timeout'));
    }, 30000);

    worker.send({ filePath });
  });
});
```

```javascript
// native-worker.js — isolated process
const { parentPort } = require('worker_threads');

parentPort.on('message', async ({ filePath }) => {
  try {
    const nativeModule = require('./native-addon.node');
    const result = nativeModule.processFile(filePath);
    parentPort.postMessage({ success: true, result });
  } catch (err) {
    parentPort.postMessage({ success: false, error: err.message });
  }
});
```

## 5. Tauri: Native Rust Integration

### 5.1 Direct Rust Commands

Tauri's primary advantage — native code IS the backend:

```rust
// src-tauri/src/image_processor.rs
use image::{DynamicImage, ImageFormat};
use std::path::PathBuf;

#[tauri::command]
pub async fn process_image(
    app: tauri::AppHandle,
    input_filename: String,
    width: u32,
    height: u32,
) -> Result<String, String> {
    // Resolve path within app data directory
    let app_dir = app.path().app_data_dir()
        .map_err(|e| e.to_string())?;

    let input_path = app_dir.join(&input_filename);
    let output_filename = format!("thumb_{}", input_filename);
    let output_path = app_dir.join(&output_filename);

    // Process image with the `image` crate (pure Rust, no C deps)
    let img = image::open(&input_path)
        .map_err(|e| format!("Cannot open image: {}", e))?;

    let thumbnail = img.resize_exact(width, height,
        image::imageops::FilterType::Lanczos3);

    thumbnail.save_with_format(&output_path, ImageFormat::Jpeg)
        .map_err(|e| format!("Cannot save: {}", e))?;

    Ok(output_filename)
}
```

### 5.2 Calling External C Libraries from Tauri

```rust
// src-tauri/src/ffi_bridge.rs
use std::ffi::{CStr, CString};
use std::os::raw::c_char;

// Link to external C library
#[link(name = "myclib")]
extern "C" {
    fn myclib_process(data: *const c_char) -> *mut c_char;
    fn myclib_free(ptr: *mut c_char);
}

#[tauri::command]
pub fn call_external_lib(input: String) -> Result<String, String> {
    let c_input = CString::new(input)
        .map_err(|e| e.to_string())?;

    // SAFETY: We trust the external library and manage memory
    unsafe {
        let result_ptr = myclib_process(c_input.as_ptr());
        if result_ptr.is_null() {
            return Err("External library returned null".into());
        }
        let result = CStr::from_ptr(result_ptr)
            .to_string_lossy()
            .into_owned();
        myclib_free(result_ptr);
        Ok(result)
    }
}
```

## 6. .NET WPF/MAUI: P/Invoke & COM

### 6.1 P/Invoke (Platform Invoke)

```csharp
using System.Runtime.InteropServices;

public static class NativeMethods
{
    // Windows kernel32
    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern IntPtr GetModuleHandle(string lpModuleName);

    // User32 for window management
    [DllImport("user32.dll")]
    public static extern bool SetWindowPos(
        IntPtr hWnd,
        IntPtr hWndInsertAfter,
        int X, int Y, int cx, int cy,
        uint uFlags);

    // Shell32 for file operations
    [DllImport("shell32.dll", CharSet = CharSet.Auto)]
    public static extern bool ShellExecuteEx(ref SHELLEXECUTEINFO lpExecInfo);
}

// Usage with proper error handling
public void BringToFront(IntPtr hwnd)
{
    const uint SWP_NOMOVE = 0x0002;
    const uint SWP_NOSIZE = 0x0001;
    const uint SWP_SHOWWINDOW = 0x0040;

    if (!NativeMethods.SetWindowPos(
        hwnd, new IntPtr(-1), // HWND_TOPMOST
        0, 0, 0, 0,
        SWP_NOMOVE | SWP_NOSIZE | SWP_SHOWWINDOW))
    {
        int error = Marshal.GetLastWin32Error();
        throw new Win32Exception(error);
    }
}
```

### 6.2 COM Interop

```csharp
// Using Windows COM components
[ComImport]
[Guid("43826D1E-E718-42EE-BC55-A1E261C37BFE")]
[InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
internal interface IShellItem
{
    void BindToHandler(IntPtr pbc, ref Guid bhid, ref Guid riid, out IntPtr ppv);
    // ... other methods
}

// Initialize COM for desktop apps
[STAThread]
static void Main()
{
    // STAThread is required for most COM interop in WPF
    // WPF Application.Run() handles the message pump
}
```

## 7. Cross-Platform Compilation

### 7.1 GitHub Actions Matrix for Native Modules

```yaml
name: Build Native Modules
on: [push]

jobs:
  prebuild:
    strategy:
      matrix:
        include:
          - os: macos-13
            target: darwin-x64
          - os: macos-14
            target: darwin-arm64
          - os: windows-2022
            target: win32-x64
          - os: ubuntu-22.04
            target: linux-x64

    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4

      - name: Install build dependencies
        if: runner.os == 'Linux'
        run: sudo apt-get install -y libvips-dev

      - name: Install build dependencies (macOS)
        if: runner.os == 'macOS'
        run: brew install vips

      - run: npm ci
      - run: npx prebuildify --napi --strip --platform=${{ matrix.target }}

      - uses: actions/upload-artifact@v4
        with:
          name: prebuilds-${{ matrix.target }}
          path: prebuilds/
```

### 7.2 Runtime Loading with Platform Detection

```typescript
// Load the correct prebuild for the current platform
import { arch, platform } from 'os';

function loadNativeModule(moduleName: string) {
  const platformMap: Record<string, string> = {
    win32: 'win32',
    darwin: 'darwin',
    linux: 'linux',
  };

  const archMap: Record<string, string> = {
    x64: 'x64',
    arm64: 'arm64',
  };

  const target = `${platformMap[platform()]}-${archMap[arch()]}`;
  const prebuildPath = `@myapp/${moduleName}-${target}`;

  try {
    return require(prebuildPath);
  } catch (err) {
    console.error(`Native module ${moduleName} not available for ${target}`);
    return null;
  }
}
```

## 8. Security Considerations

- **Never load native modules from user-writable directories.** Attackers can replace the .node/.dll/.dylib with malicious code.
- **Validate all inputs at the native boundary.** Buffer overflows in C/C++ are the #1 security vulnerability in native addons.
- **Use `--napi` for Electron addons.** Ensures ABI stability and reduces attack surface from version-specific APIs.
- **Sandbox native processing.** Run in a child process or utility process so a segfault doesn't take down the entire app.
- **Code-sign native binaries.** On macOS, `.node` files loaded by Electron must be signed by the same Developer ID as the app.
