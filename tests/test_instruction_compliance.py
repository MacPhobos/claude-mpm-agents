"""Tests for BASE-AGENT.md instruction compliance."""

import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase

from tests.fixtures.instruction_extractor import TestableRule
from tests.fixtures.mock_responses import MockResponseGenerator
from tests.metrics.instruction_compliance import (
    GitWorkflowComplianceMetric,
    InstructionComplianceMetric,
    OutputFormatComplianceMetric,
)


@pytest.mark.instruction_compliance
class TestRootBaseAgentCompliance:
    """Test compliance with root BASE-AGENT.md instructions."""

    def test_engineer_compliant_response_passes(
        self,
        mock_generator: MockResponseGenerator,
        root_base_rules: list[TestableRule],
    ):
        """Test that a compliant engineer response passes all checks."""
        # Generate compliant response
        response = mock_generator.generate_compliant_response(
            agent_type="engineer", task_type="implement_feature"
        )

        # Create test case
        test_case = LLMTestCase(
            input="Implement user authentication with JWT",
            actual_output=response.content,
        )

        # Check instruction compliance
        metric = InstructionComplianceMetric(rules=root_base_rules, threshold=0.8)
        assert_test(test_case, [metric])

    def test_engineer_non_compliant_response_fails(
        self,
        mock_generator: MockResponseGenerator,
        root_base_rules: list[TestableRule],
    ):
        """Test that a non-compliant response is detected."""
        # Generate non-compliant response
        response = mock_generator.generate_non_compliant_response(
            agent_type="engineer",
            task_type="no_structure",
            violations=["markdown_output"],
        )

        # Create test case
        test_case = LLMTestCase(
            input="Implement auth middleware",
            actual_output=response.content,
        )

        # Check instruction compliance - should fail
        metric = InstructionComplianceMetric(rules=root_base_rules, threshold=0.8)
        try:
            assert_test(test_case, [metric])
            pytest.fail("Expected assertion to fail but it passed")
        except AssertionError:
            # Expected to fail
            pass

    def test_git_workflow_conventional_commits(self, mock_generator: MockResponseGenerator):
        """Test that conventional commit format is enforced."""
        # Generate response with proper commit
        response = mock_generator.generate_compliant_response(
            agent_type="engineer", task_type="implement_feature"
        )

        test_case = LLMTestCase(
            input="Add new feature",
            actual_output=response.content,
        )

        metric = GitWorkflowComplianceMetric(threshold=0.8)
        assert_test(test_case, [metric])

    def test_git_workflow_bad_commits_detected(self, mock_generator: MockResponseGenerator):
        """Test that bad commit messages are detected."""
        # Generate response with poor commit
        response = mock_generator.generate_non_compliant_response(
            agent_type="engineer",
            task_type="poor_commit",
            violations=["git_conventional_commits"],
        )

        test_case = LLMTestCase(
            input="Fix the bug",
            actual_output=response.content,
        )

        metric = GitWorkflowComplianceMetric(threshold=0.9)
        try:
            assert_test(test_case, [metric])
            pytest.fail("Expected bad commit to be detected")
        except AssertionError:
            # Expected to fail
            pass

    def test_output_format_compliance(self, mock_generator: MockResponseGenerator):
        """Test that output format requirements are met."""
        response = mock_generator.generate_compliant_response(
            agent_type="engineer", task_type="refactor_code"
        )

        test_case = LLMTestCase(
            input="Refactor validation logic",
            actual_output=response.content,
        )

        metric = OutputFormatComplianceMetric(threshold=0.7)
        assert_test(test_case, [metric])

    def test_terse_response_fails_format_check(self, mock_generator: MockResponseGenerator):
        """Test that terse responses without structure fail."""
        response = mock_generator.generate_non_compliant_response(
            agent_type="engineer",
            task_type="no_structure",
            violations=["markdown_output"],
        )

        test_case = LLMTestCase(
            input="Add auth",
            actual_output=response.content,
        )

        metric = OutputFormatComplianceMetric(threshold=0.7)
        try:
            assert_test(test_case, [metric])
            pytest.fail("Expected terse response to fail")
        except AssertionError:
            # Expected to fail
            pass


@pytest.mark.instruction_compliance
class TestQAAgentCompliance:
    """Test QA agent-specific instruction compliance."""

    def test_qa_compliant_bug_report(
        self,
        mock_generator: MockResponseGenerator,
        category_rules,
    ):
        """Test that compliant QA bug report passes."""
        response = mock_generator.generate_compliant_response(
            agent_type="qa", task_type="bug_report"
        )

        test_case = LLMTestCase(
            input="Report login form validation bug",
            actual_output=response.content,
        )

        qa_rules = category_rules("qa")
        metric = InstructionComplianceMetric(rules=qa_rules, threshold=0.8)
        assert_test(test_case, [metric])

    def test_qa_ci_safe_test_commands(
        self,
        mock_generator: MockResponseGenerator,
        category_rules,
    ):
        """Test that CI-safe test commands are enforced."""
        response = mock_generator.generate_compliant_response(
            agent_type="qa", task_type="test_plan"
        )

        test_case = LLMTestCase(
            input="Create test plan for payment processing",
            actual_output=response.content,
        )

        qa_rules = category_rules("qa")
        # Filter to only CI-safe test rule (test plans don't need bug report format)
        ci_safe_rules = [r for r in qa_rules if r.rule_id == "qa_ci_safe_tests"]
        metric = InstructionComplianceMetric(rules=ci_safe_rules, threshold=0.8)
        assert_test(test_case, [metric])


@pytest.mark.instruction_compliance
class TestOpsAgentCompliance:
    """Test ops agent-specific instruction compliance."""

    def test_ops_deployment_verification(
        self,
        mock_generator: MockResponseGenerator,
        category_rules,
    ):
        """Test that deployment verification is required."""
        response = mock_generator.generate_compliant_response(
            agent_type="ops", task_type="deployment"
        )

        test_case = LLMTestCase(
            input="Deploy API v2 to production",
            actual_output=response.content,
        )

        ops_rules = category_rules("ops")
        metric = InstructionComplianceMetric(rules=ops_rules, threshold=0.8)
        assert_test(test_case, [metric])

    def test_ops_non_compliant_deployment_detected(
        self,
        mock_generator: MockResponseGenerator,
        category_rules,
    ):
        """Test that deployments without verification are detected."""
        response = mock_generator.generate_non_compliant_response(
            agent_type="ops",
            task_type="no_verification",
            violations=["ops_deployment_verification"],
        )

        test_case = LLMTestCase(
            input="Deploy to production",
            actual_output=response.content,
        )

        ops_rules = category_rules("ops")
        metric = InstructionComplianceMetric(rules=ops_rules, threshold=0.8)
        try:
            assert_test(test_case, [metric])
            pytest.fail("Expected deployment without verification to fail")
        except AssertionError:
            # Expected to fail
            pass
