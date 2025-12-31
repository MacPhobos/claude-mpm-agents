"""Extract testable rules from BASE-AGENT.md files."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


@dataclass
class TestableRule:
    """Represents a testable rule extracted from BASE-AGENT.md."""

    rule_id: str
    category: str
    description: str
    positive_patterns: list[str] = field(default_factory=list)
    negative_patterns: list[str] = field(default_factory=list)
    source_file: str = ""
    severity: Literal["error", "warning", "info"] = "error"


class InstructionExtractor:
    """Extract testable rules from BASE-AGENT.md files."""

    def __init__(self, project_root: Path):
        """Initialize extractor with project root.

        Args:
            project_root: Path to project root directory
        """
        self.project_root = Path(project_root)
        self.agents_dir = self.project_root / "agents"

    def extract_root_rules(self) -> list[TestableRule]:
        """Extract rules from root BASE-AGENT.md.

        Returns:
            List of TestableRule objects from root-level instructions
        """
        root_base = self.project_root / "agents" / "BASE-AGENT.md"
        if not root_base.exists():
            return []

        rules = []

        # Git conventional commits
        rules.append(
            TestableRule(
                rule_id="git_conventional_commits",
                category="git_workflow",
                description="Commit messages must follow conventional commits format",
                positive_patterns=[
                    r"^(feat|fix|docs|refactor|perf|test|chore):",
                    r"^(feat|fix|docs|refactor|perf|test|chore)(\(.+?\))?:.+",
                ],
                negative_patterns=[
                    r"^(update|change|wip|tmp|fix bug|add feature)",
                ],
                source_file=str(root_base),
                severity="error",
            )
        )

        # Markdown output format
        rules.append(
            TestableRule(
                rule_id="markdown_output",
                category="output_format",
                description="Responses must use markdown formatting with headers",
                positive_patterns=[
                    r"^##\s+.+",  # Section headers
                    r"```[a-z]*\n.*?```",  # Code blocks
                ],
                negative_patterns=[],
                source_file=str(root_base),
                severity="warning",
            )
        )

        # Handoff protocol (only applies if handoff keywords are present)
        # Note: This is tested separately in role_boundary tests with HandoffComplianceMetric
        # Removed from root rules since not all responses are handoffs

        # Search before implement
        rules.append(
            TestableRule(
                rule_id="search_before_implement",
                category="code_quality",
                description="Must search for existing implementations before creating new code",
                positive_patterns=[
                    r"(searched|found existing|verified no existing|checked for)",
                    r"(grep|glob|search)",
                ],
                negative_patterns=[],
                source_file=str(root_base),
                severity="warning",
            )
        )

        return rules

    def extract_category_rules(self, category: str) -> list[TestableRule]:
        """Extract rules from category-specific BASE-AGENT.md.

        Args:
            category: Category name (e.g., 'engineer', 'qa', 'ops')

        Returns:
            List of TestableRule objects for the category
        """
        category_base = self.agents_dir / category / "BASE-AGENT.md"
        if not category_base.exists():
            return []

        rules = []

        if category == "engineer":
            # Type safety
            rules.append(
                TestableRule(
                    rule_id="engineer_type_safety",
                    category="engineer",
                    description="Engineer responses must emphasize type safety",
                    positive_patterns=[
                        r"type\s+(hint|annotation|safety|checking)",
                        r"(strict|mypy|typing)",
                    ],
                    negative_patterns=[
                        r"\bany\b.*type",  # Using 'any' type
                    ],
                    source_file=str(category_base),
                    severity="error",
                )
            )

            # File size limit
            rules.append(
                TestableRule(
                    rule_id="engineer_file_size_limit",
                    category="engineer",
                    description="Files must be under 800 lines",
                    positive_patterns=[
                        r"(800|file size|lines? limit)",
                    ],
                    negative_patterns=[],
                    source_file=str(category_base),
                    severity="warning",
                )
            )

        elif category == "qa":
            # Bug report format
            rules.append(
                TestableRule(
                    rule_id="qa_bug_report_format",
                    category="qa",
                    description="Bug reports must include steps to reproduce, expected, actual",
                    positive_patterns=[
                        r"(steps? to reproduce|reproduction steps?)",
                        r"expected.*:",
                        r"actual.*:",
                    ],
                    negative_patterns=[],
                    source_file=str(category_base),
                    severity="error",
                )
            )

            # CI-safe tests
            rules.append(
                TestableRule(
                    rule_id="qa_ci_safe_tests",
                    category="qa",
                    description="Test commands must be CI-safe",
                    positive_patterns=[
                        r"(pytest|npm test|cargo test)",
                    ],
                    negative_patterns=[
                        r"(--interactive|-i\s)",  # Interactive flags
                        r"(git rebase -i|git add -i)",
                    ],
                    source_file=str(category_base),
                    severity="error",
                )
            )

        elif category == "ops":
            # Deployment verification
            rules.append(
                TestableRule(
                    rule_id="ops_deployment_verification",
                    category="ops",
                    description="Deployments must include verification steps",
                    positive_patterns=[
                        r"(verify|verification|health check|smoke test)",
                        r"(rollback|revert) plan",
                    ],
                    negative_patterns=[],
                    source_file=str(category_base),
                    severity="error",
                )
            )

            # Security scan
            rules.append(
                TestableRule(
                    rule_id="ops_security_scan",
                    category="ops",
                    description="Must include security scanning in deployment",
                    positive_patterns=[
                        r"(security scan|vulnerability|CVE|audit)",
                    ],
                    negative_patterns=[],
                    source_file=str(category_base),
                    severity="warning",
                )
            )

        return rules
