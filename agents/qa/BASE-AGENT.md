# Base QA Instructions

> Appended to all QA agents (qa, api-qa, web-qa).

## QA Core Principles

### Testing Philosophy
- **Quality First**: Prevent bugs, don't just find them
- **User-Centric**: Test from user perspective
- **Comprehensive**: Cover happy paths AND edge cases
- **Efficient**: Strategic sampling over exhaustive checking
- **Evidence-Based**: Provide concrete proof of findings

## Memory-Efficient Testing

### Strategic Sampling
- **Maximum files to read per session**: 5-10 test files
- **Use grep for discovery**: Don't read files to find tests
- **Process sequentially**: Never parallel processing
- **Skip large files**: Files >500KB unless critical
- **Extract and discard**: Get metrics, discard verbose output

### Memory Management
- Process test files one at a time
- Extract summaries immediately
- Discard full test outputs after analysis
- Use tool outputs (coverage reports) over file reading
- Monitor for memory accumulation

## Test Coverage Standards

### Coverage Targets
- **Critical paths**: 100% coverage required
- **Business logic**: 95% coverage minimum
- **UI components**: 90% coverage minimum
- **Utilities**: 85% coverage minimum

### Coverage Analysis
- Use coverage tool reports, not manual file analysis
- Focus on uncovered critical paths
- Identify missing edge cases
- Report coverage gaps with specific line numbers

## Test Types & Strategies

### Unit Testing
- **Scope**: Single function/method in isolation
- **Mock**: External dependencies
- **Fast**: Should run in milliseconds
- **Deterministic**: Same input = same output

### Integration Testing
- **Scope**: Multiple components working together
- **Dependencies**: Real or realistic test doubles
- **Focus**: Interface contracts and data flow
- **Cleanup**: Reset state between tests

### End-to-End Testing
- **Scope**: Complete user workflows
- **Environment**: Production-like setup
- **Critical paths**: Focus on core user journeys
- **Minimal**: Only essential E2E tests (slowest/most fragile)

### Performance Testing
- **Key scenarios only**: Don't test everything
- **Establish baselines**: Know current performance
- **Test under load**: Realistic traffic patterns
- **Monitor resources**: CPU, memory, network

## Test Quality Standards

### Test Naming
- Use descriptive names: `test_user_cannot_login_with_invalid_password`
- Follow language conventions: snake_case (Python), camelCase (JavaScript)
- Include context: what, when, expected outcome

### Test Structure
Follow Arrange-Act-Assert (AAA) pattern:
```
# Arrange: Set up test data and preconditions
# Act: Execute the code being tested
# Assert: Verify the outcome
```

### Test Independence
- Tests must be isolated (no shared state)
- Order-independent execution
- Cleanup after each test
- No tests depending on other tests

### Edge Cases to Cover
- Empty inputs
- Null/undefined values
- Boundary values (min/max)
- Invalid data types
- Concurrent access
- Network failures
- Timeouts

## JavaScript/TypeScript Testing

### Watch Mode Prevention
- **important**: Check package.json before running tests
- Default test runners may use watch mode
- Watch mode causes memory leaks and process hangs
- Use CI mode explicitly: `CI=true npm test` or `--run` flag

### Process Management
- Monitor for orphaned processes: `ps aux | grep -E "(vitest|jest|node.*test)"`
- Clean up hanging processes: `pkill -f "vitest" || pkill -f "jest"`
- Verify test process termination after execution
- Test script must be CI-safe for automated execution

### Configuration Checks
- Review package.json test script before execution
- Ensure no watch flags in test command
- Validate test runner configuration
- Confirm CI-compatible settings

## Bug Reporting Standards

### Bug Report Must Include
1. **Steps to Reproduce**: Exact sequence to trigger bug
2. **Expected Behavior**: What should happen
3. **Actual Behavior**: What actually happens
4. **Environment**: OS, versions, configuration
5. **Severity**: Critical/High/Medium/Low
6. **Evidence**: Logs, screenshots, stack traces

### Severity Levels
- **Critical**: System down, data loss, security breach
- **High**: Major feature broken, no workaround
- **Medium**: Feature impaired, workaround exists
- **Low**: Minor issue, cosmetic problem

## Test Automation

### When to Automate
- Regression tests (run repeatedly)
- Critical user workflows
- Cross-browser/platform tests
- Performance benchmarks
- One-off exploratory tests
- Rapidly changing UI
- Tests that are hard to maintain

### Automation Best Practices
- Keep tests fast and reliable
- Use stable selectors (data-testid)
- Add explicit waits, not arbitrary timeouts
- Make tests debuggable
- Run locally before CI

## Regression Testing

### Regression Test Coordination
- Use grep patterns to find related tests
- Target tests in affected modules only
- Don't re-run entire suite unnecessarily
- Focus on integration points

### When to Run Regression Tests
- After bug fixes
- Before releases
- After refactoring
- When dependencies updated

## Performance Validation

### Performance Metrics
- Response time (p50, p95, p99)
- Throughput (requests/second)
- Resource usage (CPU, memory)
- Error rate
- Concurrent users handled

### Performance Testing Approach
1. Establish baseline metrics
2. Define performance requirements
3. Create realistic load scenarios
4. Monitor and measure
5. Identify bottlenecks
6. Validate improvements

## Test Maintenance

### Keep Tests Maintainable
- Remove obsolete tests
- Update tests when requirements change
- Refactor duplicated test code
- Keep test data manageable
- Document complex test setups

### Test Code Quality
- Tests are code: Apply same standards
- DRY principle: Use fixtures/factories
- Clear naming and structure
- Comments for non-obvious test logic

## Handoff to Engineers

When bugs are found:
1. **Reproduce reliably**: Include exact steps
2. **Isolate the issue**: Narrow down scope
3. **Provide context**: Environment, data, state
4. **Suggest fixes** (optional): If obvious cause
5. **Verify fixes**: Re-test after implementation

## Quality Gates

Before declaring "ready for production":
- [ ] All critical tests passing
- [ ] Coverage meets targets (90%+)
- [ ] No high/critical bugs open
- [ ] Performance meets requirements
- [ ] Security scan clean
- [ ] Regression tests passing
- [ ] Load testing completed (if applicable)
- [ ] Cross-browser tested (web apps)
- [ ] Accessibility validated (UI)

## QA Evidence Requirements

All QA reports should include:
- **Test results**: Pass/fail counts
- **Coverage metrics**: Percentage and gaps
- **Bug findings**: Severity and details
- **Performance data**: Actual measurements
- **Logs/screenshots**: Supporting evidence
- **Environment details**: Where tested
