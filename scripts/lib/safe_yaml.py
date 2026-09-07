#!/usr/bin/env python3
"""
safe_yaml.py — Safe YAML Subset parser (stdlib only).

Parses the documented YAML subset used by workflow manifests and `workflow:` frontmatter
blocks (WORKFLOW-SYSTEM.md, Section 3):

- Scalars: quoted strings, bare strings (may contain spaces, `==`, `/`, `.`, `_`, `-`, `,`),
  integers, booleans (`true`/`false`), `null`/empty.
- Scalar-only flow lists: `[a, b, c]` as a value (no nesting, no flow maps).
- Structures: indentation-based maps and lists; one structural level of nesting inside each
  list item; values may nest one deeper level (lists inside maps, maps inside list items).
- Comments: full-line `#` comments and trailing ` # comment` (outside quotes).
- Rejected: tabs, anchors/aliases (`&`, `*`), flow maps (`{...}`), block scalars (`|`, `>`),
  multi-document files, duplicate keys.

Why a subset: manifests are validated and executed by dependency-free tooling, so the
parser must be small, strict, and auditable. Anything outside the subset is an error with a
line number — fail loud instead of mis-parsing.

Usage:
    from lib import safe_yaml
    data = safe_yaml.parse(open(path).read())     # dict / list / scalar
"""

import re

__all__ = ["parse", "parse_file", "SafeYamlError"]


class SafeYamlError(ValueError):
    """Raised when text is outside the Safe YAML Subset."""

    def __init__(self, message, line=None):
        self.message = message
        self.line = line
        where = "" if line is None else " (line %d)" % line
        super().__init__(message + where)


_KEY_RE = re.compile(r"^([^:#][^:]*?):(?:[ \t]*(.*))?$")
_INT_RE = re.compile(r"^-?\d+$")


def _strip_comment(body):
    """Remove a trailing comment outside quotes. A '#' starts a comment only when it is the
    first character of the body or preceded by whitespace."""
    quote = None
    for i, ch in enumerate(body):
        if quote:
            if ch == quote:
                quote = None
        elif ch in ("'", '"'):
            quote = ch
        elif ch == "#" and (i == 0 or body[i - 1] in " \t"):
            return body[:i].rstrip()
    return body.rstrip()


def _preprocess(text):
    lines = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            continue
        if raw.lstrip().startswith("#"):
            continue
        if "\t" in raw[: len(raw) - len(raw.lstrip(" \t"))]:
            raise SafeYamlError("tab indentation is not allowed", lineno)
        indent = len(raw) - len(raw.lstrip(" "))
        body = _strip_comment(raw[indent:])
        if not body:
            continue
        lines.append((indent, body, lineno))
    return lines


def _scalar(token, line):
    token = token.strip()
    if token == "":
        return None
    if len(token) >= 2 and token[0] == token[-1] and token[0] in ("'", '"'):
        return token[1:-1]
    # scalar-only flow list, e.g. [a, b, c] — no flow maps, no nesting
    if token.startswith("["):
        if not token.endswith("]"):
            raise SafeYamlError("unterminated flow list", line)
        inner = token[1:-1].strip()
        if inner == "":
            return []
        items = []
        for part in inner.split(","):
            part = part.strip()
            if part == "":
                raise SafeYamlError("empty item in flow list", line)
            if part.startswith(("[", "{")) or ":" in part:
                raise SafeYamlError("only scalar items allowed in flow lists", line)
            items.append(_scalar(part, line))
        return items
    if token.startswith("{"):
        raise SafeYamlError("flow maps are outside the Safe YAML Subset", line)
    low = token.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low in ("null", "none", "~"):
        return None
    if _INT_RE.match(token):
        return int(token)
    return token


class _Parser(object):
    def __init__(self, lines):
        self.lines = lines
        self.pos = 0

    def _peek(self):
        if self.pos < len(self.lines):
            return self.lines[self.pos]
        return None

    def parse_root(self):
        if not self.lines:
            return {}
        indent, body, _ = self.lines[0]
        if indent != 0:
            raise SafeYamlError("top-level content must start at column 0", self.lines[0][2])
        if body.startswith("- "):
            raise SafeYamlError("top-level content must be a mapping", self.lines[0][2])
        value, _ = self._parse_map(indent)
        if self.pos < len(self.lines):
            nxt = self.lines[self.pos]
            raise SafeYamlError("unexpected content at inconsistent indentation", nxt[2])
        return value

    def _parse_map(self, indent):
        """Parse a mapping whose keys sit at exactly `indent`. Returns (dict, consumed)."""
        result = {}
        while True:
            item = self._peek()
            if item is None or item[0] != indent:
                break
            _, body, lineno = item
            if body.startswith("- "):
                break
            m = _KEY_RE.match(body)
            if not m:
                raise SafeYamlError(
                    "expected 'key: value' at this indentation, got: %s" % body, lineno
                )
            key = m.group(1).strip()
            if key in result:
                raise SafeYamlError("duplicate key: %s" % key, lineno)
            raw_val = (m.group(2) or "").strip()
            self.pos += 1
            if raw_val == "":
                nxt = self._peek()
                if nxt is not None and nxt[0] > indent:
                    if nxt[1].startswith("- "):
                        result[key], _ = self._parse_list(nxt[0])
                    else:
                        result[key], _ = self._parse_map(nxt[0])
                else:
                    result[key] = None
            else:
                result[key] = _scalar(raw_val, lineno)
        return result, self.pos

    def _parse_list(self, indent):
        """Parse a list whose items sit at exactly `indent` and start with '- '. Returns
        (list, consumed)."""
        result = []
        while True:
            item = self._peek()
            if item is None or item[0] != indent:
                break
            _, body, lineno = item
            if not body.startswith("- "):
                break
            rest = body[2:].strip()
            self.pos += 1
            if rest == "":
                nxt = self._peek()
                if nxt is not None and nxt[0] > indent:
                    if nxt[1].startswith("- "):
                        result.append(self._parse_list(nxt[0])[0])
                    else:
                        result.append(self._parse_map(nxt[0])[0])
                else:
                    result.append(None)
                continue
            m = _KEY_RE.match(rest)
            if m and not rest.startswith("- "):
                entry = {}
                key = m.group(1).strip()
                raw_val = (m.group(2) or "").strip()
                if raw_val == "":
                    nxt = self._peek()
                    if nxt is not None and nxt[0] > indent:
                        if nxt[1].startswith("- "):
                            entry[key], _ = self._parse_list(nxt[0])
                        else:
                            entry[key], _ = self._parse_map(nxt[0])
                    else:
                        entry[key] = None
                else:
                    entry[key] = _scalar(raw_val, lineno)
                # Continuation keys of the same list-item mapping.
                while True:
                    nxt = self._peek()
                    if nxt is None or nxt[0] <= indent:
                        break
                    nind, nbody, nlineno = nxt
                    if nbody.startswith("- ") or not _KEY_RE.match(nbody):
                        break
                    nm = _KEY_RE.match(nbody)
                    nkey = nm.group(1).strip()
                    if nkey in entry:
                        raise SafeYamlError("duplicate key: %s" % nkey, nlineno)
                    nraw = (nm.group(2) or "").strip()
                    self.pos += 1
                    if nraw == "":
                        nn = self._peek()
                        if nn is not None and nn[0] > nind:
                            if nn[1].startswith("- "):
                                entry[nkey], _ = self._parse_list(nn[0])
                            else:
                                entry[nkey], _ = self._parse_map(nn[0])
                        else:
                            entry[nkey] = None
                    else:
                        entry[nkey] = _scalar(nraw, nlineno)
                result.append(entry)
            else:
                result.append(_scalar(rest, lineno))
        return result, self.pos


def parse(text):
    """Parse Safe-YAML-subset text into dict/list/scalar."""
    if not isinstance(text, str):
        raise TypeError("parse() expects str")
    lines = _preprocess(text)
    if not lines:
        return {}
    return _Parser(lines).parse_root()


def parse_file(path):
    with open(path, encoding="utf-8") as fh:
        return parse(fh.read())


if __name__ == "__main__":  # pragma: no cover - manual smoke test
    import json
    import sys

    print(json.dumps(parse_file(sys.argv[1]), indent=2, default=str))
