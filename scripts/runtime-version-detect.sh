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

detect_infrastructure() {
    # Detects Docker, Terraform, Kubernetes, Helm — best-effort, commands may be absent
    local infra='{}'
    local has_any=false

    # Docker
    local docker_ver=""
    docker_ver=$(docker version --format '{{.Server.Version}}' 2>/dev/null || echo "")
    local compose_ver=""
    compose_ver=$(docker compose version --short 2>/dev/null || docker-compose --version 2>/dev/null | awk '{print $NF}' | sed 's/,//' || echo "")

    # Terraform
    local tf_ver=""
    tf_ver=$(terraform version -json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('terraform_version',''))" 2>/dev/null || echo "")
    # Detect terraform providers
    local tf_providers="{}"
    if [[ -d ".terraform/providers" ]]; then
        tf_providers=$(find .terraform/providers -name 'terraform-provider-*' -type f 2>/dev/null | head -20 | sed 's/.*terraform-provider-//' | sed 's/_v.*//' | sort -u | python3 -c "import sys; print(json.dumps([l.strip() for l in sys.stdin if l.strip()]))" 2>/dev/null || echo "{}")
    fi

    # Kubernetes
    local k8s_ver=""
    k8s_ver=$(kubectl version --short 2>/dev/null | grep 'Server' | awk '{print $3}' || echo "")

    # Helm
    local helm_ver=""
    helm_ver=$(helm version --short 2>/dev/null | sed 's/^v//' | tr -d '\n' || echo "")

    # Only output if at least one tool detected
    if [[ -n "$docker_ver$tf_ver$k8s_ver$helm_ver$compose_ver" ]]; then
        infra=$(python3 -c "
import json
print(json.dumps({
    'docker': '$docker_ver' if '$docker_ver' else None,
    'docker_compose': '$compose_ver' if '$compose_ver' else None,
    'terraform': '$tf_ver' if '$tf_ver' else None,
    'terraform_providers': json.loads('''$tf_providers''') if '$tf_providers' != '{}' else [],
    'kubernetes_server': '$k8s_ver' if '$k8s_ver' else None,
    'helm': '$helm_ver' if '$helm_ver' else None
}))
")
    fi
    echo "$infra"
}

detect_databases() {
    local db='{}'

    # PostgreSQL
    local pg_ver=""
    pg_ver=$(psql --version 2>/dev/null | awk '{print $3}' || echo "")
    if [[ -z "$pg_ver" ]]; then
        pg_ver=$(pg_config --version 2>/dev/null | awk '{print $2}' || echo "")
    fi

    # MySQL
    local mysql_ver=""
    mysql_ver=$(mysql --version 2>/dev/null | awk '{print $3}' | sed 's/,//' || echo "")

    # ORM: Prisma
    local prisma_ver=""
    prisma_ver=$(npx prisma --version 2>/dev/null | head -5 | grep '^prisma ' | awk '{print $NF}' | tr -d '\n' || echo "")

    # ORM: Alembic
    local alembic_ver=""
    alembic_ver=$(alembic --version 2>/dev/null | awk '{print $NF}' || echo "")

    if [[ -n "$pg_ver$mysql_ver$prisma_ver$alembic_ver" ]]; then
        db=$(python3 -c "
import json
print(json.dumps({
    'postgresql': '$pg_ver' if '$pg_ver' else None,
    'mysql': '$mysql_ver' if '$mysql_ver' else None,
    'prisma': '$prisma_ver' if '$prisma_ver' else None,
    'alembic': '$alembic_ver' if '$alembic_ver' else None
}))
")
    fi
    echo "$db"
}

detect_blockchain() {
    local chain='{}'

    # Solidity (solc)
    local solc_ver=""
    solc_ver=$(solc --version 2>/dev/null | grep 'Version:' | awk '{print $2}' || echo "")

    # Foundry
    local forge_ver=""
    forge_ver=$(forge --version 2>/dev/null | head -1 | awk '{print $NF}' || echo "")

    # Hardhat
    local hardhat_ver=""
    hardhat_ver=$(npx hardhat --version 2>/dev/null | tr -d '\n' || echo "")

    # OpenZeppelin contracts version (from package.json or foundry.toml)
    local oz_ver=""
    if [[ -f "package.json" ]]; then
        oz_ver=$(python3 -c "
import json
try:
    with open('package.json') as f:
        pkg = json.load(f)
    deps = {**pkg.get('dependencies',{}), **pkg.get('devDependencies',{})}
    for k in deps:
        if 'openzeppelin/contracts' in k:
            print(deps[k].lstrip('^~>='))
            break
except: pass
" 2>/dev/null || echo "")
    fi
    if [[ -z "$oz_ver" ]] && [[ -f "foundry.toml" ]]; then
        oz_ver=$(grep 'openzeppelin' foundry.toml 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1 || echo "")
    fi

    # ethers.js version
    local ethers_ver=""
    if [[ -f "package.json" ]]; then
        ethers_ver=$(python3 -c "
import json
try:
    with open('package.json') as f:
        pkg = json.load(f)
    deps = {**pkg.get('dependencies',{}), **pkg.get('devDependencies',{})}
    for k in deps:
        if k == 'ethers':
            print(deps[k].lstrip('^~>='))
            break
except: pass
" 2>/dev/null || echo "")
    fi

    if [[ -n "$solc_ver$forge_ver$hardhat_ver$oz_ver$ethers_ver" ]]; then
        chain=$(python3 -c "
import json
print(json.dumps({
    'solidity': '$solc_ver' if '$solc_ver' else None,
    'foundry': '$forge_ver' if '$forge_ver' else None,
    'hardhat': '$hardhat_ver' if '$hardhat_ver' else None,
    'openzeppelin': '$oz_ver' if '$oz_ver' else None,
    'ethers_js': '$ethers_ver' if '$ethers_ver' else None
}))
")
    fi
    echo "$chain"
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
INFRA_INFO=$(detect_infrastructure)
DB_INFO=$(detect_databases)
BLOCKCHAIN_INFO=$(detect_blockchain)

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

# Merge infrastructure, database, and blockchain info
infra = {}
try: infra = json.loads('$INFRA_INFO')
except: pass

db = {}
try: db = json.loads('$DB_INFO')
except: pass

blockchain = {}
try: blockchain = json.loads('$BLOCKCHAIN_INFO')
except: pass

output = {
    'project_root': '$(pwd)',
    'detected_stacks': stacks,
    'infrastructure': infra if infra else None,
    'databases': db if db else None,
    'blockchain': blockchain if blockchain else None,
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

# Infrastructure tools
infra = data.get('infrastructure') or {}
if infra:
    print()
    print('**Infrastructure:**')
    for k, v in infra.items():
        if v and k != 'terraform_providers':
            print(f'- {k}: {v}')
        elif k == 'terraform_providers' and v:
            print(f'- terraform providers: {\", \".join(v)}')

# Databases
db = data.get('databases') or {}
if db:
    print()
    print('**Databases & ORMs:**')
    for k, v in db.items():
        if v:
            print(f'- {k}: {v}')

# Blockchain
blockchain = data.get('blockchain') or {}
if blockchain:
    print()
    print('**Blockchain Tools:**')
    for k, v in blockchain.items():
        if v:
            print(f'- {k}: {v}')

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
