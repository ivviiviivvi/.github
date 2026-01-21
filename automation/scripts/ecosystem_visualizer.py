#!/usr/bin/env python3
"""
Ecosystem Visualizer - Creates visual maps of the organization ecosystem
Implements AI-GH-06: Ecosystem Integration & Architecture Monitoring
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class EcosystemVisualizer:
    """Generate visual representations of the ecosystem"""

    _WORKFLOW_BASE_PATH = "../.github/workflows/"

    # Configuration: Maximum workflows to display in Mermaid diagram.
    # Large organizations can have many workflows, and rendering all
    # in a single graph quickly becomes unreadable and hard to navigate.
    # This limit only affects the visualization: the full set of
    # workflows is still listed in "Active Workflows" section below.
    MAX_DIAGRAM_WORKFLOWS = 10

    # Workflow categories mapping
    WORKFLOW_CATEGORIES = {
        "🛡️": "Safeguards & Policies",
        "🔐": "Security",
        "♻️": "Reusable Workflows",
        "🤖": "AI Agents & Automation",
        "🚀": "CI/CD & Deployment",
        "🔀": "PR Management",
        "⏱️": "Scheduled Tasks",
        "💓": "Health & Metrics",
        "⚙️": "Utility & Other",
    }

    # Pre-compile regex patterns for performance
    # Order matters: first match wins
    WORKFLOW_PATTERNS = [
        ("🛡️", re.compile(r"^safeguard|policy")),
        ("🔐", re.compile(r"security|scan|codeql|semgrep|secret")),
        ("♻️", re.compile(r"reusable")),
        (
            "🤖",
            re.compile(
                r"gemini|claude|openai|perplexity|grok|jules|" r"copilot|agent|ai\-"
            ),
        ),
        ("🚀", re.compile(r"ci|test|build|deploy|release|publish|docker")),
        ("🔀", re.compile(r"pr-|pull-request|merge")),
        ("⏱️", re.compile(r"schedule|cron|daily|weekly|monthly")),
        ("💓", re.compile(r"health|check|monitor|metrics|dashboard|report")),
    ]

    # Optimization: Combined regex for O(1) matching vs O(N) loop
    # NOTE: This logic relies on each pattern being wrapped in exactly one capturing group.
    # Future patterns MUST NOT contain their own capturing groups '(...)' as this
    # will break the match.lastindex logic. Use non-capturing groups '(?:...)' instead.
    _PRIORITY_ORDER = [e for e, _ in WORKFLOW_PATTERNS]
    _WORKFLOW_REGEX = re.compile(
        "|".join(f"({p.pattern})" for _, p in WORKFLOW_PATTERNS)
    )

    # Technology icons (extendable)
    TECHNOLOGY_ICONS: Dict[str, str] = {}

    def __init__(self, report_path: Optional[Path] = None):
        self.report_path = report_path
        self.report_data = None

        if report_path and report_path.exists():
            with open(report_path) as f:
                self.report_data = json.load(f)

    def _calculate_relative_path(self, output_path: Path, target_path: str) -> str:
        """
        Calculate relative path from output_path to target_path.

        Args:
            output_path: Path where the dashboard will be written
            target_path: Target path relative to repository root
                        (e.g., '.github/workflows/')

        Returns:
            The correct relative path to use in links
        """
        if not output_path:
            # Default case - assume output is in reports/
            return f"../{target_path}"

        # Get the parent directory of the output file
        # This represents where the file will be located
        output_dir = output_path.parent

        # Normalize the path to handle both absolute and relative
        # paths consistently. We only care about the depth of the
        # directory structure, not the absolute location.
        # Convert Path('.') to empty to handle root level
        if output_dir == Path(".") or str(output_dir) == ".":
            depth = 0
        else:
            # Count directory levels by splitting on path separator
            # This works for both absolute and relative paths
            parts = str(output_dir).replace("\\", "/").strip("/").split("/")
            # Filter out empty parts
            parts = [p for p in parts if p and p != "."]
            depth = len(parts)

        # Build the relative path with the appropriate number of ../
        if depth == 0:
            # Root level - no parent references needed
            return target_path
        else:
            parent_refs = "../" * depth
            return f"{parent_refs}{target_path}"

    def generate_mermaid_diagram(self, output_path: Optional[Path] = None) -> str:
        """Generate Mermaid diagram of the ecosystem"""

        if not self.report_data or "ecosystem_map" not in self.report_data:
            return "No ecosystem data available"

        em = self.report_data["ecosystem_map"]

        # Calculate the correct relative path for workflow links
        workflow_dir = ".github/workflows/"
        if output_path:
            workflow_path = self._calculate_relative_path(output_path, workflow_dir)
        else:
            workflow_path = workflow_dir

        # Use a list for efficient string concatenation
        parts = []
        parts.append(
            """```mermaid
graph TD
    %% Styles
    classDef org fill:#0969da,stroke:#0969da,color:#fff,stroke-width:2px;
    classDef workflow fill:#8250df,stroke:#54aeff,color:#fff,stroke-width:1px;
    classDef agent fill:#1a7f37,stroke:#d4a72c,color:#fff,stroke-width:1px;
    classDef tech fill:#57606a,stroke:#4ac26b,color:#fff,stroke-width:1px;

    subgraph "GitHub Organization"
        ORG[Organization Root]:::org
    end

    subgraph "Automation Layer"
"""
        )

        # Add workflows (limited to MAX_DIAGRAM_WORKFLOWS)
        # Note: All workflows are listed in the "Active Workflows"
        # section below
        workflows = em.get("workflows", [])
        displayed_workflows = workflows[: self.MAX_DIAGRAM_WORKFLOWS]
        for i, workflow in enumerate(displayed_workflows):
            workflow_id = f"WF{i}"
            parts.append(f"        {workflow_id}[{workflow}]:::workflow\n")
            # Add click event to open workflow file
            click_target = f"{workflow_path}{workflow}"
            parts.append(
                f'        click {workflow_id} "{click_target}" ' f'"View Workflow"\n'
            )
            parts.append(f"        ORG --> {workflow_id}\n")

        parts.append("    end\n\n")

        # Add Copilot customizations
        parts.append(
            """    subgraph "GitHub Copilot Customizations"
"""
        )

        agents = em.get("copilot_agents", [])
        if agents:
            parts.append("        AGENTS[Agents]:::agent\n")
            parts.append(f"        AGENTS_COUNT[{len(agents)} agents]:::agent\n")
            parts.append("        AGENTS --> AGENTS_COUNT\n")
            parts.append("        ORG --> AGENTS\n")

        instructions = em.get("copilot_instructions", [])
        if instructions:
            parts.append("        INSTR[Instructions]:::agent\n")
            count_node = f"INSTR_COUNT[{len(instructions)} instructions]"
            parts.append(f"        {count_node}:::agent\n")
            parts.append("        INSTR --> INSTR_COUNT\n")
            parts.append("        ORG --> INSTR\n")

        prompts = em.get("copilot_prompts", [])
        if prompts:
            parts.append("        PROMPTS[Prompts]:::agent\n")
            parts.append(f"        PROMPTS_COUNT[{len(prompts)} prompts]:::agent\n")
            parts.append("        PROMPTS --> PROMPTS_COUNT\n")
            parts.append("        ORG --> PROMPTS\n")

        chatmodes = em.get("copilot_chatmodes", [])
        if chatmodes:
            parts.append("        CHATMODES[Chat Modes]:::agent\n")
            parts.append(f"        CHATMODES_COUNT[{len(chatmodes)} modes]:::agent\n")
            parts.append("        CHATMODES --> CHATMODES_COUNT\n")
            parts.append("        ORG --> CHATMODES\n")

        parts.append("    end\n\n")

        # Add technologies
        technologies = em.get("technologies", [])
        if technologies:
            parts.append(
                """    subgraph "Technologies"
"""
            )
            for i, tech in enumerate(technologies[:15]):  # Limit to 15
                tech_id = f"TECH{i}"
                parts.append(f"        {tech_id}[{tech}]:::tech\n")

            parts.append("    end\n")

        parts.append("```\n")

        return "".join(parts)

    def _render_grouped_section(self, items: List[Dict[str, Any]]) -> List[str]:
        """Helper to render grouped alerts/points"""
        parts = []

        # Group items by category
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for item in items:
            cat = item.get("category", "Unknown")
            if cat not in grouped:
                grouped[cat] = []
            grouped[cat].append(item)

        for category, grouped_items in grouped.items():
            # Determine highest severity for the category
            severities = [i.get("severity", "unknown").upper() for i in grouped_items]
            if "CRITICAL" in severities:
                severity = "CRITICAL"
            elif "HIGH" in severities:
                severity = "HIGH"
            elif "MEDIUM" in severities:
                severity = "MEDIUM"
            elif "LOW" in severities:
                severity = "LOW"
            else:
                severity = "UNKNOWN"

            severity_emojis = {
                "CRITICAL": "🔴",
                "HIGH": "🔴",
                "MEDIUM": "🟡",
                "LOW": "🟢",
            }
            emoji = severity_emojis.get(severity, "⚪")

            # UX Improvement: Use blockquotes for better visual distinction
            parts.append(f"> {emoji} **{category}** ({severity})\n")
            for item in grouped_items:
                parts.append(f"> - {item.get('description')}\n")
                if "recommendation" in item:
                    parts.append(f">   - 💡 *{item['recommendation']}*\n")
            parts.append("\n")

        return parts

    def _classify_workflow(self, workflow_name: str) -> Tuple[str, str]:
        """
        Classify a workflow based on its name using pre-compiled
        regex patterns. Returns tuple of (emoji, category_name).
        """
        name = workflow_name.lower()
        # Optimization: Use single regex pass with capturing groups
        match = self._WORKFLOW_REGEX.search(name)
        if match:
            # lastindex is 1-based index of the matching group
            emoji = self._PRIORITY_ORDER[match.lastindex - 1]
            return emoji, self.WORKFLOW_CATEGORIES[emoji]
        return "⚙️", self.WORKFLOW_CATEGORIES["⚙️"]

    def generate_dashboard_markdown(self, output_path: Optional[Path] = None) -> str:
        """Generate a comprehensive dashboard in Markdown"""

        if not self.report_data:
            return "No report data available"

        # Use a list for efficient string concatenation
        parts = []
        # Format timestamp
        timestamp = self.report_data.get("timestamp", "Unknown")
        try:
            if timestamp != "Unknown":
                dt = datetime.fromisoformat(timestamp)
                timestamp = dt.strftime("%B %d, %Y at %I:%M %p")
        except ValueError:
            pass

        parts.append(
            f"""# 🎯 Organization Ecosystem Dashboard

{self.generate_health_badge()}

**Last Updated**: {timestamp}
**Organization**: {self.report_data.get('organization', 'Unknown')}

---

## 📋 Table of Contents

- [Quick Stats](#-quick-stats)
- [Repository Health](#-repository-health)
- [Link Health](#-link-health)
- [Alerts](#-alerts)
- [Ecosystem Map](#-ecosystem-map)
- [Technology Coverage](#-technology-coverage)
- [Active Workflows](#-active-workflows)

---

## 📊 Quick Stats

"""
        )

        # Ecosystem stats
        if "ecosystem_map" in self.report_data:
            em = self.report_data["ecosystem_map"]
            parts.append(
                f"""| Category | Count |
|----------|-------|
| ⚡ GitHub Actions Workflows | {len(em.get('workflows', []))} |
| 🤖 Copilot Agents | {len(em.get('copilot_agents', []))} |
| 📝 Copilot Instructions | {len(em.get('copilot_instructions', []))} |
| 💬 Copilot Prompts | {len(em.get('copilot_prompts', []))} |
| 🎭 Copilot Chat Modes | {len(em.get('copilot_chatmodes', []))} |
| 🛠️  Technologies Supported | {len(em.get('technologies', []))} |

"""
            )
        parts.append("[⬆️ Back to Top](#organization-ecosystem-dashboard)\n\n")

        # Repository health
        parts.append("## 🏥 Repository Health\n\n")
        if (
            "repository_health" in self.report_data
            and self.report_data["repository_health"].get("total_repos", 0) > 0
        ):
            rh = self.report_data["repository_health"]
            total = rh.get("total_repos", 0)
            active = rh.get("active_repos", 0)
            stale = rh.get("stale_repos", 0)

            active_pct = (active / total * 100) if total > 0 else 0

            # Create progress bar
            bar_length = 20
            filled_length = int(bar_length * active_pct / 100)
            bar = "█" * filled_length + "░" * (bar_length - filled_length)

            parts.append(
                f"""{bar} {active_pct:.1f}%

| Status | Count | Percentage |
|--------|-------|------------|
| 🟢 Active (< 90 days) | {active} | {active_pct:.1f}% |
| 🟠 Stale (90+ days) | {stale} | {100 - active_pct:.1f}% |
| **Total** | **{total}** | **100%** |

### Health Score: {active_pct:.0f}/100

"""
            )
        else:
            error = self.report_data.get("repository_health", {}).get(
                "error", "No data available"
            )
            parts.append(f"⚠️ **Data Unavailable**: {error}\n\n")

        parts.append("[⬆️ Back to Top](#organization-ecosystem-dashboard)\n\n")

        # Link validation
        parts.append("## 🔗 Link Health\n\n")
        if (
            "link_validation" in self.report_data
            and self.report_data["link_validation"]
            and self.report_data["link_validation"].get("total_links", 0) > 0
        ):
            lv = self.report_data["link_validation"]
            total_links = lv.get("total_links", 0)
            valid = lv.get("valid", 0)
            broken = lv.get("broken", 0)

            valid_pct = (valid / total_links * 100) if total_links > 0 else 0

            # Create progress bar
            bar_length = 20
            filled_length = int(bar_length * valid_pct / 100)
            bar = "█" * filled_length + "░" * (bar_length - filled_length)

            parts.append(
                f"""{bar} {valid_pct:.1f}%

| Status | Count | Percentage |
|--------|-------|------------|
| ✅ Valid | {valid} | {valid_pct:.1f}% |
| ❌ Broken | {broken} | {100 - valid_pct:.1f}% |
| **Total** | **{total_links}** | **100%** |

"""
            )
            # Add broken links details
            broken_links = lv.get("broken_links", [])
            if broken_links:
                display_count = min(len(broken_links), 20)
                summary = f"View top {display_count} broken links " f"(of {broken})"
                parts.append(f"<details>\n<summary>{summary}</summary>\n\n")
                parts.append("| URL | Status |\n|---|---|\n")

                for link in broken_links[:display_count]:
                    url = link.get("url", "Unknown")
                    # Sanitize URL by stripping common trailing punctuation
                    url = url.rstrip(".,;:)")
                    status = link.get("status", "Unknown")

                    # Add status indicator
                    status_str = str(status)
                    if status_str.startswith("4"):
                        status_emoji = "🔴"  # Client Error
                    elif status_str.startswith("5"):
                        status_emoji = "💥"  # Server Error
                    else:
                        status_emoji = "⚠️"  # Unknown/Other

                    # Truncate long URLs for display
                    # (max 60 characters including ellipsis)
                    display_url = url if len(url) <= 60 else url[:57] + "..."
                    # Escape pipe characters for Markdown table
                    display_url = display_url.replace("|", "\\|")
                    row = f"| `{display_url}` | {status_emoji} {status} |\n"
                    parts.append(row)

                parts.append("\n</details>\n\n")
        else:
            no_data_msg = (
                "ℹ️ **No Data**: External link validation was "
                "skipped or found no links.\n\n"
            )
            parts.append(no_data_msg)

        parts.append("[⬆️ Back to Top](#organization-ecosystem-dashboard)\n\n")

        # Alerts
        blind_spots = self.report_data.get("blind_spots", [])
        shatter_points = self.report_data.get("shatter_points", [])

        parts.append("## ⚠️  Alerts\n\n")

        if not blind_spots and not shatter_points:
            parts.append("✅ No alerts found! The ecosystem is healthy.\n\n")
        else:
            if blind_spots:
                parts.append(f"### 🔦 Blind Spots ({len(blind_spots)})\n\n")
                parts.extend(self._render_grouped_section(blind_spots))

            if shatter_points:
                sp_count = len(shatter_points)
                parts.append(f"\n### 💥 Shatter Points ({sp_count})\n\n")
                parts.extend(self._render_grouped_section(shatter_points))

        parts.append("[⬆️ Back to Top](#organization-ecosystem-dashboard)\n\n")

        # Ecosystem diagram
        parts.append("\n## 🗺️  Ecosystem Map\n\n")

        # Add note about workflow display limit if there are more
        # workflows than the limit
        if "ecosystem_map" in self.report_data:
            em = self.report_data["ecosystem_map"]
            workflows = em.get("workflows", [])
            if len(workflows) > self.MAX_DIAGRAM_WORKFLOWS:
                msg1 = (
                    f"ℹ️  *The diagram below displays the first "
                    f"{self.MAX_DIAGRAM_WORKFLOWS} workflows for "
                    f"readability. "
                )
                parts.append(msg1)
                msg2 = (
                    f"All {len(workflows)} workflows are listed in "
                    f"the [Active Workflows](#-active-workflows) "
                    f"section.*\n\n"
                )
                parts.append(msg2)

        parts.append(self.generate_mermaid_diagram(output_path))
        legend = (
            "\n**Legend:** 🔵 Organization | 🟣 Workflow | "
            "🟢 AI Agent | 🔘 Technology\n"
        )
        parts.append(legend)
        parts.append("\n[⬆️ Back to Top](#organization-ecosystem-dashboard)\n")

        # Technology coverage
        parts.append("\n## 🛠️  Technology Coverage\n\n")
        if "ecosystem_map" in self.report_data:
            em = self.report_data["ecosystem_map"]
            technologies = em.get("technologies", [])

            if technologies:
                parts.append("Supported languages and frameworks:\n\n")

                # UX Improvement: Use list for small numbers,
                # table for large to avoid empty cells
                if len(technologies) <= 5:
                    for tech in technologies:
                        icon = self.TECHNOLOGY_ICONS.get(tech.lower(), "🔹")
                        parts.append(f"- {icon} `{tech}`\n")
                    parts.append("\n")
                else:
                    summary = f"View all {len(technologies)} technologies"
                    parts.append(f"<details>\n<summary>{summary}</summary>\n\n")

                    # Group into columns
                    cols = 4
                    for i in range(0, len(technologies), cols):
                        row_techs = technologies[i : i + cols]

                        # Pad with empty strings if needed
                        current_len = len(row_techs)
                        if current_len < cols:
                            row_techs.extend([""] * (cols - current_len))

                        formatted_cells = []
                        for t in row_techs:
                            if t:
                                default_icon = "🔹"
                                icon = self.TECHNOLOGY_ICONS.get(
                                    t.lower(), default_icon
                                )
                                formatted_cells.append(f"{icon} `{t}`")
                            else:
                                formatted_cells.append("")
                        row = "| " + " | ".join(formatted_cells) + " |\n"
                        parts.append(row)

                        if i == 0:
                            sep = "| " + " | ".join(["---"] * cols) + " |\n"
                            parts.append(sep)

                    parts.append("\n</details>\n")
            else:
                parts.append("No technologies detected.\n")
        else:
            parts.append("No technology data available.\n")

        back_to_top1 = "\n[⬆️ Back to Top](#organization-ecosystem-dashboard)\n"
        parts.append(back_to_top1)

        # Top workflows
        parts.append("\n## ⚙️  Active Workflows\n\n")
        if "ecosystem_map" in self.report_data:
            em = self.report_data["ecosystem_map"]
            workflows = em.get("workflows", [])

            if workflows:
                # Calculate the correct relative path for workflow links
                if output_path:
                    workflow_path = self._calculate_relative_path(
                        output_path, ".github/workflows/"
                    )
                else:
                    workflow_path = ".github/workflows/"

                summary = f"View all {len(workflows)} workflows"
                parts.append(f"<details>\n<summary>{summary}</summary>\n\n")

                # UX Improvement: Single source of truth for legend,
                # using interpunct for cleaner look
                legend_items = [
                    f"{emoji} {name}"
                    for emoji, name in self.WORKFLOW_CATEGORIES.items()
                ]
                legend_string = " · ".join(legend_items)
                parts.append(f"> **Legend:** {legend_string}\n\n")

                # Assign workflows to categories (first match wins)
                # Grouping is now done efficiently
                grouped: Dict[str, List[str]] = {}
                for emoji in self.WORKFLOW_CATEGORIES.keys():
                    grouped[f"{emoji} {self.WORKFLOW_CATEGORIES[emoji]}"] = []

                # Populate grouped workflows
                for workflow in workflows:
                    emoji, category = self._classify_workflow(workflow)
                    key = f"{emoji} {category}"
                    if key in grouped:
                        grouped[key].append(workflow)

                # Count active categories
                active_categories = sum(
                    1 for items in grouped.values() if len(items) > 0
                )

                summary = (
                    f"View all {len(workflows)} workflows across "
                    f"{active_categories} categories"
                )
                parts.append(f"<details>\n<summary>{summary}</summary>\n\n")

                # Render categories
                for label, items in grouped.items():
                    if items:
                        parts.append(f"### {label}\n\n")
                        parts.append("| Workflow | Action |\n|---|---|\n")
                        for w in items:
                            parts.append(
                                f"| `{w}` | " f"[View]({workflow_path}{w}) |\n"
                            )
                        parts.append("\n")

                parts.append("\n</details>\n")
            else:
                parts.append("No active workflows detected.\n")
        else:
            parts.append("No workflow data available.\n")

        back_to_top2 = "\n[⬆️ Back to Top]" "(#organization-ecosystem-dashboard)\n"
        parts.append(back_to_top2)

        parts.append("\n---\n\n")
        parts.append("*Dashboard generated by Ecosystem Visualizer*\n")

        dashboard = "".join(parts)

        if output_path:
            output_path.write_text(dashboard)
            print(f"📊 Dashboard saved to {output_path}")

        return dashboard

    def generate_health_badge(self) -> str:
        """Generate a health badge in Shields.io format"""

        if not self.report_data:
            badge_url = (
                "![Health](https://img.shields.io/badge/" "health-unknown-lightgrey)"
            )
            return badge_url

        # Calculate overall health score
        score = 0
        max_score = 0

        # Repository health (40 points)
        if "repository_health" in self.report_data:
            rh = self.report_data["repository_health"]
            total = rh.get("total_repos", 0)
            active = rh.get("active_repos", 0)

            if total > 0:
                repo_score = (active / total) * 40
                score += repo_score
            max_score += 40

        # Link health (30 points)
        if (
            "link_validation" in self.report_data
            and self.report_data["link_validation"]
        ):
            lv = self.report_data["link_validation"]
            total_links = lv.get("total_links", 0)
            valid = lv.get("valid", 0)

            if total_links > 0:
                link_score = (valid / total_links) * 30
                score += link_score
            max_score += 30

        # Alerts penalty (30 points)
        blind_spots = self.report_data.get("blind_spots", [])
        shatter_points = self.report_data.get("shatter_points", [])

        critical_count = sum(
            1
            for b in blind_spots
            if b.get("severity") == "high" or b.get("severity") == "critical"
        )
        critical_count += sum(
            1
            for s in shatter_points
            if s.get("severity") == "high" or s.get("severity") == "critical"
        )

        alert_score = max(0, 30 - (critical_count * 10))
        score += alert_score
        max_score += 30

        # Calculate percentage
        if max_score > 0:
            health_pct = int((score / max_score) * 100)
        else:
            health_pct = 0

        # Determine color
        if health_pct >= 80:
            color = "brightgreen"
            status = "excellent"
        elif health_pct >= 60:
            color = "green"
            status = "good"
        elif health_pct >= 40:
            color = "yellow"
            status = "fair"
        elif health_pct >= 20:
            color = "orange"
            status = "poor"
        else:
            color = "red"
            status = "critical"

        badge_url = (
            f"![Health](https://img.shields.io/badge/"
            f"health-{health_pct}%25_{status}-{color})"
        )
        return badge_url


def main() -> None:
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Ecosystem Visualizer")
    parser.add_argument(
        "--report",
        type=Path,
        required=False,
        help="Path to health report JSON file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("reports/DASHBOARD.md"),
        help="Output path for dashboard",
    )
    parser.add_argument(
        "--find-latest",
        action="store_true",
        help="Automatically find the latest report",
    )

    args = parser.parse_args()

    report_path = args.report

    if args.find_latest:
        # Find the latest report
        reports_dir = Path("reports")
        if reports_dir.exists():
            pattern = "org_health_*.json"
            json_reports = sorted(reports_dir.glob(pattern), reverse=True)
            if json_reports:
                report_path = json_reports[0]
                print(f"📁 Using latest report: {report_path}")
            else:
                print("⚠️  No reports found in reports/ directory")
                return
        else:
            print("⚠️  reports/ directory not found")
            return

    if not report_path:
        print("❌ No report specified.")
        print("💡 Try running with --find-latest to use the " "most recent report:")
        print("   python3 scripts/ecosystem_visualizer.py --find-latest")
        return

    visualizer = EcosystemVisualizer(report_path)

    print("🎨 Generating ecosystem dashboard...")
    dashboard = visualizer.generate_dashboard_markdown(args.output)

    print("\n" + "=" * 60)
    print("🎯 DASHBOARD PREVIEW")
    print("=" * 60 + "\n")
    print(dashboard[:500] + "...\n")

    print(f"\n✨ Full dashboard saved to: {args.output}")

    # Generate health badge
    badge = visualizer.generate_health_badge()
    print(f"\n🏆 Health Badge: {badge}")


if __name__ == "__main__":
    main()
