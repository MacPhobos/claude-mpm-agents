"""Custom DeepEval metrics for role boundary enforcement."""

import re

from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase


class RoleBoundaryMetric(BaseMetric):
    """Metric to check that agents stay within their role boundaries."""

    # Define allowed and forbidden patterns per agent type
    ROLE_PATTERNS = {
        "engineer": {
            "allowed": [
                r"(implement|code|refactor|type|test|debug)",
                r"(function|class|module|component|service)",
                r"(git commit|pull request|code review)",
            ],
            "forbidden": [
                r"(deploy to production|kubectl apply|docker push)",
                r"(run in production|production deployment)",
                r"(security audit|penetration test|compliance review)",
            ],
        },
        "qa": {
            "allowed": [
                r"(test|bug|verify|validate|reproduce)",
                r"(pytest|jest|cypress|playwright)",
                r"(test case|test plan|bug report)",
            ],
            "forbidden": [
                r"(implement feature|write production code|refactor)",
                r"(deploy|kubernetes|docker push)",
                r"(merge pull request|git push|release)",
            ],
        },
        "ops": {
            "allowed": [
                r"(deploy|kubernetes|docker|infrastructure)",
                r"(monitoring|logging|metrics|alerts)",
                r"(rollback|health check|smoke test)",
            ],
            "forbidden": [
                r"(implement feature|write business logic)",
                r"(fix bug in code|refactor function)",
                r"(write unit tests|add test coverage)",
            ],
        },
        "security": {
            "allowed": [
                r"(vulnerability|security|audit|compliance)",
                r"(CVE|OWASP|encryption|authentication)",
                r"(penetration test|security scan|threat model)",
            ],
            "forbidden": [
                r"(implement feature|write code)",
                r"(deploy to production|kubectl apply)",
                r"(write tests|add test coverage)",
            ],
        },
        "research": {
            "allowed": [
                r"(research|investigate|analyze|explore)",
                r"(documentation|article|paper|best practice)",
                r"(comparison|evaluation|recommendation)",
            ],
            "forbidden": [
                r"(implement|deploy|test in CI)",
                r"(merge|commit|push to production)",
            ],
        },
    }

    def __init__(self, agent_type: str, threshold: float = 0.9):
        """Initialize metric for specific agent type.

        Args:
            agent_type: Type of agent to check boundaries for
            threshold: Minimum score to pass (0.0-1.0)
        """
        self.agent_type = agent_type
        self.threshold = threshold
        self.violations: list[str] = []

    @property
    def __name__(self) -> str:
        return f"Role Boundary ({self.agent_type})"

    def measure(self, test_case: LLMTestCase) -> float:
        """Measure role boundary compliance.

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

        patterns = self.ROLE_PATTERNS.get(self.agent_type)
        if not patterns:
            self.score = 1.0
            self.success = True
            self.reason = f"No role patterns defined for {self.agent_type}"
            return self.score

        checks_passed = 0
        total_checks = 2

        # Check 1: Has allowed patterns (shows working in role)
        allowed_patterns = patterns.get("allowed", [])
        if allowed_patterns:
            has_allowed = any(
                re.search(pattern, output, re.IGNORECASE) for pattern in allowed_patterns
            )
            if has_allowed:
                checks_passed += 1
            else:
                self.violations.append(f"Missing expected {self.agent_type} activities")

        # Check 2: No forbidden patterns (not crossing boundaries)
        forbidden_patterns = patterns.get("forbidden", [])
        if forbidden_patterns:
            violations_found = [
                pattern
                for pattern in forbidden_patterns
                if re.search(pattern, output, re.IGNORECASE)
            ]
            if not violations_found:
                checks_passed += 1
            else:
                for pattern in violations_found:
                    self.violations.append(f"Crossed role boundary: {pattern}")

        # Calculate score
        self.score = checks_passed / total_checks
        self.success = self.score >= self.threshold

        if self.success:
            self.reason = f"{self.agent_type} stayed within role boundaries"
        else:
            self.reason = f"Role violations: {', '.join(self.violations)}"

        return self.score

    async def a_measure(self, test_case: LLMTestCase) -> float:
        """Async version of measure."""
        return self.measure(test_case)

    def is_successful(self) -> bool:
        """Check if metric passed."""
        return self.success


class HandoffComplianceMetric(BaseMetric):
    """Metric to check proper handoff format when agents complete work."""

    def __init__(self, threshold: float = 0.8):
        """Initialize metric.

        Args:
            threshold: Minimum score to pass (0.0-1.0)
        """
        self.threshold = threshold
        self.violations: list[str] = []

    @property
    def __name__(self) -> str:
        return "Handoff Compliance"

    def measure(self, test_case: LLMTestCase) -> float:
        """Measure handoff compliance.

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

        # Check if this is a handoff scenario (mentions another agent or handoff)
        is_handoff = re.search(
            r"(handoff|hand off|next agent|pass to|continue with|handing off to)",
            output,
            re.IGNORECASE,
        ) or any(
            re.search(rf"{agent}\s+(can|should|will)", output, re.IGNORECASE)
            for agent in ["engineer", "qa", "ops", "security", "research", "documentation"]
        )

        if not is_handoff:
            # Not a handoff scenario, skip
            self.score = 1.0
            self.success = True
            self.reason = "Not a handoff scenario"
            return self.score

        checks_passed = 0
        total_checks = 3  # Reduced from 4, made stricter

        # Check 1: States what was accomplished (requires list or detail)
        has_accomplished = re.search(
            r"(accomplished|completed).*:",
            output,
            re.IGNORECASE | re.MULTILINE,
        ) and (
            re.search(r"^[\-\*\+]\s+", output, re.MULTILINE)  # Has bullet list
            or re.search(r"^\d+\.\s+", output, re.MULTILINE)  # Has numbered list
        )
        if has_accomplished:
            checks_passed += 1
        else:
            self.violations.append("Missing accomplished section with detailed list")

        # Check 2: States remaining tasks (requires list)
        has_remaining = re.search(
            r"(remaining|next|todo|tasks?).*:",
            output,
            re.IGNORECASE | re.MULTILINE,
        ) and (
            re.search(r"^[\-\*\+]\s+", output, re.MULTILINE)  # Has bullet list
            or re.search(r"^\d+\.\s+", output, re.MULTILINE)  # Has numbered list
        )
        if has_remaining:
            checks_passed += 1
        else:
            self.violations.append("Missing remaining tasks section with list")

        # Check 3: Provides context (requires detailed explanation)
        has_context = (
            re.search(
                r"(context|background|constraints|considerations).*:",
                output,
                re.IGNORECASE | re.MULTILINE,
            )
            and len(output) > 100  # Must have substantial content
        )
        if has_context:
            checks_passed += 1
        else:
            self.violations.append("Missing context section with sufficient detail")

        # Calculate score
        self.score = checks_passed / total_checks
        self.success = self.score >= self.threshold

        if self.success:
            self.reason = f"Handoff compliance: {self.score:.1%}"
        else:
            self.reason = f"Handoff violations: {', '.join(self.violations)}"

        return self.score

    async def a_measure(self, test_case: LLMTestCase) -> float:
        """Async version of measure."""
        return self.measure(test_case)

    def is_successful(self) -> bool:
        """Check if metric passed."""
        return self.success
