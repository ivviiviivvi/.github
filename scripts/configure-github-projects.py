#!/usr/bin/env python3
"""
GitHub Projects V2 Configuration Script

This script creates and configures comprehensive GitHub Projects using the GraphQL API.  # noqa: E501
It handles project creation, field configuration, view setup, and automation rules.

Prerequisites:
- Python 3.8+
- GitHub Personal Access Token with project:write scope
- Set GH_TOKEN environment variable

Usage:
    export GH_TOKEN="your_github_token"
    python3 configure-github-projects.py --org ivviiviivvi --repo .github
"""

import argparse
import json
import os
import sys
import time
from typing import Dict, List, Optional

import requests

# ANSI color codes


class Colors:
    BLUE = "\033[0;34m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"
    RED = "\033[0;31m"
    NC = "\033[0m"  # No Color


def log_info(message: str):
    print(f"{Colors.BLUE}ℹ {Colors.NC}{message}")


def log_success(message: str):
    print(f"{Colors.GREEN}✓{Colors.NC} {message}")


def log_warning(message: str):
    print(f"{Colors.YELLOW}⚠{Colors.NC} {message}")


def log_error(message: str):
    print(f"{Colors.RED}✗{Colors.NC} {message}")


class GitHubProjectsManager:
    """Manager for GitHub Projects V2 operations."""

    def __init__(self, token: str, org: str):
        self.token = token
        self.org = org
        self.api_url = "https://api.github.com/graphql"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def execute_query(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """Execute a GraphQL query."""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"Query failed: {response.status_code} - {response.text}")

        data = response.json()
        if "errors" in data:
            raise Exception(f"GraphQL errors: {json.dumps(data['errors'], indent=2)}")

        return data

    def get_org_id(self) -> str:
        """Get organization node ID."""
        query = """
        query($login: String!) {
            organization(login: $login) {
                id
            }
        }
        """
        result = self.execute_query(query, {"login": self.org})
        return result["data"]["organization"]["id"]

    def create_project(self, title: str, description: str) -> Dict:
        """Create a new project."""
        org_id = self.get_org_id()

        mutation = """
        mutation($input: CreateProjectV2Input!) {
            createProjectV2(input: $input) {
                projectV2 {
                    id
                    number
                    title
                    url
                }
            }
        }
        """

        variables = {
            "input": {
                "ownerId": org_id,
                "title": title,
            }
        }

        result = self.execute_query(mutation, variables)
        project = result["data"]["createProjectV2"]["projectV2"]

        # Update with description (separate API call)
        self.update_project_description(project["id"], description)

        return project

    def update_project_description(self, project_id: str, description: str):
        """Update project description."""
        mutation = """
        mutation($projectId: ID!, $readme: String!) {
            updateProjectV2(input: {
                projectId: $projectId
                readme: $readme
            }) {
                projectV2 {
                    id
                }
            }
        }
        """

        variables = {"projectId": project_id, "readme": description}

        self.execute_query(mutation, variables)

    def create_single_select_field(
        self, project_id: str, name: str, options: List[Dict[str, str]]
    ) -> str:
        """Create a single select field."""
        mutation = """
        mutation($input: CreateProjectV2FieldInput!) {
            createProjectV2Field(input: $input) {
                projectV2Field {
                    ... on ProjectV2SingleSelectField {
                        id
                        name
                    }
                }
            }
        }
        """

        # Add empty description to each option (required by API)
        options_with_desc = [{**opt, "description": ""} for opt in options]

        variables = {
            "input": {
                "projectId": project_id,
                "dataType": "SINGLE_SELECT",
                "name": name,
                "singleSelectOptions": options_with_desc,
            }
        }

        result = self.execute_query(mutation, variables)
        return result["data"]["createProjectV2Field"]["projectV2Field"]["id"]

    def create_text_field(self, project_id: str, name: str) -> str:
        """Create a text field."""
        mutation = """
        mutation($input: CreateProjectV2FieldInput!) {
            createProjectV2Field(input: $input) {
                projectV2Field {
                    ... on ProjectV2Field {
                        id
                        name
                    }
                }
            }
        }
        """

        variables = {
            "input": {
                "projectId": project_id,
                "dataType": "TEXT",
                "name": name,
            }
        }

        result = self.execute_query(mutation, variables)
        return result["data"]["createProjectV2Field"]["projectV2Field"]["id"]

    def create_number_field(self, project_id: str, name: str) -> str:
        """Create a number field."""
        mutation = """
        mutation($input: CreateProjectV2FieldInput!) {
            createProjectV2Field(input: $input) {
                projectV2Field {
                    ... on ProjectV2Field {
                        id
                        name
                    }
                }
            }
        }
        """

        variables = {
            "input": {
                "projectId": project_id,
                "dataType": "NUMBER",
                "name": name,
            }
        }

        result = self.execute_query(mutation, variables)
        return result["data"]["createProjectV2Field"]["projectV2Field"]["id"]

    def create_date_field(self, project_id: str, name: str) -> str:
        """Create a date field."""
        mutation = """
        mutation($input: CreateProjectV2FieldInput!) {
            createProjectV2Field(input: $input) {
                projectV2Field {
                    ... on ProjectV2Field {
                        id
                        name
                    }
                }
            }
        }
        """

        variables = {
            "input": {
                "projectId": project_id,
                "dataType": "DATE",
                "name": name,
            }
        }

        result = self.execute_query(mutation, variables)
        return result["data"]["createProjectV2Field"]["projectV2Field"]["id"]


# Project configurations
PROJECTS_CONFIG = {
    "ai-framework": {
        "title": "🤖 AI Framework Development",
        "description": """Development and maintenance of the AI framework including:  # noqa: E501
- 26+ specialized agents
- MCP servers for 11 programming languages
- 100+ custom instructions
- Chat modes and collections
- Automated tracking of agent lifecycle, testing, and deployment

**Key Areas:**
- Agent development and testing
- MCP server implementation
- Custom instructions authoring
- Chat mode configuration
- Framework enhancements and bug fixes""",
        "fields": {
            "Status": {
                "type": "single_select",
                "options": [
                    {"name": "🎯 Planned", "color": "GRAY"},
                    {"name": "🔬 Research", "color": "BLUE"},
                    {"name": "🏗️ In Development", "color": "YELLOW"},
                    {"name": "🧪 Testing", "color": "ORANGE"},
                    {"name": "👀 Code Review", "color": "PURPLE"},
                    {"name": "✅ Ready to Deploy", "color": "GREEN"},
                    {"name": "🚀 Deployed", "color": "GREEN"},
                    {"name": "📝 Documentation", "color": "BLUE"},
                    {"name": "⏸️ On Hold", "color": "GRAY"},
                    {"name": "✔️ Completed", "color": "GREEN"},
                ],
            },
            "Priority": {
                "type": "single_select",
                "options": [
                    {"name": "🔥 Critical", "color": "RED"},
                    {"name": "⚡ High", "color": "ORANGE"},
                    {"name": "📊 Medium", "color": "YELLOW"},
                    {"name": "🔽 Low", "color": "GRAY"},
                ],
            },
            "Type": {
                "type": "single_select",
                "options": [
                    {"name": "🤖 Agent", "color": "PURPLE"},
                    {"name": "🔌 MCP Server", "color": "BLUE"},
                    {"name": "📋 Custom Instructions", "color": "GREEN"},
                    {"name": "💬 Chat Mode", "color": "PINK"},
                    {"name": "📦 Collection", "color": "ORANGE"},
                    {"name": "🔧 Framework Enhancement", "color": "YELLOW"},
                    {"name": "🐛 Bug Fix", "color": "RED"},
                ],
            },
            "Language": {
                "type": "single_select",
                "options": [
                    {"name": "Python", "color": "BLUE"},
                    {"name": "TypeScript", "color": "BLUE"},
                    {"name": "Java", "color": "RED"},
                    {"name": "C#", "color": "PURPLE"},
                    {"name": "Go", "color": "BLUE"},
                    {"name": "Rust", "color": "ORANGE"},
                    {"name": "Multi-Language", "color": "GRAY"},
                ],
            },
            "Complexity": {
                "type": "single_select",
                "options": [
                    {"name": "🟢 Simple", "color": "GREEN"},
                    {"name": "🟡 Moderate", "color": "YELLOW"},
                    {"name": "🟠 Complex", "color": "ORANGE"},
                    {"name": "🔴 Major", "color": "RED"},
                ],
            },
            "Dependencies": {"type": "text"},
            "Testing Status": {
                "type": "single_select",
                "options": [
                    {"name": "⏳ Not Started", "color": "GRAY"},
                    {"name": "🧪 Unit Tests", "color": "YELLOW"},
                    {"name": "🔗 Integration Tests", "color": "ORANGE"},
                    {"name": "✅ All Tests Passing", "color": "GREEN"},
                ],
            },
        },
    },
    "documentation": {
        "title": "📚 Documentation & Knowledge",
        "description": """Documentation ecosystem management across 133+ files:
- Setup guides and quick starts
- Architecture documentation
- API references and technical guides
- Tutorials and learning resources
- Policy documents

**Coverage:**
- Core organizational policies
- Workflow system documentation
- AI framework guides
- Development environment setup
- Security and compliance docs""",
        "fields": {
            "Status": {
                "type": "single_select",
                "options": [
                    {"name": "📋 Backlog", "color": "GRAY"},
                    {"name": "✍️ Writing", "color": "YELLOW"},
                    {"name": "👀 Review", "color": "ORANGE"},
                    {"name": "🔄 Revision", "color": "BLUE"},
                    {"name": "✅ Approved", "color": "GREEN"},
                    {"name": "📤 Published", "color": "GREEN"},
                    {"name": "🔄 Needs Update", "color": "RED"},
                ],
            },
            "Priority": {
                "type": "single_select",
                "options": [
                    {"name": "🔥 Urgent", "color": "RED"},
                    {"name": "⚡ High", "color": "ORANGE"},
                    {"name": "📊 Medium", "color": "YELLOW"},
                    {"name": "🔽 Low", "color": "GRAY"},
                ],
            },
            "Document Type": {
                "type": "single_select",
                "options": [
                    {"name": "📖 Guide", "color": "BLUE"},
                    {"name": "🏛️ Architecture", "color": "PURPLE"},
                    {"name": "🔧 Technical Reference", "color": "ORANGE"},
                    {"name": "📚 Tutorial", "color": "GREEN"},
                    {"name": "📋 Policy", "color": "RED"},
                    {"name": "🎯 Quick Start", "color": "YELLOW"},
                ],
            },
            "Completeness": {
                "type": "single_select",
                "options": [
                    {"name": "🔴 Outline Only", "color": "RED"},
                    {"name": "🟡 Draft", "color": "YELLOW"},
                    {"name": "🟢 Complete", "color": "GREEN"},
                    {"name": "⭐ Comprehensive", "color": "GREEN"},
                ],
            },
            "Last Updated": {"type": "date"},
            "Next Review Date": {"type": "date"},
            "Word Count": {"type": "number"},
        },
    },
    "workflow-automation": {
        "title": "🔄 Workflow Automation",
        "description": """GitHub Actions workflows and automation systems:
- 98+ workflow templates and reusable workflows
- CI/CD pipeline automation
- Intelligent routing and auto-merge
- SLA monitoring and enforcement
- Self-healing workflow systems

**Key Features:**
- Auto-triage (48-hour SLA)
- Intelligent reviewer assignment
- Proactive maintenance
- Incident response automation
- Unified notification system""",
        "fields": {
            "Workflow Status": {
                "type": "single_select",
                "options": [
                    {"name": "💡 Ideation", "color": "GRAY"},
                    {"name": "📐 Design", "color": "BLUE"},
                    {"name": "⚙️ Implementation", "color": "YELLOW"},
                    {"name": "🧪 Testing", "color": "ORANGE"},
                    {"name": "🚀 Deployed", "color": "GREEN"},
                    {"name": "📊 Monitoring", "color": "PURPLE"},
                    {"name": "🔧 Maintenance", "color": "BLUE"},
                ],
            },
            "Priority": {
                "type": "single_select",
                "options": [
                    {"name": "🔥 Critical", "color": "RED"},
                    {"name": "⚡ High", "color": "ORANGE"},
                    {"name": "📊 Medium", "color": "YELLOW"},
                    {"name": "🔽 Low", "color": "GRAY"},
                ],
            },
            "Workflow Type": {
                "type": "single_select",
                "options": [
                    {"name": "🔄 CI/CD", "color": "BLUE"},
                    {"name": "🤖 Automation", "color": "PURPLE"},
                    {"name": "📊 Analytics", "color": "GREEN"},
                    {"name": "🚨 Monitoring", "color": "RED"},
                    {"name": "🔧 Maintenance", "color": "ORANGE"},
                ],
            },
            "Trigger": {
                "type": "single_select",
                "options": [
                    {"name": "⏰ Schedule", "color": "BLUE"},
                    {"name": "🎯 Event", "color": "PURPLE"},
                    {"name": "👆 Manual", "color": "GRAY"},
                    {"name": "🔗 Webhook", "color": "ORANGE"},
                ],
            },
            "SLA Target": {"type": "text"},
            "Success Rate": {"type": "number"},
            "Last Run": {"type": "date"},
        },
    },
    "security-compliance": {
        "title": "🔒 Security & Compliance",
        "description": """Security scanning, audits, and compliance tracking:
- Vulnerability scanning and remediation
- Dependency security monitoring
- Secret detection and rotation
- Compliance framework adherence
- Security policy enforcement

**Coverage:**
- OWASP Top 10 protection
- GitHub security features
- Pre-commit security hooks
- Automated security scanning
- Incident response procedures""",
        "fields": {
            "Security Status": {
                "type": "single_select",
                "options": [
                    {"name": "🔍 Identified", "color": "GRAY"},
                    {"name": "⚠️ Triaged", "color": "YELLOW"},
                    {"name": "🚨 Critical", "color": "RED"},
                    {"name": "🔧 In Progress", "color": "ORANGE"},
                    {"name": "✅ Resolved", "color": "GREEN"},
                    {"name": "🛡️ Verified", "color": "GREEN"},
                ],
            },
            "Severity": {
                "type": "single_select",
                "options": [
                    {"name": "🔴 Critical", "color": "RED"},
                    {"name": "🟠 High", "color": "ORANGE"},
                    {"name": "🟡 Medium", "color": "YELLOW"},
                    {"name": "🟢 Low", "color": "GREEN"},
                    {"name": "ℹ️ Info", "color": "GRAY"},
                ],
            },
            "Issue Type": {
                "type": "single_select",
                "options": [
                    {"name": "🐛 Vulnerability", "color": "RED"},
                    {"name": "🔐 Secret Exposure", "color": "RED"},
                    {"name": "📦 Dependency", "color": "ORANGE"},
                    {"name": "⚙️ Configuration", "color": "YELLOW"},
                    {"name": "📋 Policy", "color": "BLUE"},
                    {"name": "🔍 Audit", "color": "PURPLE"},
                ],
            },
            "CVSS Score": {"type": "number"},
            "Discovered Date": {"type": "date"},
            "Target Fix Date": {"type": "date"},
            "Affected Components": {"type": "text"},
        },
    },
    "infrastructure-devops": {
        "title": "🏗️ Infrastructure & DevOps",
        "description": """Infrastructure as code and DevOps operations:
- Cloud infrastructure management
- Container orchestration
- Deployment automation
- Environment configuration
- Monitoring and observability

**Technologies:**
- Docker and Kubernetes
- Terraform and infrastructure as code
- GitHub Codespaces and DevContainers
- Azure/AWS/GCP deployments
- Monitoring and alerting systems""",
        "fields": {
            "Deployment Status": {
                "type": "single_select",
                "options": [
                    {"name": "📋 Planned", "color": "GRAY"},
                    {"name": "🔧 Configuring", "color": "YELLOW"},
                    {"name": "🧪 Testing", "color": "ORANGE"},
                    {"name": "🚀 Deploying", "color": "BLUE"},
                    {"name": "✅ Live", "color": "GREEN"},
                    {"name": "⚠️ Issues", "color": "RED"},
                    {"name": "🔄 Updating", "color": "PURPLE"},
                ],
            },
            "Priority": {
                "type": "single_select",
                "options": [
                    {"name": "🔥 Critical", "color": "RED"},
                    {"name": "⚡ High", "color": "ORANGE"},
                    {"name": "📊 Medium", "color": "YELLOW"},
                    {"name": "🔽 Low", "color": "GRAY"},
                ],
            },
            "Infrastructure Type": {
                "type": "single_select",
                "options": [
                    {"name": "☁️ Cloud", "color": "BLUE"},
                    {"name": "🐳 Container", "color": "PURPLE"},
                    {"name": "🌐 Network", "color": "GREEN"},
                    {"name": "💾 Storage", "color": "ORANGE"},
                    {"name": "🔐 Security", "color": "RED"},
                ],
            },
            "Environment": {
                "type": "single_select",
                "options": [
                    {"name": "🧪 Development", "color": "YELLOW"},
                    {"name": "🔬 Testing", "color": "ORANGE"},
                    {"name": "🎭 Staging", "color": "PURPLE"},
                    {"name": "🚀 Production", "color": "GREEN"},
                ],
            },
            "Cost Impact": {"type": "text"},
            "Last Deployed": {"type": "date"},
            "Uptime SLA": {"type": "number"},
        },
    },
    "community-support": {
        "title": "👥 Community & Support",
        "description": """Community engagement and support management:
- Discussion moderation and facilitation
- Issue and PR triage
- Community guidelines enforcement
- Contributor onboarding
- Support ticket management

**Focus Areas:**
- GitHub Discussions management
- Contributor workflow support
- Community health metrics
- Documentation for contributors
- Recognition and acknowledgment""",
        "fields": {
            "Support Status": {
                "type": "single_select",
                "options": [
                    {"name": "🆕 New", "color": "GRAY"},
                    {"name": "👀 Reviewing", "color": "BLUE"},
                    {"name": "💬 Discussing", "color": "YELLOW"},
                    {"name": "✅ Resolved", "color": "GREEN"},
                    {"name": "🔄 Follow-up", "color": "ORANGE"},
                    {"name": "❌ Closed", "color": "RED"},
                ],
            },
            "Priority": {
                "type": "single_select",
                "options": [
                    {"name": "🔥 Urgent", "color": "RED"},
                    {"name": "⚡ High", "color": "ORANGE"},
                    {"name": "📊 Medium", "color": "YELLOW"},
                    {"name": "🔽 Low", "color": "GRAY"},
                ],
            },
            "Engagement Type": {
                "type": "single_select",
                "options": [
                    {"name": "💬 Discussion", "color": "BLUE"},
                    {"name": "🐛 Issue", "color": "RED"},
                    {"name": "🔧 Pull Request", "color": "PURPLE"},
                    {"name": "❓ Question", "color": "YELLOW"},
                    {"name": "💡 Idea", "color": "GREEN"},
                    {"name": "🎉 Show & Tell", "color": "PINK"},
                ],
            },
            "Response Time": {"type": "number"},
            "First Response": {"type": "date"},
            "Resolution Date": {"type": "date"},
            "Contributor": {"type": "text"},
        },
    },
    "product-roadmap": {
        "title": "🎯 Product Roadmap",
        "description": """Strategic planning and feature roadmap:
- Product vision and strategy
- Feature planning and prioritization
- Release planning and milestones
- Stakeholder communication
- Metrics and success tracking

**Planning Horizons:**
- Now (Current sprint)
- Next (Next 1-3 months)
- Future (3-12 months)
- Vision (12+ months)""",
        "fields": {
            "Roadmap Status": {
                "type": "single_select",
                "options": [
                    {"name": "💭 Idea", "color": "GRAY"},
                    {"name": "🔍 Research", "color": "BLUE"},
                    {"name": "📋 Planned", "color": "YELLOW"},
                    {"name": "🚧 In Progress", "color": "ORANGE"},
                    {"name": "🚀 Shipping", "color": "PURPLE"},
                    {"name": "✅ Shipped", "color": "GREEN"},
                    {"name": "📊 Measuring", "color": "BLUE"},
                ],
            },
            "Priority": {
                "type": "single_select",
                "options": [
                    {"name": "P0 - Critical", "color": "RED"},
                    {"name": "P1 - High", "color": "ORANGE"},
                    {"name": "P2 - Medium", "color": "YELLOW"},
                    {"name": "P3 - Low", "color": "GRAY"},
                ],
            },
            "Timeline": {
                "type": "single_select",
                "options": [
                    {"name": "⏰ Now", "color": "RED"},
                    {"name": "📅 Next", "color": "ORANGE"},
                    {"name": "🔮 Future", "color": "BLUE"},
                    {"name": "🌟 Vision", "color": "PURPLE"},
                ],
            },
            "Feature Area": {
                "type": "single_select",
                "options": [
                    {"name": "🤖 AI Framework", "color": "PURPLE"},
                    {"name": "📚 Documentation", "color": "BLUE"},
                    {"name": "🔄 Automation", "color": "GREEN"},
                    {"name": "🏗️ Infrastructure", "color": "ORANGE"},
                    {"name": "👥 Community", "color": "PINK"},
                ],
            },
            "Target Release": {"type": "text"},
            "Success Metrics": {"type": "text"},
            "Target Date": {"type": "date"},
        },
    },
}


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(description="Configure GitHub Projects V2")
    parser.add_argument("--org", required=True, help="GitHub organization name")
    parser.add_argument(
        "--projects",
        nargs="+",
        choices=list(PROJECTS_CONFIG.keys()),
        default=list(PROJECTS_CONFIG.keys()),
        help="Projects to create (default: all)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )

    args = parser.parse_args()

    # Check for token
    token = os.environ.get("GH_TOKEN")
    if not token:
        log_error("GH_TOKEN environment variable not set")
        sys.exit(1)

    log_info(f"Configuring projects for organization: {args.org}")

    if args.dry_run:
        log_warning("DRY RUN MODE - No changes will be made")

    manager = GitHubProjectsManager(token, args.org)

    for project_key in args.projects:
        config = PROJECTS_CONFIG[project_key]
        log_info(f"Creating project: {config['title']}")

        if args.dry_run:
            log_info(f"  Would create: {config['title']}")
            log_info(f"  Fields: {len(config['fields'])}")
            continue

        try:
            # Create project
            project = manager.create_project(config["title"], config["description"])
            log_success(f"Created project #{project['number']}: {project['title']}")
            log_info(f"  URL: {project['url']}")

            # Create fields
            for field_name, field_config in config["fields"].items():
                log_info(f"  Creating field: {field_name}")

                try:
                    if field_config["type"] == "single_select":
                        manager.create_single_select_field(
                            project["id"], field_name, field_config["options"]
                        )
                    elif field_config["type"] == "text":
                        manager.create_text_field(project["id"], field_name)
                    elif field_config["type"] == "number":
                        manager.create_number_field(project["id"], field_name)
                    elif field_config["type"] == "date":
                        manager.create_date_field(project["id"], field_name)

                    log_success(f"    ✓ {field_name}")
                    time.sleep(0.5)  # Rate limiting

                except Exception as e:
                    log_error(f"    Failed to create field {field_name}: {e}")

            log_success(f"Project {config['title']} configured successfully")
            print()

        except Exception as e:
            log_error(f"Failed to create project {config['title']}: {e}")
            continue

    log_success("All projects configured!")
    log_info("\nNext steps:")
    print("  1. Create project views in the GitHub UI")
    print("  2. Set up automation rules")
    print("  3. Add existing issues/PRs to projects")
    print("\nDocumentation: docs/GITHUB_PROJECTS_IMPLEMENTATION.md")


if __name__ == "__main__":
    main()
