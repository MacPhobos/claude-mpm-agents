"""Generate deterministic mock responses for testing."""

from dataclasses import dataclass, field
from enum import Enum


class ComplianceLevel(str, Enum):
    """Level of instruction compliance in mock response."""

    FULLY_COMPLIANT = "fully_compliant"
    MOSTLY_COMPLIANT = "mostly_compliant"
    PARTIALLY_COMPLIANT = "partially_compliant"
    NON_COMPLIANT = "non_compliant"


@dataclass
class MockResponse:
    """Mock agent response for testing."""

    content: str
    agent_type: str
    task_type: str
    compliance_level: ComplianceLevel
    expected_violations: list[str] = field(default_factory=list)


class MockResponseGenerator:
    """Generate mock responses for testing compliance."""

    # Compliant response templates
    COMPLIANT_TEMPLATES = {
        "engineer": {
            "implement_feature": """## Implementation: User Authentication

### Objective
Implement OAuth2 authentication flow with JWT tokens.

### Approach
1. Add auth middleware to Express app
2. Implement token validation with jsonwebtoken
3. Add protected routes with type-safe guards

### Code Implementation

```typescript
// src/middleware/auth.ts
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

interface JWTPayload {
  userId: string;
  email: string;
  exp: number;
}

export const authMiddleware = (
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    res.status(401).json({ error: 'No token provided' });
    return;
  }

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET!) as JWTPayload;
    req.user = payload;
    next();
  } catch (error) {
    res.status(401).json({ error: 'Invalid token' });
  }
};
```

### Testing Approach
- Unit tests for token validation logic
- Integration tests for protected routes
- Property-based tests for edge cases

### Search Before Implementation
✅ Searched for existing auth implementations - no JWT middleware found in codebase.

### Git Commit
```
feat: add OAuth2 authentication middleware

Implement JWT-based authentication with Express middleware to enable
secure API access. Uses RS256 signing for better security vs HS256.
Includes type-safe token validation and error handling.

WHY: Current API has no authentication, exposing endpoints publicly.
```

### LOC Delta
- Added: 45 lines
- Removed: 0 lines
- Net Change: +45 lines
""",
            "refactor_code": """## Refactoring: Consolidate Validation Logic

### Objective
Consolidate duplicate validation logic across components.

### Search Results
✅ Found 3 similar validation implementations:
- src/components/UserForm.tsx (lines 45-78)
- src/components/ProfileForm.tsx (lines 32-65)
- src/components/SettingsForm.tsx (lines 21-54)

### Approach
Extract shared validation to reusable hook with type safety.

### Trade-offs
- **Pros**: Eliminates 79 lines of duplicate code, single source of truth for validation
- **Cons**: Adds abstraction layer (minimal - hook is only 23 lines)
- **Decision**: Consolidation justified by DRY principle and improved testability

### Implementation

```typescript
// src/hooks/useFormValidation.ts
import { useState } from 'react';

interface ValidationRules<T> {
  [K in keyof T]?: (value: T[K]) => string | null;
}

export function useFormValidation<T extends Record<string, unknown>>(
  rules: ValidationRules<T>
) {
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});

  const validate = (field: keyof T, value: T[keyof T]): boolean => {
    const rule = rules[field];
    if (!rule) return true;

    const error = rule(value);
    setErrors(prev => ({ ...prev, [field]: error ?? undefined }));
    return error === null;
  };

  return { errors, validate };
}
```

### LOC Delta
- Added: 23 lines (new hook)
- Removed: 102 lines (duplicate validation)
- Net Change: -79 lines

### Git Commit
```
refactor: consolidate form validation into reusable hook

Extract duplicate validation logic from UserForm, ProfileForm, and
SettingsForm into type-safe useFormValidation hook. Reduces code
duplication and improves maintainability.
```
""",
        },
        "qa": {
            "bug_report": """## Bug Report: Login Form Validation Error

**Steps to Reproduce:**
1. Navigate to /login page
2. Enter valid email: test@example.com
3. Enter password less than 8 characters: "abc123"
4. Click "Login" button

**Expected Behavior:**
- Form should show validation error: "Password must be at least 8 characters"
- Login button should remain disabled
- No API call should be made

**Actual Behavior:**
- Form submits without validation
- API call returns 400 error
- Error message not shown to user

### Environment
- Browser: Chrome 120.0.6099.109
- OS: macOS 14.2
- Environment: Staging (staging.example.com)

### Test Commands (CI-Safe)
```bash
# Run validation tests
pytest tests/test_login_validation.py -v

# Run integration tests
npm test -- --grep "login form validation"
```

### Severity
High - Affects user experience and allows invalid submissions
""",
            "test_plan": """## Test Plan: Payment Processing Feature

### Unit Tests
- Test payment validation with valid/invalid card data
- Test amount formatting and currency conversion
- Test error handling for declined payments

### Integration Tests
- Test end-to-end payment flow with Stripe test mode
- Verify webhook handling for payment events
- Test retry logic for failed payments

### Test Commands (CI-Safe)
```bash
# Run all payment tests
pytest tests/payment/ --cov=src/payment --cov-report=html

# Run with test database
DATABASE_URL=sqlite:///test.db pytest tests/integration/

# No interactive flags - fully automated
npm test -- --coverage --maxWorkers=2
```

### Coverage Target
- Minimum 90% code coverage
- 100% coverage for payment validation logic
- All error paths tested
""",
        },
        "ops": {
            "deployment": """## Deployment Plan: API v2 Migration

### Pre-Deployment Verification
1. Security scan completed
   - No critical CVEs found
   - All dependencies updated
   - OWASP scan passed

2. Health checks configured
   - Liveness probe: /health
   - Readiness probe: /ready
   - Startup probe: /startup

### Deployment Steps
1. Deploy to staging environment
2. Run smoke tests against staging
3. Verify metrics and logs
4. Deploy to production with blue-green strategy
5. Monitor error rates and latency

### Verification Steps
```bash
# Health check
curl https://api.example.com/health

# Smoke test
curl https://api.example.com/v2/users/me \
  -H "Authorization: Bearer $TOKEN"

# Check metrics
curl https://api.example.com/metrics | grep http_requests_total
```

### Rollback Plan
1. Switch traffic back to old version (blue-green)
2. Verify old version serving traffic
3. Investigate deployment issue
4. Expected rollback time: < 5 minutes

### Security Scan Results
- Vulnerability scan: ✅ Passed
- Dependency audit: ✅ No high/critical CVEs
- Container scan: ✅ No security issues
""",
        },
    }

    # Non-compliant response templates
    NON_COMPLIANT_TEMPLATES = {
        "engineer": {
            "poor_commit": """Implemented the feature.

Changed some files and added code. Fixed bugs.

commit message: "update code"
""",
            "any_types": """Here's the implementation:

```typescript
function processData(data: any): any {
  return data.map((item: any) => item.value);
}
```

This should work fine.
""",
            "no_structure": """I added the auth middleware. Just copy this code:

const auth = (req, res, next) => {
  if (req.headers.token) {
    next()
  } else {
    res.status(401).send('error')
  }
}

Done.
""",
        },
        "qa": {
            "poor_bug_report": """The login form is broken. It doesn't work when I try to login.

Fix it please.
""",
            "interactive_tests": """Run these tests:

```bash
git rebase -i HEAD~5
pytest --interactive
npm test -i
```
""",
        },
        "ops": {
            "no_verification": """Deployment plan:

1. Deploy to production
2. Hope it works
3. Done

Just push and see what happens.
""",
            "no_security": """Deploy the app:

docker build -t app .
docker push app:latest
kubectl apply -f deploy.yaml

That's it.
""",
        },
    }

    def generate_compliant_response(self, agent_type: str, task_type: str) -> MockResponse:
        """Generate a compliant response for testing.

        Args:
            agent_type: Type of agent (engineer, qa, ops)
            task_type: Type of task (implement_feature, bug_report, etc.)

        Returns:
            MockResponse with compliant content
        """
        templates = self.COMPLIANT_TEMPLATES.get(agent_type, {})
        content = templates.get(task_type, f"# Compliant {agent_type} response for {task_type}")

        return MockResponse(
            content=content,
            agent_type=agent_type,
            task_type=task_type,
            compliance_level=ComplianceLevel.FULLY_COMPLIANT,
            expected_violations=[],
        )

    def generate_non_compliant_response(
        self,
        agent_type: str,
        task_type: str,
        violations: list[str],
    ) -> MockResponse:
        """Generate a non-compliant response for testing.

        Args:
            agent_type: Type of agent (engineer, qa, ops)
            task_type: Type of violation (poor_commit, any_types, etc.)
            violations: List of expected violations to detect

        Returns:
            MockResponse with non-compliant content
        """
        templates = self.NON_COMPLIANT_TEMPLATES.get(agent_type, {})
        content = templates.get(task_type, f"Non-compliant {agent_type} response")

        return MockResponse(
            content=content,
            agent_type=agent_type,
            task_type=task_type,
            compliance_level=ComplianceLevel.NON_COMPLIANT,
            expected_violations=violations,
        )
