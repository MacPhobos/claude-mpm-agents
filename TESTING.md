# Agent Testing Quick Start Guide

This repository uses [DeepEval](https://docs.confident-ai.com/) to validate that Claude MPM agents follow their BASE-AGENT.md instruction guidelines.

## Quick Start

### 1. Install Dependencies

```bash
# Install test dependencies
pip install -e ".[test]"

# Or install dev dependencies (includes ruff linter)
pip install -e ".[dev]"
```

### 2. Run Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=tests --cov-report=html --cov-report=term-missing

# Run specific test categories
pytest -m instruction_compliance
pytest -m role_boundary
pytest -m registry

# Run specific test file
pytest tests/test_instruction_compliance.py -v

# Run with verbose output and show print statements
pytest -v -s
```

### 3. View Coverage Report

After running tests with `--cov-report=html`, open the coverage report:

```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## What Gets Tested

### Instruction Compliance
- **Git Workflow**: Conventional commits (feat:, fix:, etc.)
- **Output Format**: Markdown headers, code blocks, structure
- **Search Before Implement**: Evidence of searching for existing code
- **Category Rules**: Engineer (type safety), QA (bug reports), Ops (deployment verification)

### Role Boundaries
- **Engineer**: Should implement code, NOT deploy to production
- **QA**: Should write tests, NOT implement features
- **Ops**: Should deploy/monitor, NOT write business logic
- **Handoff Protocol**: Proper handoff format with accomplished/remaining/context

### Agent Registry
- **Required Fields**: All agents have name, description, agent_id, agent_type
- **Unique IDs**: No duplicate agent_id values
- **Valid Types**: agent_type from approved list
- **Handoff Validation**: Referenced agents exist
- **Content Quality**: Non-empty body, reasonable length

## Test Markers

Use pytest markers to run specific test categories:

```bash
# Only instruction compliance tests
pytest -m instruction_compliance

# Only role boundary tests
pytest -m role_boundary

# Only registry validation tests
pytest -m registry

# Only output quality tests
pytest -m output_quality

# Run multiple categories
pytest -m "instruction_compliance or role_boundary"
```

## Example Test Output

```
tests/test_instruction_compliance.py::TestRootBaseAgentCompliance::test_engineer_compliant_response_passes PASSED
tests/test_instruction_compliance.py::TestRootBaseAgentCompliance::test_git_workflow_conventional_commits PASSED
tests/test_role_boundaries.py::TestEngineerRoleBoundaries::test_engineer_stays_in_role PASSED
tests/test_agent_registry.py::TestAgentFrontmatter::test_required_fields_present[name] PASSED

==================== 24 passed in 2.34s ====================
```

## Common Workflows

### Before Committing Agent Changes

```bash
# Validate agent definitions
python build-agent.py --validate

# Run all tests
pytest

# Check code quality
ruff check tests/
```

### Adding a New Agent

1. Create agent markdown file in `agents/`
2. Add YAML frontmatter with required fields
3. Run registry tests to validate:

```bash
pytest tests/test_agent_registry.py -v
```

### Debugging Test Failures

```bash
# Run with verbose output and show full error details
pytest -v -s --tb=long

# Run single test with debugging
pytest tests/test_instruction_compliance.py::TestRootBaseAgentCompliance::test_git_workflow_conventional_commits -v -s
```

### Updating Test Rules

1. Edit `tests/fixtures/instruction_extractor.py` to add/modify rules
2. Edit `tests/fixtures/mock_responses.py` to add response templates
3. Add new test cases in appropriate test file
4. Run tests to verify:

```bash
pytest tests/test_instruction_compliance.py -v
```

## CI/CD Integration

Tests run automatically on GitHub Actions:

- **Triggered by**: Push/PR to `main` affecting `agents/`, `tests/`, or `pyproject.toml`
- **Actions**:
  1. Validate agents with `build-agent.py --validate`
  2. Run pytest with coverage
  3. Lint tests with ruff
  4. Upload coverage reports to Codecov

See `.github/workflows/agent-tests.yml` for full configuration.

## Troubleshooting

### ModuleNotFoundError

```bash
# Reinstall in editable mode
pip install -e ".[test]"
```

### No Agents Found

Ensure agents are in `/Users/masa/Projects/claude-mpm-agents/agents/` with valid YAML frontmatter.

### DeepEval Metric Failures

Check the metric's reason and violations:

```python
# In test output, look for:
# Failure reason: Git violations: Commit messages don't follow conventional format
# This tells you exactly what failed
```

### YAML Parse Errors

Validate your agent's frontmatter:

```bash
# Check specific agent
python -c "
from tests.fixtures.agent_loader import AgentLoader
from pathlib import Path
loader = AgentLoader(Path('agents'))
agent = loader.load_agent(Path('agents/engineer/python.md'))
print(agent.name, agent.agent_id)
"
```

## Documentation

- [Full Testing Framework Documentation](tests/README.md)
- [DeepEval Documentation](https://docs.confident-ai.com/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Agent BASE Instructions](agents/BASE-AGENT.md)

## Contributing

When adding new tests:

1. Follow existing patterns in test files
2. Use descriptive test names
3. Add docstrings explaining what is tested
4. Test both compliant and non-compliant cases
5. Update this guide if adding new test categories
