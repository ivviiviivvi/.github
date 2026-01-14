"""Generate a collection inventory table from frontmatter."""

from __future__ import annotations

from pathlib import Path
import re

COLLECTIONS_DIR = Path("ai_framework/collections")
OUTPUT = Path("ai_framework/collections/INVENTORY.md")


def parse_frontmatter(lines: list[str]) -> dict[str, object]:
    data: dict[str, object] = {}
    if not lines or lines[0].strip() != "---":
        return data
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
        else:
            tags_list = list(tags)
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
