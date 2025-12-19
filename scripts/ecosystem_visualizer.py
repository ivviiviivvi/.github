#!/usr/bin/env python3
"""
Ecosystem Visualizer - Creates visual maps of the organization ecosystem
Implements AI-GH-06: Ecosystem Integration & Architecture Monitoring
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class EcosystemVisualizer:
    """Generate visual representations of the ecosystem"""

    def __init__(self, report_path: Path = None):
        self.report_path = report_path
        self.report_data = None

        if report_path and report_path.exists():
            with open(report_path) as f:
                self.report_data = json.load(f)

    def generate_mermaid_diagram(self) -> str:
        """Generate Mermaid diagram of the ecosystem"""

        if not self.report_data or 'ecosystem_map' not in self.report_data:
            return "No ecosystem data available"

        em = self.report_data['ecosystem_map']

        # Use a list for efficient string concatenation
        parts = []
        parts.append("""```mermaid
graph TD
    %% Styles
    classDef org fill:#0969da,stroke:#0969da,color:#fff,stroke-width:2px;
    classDef workflow fill:#ddf4ff,stroke:#54aeff,color:#24292f,stroke-width:1px;
    classDef agent fill:#fff8c5,stroke:#d4a72c,color:#24292f,stroke-width:1px;
    classDef tech fill:#dafbe1,stroke:#4ac26b,color:#24292f,stroke-width:1px;

    subgraph "GitHub Organization"
        ORG[Organization Root]:::org
    end

    subgraph "Automation Layer"
""")

        # Add workflows
        workflows = em.get('workflows', [])
        for i, workflow in enumerate(workflows[:10]):  # Limit to first 10
            workflow_id = f"WF{i}"
            diagram += f"        {workflow_id}[{workflow}]:::workflow\n"
            diagram += f"        ORG --> {workflow_id}\n"

        parts.append("    end\n\n")

        # Add Copilot customizations
        parts.append("""    subgraph "GitHub Copilot Customizations"
""")

        agents = em.get('copilot_agents', [])
        if agents:
            diagram += "        AGENTS[Agents]:::agent\n"
            diagram += f"        AGENTS_COUNT[{len(agents)} agents]:::agent\n"
            diagram += "        AGENTS --> AGENTS_COUNT\n"
            diagram += "        ORG --> AGENTS\n"

        instructions = em.get('copilot_instructions', [])
        if instructions:
            diagram += "        INSTR[Instructions]:::agent\n"
            diagram += f"        INSTR_COUNT[{len(instructions)} instructions]:::agent\n"
            diagram += "        INSTR --> INSTR_COUNT\n"
            diagram += "        ORG --> INSTR\n"

        prompts = em.get('copilot_prompts', [])
        if prompts:
            diagram += "        PROMPTS[Prompts]:::agent\n"
            diagram += f"        PROMPTS_COUNT[{len(prompts)} prompts]:::agent\n"
            diagram += "        PROMPTS --> PROMPTS_COUNT\n"
            diagram += "        ORG --> PROMPTS\n"

        chatmodes = em.get('copilot_chatmodes', [])
        if chatmodes:
            diagram += "        CHATMODES[Chat Modes]:::agent\n"
            diagram += f"        CHATMODES_COUNT[{len(chatmodes)} modes]:::agent\n"
            diagram += "        CHATMODES --> CHATMODES_COUNT\n"
            diagram += "        ORG --> CHATMODES\n"

        parts.append("    end\n\n")

        # Add technologies
        technologies = em.get('technologies', [])
        if technologies:
            parts.append("""    subgraph "Technologies"
""")
            for i, tech in enumerate(technologies[:15]):  # Limit to first 15
                tech_id = f"TECH{i}"
                safe_tech = tech.replace('-', '_').replace('.', '_')
                diagram += f"        {tech_id}[{tech}]:::tech\n"

            parts.append("    end\n")

        parts.append("```\n")

        return "".join(parts)

    def generate_dashboard_markdown(self, output_path: Path = None) -> str:
        """Generate a comprehensive dashboard in Markdown"""

        if not self.report_data:
            return "No report data available"

        # Use a list for efficient string concatenation
        parts = []
        parts.append(f"""# 🎯 Organization Ecosystem Dashboard

**Last Updated**: {self.report_data.get('timestamp', 'Unknown')}
**Organization**: {self.report_data.get('organization', 'Unknown')}

---

## 📊 Quick Stats

""")

        # Ecosystem stats
        if 'ecosystem_map' in self.report_data:
            em = self.report_data['ecosystem_map']
            parts.append(f"""| Category | Count |
|----------|-------|
| GitHub Actions Workflows | {len(em.get('workflows', []))} |
| Copilot Agents | {len(em.get('copilot_agents', []))} |
| Copilot Instructions | {len(em.get('copilot_instructions', []))} |
| Copilot Prompts | {len(em.get('copilot_prompts', []))} |
| Copilot Chat Modes | {len(em.get('copilot_chatmodes', []))} |
| Technologies Supported | {len(em.get('technologies', []))} |

""")

        # Repository health
        if 'repository_health' in self.report_data:
            rh = self.report_data['repository_health']
            total = rh.get('total_repos', 0)
            active = rh.get('active_repos', 0)
            stale = rh.get('stale_repos', 0)

            if total > 0:
                active_pct = (active / total * 100) if total > 0 else 0

                # Create progress bar
                bar_length = 20
                filled_length = int(bar_length * active_pct / 100)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)

                dashboard += f"""## 🏥 Repository Health

{bar} {active_pct:.1f}%

| Status | Count | Percentage |
|--------|-------|------------|
| Active (< 90 days) | {active} | {active_pct:.1f}% |
| Stale (90+ days) | {stale} | {100 - active_pct:.1f}% |
| **Total** | **{total}** | **100%** |

### Health Score: {active_pct:.0f}/100

""")

        # Link validation
        if 'link_validation' in self.report_data and self.report_data['link_validation']:
            lv = self.report_data['link_validation']
            total_links = lv.get('total_links', 0)
            valid = lv.get('valid', 0)
            broken = lv.get('broken', 0)

            if total_links > 0:
                valid_pct = (valid / total_links * 100) if total_links > 0 else 0
                parts.append(f"""## 🔗 Link Health

| Status | Count | Percentage |
|--------|-------|------------|
| Valid | {valid} | {valid_pct:.1f}% |
| Broken | {broken} | {100 - valid_pct:.1f}% |
| **Total** | **{total_links}** | **100%** |

""")

        # Alerts
        blind_spots = self.report_data.get('blind_spots', [])
        shatter_points = self.report_data.get('shatter_points', [])

        if blind_spots or shatter_points:
            parts.append("## ⚠️  Alerts\n\n")

            if blind_spots:
                parts.append(f"### 🔦 Blind Spots ({len(blind_spots)})\n\n")
                for spot in blind_spots:
                    severity = spot.get('severity', 'unknown').upper()
                    emoji = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(severity, '⚪')
                    parts.append(f"{emoji} **{spot.get('category')}** ({severity})\n")
                    parts.append(f"  - {spot.get('description')}\n\n")

            if shatter_points:
                parts.append(f"\n### 💥 Shatter Points ({len(shatter_points)})\n\n")
                for point in shatter_points:
                    severity = point.get('severity', 'unknown').upper()
                    emoji = {'HIGH': '🔴', 'MEDIUM': '🟡', 'LOW': '🟢'}.get(severity, '⚪')
                    parts.append(f"{emoji} **{point.get('category')}** ({severity})\n")
                    parts.append(f"  - {point.get('description')}\n")
                    if 'recommendation' in point:
                        parts.append(f"  - 💡 {point['recommendation']}\n")
                    parts.append("\n")

        # Ecosystem diagram
        parts.append("\n## 🗺️  Ecosystem Map\n\n")
        parts.append(self.generate_mermaid_diagram())

        # Technology coverage
        if 'ecosystem_map' in self.report_data:
            em = self.report_data['ecosystem_map']
            technologies = em.get('technologies', [])

            if technologies:
                parts.append(f"\n## 🛠️  Technology Coverage\n\n")
                parts.append("Supported languages and frameworks:\n\n")

                # Group into columns
                cols = 4
                for i in range(0, len(technologies), cols):
                    row_techs = technologies[i : i + cols]

                    # Pad with empty strings if needed
                    current_len = len(row_techs)
                    if current_len < cols:
                        row_techs.extend([""] * (cols - current_len))

                    formatted_cells = [f"`{t}`" if t else "" for t in row_techs]
                    parts.append("| " + " | ".join(formatted_cells) + " |\n")

                    if i == 0:
                        parts.append("| " + " | ".join(["---"] * cols) + " |\n")

        # Top workflows
        if 'ecosystem_map' in self.report_data:
            em = self.report_data['ecosystem_map']
            workflows = em.get('workflows', [])

            if workflows:
                parts.append(f"\n## ⚙️  Active Workflows ({len(workflows)})\n\n")
                for workflow in sorted(workflows):
                    parts.append(f"- `{workflow}`\n")

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
            return "![Health](https://img.shields.io/badge/health-unknown-lightgrey)"

        # Calculate overall health score
        score = 0
        max_score = 0

        # Repository health (40 points)
        if 'repository_health' in self.report_data:
            rh = self.report_data['repository_health']
            total = rh.get('total_repos', 0)
            active = rh.get('active_repos', 0)

            if total > 0:
                repo_score = (active / total) * 40
                score += repo_score
            max_score += 40

        # Link health (30 points)
        if 'link_validation' in self.report_data and self.report_data['link_validation']:
            lv = self.report_data['link_validation']
            total_links = lv.get('total_links', 0)
            valid = lv.get('valid', 0)

            if total_links > 0:
                link_score = (valid / total_links) * 30
                score += link_score
            max_score += 30

        # Alerts penalty (30 points)
        blind_spots = self.report_data.get('blind_spots', [])
        shatter_points = self.report_data.get('shatter_points', [])

        critical_count = sum(1 for b in blind_spots if b.get('severity') == 'high' or b.get('severity') == 'critical')
        critical_count += sum(1 for s in shatter_points if s.get('severity') == 'high' or s.get('severity') == 'critical')

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

        return f"![Health](https://img.shields.io/badge/health-{health_pct}%25_{status}-{color})"


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Ecosystem Visualizer')
    parser.add_argument('--report', type=Path, required=False,
                        help='Path to health report JSON file')
    parser.add_argument('--output', type=Path, default=Path('reports/DASHBOARD.md'),
                        help='Output path for dashboard')
    parser.add_argument('--find-latest', action='store_true',
                        help='Automatically find the latest report')

    args = parser.parse_args()

    report_path = args.report

    if args.find_latest:
        # Find the latest report
        reports_dir = Path('reports')
        if reports_dir.exists():
            json_reports = sorted(reports_dir.glob('org_health_*.json'), reverse=True)
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
        print("❌ No report specified. Use --report or --find-latest")
        return

    visualizer = EcosystemVisualizer(report_path)

    print("🎨 Generating ecosystem dashboard...")
    dashboard = visualizer.generate_dashboard_markdown(args.output)

    print("\n" + "="*60)
    print("🎯 DASHBOARD PREVIEW")
    print("="*60 + "\n")
    print(dashboard[:500] + "...\n")

    print(f"\n✨ Full dashboard saved to: {args.output}")

    # Generate health badge
    badge = visualizer.generate_health_badge()
    print(f"\n🏆 Health Badge: {badge}")


if __name__ == '__main__':
    main()
