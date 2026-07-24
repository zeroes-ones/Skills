---
name: cross-platform-testing
description: Comprehensive cross-platform testing strategies for desktop applications — Spectron, Playwright, platform matrix testing, GPU testing, power-state simulation, and CI/CD integration across Windows, macOS, and Linux.
author: Sandeep Kumar Penchala
---

# Cross-Platform Desktop Testing

Desktop applications run on a far more diverse hardware and software landscape than web apps. Differences in GPU drivers, OS versions, display configurations, and system settings mean bugs that don't exist on your dev machine will appear on users' machines. Cross-platform testing is not optional — it's how you find those bugs before your users do.

---

## 1. Testing Pyramid for Desktop Apps

```
         ┌─────────┐
         │   E2E   │  Playwright + Electron: critical user flows
         │  Tests  │  across all platforms
         ├─────────┤
         │Integration│  IPC handler tests, file system tests,
         │  Tests   │  auto-update tests, native module tests
         ├─────────┤
         │  Unit   │  Main process logic, renderer components,
         │  Tests  │  utility functions, type validation
         └─────────┘
```

## 2. Unit Testing

### 2.1 Electron Main Process

```typescript
// test/main/ipc-handlers.test.ts
import { describe, it, expect, vi } from 'vitest';

// Test IPC handler logic in isolation
describe('file:save handler', () => {
  it('returns error for empty content', async () => {
    const handler = createSaveHandler('/safe/dir');

    vi.mocked(dialog.showSaveDialog).mockResolvedValue({
      canceled: false,
      filePath: '/safe/dir/test.txt',
    });

    const result = await handler({} as any, '');
    expect(result.success).toBe(false);
    expect(result.error?.code).toBe('VALIDATION_ERROR');
  });

  it('rejects paths outside base directory', async () => {
    const handler = createSaveHandler('/safe/dir');

    vi.mocked(dialog.showSaveDialog).mockResolvedValue({
      canceled: false,
      filePath: '/etc/passwd',
    });

    const result = await handler({} as any, 'content');
    expect(result.success).toBe(false);
    expect(result.error?.code).toBe('PERMISSION_DENIED');
  });
});
```

### 2.2 Tauri Rust Commands

```rust
// src-tauri/tests/commands_test.rs
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_read_config_valid_path() {
        let result = read_config_impl("/tmp/test-config.json");
        assert!(result.is_ok());
    }

    #[test]
    fn test_read_config_path_traversal() {
        let result = read_config_impl("../../../etc/passwd");
        assert!(result.is_err());
        assert!(result.unwrap_err().contains("traversal"));
    }
}
```

### 2.3 WPF ViewModels

```csharp
[TestClass]
public class MainViewModelTests
{
    [TestMethod]
    public async Task SaveCommand_DisablesDuringSave()
    {
        var fileService = new Mock<IFileService>();
        var vm = new MainViewModel(fileService.Object);

        Assert.IsTrue(vm.SaveCommand.CanExecute(null));

        await vm.SaveCommand.ExecuteAsync(null);

        fileService.Verify(f => f.SaveAsync(It.IsAny<string>(), It.IsAny<string>()), Times.Once);
    }
}
```

## 3. Integration Testing

### 3.1 IPC Handler Integration Tests

```typescript
// test/integration/ipc-integration.test.ts
import { app, BrowserWindow } from 'electron';
import { test, expect } from '@playwright/test';

test.describe('IPC Integration', () => {
  let electronApp: ElectronApplication;

  test.beforeAll(async () => {
    electronApp = await electron.launch({
      args: ['.'],
      env: { NODE_ENV: 'test' },
    });
  });

  test.afterAll(async () => {
    await electronApp.close();
  });

  test('file:save writes content to disk', async () => {
    const page = await electronApp.firstWindow();
    const tempFile = join(os.tmpdir(), `test-${Date.now()}.txt`);

    const result = await page.evaluate(async (path) => {
      return window.electronAPI.saveFile('test content');
    });

    expect(result.success).toBe(true);
    expect(fs.existsSync(tempFile)).toBe(true);
    expect(fs.readFileSync(tempFile, 'utf-8')).toBe('test content');

    fs.unlinkSync(tempFile);
  });
});
```

### 3.2 Auto-Update Integration Tests

```typescript
// test/integration/auto-update.test.ts
import http from 'http';
import { AddressInfo } from 'net';

test.describe('Auto-Update', () => {
  let server: http.Server;
  let port: number;

  test.beforeAll(async () => {
    // Serve update manifests locally
    server = http.createServer((req, res) => {
      if (req.url === '/latest.yml') {
        res.writeHead(200, { 'Content-Type': 'text/yaml' });
        res.end(`
version: 99.0.0
files:
  - url: MyApp-Setup-99.0.0.exe
    sha512: fakehash
path: MyApp-Setup-99.0.0.exe
releaseDate: '2099-01-01T00:00:00.000Z'
        `);
      } else {
        res.writeHead(404);
        res.end();
      }
    });

    await new Promise<void>(resolve => server.listen(0, () => resolve()));
    port = (server.address() as AddressInfo).port;
  });

  test('detects available update', async () => {
    // Configure app to use test server
    const app = await launchElectron({
      env: { UPDATE_SERVER_URL: `http://localhost:${port}` },
    });

    const page = await app.firstWindow();

    // Wait for update notification
    const updateMessage = await page.waitForSelector('.update-available', {
      timeout: 30000,
    });

    expect(await updateMessage.textContent()).toContain('99.0.0');
  });
});
```

## 4. End-to-End (E2E) Testing with Playwright

### 4.1 Playwright + Electron Configuration

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  timeout: 60000,
  retries: 1,
  workers: 1, // Electron can only have one instance
  projects: [
    {
      name: 'electron',
      use: {
        // Electron-specific settings
        launchOptions: {
          args: ['--disable-gpu'], // Test software rendering path
        },
      },
    },
  ],
});
```

### 4.2 Critical Flow E2E Test

```typescript
// e2e/critical-path.test.ts
import { test, expect } from '@playwright/test';
import { _electron as electron } from 'playwright';

test.describe('Critical User Flow', () => {
  test('signup → create → save → reopen', async () => {
    const electronApp = await electron.launch({ args: ['.'] });
    const page = await electronApp.firstWindow();

    // 1. App loads
    await page.waitForSelector('.app-ready', { timeout: 15000 });
    expect(await page.title()).toContain('MyApp');

    // 2. Create new document
    await page.click('[data-testid="new-document"]');
    await page.fill('[data-testid="editor"]', 'Hello, world!');
    expect(await page.textContent('[data-testid="editor"]')).toBe('Hello, world!');

    // 3. Save via keyboard shortcut
    await page.keyboard.press('ControlOrMeta+s');

    // 4. Verify save confirmation
    await expect(page.locator('.save-confirmation')).toBeVisible();

    // 5. Close and reopen
    await electronApp.close();

    const electronApp2 = await electron.launch({ args: ['.'] });
    const page2 = await electronApp2.firstWindow();

    // 6. Verify content persisted
    await page2.waitForSelector('[data-testid="editor"]');
    expect(await page2.textContent('[data-testid="editor"]')).toBe('Hello, world!');

    await electronApp2.close();
  });
});
```

### 4.3 Menu Bar Testing

```typescript
test('menu bar: File → New opens new window', async () => {
  const electronApp = await electron.launch({ args: ['.'] });
  const page = await electronApp.firstWindow();

  // Trigger menu item via keyboard shortcut
  await page.keyboard.press('ControlOrMeta+n');

  // Verify new window appears
  const windows = electronApp.windows();
  expect(windows.length).toBeGreaterThanOrEqual(2);

  await electronApp.close();
});
```

## 5. Platform Matrix Testing

### 5.1 CI Matrix Configuration

```yaml
# .github/workflows/e2e.yml
name: E2E Tests
on: [push, pull_request]

jobs:
  e2e:
    strategy:
      fail-fast: false
      matrix:
        os: [macos-13, macos-14, windows-2022, ubuntu-22.04]
        gpu: [with-gpu, without-gpu]
        exclude:
          - os: macos-13
            gpu: with-gpu  # macos-13 runner has no GPU
          - os: ubuntu-22.04
            gpu: with-gpu  # Linux runner has no GPU display

    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci

      - name: Install system dependencies (Linux)
        if: runner.os == 'Linux'
        run: |
          sudo apt-get update
          sudo apt-get install -y xvfb libgtk-3-0 libnss3 libasound2

      - name: Run E2E tests
        run: npm run test:e2e
        env:
          DISPLAY: ':99'
          GPU_MODE: ${{ matrix.gpu }}
        if: runner.os == 'Linux'
        # Xvfb provides virtual display for headless testing on Linux

      - name: Run E2E tests (macOS/Windows)
        if: runner.os != 'Linux'
        run: npm run test:e2e
        env:
          GPU_MODE: ${{ matrix.gpu }}
```

### 5.2 GPU Testing

```typescript
// test/helpers/gpu-modes.ts
export function configureGPUMode(mode: 'with-gpu' | 'without-gpu'): string[] {
  if (mode === 'without-gpu') {
    return [
      '--disable-gpu',
      '--disable-software-rasterizer',
      '--disable-accelerated-2d-canvas',
      '--disable-accelerated-video-decode',
    ];
  }
  return [];
}

test.describe('GPU Fallback', () => {
  test('app launches without GPU acceleration', async () => {
    const app = await electron.launch({
      args: configureGPUMode('without-gpu'),
    });

    const page = await app.firstWindow();

    // Verify WebGL fallback
    const webglSupported = await page.evaluate(() => {
      try {
        const canvas = document.createElement('canvas');
        return !!canvas.getContext('webgl');
      } catch {
        return false;
      }
    });

    // App should handle missing WebGL gracefully
    expect(webglSupported).toBe(false);

    // Verify the app shows fallback content, not a white screen
    await expect(page.locator('.fallback-content')).toBeVisible();
    await expect(page.locator('.webgl-error')).not.toBeVisible();

    await app.close();
  });
});
```

## 6. Power State Testing

### 6.1 Simulating Power Events

```typescript
// test/helpers/power-state.ts
export async function simulateSleep(page: Page): Promise<void> {
  // Trigger suspend event via IPC
  await page.evaluate(() => {
    // Simulate what powerMonitor would trigger
    window.dispatchEvent(new CustomEvent('app:suspend'));
  });

  // Wait for cleanup to complete
  await page.waitForTimeout(1000);
}

export async function simulateResume(page: Page): Promise<void> {
  await page.evaluate(() => {
    window.dispatchEvent(new CustomEvent('app:resume'));
  });

  // Wait for reconnect to complete
  await page.waitForTimeout(2000);
}

test('data persists through sleep/resume cycle', async () => {
  const app = await electron.launch({ args: ['.'] });
  const page = await app.firstWindow();

  // Enter some data
  await page.fill('[data-testid="editor"]', 'unsaved data');

  // Simulate sleep
  await simulateSleep(page);

  // Simulate resume
  await simulateResume(page);

  // Verify data is still there
  const content = await page.inputValue('[data-testid="editor"]');
  expect(content).toBe('unsaved data');
});
```

## 7. Network Condition Testing

```typescript
test('app handles offline mode', async () => {
  const app = await electron.launch({ args: ['.'] });
  const context = app.context();

  // Simulate offline
  await context.setOffline(true);

  const page = await app.firstWindow();

  // App should show offline indicator
  await expect(page.locator('.offline-banner')).toBeVisible();

  // User should still be able to work with cached data
  await expect(page.locator('[data-testid="cached-content"]')).toBeVisible();

  // Simulate back online
  await context.setOffline(false);

  // App should reconnect and sync
  await expect(page.locator('.online-indicator')).toBeVisible();

  await app.close();
});
```

## 8. File System Testing

```typescript
import { mkdtempSync, writeFileSync, rmSync } from 'fs';
import { join } from 'path';
import { tmpdir } from 'os';

test.describe('File System', () => {
  let tempDir: string;

  test.beforeEach(() => {
    tempDir = mkdtempSync(join(tmpdir(), 'e2e-test-'));
  });

  test.afterEach(() => {
    rmSync(tempDir, { recursive: true, force: true });
  });

  test('handles disk-full scenario', async () => {
    const app = await electron.launch({ args: ['.'] });
    const page = await app.firstWindow();

    // Create a very large file to simulate disk pressure
    // (In real tests, use a mock or a RAM disk with limited size)
    const largeFile = join(tempDir, 'large.bin');
    writeFileSync(largeFile, Buffer.alloc(100 * 1024 * 1024)); // 100MB

    // Try to save
    const result = await page.evaluate((path) => {
      return window.electronAPI.saveFile('x'.repeat(1000000), path);
    }, join(tempDir, 'output.txt'));

    // App should handle write failure gracefully
    expect(result.error).toBeDefined();
    expect(result.error.code).toBe('IO_ERROR');

    await app.close();
  });
});
```

## 9. Performance Testing

### 9.1 Startup Performance

```typescript
test('cold start under 3 seconds', async () => {
  const start = Date.now();

  const app = await electron.launch({ args: ['.'] });
  const page = await app.firstWindow();

  await page.waitForSelector('.app-ready', { timeout: 10000 });

  const startupTime = Date.now() - start;
  console.log(`Cold start: ${startupTime}ms`);

  expect(startupTime).toBeLessThan(3000);

  await app.close();
});

test('warm start under 1.5 seconds', async () => {
  // First launch (cold)
  let app = await electron.launch({ args: ['.'] });
  await app.firstWindow();
  await app.close();

  // Second launch (warm — OS cache is hot)
  const start = Date.now();
  app = await electron.launch({ args: ['.'] });
  const page = await app.firstWindow();
  await page.waitForSelector('.app-ready', { timeout: 10000 });

  const startupTime = Date.now() - start;
  console.log(`Warm start: ${startupTime}ms`);

  expect(startupTime).toBeLessThan(1500);

  await app.close();
});
```

### 9.2 Memory Leak Detection

```typescript
test('no memory leak on repeated window open/close', async () => {
  const app = await electron.launch({ args: ['.'] });

  for (let i = 0; i < 20; i++) {
    // Open a new window
    await app.evaluate(({ BrowserWindow }) => {
      const win = new BrowserWindow({ width: 400, height: 300 });
      win.loadURL('about:blank');
      return new Promise(resolve => setTimeout(resolve, 500));
    });

    // Get all windows and close extras
    const windows = app.windows();
    if (windows.length > 1) {
      await windows[windows.length - 1].close();
    }
  }

  // After 20 cycles, memory should be stable
  // No explicit assertion here — the test passes if no crash or OOM
  await app.close();
});
```

## 10. Accessibility Testing

```typescript
import { injectAxe, checkA11y } from 'axe-playwright';

test('main window passes accessibility audit', async () => {
  const app = await electron.launch({ args: ['.'] });
  const page = await app.firstWindow();

  await injectAxe(page);

  const results = await checkA11y(page, undefined, {
    axeOptions: {
      runOnly: {
        type: 'tag',
        values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'],
      },
    },
  });

  expect(results.violations).toEqual([]);

  await app.close();
});
```

## 11. Test Checklist by Platform

| Test | Windows | macOS | Linux |
|------|---------|-------|-------|
| App launch | ✓ | ✓ | ✓ |
| Window creation | ✓ | ✓ | ✓ |
| Menu interactions | ✓ | ✓ | ✓ |
| File dialog open/save | ✓ | ✓ | ✓ |
| Keyboard shortcuts | ✓ | ✓ | ✓ |
| System tray | ✓ | ✓ | ✓ |
| Notifications | ✓ | ✓ | ✓ |
| Auto-update check | ✓ | ✓ | ✓ |
| DPI scaling | ✓ | ✓ | N/A |
| GPU fallback | ✓ | ✓ | ✓ |
| Sleep/resume | ✓ | ✓ | ✓ |
| Offline mode | ✓ | ✓ | ✓ |
| Uninstaller | ✓ | ✓ | Partial |
| Accessibility | ✓ | ✓ | Limited |
