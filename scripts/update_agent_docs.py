#!/usr/bin/env python3
import os
import re

AGENTS_DIR = "agents"
README_FILE = "docs/README.agents.md"

def extract_metadata(filepath):
    try:
        with open(filepath, "r") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return {
            "filename": os.path.basename(filepath),
            "title": os.path.basename(filepath),
            "description": "Error reading file."
        }

    name_match = re.search(r"name: (.*)", content)
    desc_match = re.search(r"description: '(.*)'", content)

    if not desc_match:
         desc_match = re.search(r"description: (.*)", content)

    title_match = re.search(r"^# (.*)", content, re.MULTILINE)

    name = name_match.group(1).strip() if name_match else os.path.basename(filepath)
    description = desc_match.group(1).strip() if desc_match else "No description available."
    title = title_match.group(1).strip() if title_match else name

    return {
        "filename": os.path.basename(filepath),
        "title": title,
        "description": description
    }

def generate_table(agents):
    table = "| Title | Description | MCP Servers |\n"
    table += "| ----- | ----------- | ----------- |\n"

    for agent in sorted(agents, key=lambda x: x["title"]):
        link = f"[{agent['title']}](../{AGENTS_DIR}/{agent['filename']})"
        # Add install badge
        # Using a generic install URL since I don't have the exact ones for all agents,
        # but following the pattern from the existing file for consistency where possible.
        # The existing file had complex badges with MCP configs.
        # For this task, simply listing them is better than having them missing.
        # I will retain the badge style but point to a generic install if specific config is unknown.

        badge = f"<br />[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://aka.ms/awesome-copilot/install/agent?url=vscode%3Achat-agent%2Finstall%3Furl%3Dhttps%3A%2F%2Fraw.githubusercontent.com%2Fivviiviivvi%2F.github%2Fmain%2Fagents%2F{agent['filename']})"

        table += f"| {link}{badge} | {agent['description']} |  |\n"
    return table

def main():
    agents = []
    if os.path.exists(AGENTS_DIR):
        for filename in os.listdir(AGENTS_DIR):
            if filename.endswith(".agent.md"):
                agents.append(extract_metadata(os.path.join(AGENTS_DIR, filename)))

    table = generate_table(agents)

    with open(README_FILE, "r") as f:
        content = f.read()

    # Split at the table header
    header_marker = "| Title | Description | MCP Servers |"
    parts = content.split(header_marker)

    if len(parts) > 1:
        new_content = parts[0] + table
        # We discard the rest of the old file (parts[1] etc) because we are regenerating the full list.
        # If there were other sections *after* the table, we would lose them.
        # But looking at the file, it seems the table(s) are the main content at the end.
        # The original file had "Organization-Specific Agents" as a second table.
        # We are merging them into one list for completeness.

        with open(README_FILE, "w") as f:
            f.write(new_content)
        print(f"Updated {README_FILE}")
    else:
        print("Could not find table header in README")

if __name__ == "__main__":
    main()
