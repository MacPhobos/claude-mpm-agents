#!/usr/bin/env python3
"""Validation script to verify DeepEval testing framework setup.

Run this script to check that all components are properly installed and configured.

Usage:
    python validate_test_setup.py
"""

import sys
from pathlib import Path


def check_file_exists(path: Path, description: str) -> bool:
    """Check if a file exists.

    Args:
        path: Path to check
        description: Human-readable description

    Returns:
        True if file exists, False otherwise
    """
    if path.exists():
        print(f"✅ {description}: {path}")
        return True
    else:
        print(f"❌ {description} MISSING: {path}")
        return False


def check_directory_exists(path: Path, description: str) -> bool:
    """Check if a directory exists.

    Args:
        path: Path to check
        description: Human-readable description

    Returns:
        True if directory exists, False otherwise
    """
    if path.is_dir():
        file_count = len(list(path.glob("**/*.py")))
        print(f"✅ {description}: {path} ({file_count} Python files)")
        return True
    else:
        print(f"❌ {description} MISSING: {path}")
        return False


def check_import(module: str, description: str) -> bool:
    """Check if a module can be imported.

    Args:
        module: Module name to import
        description: Human-readable description

    Returns:
        True if import succeeds, False otherwise
    """
    try:
        __import__(module)
        print(f"✅ {description}: {module}")
        return True
    except ImportError as e:
        print(f"❌ {description} FAILED: {module} ({e})")
        return False


def main():
    """Run validation checks."""
    print("=" * 70)
    print("DeepEval Testing Framework Setup Validation")
    print("=" * 70)
    print()

    project_root = Path(__file__).parent
    checks_passed = []

    # Check project configuration
    print("📦 Project Configuration")
    print("-" * 70)
    checks_passed.append(
        check_file_exists(project_root / "pyproject.toml", "pyproject.toml configuration")
    )
    checks_passed.append(
        check_file_exists(
            project_root / ".github/workflows/agent-tests.yml", "GitHub Actions workflow"
        )
    )
    print()

    # Check documentation
    print("📚 Documentation")
    print("-" * 70)
    checks_passed.append(check_file_exists(project_root / "TESTING.md", "Quick start guide"))
    checks_passed.append(check_file_exists(project_root / "tests/README.md", "Framework docs"))
    checks_passed.append(
        check_file_exists(project_root / "IMPLEMENTATION_SUMMARY.md", "Implementation summary")
    )
    print()

    # Check test directories
    print("📁 Test Directories")
    print("-" * 70)
    checks_passed.append(check_directory_exists(project_root / "tests", "Tests directory"))
    checks_passed.append(
        check_directory_exists(project_root / "tests/fixtures", "Fixtures directory")
    )
    checks_passed.append(
        check_directory_exists(project_root / "tests/metrics", "Metrics directory")
    )
    checks_passed.append(
        check_directory_exists(project_root / "tests/examples", "Examples directory")
    )
    print()

    # Check key test files
    print("📄 Test Files")
    print("-" * 70)
    test_files = [
        ("conftest.py", "Pytest fixtures"),
        ("test_instruction_compliance.py", "Instruction compliance tests"),
        ("test_role_boundaries.py", "Role boundary tests"),
        ("test_agent_registry.py", "Agent registry tests"),
        ("test_setup.py", "Setup validation tests"),
    ]
    for filename, description in test_files:
        checks_passed.append(check_file_exists(project_root / "tests" / filename, description))
    print()

    # Check fixture files
    print("🔧 Fixture Files")
    print("-" * 70)
    fixture_files = [
        ("agent_loader.py", "Agent loader"),
        ("instruction_extractor.py", "Instruction extractor"),
        ("mock_responses.py", "Mock response generator"),
    ]
    for filename, description in fixture_files:
        checks_passed.append(
            check_file_exists(project_root / "tests/fixtures" / filename, description)
        )
    print()

    # Check metric files
    print("📊 Metric Files")
    print("-" * 70)
    metric_files = [
        ("instruction_compliance.py", "Instruction compliance metrics"),
        ("role_boundary.py", "Role boundary metrics"),
    ]
    for filename, description in metric_files:
        checks_passed.append(
            check_file_exists(project_root / "tests/metrics" / filename, description)
        )
    print()

    # Check Python imports
    print("🐍 Python Dependencies")
    print("-" * 70)
    dependencies = [
        ("yaml", "PyYAML"),
        ("pytest", "pytest"),
        ("deepeval", "DeepEval"),
        ("pydantic", "Pydantic"),
    ]
    for module, description in dependencies:
        checks_passed.append(check_import(module, description))
    print()

    # Check agents directory
    print("👥 Agent Files")
    print("-" * 70)
    agents_dir = project_root / "agents"
    if agents_dir.is_dir():
        agent_files = list(agents_dir.rglob("*.md"))
        base_agent_files = [f for f in agent_files if f.name.startswith("BASE-AGENT")]
        regular_agent_files = [f for f in agent_files if not f.name.startswith("BASE-AGENT")]

        print(f"✅ Agents directory: {agents_dir}")
        print(f"   - BASE-AGENT files: {len(base_agent_files)}")
        print(f"   - Agent definitions: {len(regular_agent_files)}")
        checks_passed.append(True)
    else:
        print(f"❌ Agents directory MISSING: {agents_dir}")
        checks_passed.append(False)
    print()

    # Summary
    print("=" * 70)
    print("Summary")
    print("=" * 70)
    total_checks = len(checks_passed)
    passed_checks = sum(checks_passed)
    failed_checks = total_checks - passed_checks

    print(f"Total checks: {total_checks}")
    print(f"Passed: {passed_checks} ✅")
    print(f"Failed: {failed_checks} ❌")
    print()

    if failed_checks == 0:
        print("🎉 All checks passed! Setup is complete.")
        print()
        print("Next steps:")
        print("  1. Install dependencies: pip install -e '.[test]'")
        print("  2. Run tests: pytest -v")
        print("  3. Check coverage: pytest --cov=tests --cov-report=html")
        print("  4. Read documentation: cat TESTING.md")
        return 0
    else:
        print("⚠️  Some checks failed. Please review the errors above.")
        print()
        print("To fix:")
        print("  1. Ensure you're in the project root directory")
        print("  2. Install dependencies: pip install -e '.[test]'")
        print("  3. Check that all files were created correctly")
        return 1


if __name__ == "__main__":
    sys.exit(main())
