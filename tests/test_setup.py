"""Basic tests to verify testing framework setup."""

import pytest

from tests.fixtures.agent_loader import AgentLoader
from tests.fixtures.instruction_extractor import InstructionExtractor
from tests.fixtures.mock_responses import ComplianceLevel, MockResponseGenerator


def test_agent_loader_initialization(agents_dir):
    """Test that AgentLoader can be initialized."""
    loader = AgentLoader(agents_dir)
    assert loader.agents_dir == agents_dir


def test_instruction_extractor_initialization(project_root):
    """Test that InstructionExtractor can be initialized."""
    extractor = InstructionExtractor(project_root)
    assert extractor.project_root == project_root


def test_mock_generator_creates_compliant_response():
    """Test that MockResponseGenerator creates compliant responses."""
    generator = MockResponseGenerator()
    response = generator.generate_compliant_response(
        agent_type="engineer", task_type="implement_feature"
    )

    assert response.agent_type == "engineer"
    assert response.task_type == "implement_feature"
    assert response.compliance_level == ComplianceLevel.FULLY_COMPLIANT
    assert len(response.content) > 0
    assert len(response.expected_violations) == 0


def test_mock_generator_creates_non_compliant_response():
    """Test that MockResponseGenerator creates non-compliant responses."""
    generator = MockResponseGenerator()
    response = generator.generate_non_compliant_response(
        agent_type="engineer", task_type="poor_commit", violations=["git_conventional_commits"]
    )

    assert response.agent_type == "engineer"
    assert response.compliance_level == ComplianceLevel.NON_COMPLIANT
    assert len(response.expected_violations) > 0
    assert "git_conventional_commits" in response.expected_violations


def test_root_base_rules_extracted(root_base_rules):
    """Test that root BASE-AGENT.md rules are extracted."""
    # Should have at least the core rules
    assert len(root_base_rules) > 0

    rule_ids = [rule.rule_id for rule in root_base_rules]
    expected_rules = [
        "git_conventional_commits",
        "markdown_output",
        "search_before_implement",
    ]

    for expected in expected_rules:
        assert expected in rule_ids, f"Missing rule: {expected}"

    # Note: handoff_protocol removed from root rules as it only applies
    # to handoff scenarios, tested separately in role_boundary tests


def test_all_agents_loaded(all_agents):
    """Test that agents can be loaded from repository."""
    # Skip if no agents (allows testing in empty repo)
    if not all_agents:
        pytest.skip("No agents found in repository")

    # Should have at least one agent
    assert len(all_agents) > 0

    # Each agent should have required fields
    for agent in all_agents:
        assert agent.path is not None
        assert agent.body_content is not None
