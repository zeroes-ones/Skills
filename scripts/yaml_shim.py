#!/usr/bin/env python3
"""yaml_shim.py — stdlib-only stand-in for the small PyYAML subset used by governance checks.

validate-skills.sh imports the real `yaml` module first and falls back to this
module only on ImportError, so CI (which installs PyYAML) is byte-for-byte
unchanged. This shim exists so the suite also runs to completion in
environments where PyYAML is unavailable (e.g. offline sandboxes), instead of
crashing every YAML-dependent check with ModuleNotFoundError.

Implements only what the checks use:
    safe_load(text) -> dict   (SKILL.md frontmatter, no document markers needed)
    YAMLError                  (exception type, raised on structurally missing frontmatter)

The parser mirrors scripts/_compile_skill.py::parse_frontmatter, which is proven
over the whole corpus: it handles `key: value`, `key: >` multiline values,
`key:` + `- item` lists, and the nested `chain:` block (consumes_from /
feeds_into). Bare numeric scalars are coerced to int/float like PyYAML would.

Known, accepted divergence from real PyYAML (documented, local-env only):
malformed YAML that PyYAML would reject is parsed leniently here, so the
"valid YAML" check is weaker in shim mode; key-presence checks are equivalent.
"""

import re

__all__ = ["safe_load", "YAMLError"]


class YAMLError(Exception):
    """Raised when no parseable frontmatter is present."""


def _scalar(value):
    """Coerce a bare numeric scalar to int/float the way PyYAML would."""
    v = value.strip()
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d+\.\d+", v):
        return float(v)
    return v


def _flow_list(value):
    """Parse a YAML flow-style sequence '[a, "b", c]' into a list of strings."""
    m = re.search(r"\[(.*)\]", value.strip(), re.DOTALL)
    if not m:
        return None
    items = []
    for raw in m.group(1).split(","):
        item = raw.strip().strip('"').strip("'").strip()
        if item:
            items.append(item)
    return items


def _parse(raw):
    """Parse raw frontmatter text (without --- delimiters) into a dict."""
    data = {}
    lines = raw.split("\n")
    i, n = 0, len(lines)

    def _is_blank(l):
        return not l.strip()

    def _key_line(l):
        return re.match(r"^(\w[\w_-]*):\s*(.*)$", l)

    def _is_bullet(l):
        # Flush-left ('- item') and indented ('  - item') YAML block bullets.
        return re.match(r"^\s*-\s+", l) is not None

    while i < n:
        line = lines[i]
        if _is_blank(line):
            i += 1
            continue
        m = _key_line(line)
        if not m:
            i += 1
            continue
        key, rest = m.group(1), m.group(2).strip()

        # Block/folded scalar marker: 'key: >', 'key: >-', 'key: |', 'key: |-'.
        if re.match(r"^([>|])(-?)$", rest):
            collected = []
            j = i + 1
            while j < n:
                l2 = lines[j]
                if _is_blank(l2):
                    j += 1
                    continue
                if not re.match(r"^\s{2,}\S", l2):
                    break
                collected.append(l2.strip())
                j += 1
            data[key] = " ".join(collected)
            i = j
            continue

        # 'key:' with no value -> a block list of '- item' lines.
        if rest == "":
            collected = []
            j = i + 1
            while j < n and _is_bullet(lines[j]):
                collected.append(re.match(r"^\s*-\s+(.*)", lines[j]).group(1).strip())
                j += 1
            data[key] = collected
            i = j
            continue

        # Flow-style list value: '[a, "b", c]'.
        fl = _flow_list(rest)
        if fl is not None:
            data[key] = fl
            i += 1
            continue

        # Single/double-quoted scalar, possibly spanning multiple lines.
        if rest[:1] in ("'", '"'):
            q = rest[0]
            if len(rest) >= 2 and rest[-1] == q and not rest[-2:] == q + q:
                data[key] = rest[1:-1].strip()
                i += 1
                continue
            parts = [rest[1:]]
            j = i + 1
            while j < n:
                t = lines[j].strip()
                if t.endswith(q) and not t.endswith("\\" + q):
                    parts.append(t[:-1])
                    j += 1
                    break
                parts.append(t)
                j += 1
            data[key] = " ".join(p.strip() for p in parts).strip()
            i = j
            continue

        # Plain scalar with indented continuation lines (YAML folding).
        parts = [rest]
        j = i + 1
        while j < n:
            l2 = lines[j]
            if (re.match(r"^\s{2,}\S", l2) and not _is_bullet(l2)
                    and not re.match(r"^\s+[\w_-]+:", l2)):
                parts.append(l2.strip())
                j += 1
            else:
                break
        data[key] = _scalar(" ".join(parts))
        i = j

    # Nested chain block: chain: -> consumes_from/feeds_into (flow '[a,b]' or bullet '- a' style),
    # with interleaved non-edge subkeys (examples:, type:, portability:) whose bullets must be ignored.
    chain_match = re.search(r"^chain:\s*\n((?:\s+.*\n)*)", raw, re.MULTILINE)
    if chain_match:
        consumes = []
        feeds = []
        seen_key = None
        for line in chain_match.group(1).split("\n"):
            m_key = re.match(r"\s*(consumes_from|feeds_into):\s*(.*)", line)
            if m_key:
                seen_key = "consumes" if m_key.group(1) == "consumes_from" else "feeds"
                inline = _flow_list(m_key.group(2))
                if inline is not None:
                    target = consumes if seen_key == "consumes" else feeds
                    target.extend(inline)
                continue
            # Any other subkey (examples:, type:, ...) ends the current edge key.
            if re.match(r"\s*[A-Za-z_][\w-]*:", line):
                seen_key = None
                continue
            m_item = re.search(r"-\s+(.+)", line)
            if m_item and seen_key == "consumes":
                consumes.append(m_item.group(1).strip())
            elif m_item and seen_key == "feeds":
                feeds.append(m_item.group(1).strip())
        data["chain"] = {"consumes_from": consumes, "feeds_into": feeds}

    # Defensive: the generic loop may leave chain as an empty list when the
    # nested block is absent; checks expect a dict (or a missing key).
    if isinstance(data.get("chain"), list):
        data["chain"] = {}

    return data


def safe_load(text):
    """Parse frontmatter text (between --- delimiters) into a dict.

    Raises YAMLError if no frontmatter-shaped content is present.
    """
    if text is None or not text.strip():
        raise YAMLError("empty frontmatter")
    # Structural gate: at least one "key:" line must exist.
    if not re.search(r"^\w[\w_-]*:", text, re.MULTILINE):
        raise YAMLError("no YAML keys found")
    return _parse(text)
