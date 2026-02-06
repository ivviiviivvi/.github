"""Generate a chatmode inventory table from frontmatter."""

from __future__ import annotations

import re
from pathlib import Path

CHATMODES_DIR = Path("src/ai_framework/chatmodes")
OUTPUT = Path("src/ai_framework/chatmodes/INVENTORY.md")
_DELIMITER_RE = re.compile(r"^(?:---|_{5,})$")
_KNOWN_KEYS = ("name", "description", "model", "tools", "tags", "updated")
_KEY_BOUNDARY_RE = re.compile(r"\b(" + "|".join(sorted(_KNOWN_KEYS)) + r"):\s*", re.IGNORECASE)


def _parse_joined_block(text: str) -> dict[str, object]:
    """Parse a block by splitting on known key boundaries."""
    positions = [(m.start(), m.end(), m.group(1).lower()) for m in _KEY_BOUNDARY_RE.finditer(text)]
    if not positions:
        return {}
    result: dict[str, object] = {}
    for idx, (_start, end, key) in enumerate(positions):
        value_end = positions[idx + 1][0] if idx + 1 < len(positions) else len(text)
        raw = text[end:value_end].strip()
        # Check if value is a list (lines starting with "- ")
        list_items = re.findall(r"^-\s+(.+)$", raw, re.MULTILINE)
        if list_items and (not raw or raw.startswith("-") or raw.startswith("\n")):
            result[key] = list_items
        elif list_items and "\n-" in raw:
            # Value has leading text then list items; keep just the list
            result[key] = list_items
        else:
            # Collapse multi-line text into single line
            result[key] = " ".join(raw.split())
    return result


def parse_frontmatter(lines: list[str]) -> dict[str, object]:
    data: dict[str, object] = {}
    if not lines or not _DELIMITER_RE.match(lines[0].strip()):
        return data
    end_idx = None
    for i in range(1, len(lines)):
        if _DELIMITER_RE.match(lines[i].strip()):
            end_idx = i
            break
    if end_idx is None:
        return data

    block = lines[1:end_idx]
    # Check if this uses --- (standard YAML) or ______ (concatenated format)
    is_yaml = lines[0].strip() == "---"

    if is_yaml:
        # Standard YAML-style: parse line by line
        i = 0
        while i < len(block):
            line = block[i].rstrip()
            if not line or line.lstrip().startswith("#"):
                i += 1
                continue
            if re.match(r"^[a-z0-9_-]+:\s*$", line):
                key = line.split(":", 1)[0].strip()
                values: list[str] = []
                j = i + 1
                while j < len(block) and block[j].startswith("  - "):
                    values.append(block[j].replace("  - ", "", 1).strip())
                    j += 1
                data[key] = values
                i = j
                continue
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()
            i += 1
    else:
        # Concatenated format: join all lines then split by key boundaries
        joined = "\n".join(block)
        data = _parse_joined_block(joined)

    return data


def main() -> None:
    rows = []
    for path in sorted(CHATMODES_DIR.glob("*.chatmode.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        fm = parse_frontmatter(lines)
        name = str(fm.get("name", ""))
        description = str(fm.get("description", ""))
        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags_list = [tags]
        elif isinstance(tags, list):
            tags_list = tags
        else:
            tags_list = []
        tags_text = ", ".join(tags_list)
        rows.append((path.name, name, description, tags_text))

    header = "# Chatmode Inventory\n\n"
    header += "| File | Name | Description | Tags |\n"
    header += "| --- | --- | --- | --- |\n"

    lines = [header]
    for filename, name, description, tags in rows:
        lines.append(f"| `{filename}` | {name} | {description} | {tags} |\n")

    OUTPUT.write_text("".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
