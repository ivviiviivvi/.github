#!/usr/bin/env python3
"""Intelligent Routing Algorithm.

Optimizes issue and PR assignment using multi-factor scoring:
- Expertise: Historical contribution patterns
- Workload: Current assignment count
- Response Time: Average time to first response
- Availability: Recent activity patterns
- Performance: Success rate and quality metrics

Usage:
    python issue_assignment_router.py --owner ORG --repo REPO --issue ISSUE_NUMBER

Environment Variables:
    GITHUB_TOKEN: GitHub API token with repo access
"""

import argparse
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

from models import RoutingConfig, RoutingDecision, RoutingFactorScores
from utils import ConfigLoader, GitHubAPIClient, setup_logger

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))


class IntelligentRouter:
    """Intelligent routing engine for issue/PR assignment."""

    def __init__(self, client: GitHubAPIClient, config: RoutingConfig):
        """Initialize intelligent router.

        Args:
            client: GitHub API client
            config: Routing configuration

        """
        self.client = client
        self.config = config
        self.logger = setup_logger(__name__)

    def calculate_assignment(self, owner: str, repo: str, issue_number: int) -> RoutingDecision:
        """Calculate optimal assignment for issue/PR.

        Args:
            owner: Repository owner
            repo: Repository name
            issue_number: Issue or PR number

        Returns:
            Routing decision with selected assignee

        """
        self.logger.info(f"Calculating assignment for {owner}/{repo}#{issue_number}")

        # Get issue/PR details
        issue = self._get_issue(owner, repo, issue_number)

        # Get candidate assignees
        candidates = self._get_candidates(owner, repo)

        if not candidates:
            raise ValueError("No candidates available for assignment")

        # Check if issue has exempt labels (manual assignment required)
        issue_labels = {label["name"] for label in issue.get("labels", [])}
        if any(label in self.config.exempt_labels for label in issue_labels):
            self.logger.info("Issue has exempt label, using fallback strategy")
            return self._fallback_assignment(owner, repo, issue_number, issue, candidates)

        # Calculate scores for each candidate
        candidate_scores = []
        for candidate in candidates:
            scores = self._calculate_factor_scores(owner, repo, candidate, issue)
            overall_score = self._calculate_overall_score(scores)
            candidate_scores.append(
                {
                    "username": candidate["login"],
                    "score": overall_score,
                    "scores": scores,
                }
            )

        # Sort by score (highest first)
        candidate_scores.sort(key=lambda x: x["score"], reverse=True)

        # Select best candidate
        best = candidate_scores[0]
        alternatives = [
            {"username": c["username"], "score": c["score"]}
            for c in candidate_scores[1:5]  # Top 5 alternatives
        ]

        # Calculate confidence based on score gap
        confidence = self._calculate_confidence(candidate_scores)

        result = RoutingDecision(
            issue_number=issue_number,
            repository=f"{owner}/{repo}",
            assignee=best["username"],
            score=best["score"],
            scores=best["scores"],
            confidence=confidence,
            fallback_used=False,
            alternatives=alternatives,
        )

        self.logger.info(
            f"Assignment: {result.assignee} (score: {result.score:.3f}, confidence: {result.confidence:.3f})"
        )

        return result

    def _get_issue(self, owner: str, repo: str, issue_number: int) -> dict:
        """Get issue or PR details."""
        endpoint = f"/repos/{owner}/{repo}/issues/{issue_number}"
        return self.client.get(endpoint)

    def _get_candidates(self, owner: str, repo: str) -> list[dict]:
        """Get list of candidate assignees.

        Returns organization members with write access to repository.
        """
        # Get repository collaborators
        endpoint = f"/repos/{owner}/{repo}/collaborators"
        collaborators = self.client.get(endpoint)

        # Filter to those with write access or higher
        candidates = []
        for collaborator in collaborators:
            permissions = collaborator.get("permissions", {})
            if permissions.get("push") or permissions.get("admin"):
                candidates.append(collaborator)

        self.logger.debug(f"Found {len(candidates)} candidate assignees")
        return candidates

    def _calculate_factor_scores(self, owner: str, repo: str, candidate: dict, issue: dict) -> RoutingFactorScores:
        """Calculate routing factor scores for candidate.

        Args:
            owner: Repository owner
            repo: Repository name
            candidate: Candidate user data
            issue: Issue/PR data

        Returns:
            Factor scores (0.0 to 1.0 for each factor)

        """
        username = candidate["login"]

        # Calculate each factor
        expertise = self._calculate_expertise(owner, repo, username, issue)
        workload = self._calculate_workload(owner, repo, username)
        response_time = self._calculate_response_time(owner, repo, username)
        availability = self._calculate_availability(owner, repo, username)
        performance = self._calculate_performance(owner, repo, username)

        return RoutingFactorScores(
            expertise=expertise,
            workload=workload,
            response_time=response_time,
            availability=availability,
            performance=performance,
        )

    def _calculate_expertise(self, owner: str, repo: str, username: str, issue: dict) -> float:
        """Calculate expertise score based on historical contributions.

        Factors:
        - Commits to files in issue
        - Past issues/PRs with similar labels
        - Code review participation

        Returns:
            Expertise score (0.0 to 1.0)

        """
        score = 0.0

        try:
            # Get user's commits in last 90 days
            since = (datetime.now(timezone.utc) - timedelta(days=90)).isoformat()
            endpoint = f"/repos/{owner}/{repo}/commits"
            params = {"author": username, "since": since, "per_page": 100}
            commits = self.client.get(endpoint, params=params)

            # More commits = higher expertise (up to 50 commits)
            commit_score = min(1.0, len(commits) / 50)
            score += commit_score * 0.5

            # Get user's closed issues in last 90 days
            endpoint = f"/repos/{owner}/{repo}/issues"
            params = {
                "assignee": username,
                "state": "closed",
                "since": since,
                "per_page": 100,
            }
            closed_issues = self.client.get(endpoint, params=params)

            # More closed issues = higher expertise (up to 20 issues)
            issues_score = min(1.0, len(closed_issues) / 20)
            score += issues_score * 0.3

            # Check for label overlap with past issues
            issue_labels = {label["name"] for label in issue.get("labels", [])}
            if issue_labels:
                matching_labels = 0
                for closed_issue in closed_issues[:20]:  # Check recent 20
                    closed_labels = {label["name"] for label in closed_issue.get("labels", [])}
                    if issue_labels & closed_labels:  # Intersection
                        matching_labels += 1

                label_score = min(1.0, matching_labels / 5)
                score += label_score * 0.2

            return min(1.0, score)

        except Exception as e:
            self.logger.warning(f"Error calculating expertise for {username}: {e}")
            return 0.5  # Default middle score on error

    def _calculate_workload(self, owner: str, repo: str, username: str) -> float:
        """Calculate workload score (inverse of current assignments).

        Lower workload = higher score

        Returns:
            Workload score (0.0 to 1.0)

        """
        try:
            # Get currently assigned open issues
            endpoint = f"/repos/{owner}/{repo}/issues"
            params = {"assignee": username, "state": "open", "per_page": 100}
            open_issues = self.client.get(endpoint, params=params)

            current_count = len(open_issues)

            # Normalize based on max assignments (inverted)
            # Guard against division by zero
            max_assignments = self.config.max_assignments_per_user
            if max_assignments <= 0:
                max_assignments = 10  # Default fallback
            normalized = current_count / max_assignments

            # Score is inverse of workload (more work = lower score)
            score = max(0.0, 1.0 - normalized)

            self.logger.debug(
                f"Workload for {username}: {current_count} issues (score: {score:.3f})"  # noqa: E501
            )

            return score

        except Exception as e:
            self.logger.warning(f"Error calculating workload for {username}: {e}")
            return 0.5

    def _calculate_response_time(self, owner: str, repo: str, username: str) -> float:
        """Calculate response time score based on average time to first comment.

        Faster response = higher score

        Returns:
            Response time score (0.0 to 1.0)

        """
        try:
            # Get recent closed issues assigned to user
            since = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
            endpoint = f"/repos/{owner}/{repo}/issues"
            params = {
                "assignee": username,
                "state": "closed",
                "since": since,
                "per_page": 20,
            }
            issues = self.client.get(endpoint, params=params)

            if not issues:
                return 0.5  # No data, use middle score

            total_response_time = 0.0
            count = 0

            for issue in issues[:10]:  # Sample recent 10
                created = datetime.fromisoformat(issue["created_at"].replace("Z", "+00:00"))

                # Get first comment by assignee
                comments_endpoint = issue["comments_url"]
                try:
                    comments = self.client.get(comments_endpoint.replace(self.client.base_url, ""))
                except Exception as exc:
                    self.logger.debug(
                        "Failed to fetch comments for %s: %s",
                        comments_endpoint,
                        exc,
                    )
                    comments = None

                if comments is None:
                    continue

                for comment in comments:
                    if comment["user"]["login"] == username:
                        commented = datetime.fromisoformat(comment["created_at"].replace("Z", "+00:00"))
                        response_time = (
                            # hours
                            commented - created
                        ).total_seconds() / 3600
                        total_response_time += response_time
                        count += 1
                        break  # First comment only

            if count == 0:
                return 0.5

            avg_response_hours = total_response_time / count

            # Score based on response time (faster = better)
            # 1 hour = 1.0, 24 hours = 0.5, 48+ hours = 0.0
            if avg_response_hours <= 1:
                score = 1.0
            elif avg_response_hours <= 24:
                score = 1.0 - ((avg_response_hours - 1) / 23) * 0.5
            else:
                score = max(0.0, 0.5 - ((avg_response_hours - 24) / 24) * 0.5)

            self.logger.debug(f"Response time for {username}: {avg_response_hours:.1f}h (score: {score:.3f})")

            return score

        except Exception as e:
            self.logger.warning(f"Error calculating response time for {username}: {e}")
            return 0.5

    def _calculate_availability(self, owner: str, repo: str, username: str) -> float:
        """Calculate availability score based on recent activity.

        More recent activity = higher availability

        Returns:
            Availability score (0.0 to 1.0)

        """
        try:
            # Get user's recent events
            endpoint = f"/users/{username}/events"
            params = {"per_page": 100}
            events = self.client.get(endpoint, params=params)

            if not events:
                return 0.3  # No recent activity

            # Find most recent event
            latest_event = events[0]
            latest_time = datetime.fromisoformat(latest_event["created_at"].replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            hours_since = (now - latest_time).total_seconds() / 3600

            # Score based on recency
            # < 1 hour = 1.0, < 24 hours = 0.8, < 7 days = 0.5, else 0.2
            if hours_since < 1:
                score = 1.0
            elif hours_since < 24:
                score = 0.8
            elif hours_since < 168:  # 7 days
                score = 0.5
            else:
                score = 0.2

            self.logger.debug(f"Availability for {username}: {hours_since:.1f}h ago (score: {score:.3f})")

            return score

        except Exception as e:
            self.logger.warning(f"Error calculating availability for {username}: {e}")
            return 0.5

    def _calculate_performance(self, owner: str, repo: str, username: str) -> float:
        """Calculate performance score based on success rate.

        Higher success rate = higher score

        Returns:
            Performance score (0.0 to 1.0)

        """
        try:
            # Get issues closed by user in last 90 days
            since = (datetime.now(timezone.utc) - timedelta(days=90)).isoformat()
            endpoint = f"/repos/{owner}/{repo}/issues"
            params = {
                "assignee": username,
                "state": "closed",
                "since": since,
                "per_page": 100,
            }
            closed_issues = self.client.get(endpoint, params=params)

            if not closed_issues:
                return 0.5  # No data

            # Count how many were closed as completed vs other reasons
            completed = 0
            for issue in closed_issues[:30]:  # Sample recent 30
                # Check if closed with resolution (not stale, not duplicate,
                # etc.)
                labels = {label["name"].lower() for label in issue.get("labels", [])}

                # Consider completed if no negative labels
                negative_labels = {"wontfix", "duplicate", "invalid", "stale"}
                if not labels & negative_labels:
                    completed += 1

            total = min(len(closed_issues), 30)
            success_rate = completed / total if total > 0 else 0.5

            self.logger.debug(f"Performance for {username}: {completed}/{total} (score: {success_rate:.3f})")

            return success_rate

        except Exception as e:
            self.logger.warning(f"Error calculating performance for {username}: {e}")
            return 0.5

    def _calculate_overall_score(self, scores: RoutingFactorScores) -> float:
        """Calculate weighted overall score from factor scores.

        Args:
            scores: Individual factor scores

        Returns:
            Overall score (0.0 to 1.0)

        """
        overall = (
            scores.expertise * self.config.factors["expertise"]
            + scores.workload * self.config.factors["workload"]
            + scores.response_time * self.config.factors["response_time"]
            + scores.availability * self.config.factors["availability"]
            + scores.performance * self.config.factors["performance"]
        )

        return min(1.0, max(0.0, overall))

    def _calculate_confidence(self, candidate_scores: list[dict]) -> float:
        """Calculate confidence in routing decision.

        Higher score gap between top candidates = higher confidence

        Args:
            candidate_scores: Sorted list of candidate scores

        Returns:
            Confidence score (0.0 to 1.0)

        """
        if len(candidate_scores) < 2:
            return 1.0  # Only one candidate

        top_score = candidate_scores[0]["score"]
        second_score = candidate_scores[1]["score"]

        # Score gap as confidence
        gap = top_score - second_score

        # Larger gap = higher confidence
        confidence = min(1.0, 0.5 + (gap * 2))  # Base 0.5, up to 1.0

        return confidence

    def _fallback_assignment(
        self,
        owner: str,
        repo: str,
        issue_number: int,
        issue: dict,
        candidates: list[dict],
    ) -> RoutingDecision:
        """Fallback assignment using simple strategy.

        Args:
            owner: Repository owner
            repo: Repository name
            issue_number: Issue number
            issue: Issue data
            candidates: List of candidates

        Returns:
            Routing decision using fallback

        """
        self.logger.info("Using fallback assignment strategy")

        # Try strategies in order from config
        for strategy in self.config.fallback_strategy:
            if strategy == "round_robin":
                # Get last assigned user and pick next
                try:
                    endpoint = f"/repos/{owner}/{repo}/issues"
                    params = {"state": "all", "per_page": 10}
                    recent = self.client.get(endpoint, params=params)

                    # Find last assigned
                    last_assigned = None
                    for r_issue in recent:
                        if r_issue.get("assignee"):
                            last_assigned = r_issue["assignee"]["login"]
                            break

                    if last_assigned:
                        # Find next candidate after last assigned
                        usernames = [c["login"] for c in candidates]
                        if last_assigned in usernames:
                            idx = usernames.index(last_assigned)
                            next_idx = (idx + 1) % len(usernames)
                            assignee = usernames[next_idx]
                        else:
                            assignee = usernames[0]
                    else:
                        assignee = candidates[0]["login"]

                    return RoutingDecision(
                        issue_number=issue_number,
                        repository=f"{owner}/{repo}",
                        assignee=assignee,
                        score=0.5,
                        scores=RoutingFactorScores(
                            expertise=0.5,
                            workload=0.5,
                            response_time=0.5,
                            availability=0.5,
                            performance=0.5,
                        ),
                        confidence=0.3,
                        fallback_used=True,
                        alternatives=[],
                    )

                except Exception as e:
                    self.logger.warning(f"Round robin failed: {e}")
                    continue

            elif strategy == "random":
                # Random assignment
                import random

                assignee = random.choice(candidates)["login"]  # nosec B311

                return RoutingDecision(
                    issue_number=issue_number,
                    repository=f"{owner}/{repo}",
                    assignee=assignee,
                    score=0.5,
                    scores=RoutingFactorScores(
                        expertise=0.5,
                        workload=0.5,
                        response_time=0.5,
                        availability=0.5,
                        performance=0.5,
                    ),
                    confidence=0.2,
                    fallback_used=True,
                    alternatives=[],
                )

        # If all strategies fail, assign to first candidate
        return RoutingDecision(
            issue_number=issue_number,
            repository=f"{owner}/{repo}",
            assignee=candidates[0]["login"],
            score=0.5,
            scores=RoutingFactorScores(
                expertise=0.5,
                workload=0.5,
                response_time=0.5,
                availability=0.5,
                performance=0.5,
            ),
            confidence=0.1,
            fallback_used=True,
            alternatives=[],
        )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Intelligent routing for issue/PR assignment")
    parser.add_argument("--owner", required=True, help="Repository owner")
    parser.add_argument("--repo", required=True, help="Repository name")
    parser.add_argument("--issue", required=True, type=int, help="Issue number")
    parser.add_argument(
        "--assign",
        action="store_true",
        help="Actually assign the issue (default: dry run)",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    # Set up logging
    log_level = "DEBUG" if args.debug else "INFO"
    logger = setup_logger(__name__, log_level)

    try:
        # Initialize GitHub client
        client = GitHubAPIClient()

        # Load configuration
        config_loader = ConfigLoader()
        try:
            config_dict = config_loader.load("routing.yml")
            config = RoutingConfig(**config_dict.get("issue_assignment_router", {}))
        except FileNotFoundError:
            logger.warning("No routing config found, using defaults")
            config = RoutingConfig()

        # Calculate assignment
        router = IntelligentRouter(client, config)
        result = router.calculate_assignment(args.owner, args.repo, args.issue)

        # Output result
        print(f"\n{'=' * 60}")
        print("Intelligent Routing Decision")
        print(f"{'=' * 60}")
        print(f"Repository: {result.repository}")
        print(f"Issue Number: {result.issue_number}")
        print(f"Timestamp: {result.timestamp.isoformat()}")
        print(f"\nSelected Assignee: {result.assignee}")
        print(f"Overall Score: {result.score:.3f}")
        print(f"Confidence: {result.confidence:.1%}")
        print(f"Fallback Used: {'Yes' if result.fallback_used else 'No'}")

        print("\nFactor Scores:")
        print(
            f"  • Expertise: {result.scores.expertise:.3f} (weight: {config.factors['expertise']})"  # noqa: E501
        )
        print(
            f"  • Workload: {result.scores.workload:.3f} (weight: {config.factors['workload']})"  # noqa: E501
        )
        print(
            f"  • Response Time: {result.scores.response_time:.3f} (weight: {config.factors['response_time']})"  # noqa: E501
        )
        print(
            f"  • Availability: {result.scores.availability:.3f} (weight: {config.factors['availability']})"  # noqa: E501
        )
        print(
            f"  • Performance: {result.scores.performance:.3f} (weight: {config.factors['performance']})"  # noqa: E501
        )

        if result.alternatives:
            print("\nAlternative Assignees:")
            for alt in result.alternatives[:3]:
                print(f"  • {alt['username']}: {alt['score']:.3f}")

        print(f"{'=' * 60}\n")

        # Actually assign if requested
        if args.assign:
            logger.info(f"Assigning issue to {result.assignee}")
            endpoint = f"/repos/{args.owner}/{args.repo}/issues/{args.issue}"
            client.patch(endpoint, {"assignees": [result.assignee]})
            print(f"✅ Assigned issue #{args.issue} to {result.assignee}")

        sys.exit(0)

    except Exception as e:
        logger.error(f"Error calculating routing: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
