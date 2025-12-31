"""Custom DeepEval metrics for instruction compliance."""

import re

from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

from tests.fixtures.instruction_extractor import TestableRule


class InstructionComplianceMetric(BaseMetric):
    """Metric to check compliance with instruction rules via regex patterns."""

    def __init__(
        self,
        rules: list[TestableRule],
        threshold: float = 0.8,
        strict_mode: bool = False,
    ):
        """Initialize metric with rules.

        Args:
            rules: List of TestableRule objects to check
            threshold: Minimum score to pass (0.0-1.0)
            strict_mode: If True, all rules must pass
        """
        self.rules = rules
        self.threshold = threshold
        self.strict_mode = strict_mode
        self.violations: list[str] = []

    @property
    def __name__(self) -> str:
        return "Instruction Compliance"

    def measure(self, test_case: LLMTestCase) -> float:
        """Measure compliance with instruction rules.

        Args:
            test_case: Test case with actual_output to validate

        Returns:
            Score between 0.0 and 1.0
        """
        self.violations = []
        output = test_case.actual_output

        if not output:
            self.score = 0.0
            self.success = False
            self.reason = "Empty output"
            return self.score

        passed_rules = 0
        total_rules = len(self.rules)

        for rule in self.rules:
            rule_passed = self._check_rule(output, rule)
            if rule_passed:
                passed_rules += 1
            else:
                self.violations.append(f"{rule.rule_id}: {rule.description}")

        # Calculate score
        if total_rules == 0:
            self.score = 1.0
        else:
            self.score = passed_rules / total_rules

        # Determine success
        if self.strict_mode:
            self.success = self.score == 1.0
        else:
            self.success = self.score >= self.threshold

        # Build reason
        if self.success:
            self.reason = f"Passed {passed_rules}/{total_rules} rules"
        else:
            self.reason = f"Failed {total_rules - passed_rules}/{total_rules} rules: {', '.join(self.violations[:3])}"

        return self.score

    def _check_rule(self, output: str, rule: TestableRule) -> bool:
        """Check if output complies with a single rule.

        Args:
            output: Agent output to check
            rule: TestableRule to validate

        Returns:
            True if rule passes, False otherwise
        """
        # Check positive patterns (at least one must match)
        if rule.positive_patterns:
            has_positive = any(
                re.search(pattern, output, re.IGNORECASE | re.MULTILINE)
                for pattern in rule.positive_patterns
            )
            if not has_positive:
                return False

        # Check negative patterns (none should match)
        if rule.negative_patterns:
            has_negative = any(
                re.search(pattern, output, re.IGNORECASE | re.MULTILINE)
                for pattern in rule.negative_patterns
            )
            if has_negative:
                return False

        return True

    async def a_measure(self, test_case: LLMTestCase) -> float:
        """Async version of measure."""
        return self.measure(test_case)

    def is_successful(self) -> bool:
        """Check if metric passed."""
        return self.success


class GitWorkflowComplianceMetric(BaseMetric):
    """Metric specifically for git workflow compliance."""

    def __init__(self, threshold: float = 0.9):
        """Initialize metric.

        Args:
            threshold: Minimum score to pass (0.0-1.0)
        """
        self.threshold = threshold
        self.violations: list[str] = []

    @property
    def __name__(self) -> str:
        return "Git Workflow Compliance"

    def measure(self, test_case: LLMTestCase) -> float:
        """Measure git workflow compliance.

        Args:
            test_case: Test case with actual_output to validate

        Returns:
            Score between 0.0 and 1.0
        """
        self.violations = []
        output = test_case.actual_output

        if not output:
            self.score = 0.0
            self.success = False
            self.reason = "Empty output"
            return self.score

        checks_passed = 0
        total_checks = 3

        # Check 1: Conventional commit format
        conventional_pattern = r"^(feat|fix|docs|refactor|perf|test|chore)(\(.+?\))?:.+"
        commit_blocks = re.findall(r"```(?:bash|sh)?\n(.*?)```", output, re.DOTALL)
        commit_messages = []

        # Extract commit messages from git commit commands
        for block in commit_blocks:
            git_commits = re.findall(r'git commit.*?-m\s+["\'](.+?)["\']', block, re.DOTALL)
            commit_messages.extend(git_commits)

        # Also check for commit message sections
        commit_sections = re.findall(
            r"(?:commit message|git commit).*?:\s*[`\"'](.+?)[`\"']", output, re.IGNORECASE
        )
        commit_messages.extend(commit_sections)

        # Check for commit messages in code blocks (common pattern: ### Git Commit followed by ```)
        for block in commit_blocks:
            # Look for lines starting with conventional commit prefixes
            lines = block.strip().split("\n")
            for line in lines:
                if re.match(conventional_pattern, line.strip(), re.MULTILINE):
                    commit_messages.append(line.strip())
                    break  # Only take first line of commit message

        if commit_messages:
            valid_commits = sum(
                1
                for msg in commit_messages
                if re.match(conventional_pattern, msg.strip(), re.MULTILINE)
            )
            if valid_commits > 0:
                checks_passed += 1
            else:
                self.violations.append("Commit messages don't follow conventional format")
        else:
            # No commits found, check if output mentions git workflow
            if re.search(r"(git|commit|conventional)", output, re.IGNORECASE):
                checks_passed += 0.5

        # Check 2: Explanation of WHY (not just WHAT)
        # Look for explicit WHY or descriptive reasoning
        has_why = (
            re.search(r"\b(why|because|reason|rationale)[\s:]", output, re.IGNORECASE)
            or re.search(r"WHY:", output)
            or any(
                # Check if commit messages are descriptive (>40 chars and explain purpose)
                len(msg.strip()) > 40
                and any(
                    word in msg.lower()
                    for word in ["enable", "improve", "fix", "add", "remove", "update"]
                )
                for msg in commit_messages
            )
        )
        if has_why:
            checks_passed += 1
        else:
            self.violations.append("Missing explanation of WHY changes were made")

        # Check 3: No bad commit messages
        bad_patterns = [
            r"(update code|fix bug|changes|wip|tmp)",
        ]
        has_bad_commit = any(re.search(pattern, output, re.IGNORECASE) for pattern in bad_patterns)
        if not has_bad_commit:
            checks_passed += 1
        else:
            self.violations.append("Contains poor commit message examples")

        # Calculate score
        self.score = checks_passed / total_checks
        self.success = self.score >= self.threshold

        if self.success:
            self.reason = f"Git workflow compliance: {self.score:.1%}"
        else:
            self.reason = f"Git violations: {', '.join(self.violations)}"

        return self.score

    async def a_measure(self, test_case: LLMTestCase) -> float:
        """Async version of measure."""
        return self.measure(test_case)

    def is_successful(self) -> bool:
        """Check if metric passed."""
        return self.success


class OutputFormatComplianceMetric(BaseMetric):
    """Metric for checking output format compliance (markdown, structure)."""

    def __init__(self, threshold: float = 0.7):
        """Initialize metric.

        Args:
            threshold: Minimum score to pass (0.0-1.0)
        """
        self.threshold = threshold
        self.violations: list[str] = []

    @property
    def __name__(self) -> str:
        return "Output Format Compliance"

    def measure(self, test_case: LLMTestCase) -> float:
        """Measure output format compliance.

        Args:
            test_case: Test case with actual_output to validate

        Returns:
            Score between 0.0 and 1.0
        """
        self.violations = []
        output = test_case.actual_output

        if not output:
            self.score = 0.0
            self.success = False
            self.reason = "Empty output"
            return self.score

        checks_passed = 0
        total_checks = 5

        # Check 1: Has markdown headers
        if re.search(r"^##+ .+", output, re.MULTILINE):
            checks_passed += 1
        else:
            self.violations.append("Missing markdown section headers")

        # Check 2: Has code blocks (if code is mentioned)
        if re.search(r"(code|implementation|function|class)", output, re.IGNORECASE):
            if re.search(r"```[a-z]*\n.*?```", output, re.DOTALL):
                checks_passed += 1
            else:
                self.violations.append("Code mentioned but no code blocks found")
        else:
            checks_passed += 1  # Not applicable

        # Check 3: Has clear structure (multiple sections)
        section_count = len(re.findall(r"^##+ .+", output, re.MULTILINE))
        if section_count >= 2:
            checks_passed += 1
        else:
            self.violations.append("Insufficient structure (less than 2 sections)")

        # Check 4: Not too terse (at least 100 characters)
        if len(output) >= 100:
            checks_passed += 1
        else:
            self.violations.append(f"Output too terse ({len(output)} chars)")

        # Check 5: Has proper lists or bullet points
        if re.search(r"^[\-\*\+] .+", output, re.MULTILINE) or re.search(
            r"^\d+\. .+", output, re.MULTILINE
        ):
            checks_passed += 1
        else:
            self.violations.append("No lists or bullet points found")

        # Calculate score
        self.score = checks_passed / total_checks
        self.success = self.score >= self.threshold

        if self.success:
            self.reason = f"Format compliance: {self.score:.1%}"
        else:
            self.reason = f"Format violations: {', '.join(self.violations)}"

        return self.score

    async def a_measure(self, test_case: LLMTestCase) -> float:
        """Async version of measure."""
        return self.measure(test_case)

    def is_successful(self) -> bool:
        """Check if metric passed."""
        return self.success
