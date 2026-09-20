#!/usr/bin/env python3
"""check-token-budget.py — compile-coverage gate + token-budget measurement (stdlib only).

The repo's architecture treats the *compiled* skill XML
(.skills-compiled/<name>/skill.xml) as the agent-load artifact, and each skill
declares a `token_budget` in frontmatter that the compile step targets
(compile-skills.sh exit code 3 = "Token budget exceeded").

Two distinct things are checked, and they are NOT equally measurable:

  1. Compile coverage — every skill in the corpus has a compiled artifact.
     This is deterministic and always gates (exit 1 on shortfall).

  2. Budget comparison — `compiled_tokens` (metadata.json) <= `budget`
     (skill.xml root attribute). This is only a *token* comparison when a real
     BPE tokenizer is installed. Without one, `_compile_skill.estimate_tokens`
     falls back to `len(text.split())` (scripts/_compile_skill.py:136), so the
     "tokens" are WORD COUNTS and the declared `token_budget` (authored in real
     tokens) is compared against a figure in a different unit. That comparison
     is unmeasured, not passing — so the tool refuses to report it as a pass.

Usage:
    python3 scripts/check-token-budget.py                    # strict: exit 2 if unmeasured
    python3 scripts/check-token-budget.py --json             # machine-readable
    python3 scripts/check-token-budget.py --allow-over       # report only, exit 0
    python3 scripts/check-token-budget.py --allow-unmeasured # don't fail on missing tokenizer

Exit codes:
  0 = measured and within budget (or report-only),
  1 = compile-coverage shortfall or budget violations found,
  2 = budget comparison UNMEASURED (no real tokenizer available).
"""

import argparse
import glob
import importlib.util
import json
import os
import re
import sys

REPO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DEFAULT_ROOT = os.path.join(REPO, ".skills-compiled")
DEFAULT_CORPUS = os.path.join(REPO, "skills")


def _budget_from_xml(xml_path):
    """Read the budget="N" attribute from a compiled skill.xml root element."""
    try:
        head = open(xml_path, encoding="utf-8").read(512)
    except OSError:
        return None
    m = re.search(r'budget="(\d+)"', head)
    return int(m.group(1)) if m else None


def _frontmatter_budget(md_path):
    """Read token_budget directly from the SKILL.md frontmatter (independent source)."""
    try:
        text = open(md_path, encoding="utf-8").read()
    except OSError:
        return None
    m = re.search(r"^---\s*\n(.*?)\n---", text, re.S | re.M)
    if not m:
        return None
    b = re.search(r"(?m)^token_budget:\s*(\d+)", m.group(1))
    return int(b.group(1)) if b else None


def _real_tokenizer():
    """Return a callable counting real BPE tokens, or None when unavailable.

    tiktoken is optional. When it is absent, `_compile_skill.estimate_tokens`
    (scripts/_compile_skill.py:136) silently returns `len(text.split())` — a word
    count — so the compiled_tokens/budget comparison would be in mismatched
    units. Returning None here is what lets the tool refuse to fake that pass.
    """
    if importlib.util.find_spec("tiktoken") is None:
        return None
    try:
        import tiktoken
        enc = tiktoken.get_encoding("cl100k_base")
        return lambda text: len(enc.encode(text))
    except Exception:
        return None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=DEFAULT_ROOT, help="compiled output dir")
    ap.add_argument("--corpus", default=DEFAULT_CORPUS,
                    help="source skills dir used to compute expected compile coverage")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--allow-over", action="store_true", help="report-only mode (exit 0)")
    ap.add_argument("--allow-unmeasured", action="store_true",
                    help="exit 0 even when no real tokenizer is available (still reports UNMEASURED)")
    args = ap.parse_args()

    tokenizer = _real_tokenizer()
    measured = tokenizer is not None

    rows = []
    for meta_path in sorted(glob.glob(os.path.join(args.root, "*", "metadata.json"))):
        name = os.path.basename(os.path.dirname(meta_path))
        try:
            meta = json.load(open(meta_path, encoding="utf-8"))
        except (OSError, ValueError) as e:
            rows.append({"skill": name, "error": f"metadata unreadable: {e}"})
            continue
        skill_dir = os.path.dirname(meta_path)
        xml_path = os.path.join(skill_dir, "skill.xml")
        budget = _budget_from_xml(xml_path)
        compiled = meta.get("compiled_tokens")
        original = meta.get("original_tokens")
        # Cross-check the xml budget against the source frontmatter, which is the
        # declared source of truth. The compiled dir has no SKILL.md of its own,
        # so look the skill up under the corpus.
        mismatch = None
        if budget is not None:
            for cand in glob.glob(os.path.join(args.corpus, "*", name, "SKILL.md")):
                fm_budget = _frontmatter_budget(cand)
                if fm_budget is not None and fm_budget != budget:
                    mismatch = {"xml_budget": budget, "frontmatter_budget": fm_budget}
                break
        rows.append({
            "skill": name,
            "original_tokens": original,
            "compiled_tokens": compiled,
            "budget": budget,
            "budget_mismatch": mismatch,
            # only a real unit comparison counts as "over"
            "over": bool(measured and compiled is not None and budget is not None
                         and compiled > budget),
        })

    violations = [r for r in rows if r.get("over")]
    mismatches = [r for r in rows if r.get("budget_mismatch")]
    errors = [r for r in rows if "error" in r]
    missing_budget = [r["skill"] for r in rows if "budget" not in r and r.get("budget") is None and "error" not in r]

    # Compile coverage: every skill in the corpus must have a compiled artifact,
    # otherwise stale/partial compile output could silently under-report.
    corpus_count = 0
    if os.path.isdir(args.corpus):
        for domain in os.listdir(args.corpus):
            dpath = os.path.join(args.corpus, domain)
            if os.path.isdir(dpath):
                corpus_count += sum(
                    1 for n in os.listdir(dpath)
                    if os.path.isfile(os.path.join(dpath, n, "SKILL.md")))
    compiled_count = len(rows)
    coverage_shortfall = max(0, corpus_count - compiled_count)

    if args.json:
        print(json.dumps({
            "total_compiled": len(rows),
            "corpus_skills": corpus_count,
            "coverage": f"{compiled_count}/{corpus_count}",
            "coverage_shortfall": coverage_shortfall,
            "tokenizer": "cl100k_base" if measured else None,
            "budget_comparison": "measured" if measured else "unmeasured",
            "within_budget": sum(1 for r in rows if not r.get("over") and "error" not in r) if measured else None,
            "over_budget": len(violations),
            "budget_mismatches": len(mismatches),
            "metadata_errors": len(errors),
            "violations": [{"skill": r["skill"], "compiled_tokens": r["compiled_tokens"],
                            "budget": r["budget"],
                            "ratio": round(r["compiled_tokens"] / r["budget"], 2) if r["budget"] else None}
                           for r in sorted(violations, key=lambda r: r["compiled_tokens"] / r["budget"] if r["budget"] else 0, reverse=True)],
        }, indent=2))
    else:
        print(f"compiled skills checked : {len(rows)}")
        print(f"corpus skills           : {corpus_count}")
        print(f"compile coverage        : {compiled_count}/{corpus_count} "
              f"({'OK' if coverage_shortfall == 0 else f'MISSING {coverage_shortfall}'})")
        if measured:
            print(f"tokenizer                : cl100k_base (real BPE)")
            print(f"within declared budget  : {sum(1 for r in rows if not r.get('over') and 'error' not in r)}")
            print(f"OVER declared budget    : {len(violations)}")
        else:
            print(f"tokenizer                : NONE — budget comparison UNMEASURED")
            print(f"  compiled_tokens is len(text.split()) (a WORD COUNT, scripts/_compile_skill.py:136)")
            print(f"  declared token_budget is real tokens — the two figures are not comparable")
        if mismatches:
            print(f"declared-budget mismatches: {len(mismatches)}")
        if errors:
            print(f"metadata errors          : {len(errors)}")
        for r in sorted(violations, key=lambda r: r["compiled_tokens"] / r["budget"] if r["budget"] else 0, reverse=True):
            ratio = r["compiled_tokens"] / r["budget"] if r["budget"] else float("inf")
            print(f"  OVER  {r['skill']}: compiled {r['compiled_tokens']} vs budget {r['budget']} ({ratio:.1f}x)")
        for r in mismatches:
            print(f"  MISMATCH {r['skill']}: xml budget {r['budget_mismatch']['xml_budget']} "
                  f"!= frontmatter {r['budget_mismatch']['frontmatter_budget']}")
        for r in rows:
            if "error" in r:
                print(f"  ERROR {r['skill']}: {r['error']}")

    if errors:
        print("note: metadata errors should be investigated", file=sys.stderr)
    if coverage_shortfall > 0 and not args.allow_over:
        print(f"FAIL: compile coverage {compiled_count}/{corpus_count} "
              f"(missing {coverage_shortfall} — run scripts/compile-skills.sh --all).")
        return 1
    if mismatches and not args.allow_over:
        print(f"FAIL: {len(mismatches)} skills declare a token_budget that disagrees with the "
              f"compiled skill.xml (frontmatter is the source of truth).")
        return 1
    if violations and not args.allow_over:
        print(f"FAIL: {len(violations)} compiled skills exceed their declared token_budget "
              f"(see docs — compiled XML is the agent-load artifact; budgets are a hard contract).")
        return 1
    # The honest outcome when no real tokenizer exists: the budget comparison is
    # UNMEASURED. Reporting it as a pass is a false green, so fail loudly unless
    # the caller explicitly opts out.
    if not measured and not args.allow_over and not args.allow_unmeasured:
        print(f"FAIL(UNMEASURED): no real tokenizer available — the compiled_tokens/budget "
              f"comparison cannot be trusted. Install tiktoken (python3 -m pip install tiktoken) "
              f"or pass --allow-unmeasured to accept an unmeasured report.")
        return 2
    if coverage_shortfall > 0:
        print(f"report: compile coverage {compiled_count}/{corpus_count} (non-blocking).")
    if mismatches:
        print(f"report: {len(mismatches)} declared-budget mismatches (non-blocking).")
    if violations:
        print(f"report: {len(violations)} compiled skills exceed their declared token_budget (non-blocking).")
    elif coverage_shortfall == 0 and measured:
        print("All compiled skills within declared token budget (measured with a real BPE tokenizer); "
              "full compile coverage.")
    elif coverage_shortfall == 0:
        print("Compile coverage full. Budget comparison UNMEASURED (no real tokenizer) — "
              "not a pass, see --allow-unmeasured.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
