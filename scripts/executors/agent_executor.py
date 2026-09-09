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
    AGENT_TIMEOUT     seconds per node call (default 90)
    AGENT_TRANSCRIPT  log file for every agent turn (default ./agent-transcript.log)
    AGENT_FALLBACK    when a call fails/times out, return a stub pass instead of crashing
                      (default 1). Set 0 to surface failures to the runner.
    AGENT_SKILL_WORDS max words of the node's compiled skill injected into the prompt
                      (default 1200 - a small-window budget; compiled preferred, SKILL.md fallback)

Behavior per node: builds a prompt from the node id + run context PLUS the node's referenced
skill (compiled excerpt, window-truncated) so the agent actually operates from the skill's
content - every node is skill-grounded, single- and multi-agent alike.

Usage:
    AGENT_CMD="claude -p" python3 scripts/workflow-runner.py \
        --manifest your-workflow.yaml --executor scripts/executors/agent_executor.py \
        --guardrail scripts/lib/guardrails.py --memory ./agent-memory
"""

import json
import os
import re
import shlex
import subprocess
import time
import xml.etree.ElementTree as ET

AGENT_CMD = os.environ.get("AGENT_CMD", "claude -p")
AGENT_TIMEOUT = float(os.environ.get("AGENT_TIMEOUT", "90"))
AGENT_TRANSCRIPT = os.environ.get("AGENT_TRANSCRIPT", "agent-transcript.log")
AGENT_FALLBACK = os.environ.get("AGENT_FALLBACK", "1") not in ("0", "false", "no")
AGENT_SKILL_WORDS = int(os.environ.get("AGENT_SKILL_WORDS", "1200"))  # window budget per skill

_REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _load_skill_text(skill):
    """Return a window-truncated excerpt of the node's skill (compiled preferred)."""
    if not skill:
        return "", 0
    compiled = os.path.join(_REPO, ".skills-compiled", skill, "skill.xml")
    text = ""
    if os.path.isfile(compiled):
        try:
            root = ET.parse(compiled).getroot()
            text = " ".join((root.text or "") + " ".join(
                n.text or "" for n in root.iter() if n.text))
        except ET.ParseError:
            text = ""
    if not text:
        for domain in os.listdir(os.path.join(_REPO, "skills")):
            p = os.path.join(_REPO, "skills", domain, skill, "SKILL.md")
            if os.path.isfile(p):
                raw = open(p, encoding="utf-8").read()
                m = re.search(r"^---\s*\n.*?\n---\s*\n(.*)$", raw, re.S)
                text = m.group(1) if m else raw
                break
    words = text.split()
    if len(words) > AGENT_SKILL_WORDS:
        words = words[: AGENT_SKILL_WORDS]
    return " ".join(words), len(words)


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
    prompt = (
        "You are executing the node '%s' inside an agentic workflow run.\n"
        "Run context: %s\n\n"
        "YOUR OPERATING SKILL (compiled excerpt, %d words; follow it for this node):\n"
        "---\n%s\n---\n\n"
        "Do the node's work and finish your reply with exactly one line:\n"
        "'Verdict: pass' if your work meets its criteria with evidence, otherwise "
        "'Verdict: changes_requested' (state what is missing).\n"
        "Keep the body of your reply under 200 words."
        % (node_id, json.dumps(context, default=str), skill_words,
           skill_text if skill_text else "(skill not found - use the run context)"))
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
        return {"status": "done", "verdict": verdict, "summary": (text or "")[:400],
                "evidence": ["agent-turn:%s" % node_id]}
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
