#!/usr/bin/env python3
"""
agent_executor.py — run workflow nodes with a real agent CLI (stdlib only, opt-in).

Drop-in executor for scripts/workflow-runner.py that calls an agentic CLI headlessly per node
(the real 'content' leg of the canonical split: engine does control flow, the agent does work).
Works with any CLI that accepts '<command> -p "<prompt>"' (claude, gemini, ...).

Configuration (env):
    AGENT_CMD         command + args. Supports a {prompt} placeholder for ANY backend, e.g.:
                          claude : AGENT_CMD='claude -p "{prompt}"'
                          gemini : AGENT_CMD='gemini -p "{prompt}"'
                          codex  : AGENT_CMD='codex exec "{prompt}"'
                          ollama : AGENT_CMD='ollama run llama3.1 "{prompt}"'
                          other  : any CLI/wrapper that prints the model reply to stdout, with
                                   "{prompt}" where the prompt goes.
                      If no {prompt} placeholder is present, the prompt is appended as the last
                      argument (legacy behavior; works for claude -p and gemini -p).
    AGENT_TIMEOUT     seconds per node call (default 600). A real node is NOT a 90s call: this value
                      must cover the agent reading a full skill excerpt and reasoning over it.
                      Measured on the flagship senior-dev-loop manifest (D1 in
                      docs/skill-automation-platform.md): 149.6s for one implement node and >180s
                      for the next, so anything below ~300s produces spurious timeouts. Lower it
                      only for cheap/throwaway models.
    AGENT_TRANSCRIPT  log file for every agent turn (default ./agent-transcript.log)
    AGENT_FALLBACK    when a call fails/times out, return a stub pass instead of crashing
                      (default 1). Set 0 to surface failures to the runner.
    AGENT_SKILL_WORDS max words of the node's compiled skill injected into the prompt
                      (default 1200 - a small-window budget; compiled preferred, SKILL.md fallback)
    AGENT_SKILL_DEPTH 1 = depth-aware selection (default), 0 = legacy first-N-words truncation.
                      Depth-aware fills the budget by priority - Route the Request, Ground Rules,
                      Decision Trees, Core Workflow and Verification/completion criteria first,
                      narrative sections (Mindset, Levels, Deliberate Practice, What Good Looks
                      Like) only if words remain - instead of cutting at a word offset that lands
                      mid-section and can drop the completion criteria entirely.
                      Words are the same heuristic the token budget uses
                      (`scripts/_compile_skill.py:136`, word-count fallback), not a tokenizer.

Trailer contract (criteria coverage + evidence):
    Every node reply is asked for the library's own verify-node.md output markers
    (`workflow/templates/verify-node.md` "Output markers", WORKFLOW-SYSTEM.md Section 7):

        [VERIFY: <k>/<n> criteria met]
          criterion: <criterion text, verbatim from the declared criteria listed in the prompt>
          evidence: <artifact path + sha | command output | named reasoning trace>
          unmet: <criterion> (no evidence)          # only for criteria not met
        [VERIFY RESULT: pass|fail]
        Verdict: pass|changes_requested

    The node's declared `workflow: completion.criteria` - read from the skill's frontmatter with
    the repo's own parsers (`scripts/lib/lint-workflow.py` + `scripts/lib/safe_yaml.py`) - are
    listed in the prompt, because they live in frontmatter and are therefore absent from the
    skill BODY the depth-aware excerpt is cut from. A well-formed trailer is mapped onto the
    runner's `criteria_met` shape, resolving each reported criterion to the DECLARED criterion's
    own text (one of the three references `_criteria_covered` accepts, alongside `1` and `c2`).
    Criteria the agent reports that the contract never declared are NOT claimed as coverage -
    they are reported on the result's `diagnostics`, because claiming coverage the contract does
    not recognize is a false claim rather than a covered criterion.

    Known limit (verified, not fixed here): `workflow-runner.py`'s `_mark_done` copies `status`,
    `verdict`, `evidence`, `summary`, `artifacts`, `decisions`, `open_questions` and
    `verification_evidence` onto the node record and **not** `diagnostics`, so today those notes
    are visible to a caller that invokes `execute_node` directly and are dropped by a `--executor`
    run. Changing that is the runner's call, not the executor's.

    `evidence` then carries the reply digest plus one line per reported claim, prefixed
    `agent-reply:` / `agent-claim:` - named that way deliberately. This executor drives an opaque
    CLI, so the strongest thing it can attest is *the agent asserted this, and here is the reply
    it asserted it in*. It never implies a check ran: overstating evidence is the defect
    `verify-node.md` exists to prevent.

    Backward compatibility: a reply with NO trailer (what every existing backend emits) is
    unchanged - the `Verdict:` line is parsed exactly as before, `evidence` stays
    `["agent-turn:<node>"]`, and `criteria_met` is NOT emitted. Under `--enforce-contracts` that
    node is still refused: no trailer means no coverage claimed, and that must not silently pass.

Behavior per node: builds a prompt from the node id + run context PLUS the node's referenced
skill (compiled excerpt, depth-aware selection) so the agent actually operates from the skill's
content - every node is skill-grounded, single- and multi-agent alike.

Usage:
    AGENT_CMD="claude -p" python3 scripts/workflow-runner.py \
        --manifest your-workflow.yaml --executor scripts/executors/agent_executor.py \
        --guardrail scripts/lib/guardrails.py --memory ./agent-memory
"""

import hashlib
import importlib.util
import json
import os
import re
import shlex
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

AGENT_CMD = os.environ.get("AGENT_CMD", "claude -p")
AGENT_TIMEOUT = float(os.environ.get("AGENT_TIMEOUT", "600"))
AGENT_TRANSCRIPT = os.environ.get("AGENT_TRANSCRIPT", "agent-transcript.log")
AGENT_FALLBACK = os.environ.get("AGENT_FALLBACK", "1") not in ("0", "false", "no")
AGENT_SKILL_WORDS = int(os.environ.get("AGENT_SKILL_WORDS", "1200"))  # window budget per skill
AGENT_SKILL_DEPTH = os.environ.get("AGENT_SKILL_DEPTH", "1") not in ("0", "false", "no")

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Depth-aware section priority. The three tiers are ordered by what a node MUST have to be
# verifiable: the completion criteria and the rules govern the verdict, the trees and workflow
# drive the work, and the narrative tiers only help as budget allows:
#   core    - Route the Request, Ground Rules, Decision Trees, Core Workflow, Verification,
#             Verification Guardrails, Production Checklist ("Complete when" rows live there).
#   support - Gotchas, Error Recovery/Decoder, Best Practices, Anti-Patterns, Proactive Triggers,
#             Cross-Skill Coordination, State Log, Anti-Rationalization.
#   narrative - The Expert's Mindset, Operating at Different Levels, Deliberate Practice,
#             What Good Looks Like, When to Use, When NOT to Use.
# A recognised tier is a *preference, never a gate*: every section competes for the same word
# budget, so a long core section cannot crowd out the rest entirely.
_CORE_SECTIONS = {
    "route the request": 0, "ground rules": 1, "decision trees": 2, "core workflow": 3,
    "verification": 4, "verification guardrails": 4, "production checklist": 5,
    "escalation path": 5, "guardrails": 5,
}
_SUPPORT_SECTIONS = {
    "gotchas": 0, "anti-hallucination": 1, "error recovery": 2, "error decoder": 2,
    "best practices": 3, "anti-patterns": 4, "proactive triggers": 5, "state log": 6,
    "cross-skill": 7, "anti-rationalization": 8, "failure modes": 9,
}
_NARRATIVE_SECTIONS = {
    "the expert": 0, "operating at different levels": 1, "deliberate practice": 2,
    "what good looks like": 3, "when to use": 4, "when not to use": 5,
}
# Within one section the depth markers grade the blocks: QUICK/STANDARD before DEEP, so a
# tight budget keeps the 30-second and 3-minute material over the 10-minute deep dive.
_DEPTH_MARKER = re.compile(
    r"<!--\s*(QUICK|STANDARD|DEEP)\b[^>]*-->|\*\*\((QUICK|STANDARD|DEEP)\b[^)]*\)\*\*")
_DEPTH_RANK = {"QUICK": 0, "STANDARD": 1, "DEEP": 2}
_HEADING = re.compile(r"^##\s+(.+?)\s*$")


def _section_tier(title):
    """Classify a section heading into (tier, rank), or None if unrecognised."""
    t = title.lower()
    for table, tier in ((_CORE_SECTIONS, "core"), (_SUPPORT_SECTIONS, "support"),
                        (_NARRATIVE_SECTIONS, "narrative")):
        for key, rank in table.items():
            if t.startswith(key):
                return tier, rank
    return None


def _split_sections(body):
    """Split a markdown body into (title, text) at `## ` headings; a leading titleless part
    (a preamble before the first heading) is returned with an empty title.

    Headings are matched the same way the compiler does (`scripts/_compile_skill.py:124`, a plain
    `^## ` regex) rather than with fence tracking: this corpus contains unbalanced code fences,
    and tracking them would quarantine real sections like `## Core Workflow` as if they were code.
    """
    lines = body.splitlines(True)
    heads = [(i, m.group(1)) for i, line in enumerate(lines)
             if (m := _HEADING.match(line))]
    out = []
    if heads and heads[0][0] > 0:
        lead = "".join(lines[: heads[0][0]]).strip()
        if lead:
            out.append(("", lead))
    for idx, (i, title) in enumerate(heads):
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
        out.append((title, "".join(lines[i:end]).strip()))
    return out


def _depth_blocks(text):
    """Split section text at depth markers into (rank, block) pairs using the marker that
    governs each block; the heading line carries no marker, so it stays ranked STANDARD."""
    parts, cur, last = [], "STANDARD", 0
    for m in _DEPTH_MARKER.finditer(text):
        parts.append((cur, text[last:m.start()]))
        cur = m.group(1) or m.group(2)
        last = m.end()
    parts.append((cur, text[last:]))
    return [(_DEPTH_RANK[rank], blk) for rank, blk in parts if blk.strip()]


def _title_key(title):
    """Heading text with depth markers and decoration removed, for tier matching."""
    t = _DEPTH_MARKER.sub(" ", title)
    return re.sub(r"[*_`]+", "", t).strip(" :#-").lower()


def _rank_sections(body):
    """Order a body's sections by what a node needs, deterministically.

    Returns [(title, text, is_low_signal)]. High-signal sections come first in tier order;
    an unrecognised section (a domain-specific heading this table has never seen) is ranked
    with support, never dropped - so unusual headings can lose a tight budget, not disappear
    silently. Empty result means 'not parseable as a skill' and the caller falls back.
    """
    ranked = []
    for title, text in _split_sections(body):
        if not text:
            continue
        tier = _section_tier(_title_key(title)) if title else None
        if tier is None:
            tier, rank = ("support", 0) if title else ("core", 9)
            low = False
        else:
            tier, rank = tier
            low = tier == "narrative"
        order = {"core": 0, "support": 1, "narrative": 2}[tier]
        ranked.append((order, rank, title, text, low))
    ranked.sort(key=lambda r: (r[0], r[1]))
    return [(r[2], r[3], r[4]) for r in ranked]


def _clip_words(text, take):
    """Keep the first `take` words of `text`, preserving its line structure and code fences so
    the excerpt stays readable markdown for the agent (a word-joined blob destroys the tables
    the completion criteria live in)."""
    lines = text.splitlines(True)
    total = sum(len(line.split()) for line in lines)
    if take >= total:
        return text
    kept, remaining = [], take
    for line in lines:
        words = len(line.split())
        if words == 0:
            kept.append(line)
            continue
        if words <= remaining:
            kept.append(line)
            remaining -= words
        else:
            kept.append(" ".join(line.split()[:remaining]) + "\n")
            break
    return "".join(kept).rstrip()


def _select_depth_aware(body, budget):
    """Fill `budget` words by priority instead of position: high-signal sections first, and
    within a section the QUICK/STANDARD blocks before the DEEP ones. Every section gets an
    equal share of what is left, so one oversized section cannot evict the others."""
    def _fill(units, allowance, taken):
        remaining = allowance
        while remaining > 0 and not all(taken):
            pending = [i for i, t in enumerate(units) if not taken[i]]
            share = max(1, remaining // len(pending))
            progressed = False
            for i in pending:
                if remaining <= 0:
                    break
                title, blk, _low = units[i]
                words = blk.split()
                take = min(len(words), share, remaining)
                if take <= 0:
                    continue
                units[i] = (title, _clip_words(blk, take), _low)
                taken[i] = True
                remaining -= take
                progressed = True
                if take < len(words):  # clipped here: stop, don't spend the rest on this block
                    break
            if not progressed:
                break
        return allowance - remaining

    def _reserve(units, taken, allowance, reserve):
        """Spend up to `reserve` words on the blocks that hold the completion criteria
        ("Complete when" / check-box rows). Some skills declare their criteria inside Core
        Workflow rather than a Verification section, and a round-robin share would clip them
        away before they are ever reached."""
        budget = allowance
        for i, (title, blk, low) in enumerate(units):
            if budget <= 0 or taken[i] or "complete when" not in blk.lower():
                continue
            words = blk.split()
            take = min(len(words), budget)
            units[i] = (title, _clip_words(blk, take), low)
            taken[i] = True
            budget -= take
        return allowance - budget

    sections = _rank_sections(body)
    if not sections:
        return "", 0, []
    units = [(title, blk, low)
             for title, text, low in sections
             for _, blk in _depth_blocks(text)]
    if not units:
        return "", 0, []
    kept_units = [False] * len(units)
    # Reserve at most this share of the budget for the completion criteria blocks, then spend
    # the rest by priority. A skill with no such block simply loses the carve-out.
    reserve = budget // 3
    used = _reserve(units, kept_units, reserve, reserve)
    used += _fill(units, budget - used, kept_units)
    blocks = [(t, blk, low) for (t, blk, low), done in zip(units, kept_units)
              if done and blk.strip()]
    return "\n\n".join(b for _, b, _ in blocks), used, blocks


def _skill_bodies(skill):
    """Yield candidate skill bodies in preference order.

    A SKILL.md body is preferred over the compiled XML because the executor needs `## ` headings
    and `<!-- QUICK/STANDARD/DEEP -->` markers, and the compiler emits neither: the XML names each
    section by tag (`<route>`, `<workflow>`) and carries no marker text. The compiled XML stays as
    the fallback source, and with AGENT_SKILL_DEPTH=0 it stays the primary one, matching the
    pre-depth-aware behaviour.
    """
    if not skill:
        return
    sources = []
    skills_dir = os.path.join(_REPO, "skills")
    if os.path.isdir(skills_dir):
        for domain in sorted(os.listdir(skills_dir)):
            p = os.path.join(skills_dir, domain, skill, "SKILL.md")
            if os.path.isfile(p):
                raw = open(p, encoding="utf-8").read()
                m = re.search(r"^---\s*\n.*?\n---\s*\n(.*)$", raw, re.S)
                sources.append(m.group(1) if m else raw)
                break
    compiled = os.path.join(_REPO, ".skills-compiled", skill, "skill.xml")
    if os.path.isfile(compiled):
        try:
            root = ET.parse(compiled).getroot()
            sources.append(" ".join((root.text or "") + " ".join(
                n.text or "" for n in root.iter() if n.text)))
        except ET.ParseError:
            pass
    order = sources if AGENT_SKILL_DEPTH else list(reversed(sources))
    for body in order:
        yield body


def _truncate_words(text, budget):
    """Legacy positional cut: the first `budget` words, whatever section that lands in."""
    words = text.split()
    if len(words) > budget:
        words = words[:budget]
    return " ".join(words), len(words)


def _load_skill_text(skill, budget=None):
    """Return the node's skill excerpt, depth-aware by default.

    Fills the word budget by priority (see `_rank_sections`) rather than by position, so the
    completion criteria and ground rules survive a truncation that used to end mid-section.
    Falls back to the legacy first-N-words cut when no structured body is available, when the
    body parses to no sections at all (an unusual skill), or when AGENT_SKILL_DEPTH=0.
    Returns (text, words).
    """
    if not skill:
        return "", 0
    budget = AGENT_SKILL_WORDS if budget is None else budget
    fallback, fallback_low = "", False
    for body in _skill_bodies(skill):
        if not body.strip():
            continue
        if not fallback:
            fallback, fallback_low = _truncate_words(body, budget)
        if not AGENT_SKILL_DEPTH:
            return fallback, len(fallback.split())
        stripped = body.strip()
        if not re.search(r"^##\s+\S", stripped, re.M):
            continue  # no recognisable sections: try the next source, else legacy
        text, words, blocks = _select_depth_aware(stripped, budget)
        if words and any(not low for _, _, low in blocks):
            return text, words
    if not fallback:
        return "", 0
    return fallback, len(fallback.split())


def _skill_file(skill):
    """Absolute path of the skill's SKILL.md, or None. Mirrors `_skill_bodies`' lookup."""
    if not skill:
        return None
    skills_dir = os.path.join(_REPO, "skills")
    if not os.path.isdir(skills_dir):
        return None
    for domain in sorted(os.listdir(skills_dir)):
        p = os.path.join(skills_dir, domain, skill, "SKILL.md")
        if os.path.isfile(p):
            return p
    return None


def _completion_criteria(skill):
    """Return the node skill's declared `workflow: completion.criteria` list (possibly []).

    Read with the repo's own contract parsers - `scripts/lib/lint-workflow.py`
    (`extract_workflow_block`) + `scripts/lib/safe_yaml.py` - so the executor and the runner
    (`workflow-runner.py`, `load_contract`) resolve the same block the same way. The criteria live
    in the frontmatter, which the skill *body* (what `_load_skill_text` injects) does not contain,
    so the agent cannot see them unless the prompt states them.

    Best-effort by design: an unreadable or contract-less skill returns [], and the prompt then
    asks for no criteria trailer - a node with no declared contract is already in default mode.
    """
    path = _skill_file(skill)
    if not path:
        return []
    try:
        spec = importlib.util.spec_from_file_location(
            "agent_executor_lint_workflow", os.path.join(_REPO, "scripts", "lib", "lint-workflow.py"))
        lw = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(lw)
        sys.path.insert(0, os.path.join(_REPO, "scripts"))
        from lib import safe_yaml
        block = lw.extract_workflow_block(open(path, encoding="utf-8").read())
        if not block or not block.strip():
            return []
        lines = [ln for ln in block.splitlines() if ln.strip()]
        ind = min(len(ln) - len(ln.lstrip(" ")) for ln in lines)
        parsed = safe_yaml.parse("\n".join(ln[ind:] if len(ln) >= ind else ln for ln in lines))
        criteria = ((parsed or {}).get("completion") or {}).get("criteria") or []
    except Exception:  # noqa: BLE001 - an unreadable contract means "no criteria to ask for"
        return []
    if not isinstance(criteria, list):
        return []
    return [str(c).strip() for c in criteria if str(c).strip()]


_VERIFY_HEADER = re.compile(r"^\s*\[VERIFY:\s*(\d+)\s*/\s*(\d+)\s+criteria?\s+met\s*\]\s*$", re.I)
_VERIFY_RESULT = re.compile(r"^\s*\[VERIFY RESULT:\s*(pass|fail)\s*\]\s*$", re.I)
_VERIFY_FIELD = re.compile(r"^\s*(criterion|evidence|unmet)\s*:\s*(.*\S)\s*$", re.I)
_REPLY_DIGEST_CHARS = 120


def _reply_digest(text):
    """Stable 12-hex digest of the agent's reply - what "here is the reply it asserted it in"
    pins down, so `evidence` names a specific turn rather than an unfalsifiable claim."""
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()[:12]


def _parse_verify_trailer(text, criteria):
    """Parse the `[VERIFY: k/n criteria met] ... [VERIFY RESULT: pass|fail]` trailer.

    Returns (reported, unmet, result, evidence, diagnostics):
      reported  - declared criterion texts the agent claims met
      unmet     - declared criterion texts the agent named as unmet (kept, never dropped)
      result    - 'pass'|'fail' from [VERIFY RESULT], or None when the marker is missing
      evidence  - one `agent-claim:` line per criterion the trailer reported on
      diagnostics - everything not trustworthy about the report: claims the contract does not
                    declare, a header count that contradicts the lines it summarises, a failed
                    result marker, or an unknown line kind inside the block

    Returns None when the trailer is ABSENT or unreadable (no header, or a header about a
    different criteria list). A trailer that cannot be read is not a claim of coverage, and
    guessing what it meant is the failure mode this contract exists to catch.
    """
    lines = (text or "").splitlines()
    start = None
    for i, ln in enumerate(lines):
        if _VERIFY_HEADER.match(ln):
            start = i
            break
    if start is None:
        return None
    reported_k, reported_n = (int(g) for g in _VERIFY_HEADER.match(lines[start]).groups())
    if reported_n != len(criteria):
        return None  # the trailer describes a different criteria list than the declared one
    reported, unmet, evidence, diagnostics = [], [], [], []
    seen_declared, current = set(), None
    for ln in lines[start + 1:]:
        if _VERIFY_RESULT.match(ln):
            break
        field = _VERIFY_FIELD.match(ln)
        if not field:
            if ln.strip() and not ln.startswith((" ", "\t")):
                diagnostics.append("unrecognized line in verify trailer: %s" % ln.strip()[:80])
            continue
        key, value = field.group(1).lower(), field.group(2).strip()
        if key == "criterion":
            current = value
            matched = next((c for c in criteria if c.lower() == value.lower()), None)
            if matched is None:
                diagnostics.append("criterion reported but not declared in the contract: %s" % value)
                continue
            if matched in seen_declared:
                diagnostics.append("declared criterion reported more than once: %s" % matched)
                continue
            seen_declared.add(matched)
            reported.append(matched)          # a re-named 'unmet:' line below withdraws it again
        elif current is None:
            diagnostics.append("%s: line before any criterion: line" % key)
        elif key == "evidence":
            evidence.append("agent-claim: %s | evidence: %s" % (current, value))
        else:  # unmet
            if current in reported:
                reported.remove(current)
            if current not in unmet:
                unmet.append(current)
            diagnostics.append("criterion reported unmet: %s" % current)
    result = next((m.group(1).lower() for ln in lines[start:] if (m := _VERIFY_RESULT.match(ln))),
                  None)
    if result is None:
        diagnostics.append("verify trailer has no [VERIFY RESULT: ...] line")
    if reported_k != len(reported):
        diagnostics.append("verify header claims %d met but %d declared criterion line(s) were "
                           "readable" % (reported_k, len(reported)))
    if result == "fail":
        diagnostics.append("verify result is fail: coverage is not claimed")
    return reported, unmet, result, evidence, diagnostics


def _context_prompt(node_id, state, ctx):
    context = {
        "workflow": state.get("workflow"),
        "iteration": state.get("iteration"),
        "loop": ctx.get("loop_id"),
        "pass": ctx.get("pass"),
        "skill": ctx.get("skill"),
        "open_questions": (state.get("open_questions") or [])[-3:],
    }
    skill_text, skill_words = _load_skill_text(ctx.get("skill"))
    criteria = _completion_criteria(ctx.get("skill"))
    if criteria:
        # The declared criteria are frontmatter, so they are NOT in the body excerpt above. Stated
        # in the prompt verbatim, and the trailer's `criterion:` line is required to copy one back
        # word-for-word - the runner matches on the declared text, so a paraphrase claims nothing.
        trailer = (
            "\n\nYOUR NODE'S DECLARED COMPLETION CRITERIA (%d). Every one must be reported in the\n"
            "trailer below, copying its text verbatim onto a 'criterion:' line:\n%s\n"
            % (len(criteria), "\n".join("  %d. %s" % (i + 1, c)
                                        for i, c in enumerate(criteria))))
    else:
        trailer = ("\n\nThis node declares no workflow: completion contract, so there are no "
                   "criteria to report;\nreport the trailer with an empty body.\n")
    prompt = (
        "You are executing the node '%s' inside an agentic workflow run.\n"
        "Run context: %s\n\n"
        "YOUR OPERATING SKILL (compiled excerpt, %d words; priority-selected - its completion\n"
        "criteria, ground rules and workflow come first; follow it for this node):\n"
        "---\n%s\n---\n%s"
        "Finish your reply with this trailer (workflow/templates/verify-node.md output markers),\n"
        "then the verdict line. A criterion with no evidence you actually have is NOT met - mark\n"
        "it 'unmet' rather than claiming it; a fabricated evidence line is worse than an honest\n"
        "unmet criterion.\n\n"
        "[VERIFY: <number of criteria above you met>/%d criteria met]\n"
        "  criterion: <the criterion's text, copied verbatim from the list above>\n"
        "  evidence: <artifact path + sha | command output | named reasoning trace>\n"
        "  unmet: <criterion, only if you could not meet it>\n"
        "[VERIFY RESULT: pass|fail]\n"
        "Verdict: pass|changes_requested\n\n"
        "Use 'Verdict: pass' if your work meets its criteria with evidence, otherwise\n"
        "'Verdict: changes_requested' (state what is missing).\n"
        "Keep the body of your reply under 200 words."
        % (node_id, json.dumps(context, default=str), skill_words,
           skill_text if skill_text else "(skill not found - use the run context)",
           trailer, len(criteria))
    )
    return prompt, skill_words


def _call_agent(prompt):
    tokens = shlex.split(AGENT_CMD)
    if any("{prompt}" in t for t in tokens):
        tokens = [t.replace("{prompt}", prompt) for t in tokens]
    else:
        tokens.append(prompt)  # legacy: append the prompt as the final argument
    started = time.time()
    proc = subprocess.run(tokens, capture_output=True, text=True, timeout=AGENT_TIMEOUT)
    return (proc.stdout or "").strip(), time.time() - started


def _record(node_id, verdict, text, seconds, fallback, prompt_words=None, skill=None):
    line = json.dumps({
        "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "node": node_id, "verdict": verdict, "seconds": round(seconds, 1),
        "fallback": fallback, "skill": skill, "prompt_words": prompt_words,
        "agent_reply": (text or "")[:600],
    }, sort_keys=True)
    try:
        with open(AGENT_TRANSCRIPT, "a", encoding="utf-8") as fh:
            fh.write(line + "\n")
    except OSError:
        pass  # transcript is best-effort


def _identify_prompt(node_id, state, ctx):
    """Prompt for a kind: agent gate — pick the corrective channel from the pool."""
    lines = ["You are the identify-agent gate '%s' in an agentic workflow run." % node_id,
             "A bounded loop exhausted and escalated to you. Choose which channel should",
             "lead the next bounded window, or decide the blocker needs a human.",
             "Exhaustion reason: %s (reroute %d/%d)."
             % (ctx.get("reason"), ctx.get("reroute"), ctx.get("max_reroutes")),
             "Candidate channels (current records):"]
    records = state.get("nodes", {}) if isinstance(state, dict) else {}
    for cand in ctx.get("pool") or []:
        rec = records.get(cand) or {}
        lines.append("- %s: verdict=%s summary=%s"
                     % (cand, rec.get("verdict"), (rec.get("summary") or "")[:120]))
    lines.append("")
    lines.append("Reply with exactly one line: 'NEXT: <channel id>' to reroute, or 'HUMAN'.")
    return "\n".join(lines)


def _identify(node_id, state, ctx):
    """mode=identify content leg. Asks the agent; deterministic fallback matches
    repo_checks.py (prefer a pool member still needing work, else first untried)."""
    fallback = {"status": "done", "verdict": "human", "summary": "no channels left",
                "evidence": ["identify:none"]}
    pool = ctx.get("pool") or []
    if not pool:
        return fallback

    def default_pick():
        records = state.get("nodes", {}) if isinstance(state, dict) else {}
        for cand in pool:
            rec = records.get(cand) or {}
            if rec.get("verdict") and rec.get("verdict") != "pass":
                return cand
        return pool[0]

    try:
        text, seconds = _call_agent(_identify_prompt(node_id, state, ctx))
    except (OSError, subprocess.TimeoutExpired) as exc:
        _record(node_id, "reroute", "identify fallback: %s" % exc, 0.0, fallback=True)
        cand = default_pick()
        return {"status": "done", "verdict": "reroute", "next": cand,
                "summary": "identified %s (agent unavailable, deterministic)" % cand,
                "evidence": ["identify-fallback:%s" % cand]}
    m = re.search(r"^NEXT:\s*([a-z0-9][a-z0-9-]*)", text or "", re.M | re.I)
    if m and m.group(1) in pool:
        _record(node_id, "reroute", text, seconds, fallback=False)
        return {"status": "done", "verdict": "reroute", "next": m.group(1),
                "summary": "identified %s" % m.group(1),
                "evidence": ["identify:%s" % m.group(1)]}
    if re.search(r"^HUMAN", text or "", re.M | re.I):
        _record(node_id, "human", text, seconds, fallback=False)
        return {"status": "done", "verdict": "human",
                "summary": "blocker needs a human", "evidence": ["identify:human"]}
    _record(node_id, "reroute", "identify unparseable, deterministic pick", seconds,
            fallback=True)
    cand = default_pick()
    return {"status": "done", "verdict": "reroute", "next": cand,
            "summary": "identified %s (unparseable reply, deterministic)" % cand,
            "evidence": ["identify-fallback:%s" % cand]}


def _trailer_result(node_id, text, ctx):
    """Map a parsed verify trailer onto the runner's result fields. Returns None when the reply
    carries no readable trailer, which is the "claim nothing" path.

    `criteria_met` is emitted ONLY when the trailer read cleanly. Each entry is the DECLARED
    criterion's own text - one of the three references `workflow-runner._criteria_covered` accepts
    (`1`, `c2`, or the criterion text), and the one that survives the runner's `_verification_evidence`
    mapping without inventing an index scheme. A criterion the agent claimed that the contract does
    not declare is deliberately NOT added: it would be reported as an unrecognized reference and
    turn a good answer into a violation.
    """
    criteria = _completion_criteria(ctx.get("skill"))
    parsed = _parse_verify_trailer(text, criteria)
    if parsed is None:
        return None
    reported, unmet, verify_result, claims, diagnostics = parsed
    # A failed verification result is not a claim of coverage, whatever the criterion lines say:
    # the marker is the template's own verdict on the whole check.
    met = reported if verify_result != "fail" else []
    diagnostics = list(diagnostics) + ["reported %d/%d criteria met" % (len(reported), len(criteria))]
    return {
        "criteria_met": met,
        "diagnostics": diagnostics,
        "unmet": unmet,
        "verify_result": verify_result,
        "evidence": ["agent-reply:%s sha256=%s" % (node_id, _reply_digest(text))]
                    + claims,
    }


def execute_node(node_id, state, ctx):
    if ctx and ctx.get("mode") == "identify":
        return _identify(node_id, state, ctx)
    prompt, skill_words = _context_prompt(node_id, state, ctx)
    try:
        text, seconds = _call_agent(prompt)
        if "Verdict: pass" in text:
            verdict = "pass"
        elif "Verdict: changes_requested" in text:
            verdict = "changes_requested"
        else:
            # agent answered but not with a parseable verdict: treat as needs work
            _record(node_id, "changes_requested", text, seconds, fallback=False,
                    prompt_words=skill_words, skill=ctx.get("skill"))
            return {"status": "needs_review", "verdict": "unparseable_verdict",
                    "summary": (text or "")[:400],
                    "evidence": ["agent-turn:%s" % node_id]}
        _record(node_id, verdict, text, seconds, fallback=False,
                prompt_words=skill_words, skill=ctx.get("skill"))
        trailer = _trailer_result(node_id, text, ctx)
        if trailer is None:
            # NO readable trailer: exactly the pre-existing result. `criteria_met` stays absent
            # rather than empty, so `--enforce-contracts` still refuses the node - the honest
            # outcome, because no coverage was claimed.
            return {"status": "done", "verdict": verdict, "summary": (text or "")[:400],
                    "evidence": ["agent-turn:%s" % node_id]}
        result = {"status": "done", "verdict": verdict, "summary": (text or "")[:400],
                  "evidence": trailer["evidence"], "criteria_met": trailer["criteria_met"],
                  "diagnostics": trailer["diagnostics"]}
        return result
    except (OSError, subprocess.TimeoutExpired) as exc:
        seconds = 0.0
        reason = "%s" % exc
        if not AGENT_FALLBACK:
            raise
        _record(node_id, "pass", "fallback (stub): %s" % reason, seconds, fallback=True,
                prompt_words=skill_words, skill=ctx.get("skill"))
        return {"status": "done", "verdict": "pass",
                "summary": "agent call unavailable (%s); deterministic stub fallback" % reason,
                "evidence": ["fallback:%s" % node_id]}


# ---------------------------------------------------------------- depth report
# The measurable form of the truncation fix: the same skill, the legacy first-N-words cut and
# the depth-aware selection side by side, with each high-signal probe resolved. Deterministic
# and network-free, so it doubles as the executor's self-test.

_PROBES = {
    "completion criteria": "Complete when",
    "ground rules": "Ground Rules",
    "decision trees": "Decision Tree",
    "core workflow": "Core Workflow",
}

_DEFAULT_SAMPLE = [
    "multi-agent-orchestration",  # 9,283-word body: the legacy cut drops every probe
    "incremental-implementation",
    "code-reviewer",
    "caching-architect",
]


def depth_report(sample=None, budget=None):
    """Print legacy-vs-depth-aware excerpts for a sample of skills. Returns an exit code:
    0 when every sampled skill kept its high-signal sections, 1 when any lost them."""
    sample = sample or _DEFAULT_SAMPLE
    budget = AGENT_SKILL_WORDS if budget is None else budget
    print("depth-aware selection: %s | word budget: %d | words are the word-count heuristic, "
          "not tokens" % ("on" if AGENT_SKILL_DEPTH else "OFF (legacy)", budget))
    rc = 0
    for skill in sample:
        body = next((b for b in _skill_bodies(skill) if b.strip()), "")
        if not body.strip():
            print("\n%-32s SKIPPED (no SKILL.md body or compiled XML found)" % skill)
            continue
        legacy, lw = _truncate_words(body, budget)
        if AGENT_SKILL_DEPTH:
            new, nw = _load_skill_text(skill, budget)
        else:
            new, nw = legacy, lw
        print("\n%-32s body %5d words | legacy cut %4d | depth-aware %4d"
              % (skill, len(body.split()), lw, nw))
        lost = []
        for label, probe in _PROBES.items():
            in_legacy, in_new = probe in legacy, probe in new
            if in_new and not in_legacy:
                lost.append(label)
            print("    %-20s legacy=%-3s depth-aware=%-3s%s"
                  % (label, "yes" if in_legacy else "no", "yes" if in_new else "no",
                     "   <-- RECOVERED" if in_new and not in_legacy else
                     "   <-- LOST" if in_legacy and not in_new else ""))
        if any(probe not in new for probe in _PROBES.values()):
            rc = 1
        print("    section headings kept: %d" % len(re.findall(r"(?m)^## .+$", new)))
    return rc


def _selftest_reply(criteria, met, verdict="pass"):
    """A well-formed trailer for `criteria`, met indexes are 1-based positions into it."""
    lines = ["[VERIFY: %d/%d criteria met]" % (len(met), len(criteria))]
    for i, c in enumerate(criteria, 1):
        if i in met:
            lines.append("  criterion: %s" % c)
            lines.append("  evidence: check-%d output" % i)
        else:
            lines.append("  criterion: %s" % c)
            lines.append("  unmet: %s" % c)
    lines.append("[VERIFY RESULT: %s]" % verdict)
    lines.append("Verdict: %s" % ("pass" if verdict == "pass" else "changes_requested"))
    return "\n".join(lines)


def selftest():
    """Trailer parsing / fallback matrix, without calling an agent. Exit 0 when all checks pass.

    Two of the three branches are asserted through `execute_node` itself, with `_call_agent`
    monkeypatched to a canned reply, so the test pins the real result shape the runner consumes
    rather than a helper's return value.
    """
    results = []

    def check(name, ok):
        results.append((name, bool(ok)))

    saved_call, saved_transcript = _call_agent, AGENT_TRANSCRIPT
    # `_call_agent` returns `proc.stdout.strip()`, and these canned replies stand in for it, so the
    # stub strips too - otherwise the test would assert a summary the real path can never produce.
    globals()["_call_agent"] = lambda prompt: (CANNED[0].strip(), 0.0)
    globals()["AGENT_TRANSCRIPT"] = os.devnull        # never write into the checkout
    CANNED = [""]
    skill = "code-reviewer"
    criteria = _completion_criteria(skill)
    ctx = {"skill": skill}
    state = {"workflow": "selftest"}
    try:
        check("the sampled skill declares completion criteria to report",
              len(criteria) >= 1)

        # (a) a well-formed trailer: full coverage + real evidence; the runner must be satisfiable.
        CANNED[0] = _selftest_reply(criteria, met=range(1, len(criteria) + 1))
        result = execute_node("review", state, ctx)
        check("(a) a well-formed trailer yields criteria_met covering every declared criterion",
              sorted(result.get("criteria_met") or []) == sorted(criteria))
        check("(a) the trailer's evidence is not the agent-turn stub",
              bool(result.get("evidence"))
              and all(e.startswith(("agent-reply:", "agent-claim:")) for e in result["evidence"])
              and not any(e == "agent-turn:review" for e in result["evidence"]))
        check("(a) the reply digest is recorded, so the claim names a specific turn",
              any(e.startswith("agent-reply:review sha256=") for e in result["evidence"]))
        check("(a) one evidence line per claimed criterion",
              len([e for e in result["evidence"] if e.startswith("agent-claim:")]) == len(criteria))
        check("(a) the verdict line is still parsed as before", result.get("verdict") == "pass")

        # (b) a MALFORMED trailer: no coverage claimed, the pre-existing verdict preserved.
        CANNED[0] = ("I reviewed it.\n[VERIFY: no idea]\nVerdict: pass\n")
        malformed = execute_node("review", state, ctx)
        check("(b) a malformed trailer claims no coverage (criteria_met absent)",
              "criteria_met" not in malformed)
        check("(b) a malformed trailer falls back to the agent-turn evidence shape",
              malformed.get("evidence") == ["agent-turn:review"])
        check("(b) a malformed trailer keeps today's verdict and status",
              malformed.get("verdict") == "pass" and malformed.get("status") == "done")

        # (b2) a trailer about a DIFFERENT criteria list is also refused, not guessed at.
        wrong_n = len(criteria) + 1
        CANNED[0] = ("[VERIFY: %d/%d criteria met]\n" % (wrong_n, wrong_n)
                     + "".join("  criterion: %s\n  evidence: e\n" % c for c in criteria)
                     + "  criterion: extra\n  evidence: e\n"
                     + "[VERIFY RESULT: pass]\nVerdict: pass\n")
        check("(b2) a header naming a different criteria count claims no coverage",
              "criteria_met" not in execute_node("review", state, ctx))

        # (b3) a partial trailer claims only what it covered - the runner names the rest.
        if len(criteria) >= 2:
            CANNED[0] = _selftest_reply(criteria, met=[1])
            partial = execute_node("review", state, ctx)
            check("(b3) a partial trailer claims exactly the covered criteria",
                  partial.get("criteria_met") == [criteria[0]])
            check("(b3) an unmet criterion is named in diagnostics, not silently dropped",
                  any(criteria[1] in d for d in partial.get("diagnostics") or []))

        # (b4) a claim the contract never declared is a diagnostic, NOT coverage.
        if criteria:
            CANNED[0] = ("[VERIFY: %d/%d criteria met]\n" % (len(criteria), len(criteria))
                         + "".join("  criterion: %s\n  evidence: e\n" % c for c in criteria)
                         + "  criterion: invented criterion\n  evidence: e\n"
                         + "[VERIFY RESULT: pass]\nVerdict: pass\n")
            undeclared = execute_node("review", state, ctx)
            check("(b4) a criterion outside the contract is never added to criteria_met",
                  undeclared.get("criteria_met") == criteria)
            check("(b4) the criterion outside the contract is named in diagnostics",
                  any("not declared" in d for d in undeclared.get("diagnostics") or []))

        # (b5) [VERIFY RESULT: fail] is not coverage, whatever the criterion lines claim.
        CANNED[0] = _selftest_reply(criteria, met=range(1, len(criteria) + 1), verdict="fail")
        failed = execute_node("review", state, ctx)
        check("(b5) a failed verify result claims no coverage",
              failed.get("criteria_met") == [])

        # (c) NO trailer: byte-identical to the pre-change result shape for the same reply.
        CANNED[0] = "Did the work.\nVerdict: pass\n"
        plain = execute_node("review", state, ctx)
        check("(c) no trailer reproduces today's result exactly",
              plain == {"status": "done", "verdict": "pass",
                        "summary": "Did the work.\nVerdict: pass",
                        "evidence": ["agent-turn:review"]})
        CANNED[0] = "Could not finish.\nVerdict: changes_requested\n"
        plain2 = execute_node("review", state, ctx)
        check("(c) no trailer with changes_requested is unchanged too",
              plain2 == {"status": "done", "verdict": "changes_requested",
                         "summary": "Could not finish.\nVerdict: changes_requested",
                         "evidence": ["agent-turn:review"]})
        CANNED[0] = "no verdict line at all"
        plain3 = execute_node("review", state, ctx)
        check("(c) an unparseable reply is still needs_review/unparseable_verdict",
              plain3 == {"status": "needs_review", "verdict": "unparseable_verdict",
                         "summary": "no verdict line at all",
                         "evidence": ["agent-turn:review"]})

        # (d) a skill with no workflow: contract asks for no criteria and claims none.
        check("(d) a contract-less skill declares no criteria",
              _completion_criteria("using-agent-skills") == [])
        CANNED[0] = "Done.\n[VERIFY: 0/0 criteria met]\n[VERIFY RESULT: pass]\nVerdict: pass\n"
        nocontract = execute_node("gate", {"workflow": "selftest"}, {"skill": "using-agent-skills"})
        check("(d) a contract-less node's empty trailer is not an error",
              nocontract.get("criteria_met") == [])
    finally:
        globals()["_call_agent"] = saved_call
        globals()["AGENT_TRANSCRIPT"] = saved_transcript
        CANNED.clear()

    failed = [name for name, ok in results if not ok]
    for name, ok in results:
        print("%s %s" % ("PASS" if ok else "FAIL", name))
    print("selftest: %d checks, %d failed" % (len(results), len(failed)))
    return 1 if failed else 0


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] in ("--depth-report", "report"):
        sample = [a for a in argv[1:] if not a.isdigit()]
        budget = next((int(a) for a in argv[1:] if a.isdigit()), None)
        return depth_report(sample or None, budget)
    if argv and argv[0] == "--selftest":
        return selftest()
    print(__doc__.strip())
    print("\nRun `python3 %s --depth-report [skill ...] [budget]` to compare the legacy and "
          "depth-aware excerpts." % os.path.basename(__file__))
    print("Run `python3 %s --selftest` to check trailer parsing without calling any agent."
          % os.path.basename(__file__))
    return 0


if __name__ == "__main__":
    import sys
    raise SystemExit(main())
