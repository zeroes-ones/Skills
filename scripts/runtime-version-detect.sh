#!/usr/bin/env bash
# ==============================================================================
# runtime-version-detect.sh — Dynamic Tech Stack Version Detection
# ==============================================================================
# Reads package.json, go.mod, requirements.txt, Cargo.toml, etc. from the
# current project and outputs a JSON manifest of detected frameworks, languages,
# and their versions. This bridges the gap between static skill reference docs
# and the actual runtime environment.
#
# Usage:
#   ./scripts/runtime-version-detect.sh [project-root]
#   ./scripts/runtime-version-detect.sh --json           # JSON output
#   ./scripts/runtime-version-detect.sh --skill-context  # Skill-ready context block
#
# Output: JSON object with detected stack, versions, and doc URLs
# ==============================================================================
set -euo pipefail

TARGET="."
OUTPUT_MODE="text"

# Parse arguments — flags first, then optional target directory
for arg in "$@"; do
    case "$arg" in
        --json) OUTPUT_MODE="json" ;;
        --skill-context) OUTPUT_MODE="skill-context" ;;
        --help|-h)
            echo "Usage: runtime-version-detect.sh [project-dir] [--json|--skill-context]"
            exit 0 ;;
        *) TARGET="$arg" ;;
    esac
done

cd "$TARGET" 2>/dev/null || { echo '{"error":"cannot access directory '$TARGET'"}'; exit 1; }

# ─── Detection Functions ──────────────────────────────────────────────────────

detect_node() {
    local result="{}"
    if [[ -f "package.json" ]]; then
        local node_ver=""
        node_ver=$(node --version 2>/dev/null | sed 's/^v//' || echo "")
        local pm="npm"
        [[ -f "pnpm-lock.yaml" ]] && pm="pnpm"
        [[ -f "yarn.lock" ]] && pm="yarn"
        [[ -f "bun.lockb" ]] && pm="bun"

        # Extract key framework versions
        local deps=""
        deps=$(python3 -c "
import json, sys
try:
    with open('package.json') as f:
        pkg = json.load(f)
    deps = {}
    all_deps = {**pkg.get('dependencies',{}), **pkg.get('devDependencies',{}), **pkg.get('peerDependencies',{})}
    for name, ver in all_deps.items():
        if name in ['react','next','vue','nuxt','svelte','@sveltejs/kit','angular','express','fastify','@nestjs/core','prisma','drizzle-orm','typeorm','tailwindcss','vite','webpack','typescript','electron','expo','react-native','astro','remix','gatsby']:
            deps[name] = ver.lstrip('^~>=')
    print(json.dumps(deps))
except: print('{}')
" 2>/dev/null || echo "{}")

        result=$(python3 -c "
import json
print(json.dumps({
    'runtime': 'node',
    'runtime_version': '$node_ver',
    'package_manager': '$pm',
    'frameworks': json.loads('''$deps''')
}))
")
    fi
    echo "$result"
}

detect_python() {
    local result="{}"
    if [[ -f "requirements.txt" ]] || [[ -f "pyproject.toml" ]] || [[ -f "setup.py" ]] || [[ -f "Pipfile" ]]; then
        local py_ver=""
        py_ver=$(python3 --version 2>/dev/null | awk '{print $2}' || echo "")

        local frameworks="{}"
        if [[ -f "requirements.txt" ]]; then
            frameworks=$(python3 -c "
import json, re
frameworks = {}
try:
    with open('requirements.txt') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'): continue
            for fw in ['fastapi','flask','django','starlette','sanic','tornado','aiohttp','sqlalchemy','pydantic','celery','alembic']:
                if line.lower().startswith(fw):
                    ver = re.sub(r'[^0-9.]', '', line.split('==')[-1] if '==' in line else line.split('>=')[-1] if '>=' in line else 'latest')
                    frameworks[fw] = ver or 'pinned'
except: pass
print(json.dumps(frameworks))
" 2>/dev/null || echo "{}")
        fi

        result=$(python3 -c "
import json
print(json.dumps({
    'runtime': 'python',
    'runtime_version': '$py_ver',
    'frameworks': json.loads('''$frameworks''')
}))
")
    fi
    echo "$result"
}

detect_go() {
    local result="{}"
    if [[ -f "go.mod" ]]; then
        local go_ver=""
        go_ver=$(head -5 go.mod | grep '^go ' | awk '{print $2}' || echo "")
        local modules="{}"
        modules=$(python3 -c "
import json, re
mods = {}
try:
    with open('go.mod') as f:
        for line in f:
            line = line.strip()
            for m in ['gin-gonic/gin','labstack/echo','gorilla/mux','gorm.io/gorm','ent/ent','sqlx','pgx','chi','fiber']:
                if m in line:
                    parts = line.split()
                    ver = parts[-1] if parts else 'latest'
                    mods[m.split('/')[-1]] = ver.lstrip('v')
except: pass
print(json.dumps(mods))
" 2>/dev/null || echo "{}")

        result=$(python3 -c "
import json
print(json.dumps({
    'runtime': 'go',
    'runtime_version': '$go_ver',
    'modules': json.loads('''$modules''')
}))
")
    fi
    echo "$result"
}

detect_rust() {
    local result="{}"
    if [[ -f "Cargo.toml" ]]; then
        local rust_ver=""
        rust_ver=$(rustc --version 2>/dev/null | awk '{print $2}' || echo "")
        result=$(python3 -c "
import json
print(json.dumps({
    'runtime': 'rust',
    'runtime_version': '$rust_ver'
}))
")
    fi
    echo "$result"
}

generate_doc_urls() {
    local frameworks_json="$1"
    python3 -c "
import json, sys
try:
    frameworks = json.loads(sys.argv[1])
except:
    print('[]')
    sys.exit(0)

doc_map = {
    'react':     lambda v: f'https://react.dev/reference/react/{v or \"\"}',
    'next':      lambda v: f'https://nextjs.org/docs/{v or \"\"}',
    'vue':       lambda v: f'https://vuejs.org/guide/{v or \"\"}',
    'svelte':    lambda v: f'https://svelte.dev/docs/{v or \"\"}',
    'angular':   lambda v: f'https://angular.dev/{v or \"\"}',
    'express':   lambda v: f'https://expressjs.com/en/{v or \"\"}api.html',
    'fastify':   lambda v: f'https://fastify.dev/docs/{v or \"\"}',
    'fastapi':   lambda v: f'https://fastapi.tiangolo.com/{v or \"\"}',
    'django':    lambda v: f'https://docs.djangoproject.com/en/{v or \"\"}',
    'flask':     lambda v: f'https://flask.palletsprojects.com/en/{v or \"\"}',
    'prisma':    lambda v: f'https://www.prisma.io/docs/{v or \"\"}',
    'vite':      lambda v: f'https://vitejs.dev/{v or \"\"}',
    'tailwindcss': lambda v: f'https://tailwindcss.com/docs/{v or \"\"}',
    'astro':     lambda v: f'https://docs.astro.build/en/{v or \"\"}',
    'gin':       lambda v: f'https://gin-gonic.com/docs/{v or \"\"}',
    'echo':      lambda v: f'https://echo.labstack.com/docs/{v or \"\"}',
    'gorm':      lambda v: f'https://gorm.io/docs/{v or \"\"}',
    'ent':       lambda v: f'https://entgo.io/docs/{v or \"\"}',
}

urls = []
for name, ver in frameworks.items():
    if name in doc_map:
        urls.append({'framework': name, 'version': ver, 'docs_url': doc_map[name](ver)})
print(json.dumps(urls, indent=2))
" "$frameworks_json"
}

# ─── Main ──────────────────────────────────────────────────────────────────────

NODE_INFO=$(detect_node)
PYTHON_INFO=$(detect_python)
GO_INFO=$(detect_go)
RUST_INFO=$(detect_rust)

# Build combined output
RESULT=$(python3 -c "
import json

stacks = []
for info in ['$NODE_INFO','$PYTHON_INFO','$GO_INFO','$RUST_INFO']:
    try:
        d = json.loads(info)
        if d.get('runtime'):
            stacks.append(d)
    except: pass

output = {
    'project_root': '$(pwd)',
    'detected_stacks': stacks,
    'detected_at': '$(date -u +"%Y-%m-%dT%H:%M:%SZ")',
    'skill_context_hint': 'Use these versions when consulting documentation. Prefer official docs over LLM training data.'
}
print(json.dumps(output, indent=2))
")

if [[ "$OUTPUT_MODE" == "skill-context" ]]; then
    echo "## Runtime Environment Detected"
    echo ""
    python3 -c "
import json
data = json.loads('''$RESULT''')
for stack in data.get('detected_stacks', []):
    rt = stack.get('runtime', 'unknown')
    ver = stack.get('runtime_version', 'unknown')
    pm = stack.get('package_manager', '')
    print(f'- **{rt}** {ver}' + (f' (pm: {pm})' if pm else ''))
    fws = stack.get('frameworks', {}) or stack.get('modules', {})
    if fws:
        for name, v in fws.items():
            print(f'  - {name}: {v}')
print()
print('**Documentation to consult:**')
# Generate doc URLs
node_fws = json.dumps({})
py_fws = json.dumps({})
go_mods = json.dumps({})
import json
for s in data.get('detected_stacks', []):
    if s.get('runtime') == 'node':
        node_fws = json.dumps(s.get('frameworks', {}))
    elif s.get('runtime') == 'python':
        py_fws = json.dumps(s.get('frameworks', {}))
    elif s.get('runtime') == 'go':
        go_mods = json.dumps(s.get('modules', {}))
"
    # Use the doc URL generator
    ALL_FRAMEWORKS=$(python3 -c "
import json
data = json.loads('''$RESULT''')
all_fw = {}
for s in data.get('detected_stacks', []):
    all_fw.update(s.get('frameworks', {}))
    all_fw.update(s.get('modules', {}))
print(json.dumps(all_fw))
")
    generate_doc_urls "$ALL_FRAMEWORKS" 2>/dev/null || true
    echo ""
    echo "> ⚠️  **VERIFY**: These versions were detected at runtime. Always cross-reference official docs before writing framework-specific code."

elif [[ "$OUTPUT_MODE" == "text" ]]; then
    echo "$RESULT" | python3 -m json.tool 2>/dev/null || echo "$RESULT"
else
    echo "$RESULT"
fi
