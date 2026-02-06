"""Generate a collection inventory table from frontmatter."""

from __future__ import annotations

import re
from pathlib import Path

COLLECTIONS_DIR = Path("src/ai_framework/collections")
OUTPUT = Path("src/ai_framework/collections/INVENTORY.md")
_DELIMITER_RE = re.compile(r"^(?:---|_{5,})$")
_KNOWN_KEYS = ("name", "description", "model", "tools", "tags", "updated")
_KEY_BOUNDARY_RE = re.compile(r"\b(" + "|".join(sorted(_KNOWN_KEYS)) + r"):\s*", re.IGNORECASE)


def parse_frontmatter(lines: list[str]) -> dict[str, object]:
    data: dict[str, object] = {}
    if not lines or not _DELIMITER_RE.match(lines[0].strip()):
        return data
    is_yaml = lines[0].strip() == "---"

    if is_yaml:
        # Standard YAML: require closing ---
        end_idx = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end_idx = i
                break
        if end_idx is None:
            return data
        i = 1
        while i < end_idx:
            line = lines[i].rstrip()
            if not line or line.lstrip().startswith("#"):
                i += 1
                continue
            if re.match(r"^[a-z0-9_-]+:\s*$", line):
                key = line.split(":", 1)[0].strip()
                values: list[str] = []
                j = i + 1
                while j < end_idx and lines[j].startswith("  - "):
                    values.append(lines[j].replace("  - ", "", 1).strip())
                    j += 1
                data[key] = values
                i = j
                continue
            if ":" in line:
                key, value = line.split(":", 1)
                data[key.strip()] = value.strip()
            i += 1
    else:
        # Concatenated format (______): find end at closing delimiter or heading
        end_idx = len(lines)
        for i in range(1, len(lines)):
            stripped = lines[i].strip()
            if _DELIMITER_RE.match(stripped):
                end_idx = i
                break
            if stripped.startswith("# ") and not stripped.startswith("## "):
                end_idx = i
                break
        block = lines[1:end_idx]
        cleaned_lines = [re.sub(r"^##\s+", "", line.rstrip()) for line in block]
        joined = "\n".join(cleaned_lines)
        positions = [(m.start(), m.end(), m.group(1).lower()) for m in _KEY_BOUNDARY_RE.finditer(joined)]
        for idx, (_start, end, key) in enumerate(positions):
            value_end = positions[idx + 1][0] if idx + 1 < len(positions) else len(joined)
            raw = joined[end:value_end].strip()
            list_items = re.findall(r"^-\s+(.+)$", raw, re.MULTILINE)
            if list_items and (not raw or raw.startswith("-") or raw.startswith("\n")):
                data[key] = list_items
            elif list_items and "\n-" in raw:
                data[key] = list_items
            else:
                value = " ".join(raw.split())
                value = value.replace("\\[", "[").replace("\\]", "]")
                data[key] = value

    return data


def main() -> None:
    rows = []
    for path in sorted(COLLECTIONS_DIR.glob("*.*")):
        if not (path.name.endswith(".md") or path.name.endswith(".yml")):
            continue
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

    header = "# Collection Inventory\n\n"
    header += "| File | Name | Description | Tags |\n"
    header += "| --- | --- | --- | --- |\n"

    lines = [header]
    for filename, name, description, tags in rows:
        lines.append(f"| `{filename}` | {name} | {description} | {tags} |\n")

    OUTPUT.write_text("".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
