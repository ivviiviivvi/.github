#!/usr/bin/env python3
"""
Web Crawler for GitHub Organization Health Monitoring
Implements AI-GH-06, AI-GH-07, and AI-GH-08 modules
"""

import os
import re
import json
import socket
import ipaddress
import requests
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import time


class OrganizationCrawler:
    """Crawls and analyzes organization repositories and documentation"""

    def __init__(self, github_token: str = None, org_name: str = None):
        self.github_token = github_token or os.environ.get('GITHUB_TOKEN')
        self.org_name = org_name or os.environ.get('GITHUB_REPOSITORY', '').split('/')[0]
        self.session = requests.Session()
        if self.github_token:
            self.session.headers.update({'Authorization': f'token {self.github_token}'})

        self.results = {
            'timestamp': datetime.utcnow().isoformat(),
            'organization': self.org_name,
            'link_validation': {},
            'repository_health': {},
            'ecosystem_map': {},
            'blind_spots': [],
            'shatter_points': [],
            'recommendations': []
        }

    def crawl_markdown_files(self, directory: Path) -> Dict[str, List[str]]:
        """Extract all links from markdown files"""
        print(f"🔍 Crawling markdown files in {directory}")
        links_by_file = {}

        for md_file in directory.rglob('*.md'):
            try:
                content = md_file.read_text(encoding='utf-8')
                links = self._extract_links(content)
                if links:
                    links_by_file[str(md_file.relative_to(directory))] = links
            except Exception as e:
                print(f"  ⚠️  Error reading {md_file}: {e}")

        return links_by_file

    def _extract_links(self, content: str) -> List[str]:
        """Extract URLs from markdown content"""
        # Match both [text](url) and bare URLs
        markdown_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        bare_urls = re.findall(r'https?://[^\s<>"{}|\\^`\[\]]+', content)

        urls = [url for _, url in markdown_links] + bare_urls
        return list(set(urls))  # Remove duplicates

    def validate_links(self, links_by_file: Dict[str, List[str]]) -> Dict:
        """Validate all extracted links"""
        print("\n🌐 Validating links...")

        results = {
            'total_links': 0,
            'valid': 0,
            'broken': 0,
            'broken_links': [],
            'warnings': []
        }

        all_links = set()
        for links in links_by_file.values():
            all_links.update(links)

        results['total_links'] = len(all_links)

        for link in sorted(all_links):
            # Skip internal anchors and relative paths
            if link.startswith('#') or link.startswith('./') or link.startswith('../'):
                continue

            # Skip mailto: and other protocols
            if not link.startswith('http'):
                continue

            status = self._check_link(link)
            if status == 200:
                results['valid'] += 1
                print(f"  ✓ {link}")
            elif status == 999:  # Rate limited or blocked
                results['warnings'].append({'url': link, 'reason': 'Rate limited or blocked by server'})
                print(f"  ⚠️  {link} (rate limited)")
            else:
                results['broken'] += 1
                results['broken_links'].append({'url': link, 'status': status})
                print(f"  ✗ {link} (HTTP {status})")

            time.sleep(0.5)  # Be respectful with requests

        return results

    def _is_url_safe(self, url: str) -> bool:
        """
        Validate URL to prevent Server-Side Request Forgery (SSRF).
        Checks if the hostname resolves to a private or reserved IP address.
        """
        try:
            parsed = urllib.parse.urlparse(url)
            hostname = parsed.hostname
            if not hostname:
                return False

            # Resolve hostname to IP(s)
            try:
                # getaddrinfo supports both IPv4 and IPv6
                addr_info = socket.getaddrinfo(hostname, None)
            except socket.gaierror:
                return False

            for res in addr_info:
                # res[4][0] is the IP address string
                ip_str = res[4][0]
                # Remove scope ID if present
                if '%' in ip_str:
                    ip_str = ip_str.split('%')[0]

                try:
                    ip_obj = ipaddress.ip_address(ip_str)

                    if (ip_obj.is_private or
                        ip_obj.is_loopback or
                        ip_obj.is_link_local or
                        ip_obj.is_reserved or
                        ip_obj.is_multicast):
                        return False

                except ValueError:
                    continue

            return True

        except Exception:
            return False

    def _check_link(self, url: str, timeout: int = 10) -> int:
        """Check if a link is accessible"""
        if not self._is_url_safe(url):
            return 403

        try:
            response = self.session.head(
                url,
                timeout=timeout,
                allow_redirects=True,
                headers={'User-Agent': 'Mozilla/5.0 GitHub Organization Health Crawler'}
            )

            # Some servers don't support HEAD, try GET
            if response.status_code >= 400:
                response = self.session.get(url, timeout=timeout, allow_redirects=True)

            return response.status_code
        except requests.exceptions.Timeout:
            return 408
        except requests.exceptions.TooManyRedirects:
            return 310
        except requests.exceptions.RequestException:
            return 500

    def analyze_repository_health(self) -> Dict:
        """Analyze health metrics across organization repositories (AI-GH-07)"""
        print("\n🏥 Analyzing repository health...")

        if not self.github_token:
            print("  ⚠️  No GitHub token provided, skipping API calls")
            return {'error': 'No GitHub token provided'}

        health_metrics = {
            'repositories': [],
            'total_repos': 0,
            'active_repos': 0,
            'stale_repos': 0,
            'security_alerts': []
        }

        try:
            # Get organization repositories
            api_url = f'https://api.github.com/orgs/{self.org_name}/repos'
            response = self.session.get(api_url, params={'per_page': 100})

            if response.status_code != 200:
                return {'error': f'API request failed: {response.status_code}'}

            repos = response.json()
            health_metrics['total_repos'] = len(repos)

            for repo in repos:
                repo_health = self._analyze_single_repo(repo)
                health_metrics['repositories'].append(repo_health)

                if repo_health['is_active']:
                    health_metrics['active_repos'] += 1
                else:
                    health_metrics['stale_repos'] += 1

                time.sleep(0.3)  # Rate limiting

        except Exception as e:
            print(f"  ✗ Error analyzing repositories: {e}")
            health_metrics['error'] = str(e)

        return health_metrics

    def _analyze_single_repo(self, repo: Dict) -> Dict:
        """Analyze health of a single repository"""
        name = repo['name']
        print(f"  📊 Analyzing {name}...")

        # Calculate days since last update
        updated_at = datetime.fromisoformat(repo['updated_at'].replace('Z', '+00:00'))
        days_since_update = (datetime.now(updated_at.tzinfo) - updated_at).days

        return {
            'name': name,
            'full_name': repo['full_name'],
            'is_active': days_since_update < 90,
            'days_since_update': days_since_update,
            'stars': repo['stargazers_count'],
            'open_issues': repo['open_issues_count'],
            'language': repo['language'],
            'has_wiki': repo['has_wiki'],
            'has_pages': repo['has_pages'],
            'visibility': repo['visibility']
        }

    def map_ecosystem(self, base_dir: Path) -> Dict:
        """Map the technology ecosystem (AI-GH-06)"""
        print("\n🗺️  Mapping ecosystem...")

        ecosystem = {
            'workflows': [],
            'copilot_agents': [],
            'copilot_instructions': [],
            'copilot_prompts': [],
            'copilot_chatmodes': [],
            'technologies': set(),
            'integrations': set()
        }

        # Scan workflows
        workflows_dir = base_dir / '.github' / 'workflows'
        if workflows_dir.exists():
            for workflow_file in workflows_dir.glob('*.yml'):
                ecosystem['workflows'].append(workflow_file.name)

        # Scan Copilot customizations
        for agent_file in (base_dir / 'agents').glob('*.md'):
            ecosystem['copilot_agents'].append(agent_file.stem)

        for instruction_file in (base_dir / 'instructions').glob('*.md'):
            ecosystem['copilot_instructions'].append(instruction_file.stem)
            # Extract technology from filename
            tech = instruction_file.stem.split('.')[0]
            ecosystem['technologies'].add(tech)

        for prompt_file in (base_dir / 'prompts').glob('*.md'):
            ecosystem['copilot_prompts'].append(prompt_file.stem)

        for chatmode_file in (base_dir / 'chatmodes').glob('*.md'):
            ecosystem['copilot_chatmodes'].append(chatmode_file.stem)

        # Convert sets to lists for JSON serialization
        ecosystem['technologies'] = sorted(list(ecosystem['technologies']))
        ecosystem['integrations'] = sorted(list(ecosystem['integrations']))

        return ecosystem

    def identify_blind_spots(self, ecosystem: Dict, health: Dict) -> List[Dict]:
        """Identify blind spots and risks (AI-GH-08-A)"""
        print("\n🔦 Identifying blind spots...")

        blind_spots = []

        # Check for repositories without recent activity
        if 'repositories' in health:
            stale_repos = [r for r in health['repositories'] if not r['is_active']]
            if stale_repos:
                blind_spots.append({
                    'category': 'Stale Repositories',
                    'severity': 'medium',
                    'description': f'Found {len(stale_repos)} repositories with no activity in 90+ days',
                    'affected_items': [r['name'] for r in stale_repos[:5]]
                })

        # Check for missing documentation
        required_docs = ['README.md', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md', 'SECURITY.md']
        # This would need actual file checking in the implementation

        # Check for workflow coverage
        if len(ecosystem.get('workflows', [])) < 5:
            blind_spots.append({
                'category': 'CI/CD Coverage',
                'severity': 'low',
                'description': 'Limited GitHub Actions workflows detected',
                'recommendation': 'Consider adding more automation workflows'
            })

        return blind_spots

    def identify_shatter_points(self, ecosystem: Dict) -> List[Dict]:
        """Identify single points of failure (AI-GH-08-B)"""
        print("\n💥 Identifying shatter points...")

        shatter_points = []

        # Check for critical workflows without backups
        critical_workflows = ['ci.yml', 'security-scan.yml', 'deployment.yml']
        existing_workflows = ecosystem.get('workflows', [])

        for critical in critical_workflows:
            if critical not in existing_workflows:
                shatter_points.append({
                    'category': 'Missing Critical Workflow',
                    'severity': 'high',
                    'description': f'Critical workflow {critical} not found',
                    'recommendation': f'Implement {critical} to ensure automated {critical.split(".")[0]}'
                })

        return shatter_points

    def generate_report(self, output_dir: Path) -> Path:
        """Generate comprehensive analysis report"""
        print("\n📝 Generating report...")

        report_filename = f"org_health_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        report_path = output_dir / report_filename

        output_dir.mkdir(parents=True, exist_ok=True)

        with open(report_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)

        # Also generate a markdown summary
        md_report = self._generate_markdown_report()
        md_path = output_dir / report_filename.replace('.json', '.md')
        md_path.write_text(md_report)

        print(f"  ✓ Report saved to {report_path}")
        print(f"  ✓ Markdown summary saved to {md_path}")

        return report_path

    def _generate_markdown_report(self) -> str:
        """Generate markdown summary report"""
        report = f"""# Organization Health Report
Generated: {self.results['timestamp']}
Organization: {self.results['organization']}

## 🌐 Link Validation

"""

        if 'link_validation' in self.results and self.results['link_validation']:
            lv = self.results['link_validation']
            report += f"""- **Total Links**: {lv.get('total_links', 0)}
- **Valid**: {lv.get('valid', 0)}
- **Broken**: {lv.get('broken', 0)}
- **Warnings**: {len(lv.get('warnings', []))}
"""

            if lv.get('broken_links'):
                report += "\n### Broken Links\n\n"
                for broken in lv['broken_links'][:10]:
                    report += f"- `{broken['url']}` (HTTP {broken['status']})\n"

        report += "\n## 🏥 Repository Health\n\n"

        if 'repository_health' in self.results and self.results['repository_health']:
            rh = self.results['repository_health']
            report += f"""- **Total Repositories**: {rh.get('total_repos', 0)}
- **Active** (updated within 90 days): {rh.get('active_repos', 0)}
- **Stale** (90+ days): {rh.get('stale_repos', 0)}
"""

        report += "\n## 🗺️  Ecosystem Map\n\n"

        if 'ecosystem_map' in self.results and self.results['ecosystem_map']:
            em = self.results['ecosystem_map']
            report += f"""- **GitHub Actions Workflows**: {len(em.get('workflows', []))}
- **Copilot Agents**: {len(em.get('copilot_agents', []))}
- **Copilot Instructions**: {len(em.get('copilot_instructions', []))}
- **Copilot Prompts**: {len(em.get('copilot_prompts', []))}
- **Copilot Chat Modes**: {len(em.get('copilot_chatmodes', []))}
- **Technologies**: {len(em.get('technologies', []))}
"""

        report += "\n## 🔦 Blind Spots\n\n"

        blind_spots = self.results.get('blind_spots', [])
        if blind_spots:
            for spot in blind_spots:
                report += f"### {spot.get('category')} ({spot.get('severity', 'unknown')})\n\n"
                report += f"{spot.get('description')}\n\n"
                if 'recommendation' in spot:
                    report += f"**Recommendation**: {spot['recommendation']}\n\n"
        else:
            report += "No significant blind spots detected.\n\n"

        report += "\n## 💥 Shatter Points\n\n"

        shatter_points = self.results.get('shatter_points', [])
        if shatter_points:
            for point in shatter_points:
                report += f"### {point.get('category')} ({point.get('severity', 'unknown')})\n\n"
                report += f"{point.get('description')}\n\n"
                if 'recommendation' in point:
                    report += f"**Recommendation**: {point['recommendation']}\n\n"
        else:
            report += "No critical shatter points detected.\n\n"

        report += "\n---\n\n"
        report += "*Generated by Organization Health Crawler - Implementing AI-GH-06, AI-GH-07, and AI-GH-08*\n"

        return report

    def run_full_analysis(self, base_dir: Path, validate_external_links: bool = False):
        """Run complete organization analysis"""
        print("🚀 Starting full organization analysis...\n")

        # 1. Map ecosystem (AI-GH-06)
        ecosystem = self.map_ecosystem(base_dir)
        self.results['ecosystem_map'] = ecosystem

        # 2. Analyze repository health (AI-GH-07)
        health = self.analyze_repository_health()
        self.results['repository_health'] = health

        # 3. Crawl and validate links (AI-GH-05 & AI-GH-07)
        if validate_external_links:
            links_by_file = self.crawl_markdown_files(base_dir)
            link_validation = self.validate_links(links_by_file)
            self.results['link_validation'] = link_validation
        else:
            print("\n🌐 Skipping external link validation (use --validate-links to enable)")

        # 4. Identify blind spots (AI-GH-08-A)
        blind_spots = self.identify_blind_spots(ecosystem, health)
        self.results['blind_spots'] = blind_spots

        # 5. Identify shatter points (AI-GH-08-B)
        shatter_points = self.identify_shatter_points(ecosystem)
        self.results['shatter_points'] = shatter_points

        # 6. Generate report
        report_path = self.generate_report(base_dir / 'reports')

        print(f"\n✨ Analysis complete! Report saved to: {report_path}")

        return self.results


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='GitHub Organization Health Crawler')
    parser.add_argument('--base-dir', type=Path, default=Path.cwd(),
                        help='Base directory to analyze (default: current directory)')
    parser.add_argument('--validate-links', action='store_true',
                        help='Validate external links (may be slow)')
    parser.add_argument('--github-token', type=str,
                        help='GitHub API token (or set GITHUB_TOKEN env var)')
    parser.add_argument('--org-name', type=str,
                        help='GitHub organization name (or set from GITHUB_REPOSITORY)')

    args = parser.parse_args()

    crawler = OrganizationCrawler(
        github_token=args.github_token,
        org_name=args.org_name
    )

    results = crawler.run_full_analysis(
        base_dir=args.base_dir,
        validate_external_links=args.validate_links
    )

    # Print summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)

    if 'ecosystem_map' in results:
        em = results['ecosystem_map']
        print(f"Workflows: {len(em.get('workflows', []))}")
        print(f"Copilot Customizations: {len(em.get('copilot_agents', [])) + len(em.get('copilot_instructions', [])) + len(em.get('copilot_prompts', [])) + len(em.get('copilot_chatmodes', []))}")

    if 'repository_health' in results and 'total_repos' in results['repository_health']:
        rh = results['repository_health']
        print(f"Total Repositories: {rh.get('total_repos', 0)}")
        print(f"Active Repositories: {rh.get('active_repos', 0)}")

    print(f"Blind Spots Identified: {len(results.get('blind_spots', []))}")
    print(f"Shatter Points Identified: {len(results.get('shatter_points', []))}")

    print("\n✨ Organization is coming to life!")


if __name__ == '__main__':
    main()
