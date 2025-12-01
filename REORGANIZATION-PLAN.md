# Agent Repository Reorganization Plan

## Overview

This document describes the complete reorganization of the Claude MPM agent templates repository from a flat structure to a hierarchical organization with BASE-AGENT.md inheritance.

## Goals

1. **Eliminate Duplication**: Extract common instructions into BASE-AGENT.md files
2. **Improve Maintainability**: Update shared instructions in one place
3. **Enhance Discoverability**: Organize agents by functional relationships
4. **Standardize Naming**: Use consistent dash-based naming convention
5. **Enable Auto-Deployment**: Detect project types and deploy appropriate agents

## New Repository Structure

```
claude-mpm-agents/
├── build-agent.py                      # Build script for flattening agents
├── AUTO-DEPLOY-INDEX.md                # Auto-deployment rules by project type
├── README.md                           # Updated with BASE-AGENT.md documentation
├── REORGANIZATION-PLAN.md             # This file
│
├── agents/
│   ├── BASE-AGENT.md                  # Root level (ALL agents inherit)
│   │
│   ├── claude-mpm/                     # Claude MPM framework agents
│   │   ├── BASE-AGENT.md              # MPM framework awareness
│   │   └── mpm-agent-manager.md       # Agent discovery & deployment
│   │
│   ├── universal/                      # Cross-cutting concerns
│   │   ├── memory-manager.md
│   │   ├── product-owner.md
│   │   ├── project-organizer.md
│   │   ├── research.md
│   │   ├── code-analyzer.md
│   │   └── content-agent.md
│   │
│   ├── engineer/                       # Implementation specialists
│   │   ├── BASE-AGENT.md              # All engineers inherit this
│   │   │
│   │   ├── core/
│   │   │   └── engineer.md
│   │   │
│   │   ├── frontend/
│   │   │   ├── web-ui.md
│   │   │   ├── react-engineer.md
│   │   │   ├── nextjs-engineer.md
│   │   │   └── svelte-engineer.md
│   │   │
│   │   ├── backend/
│   │   │   ├── python-engineer.md
│   │   │   ├── golang-engineer.md
│   │   │   ├── java-engineer.md
│   │   │   ├── ruby-engineer.md
│   │   │   ├── rust-engineer.md
│   │   │   ├── php-engineer.md
│   │   │   └── javascript-engineer.md
│   │   │
│   │   ├── mobile/
│   │   │   ├── dart-engineer.md
│   │   │   └── tauri-engineer.md
│   │   │
│   │   ├── data/
│   │   │   ├── data-engineer.md
│   │   │   └── typescript-engineer.md
│   │   │
│   │   └── specialized/
│   │       ├── refactoring-engineer.md
│   │       ├── agentic-coder-optimizer.md
│   │       ├── imagemagick.md
│   │       └── prompt-engineer.md
│   │
│   ├── qa/                             # Quality assurance
│   │   ├── BASE-AGENT.md              # All QA agents inherit this
│   │   ├── qa.md
│   │   ├── api-qa.md
│   │   └── web-qa.md
│   │
│   ├── ops/                            # Operations & deployment
│   │   ├── BASE-AGENT.md              # All ops agents inherit this
│   │   │
│   │   ├── core/
│   │   │   └── ops.md
│   │   │
│   │   ├── platform/
│   │   │   ├── vercel-ops.md
│   │   │   ├── gcp-ops.md
│   │   │   ├── clerk-ops.md
│   │   │   └── local-ops.md
│   │   │
│   │   └── tooling/
│   │       └── version-control.md
│   │
│   ├── security/
│   │   └── security.md
│   │
│   ├── documentation/
│   │   ├── documentation.md
│   │   └── ticketing.md
│   │
│   └── templates/                      # Shared reference materials
│       ├── circuit-breakers.md
│       ├── git-file-tracking.md
│       ├── pm-examples.md
│       ├── pm-red-flags.md
│       ├── research-gate-examples.md
│       ├── response-format.md
│       ├── ticket-completeness-examples.md
│       └── validation-templates.md
│
└── dist/                               # Build output (gitignored)
    └── agents/                         # Flattened agents ready for deployment
        └── (mirrors structure of agents/)
```

## File Renaming Map

### Agents with Name Changes (underscore → dash)

| Current Name | New Name | Category |
|--------------|----------|----------|
| `agent-manager.md` | `mpm-agent-manager.md` | claude-mpm (new) |
| `memory_manager.md` | `memory-manager.md` | universal |
| `product_owner.md` | `product-owner.md` | universal |
| `project_organizer.md` | `project-organizer.md` | universal |
| `code_analyzer.md` | `code-analyzer.md` | universal |
| `web_ui.md` | `web-ui.md` | engineer/frontend |
| `react_engineer.md` | `react-engineer.md` | engineer/frontend |
| `nextjs_engineer.md` | `nextjs-engineer.md` | engineer/frontend |
| `golang_engineer.md` | `golang-engineer.md` | engineer/backend |
| `java_engineer.md` | `java-engineer.md` | engineer/backend |
| `rust_engineer.md` | `rust-engineer.md` | engineer/backend |
| `javascript-engineer-agent.md` | `javascript-engineer.md` | engineer/backend |
| `dart_engineer.md` | `dart-engineer.md` | engineer/mobile |
| `tauri_engineer.md` | `tauri-engineer.md` | engineer/mobile |
| `data_engineer.md` | `data-engineer.md` | engineer/data |
| `typescript_engineer.md` | `typescript-engineer.md` | engineer/data |
| `refactoring_engineer.md` | `refactoring-engineer.md` | engineer/specialized |
| `api_qa.md` | `api-qa.md` | qa |
| `web_qa.md` | `web-qa.md` | qa |
| `vercel_ops_agent.md` | `vercel-ops.md` | ops/platform |
| `gcp_ops_agent.md` | `gcp-ops.md` | ops/platform |
| `local-ops-agent.md` | `local-ops.md` | ops/platform |
| `version_control.md` | `version-control.md` | ops/tooling |
| `circuit_breakers.md` | `circuit-breakers.md` | templates |
| `git_file_tracking.md` | `git-file-tracking.md` | templates |
| `pm_examples.md` | `pm-examples.md` | templates |
| `pm_red_flags.md` | `pm-red-flags.md` | templates |
| `research_gate_examples.md` | `research-gate-examples.md` | templates |
| `response_format.md` | `response-format.md` | templates |
| `ticket_completeness_examples.md` | `ticket-completeness-examples.md` | templates |
| `validation_templates.md` | `validation-templates.md` | templates |

### Agents Keeping Current Names

All other agents retain their current names (already using dashes or single word).

## BASE-AGENT.md Inheritance System

### Inheritance Hierarchy

Each agent inherits from multiple BASE-AGENT.md files in this order:

1. **Agent-specific content** - Unique to this agent
2. **Directory BASE-AGENT.md** - Shared with siblings in same directory
3. **Parent BASE-AGENT.md** - Shared with parent category
4. **Root BASE-AGENT.md** - Shared with ALL agents

### Example: Python Engineer Inheritance

For `agents/engineer/backend/python-engineer.md`:

```
python-engineer.md (150 lines)
  + agents/engineer/BASE-AGENT.md (300 lines)
  + agents/BASE-AGENT.md (200 lines)
  = 650 lines total (only 150 unique to Python)
```

### BASE-AGENT.md Content Summary

#### Root Level (`agents/BASE-AGENT.md`)
- Git workflow standards (commit messages, conventional commits)
- Memory routing protocols
- Output format standards (markdown, structure)
- Handoff protocols (when to delegate to other agents)
- Quality standards (what makes work complete)
- Communication standards (clarity, brevity, transparency)

#### Engineer Level (`agents/engineer/BASE-AGENT.md`)
- Code reduction principles (target zero net new lines)
- Search-before-implement protocol (vector search, grep)
- Type safety standards (100% coverage)
- SOLID principles
- Dependency injection patterns
- File size limits (800 lines max)
- Testing requirements (90%+ coverage)
- Performance considerations (Big O notation)
- Security baseline (input validation, auth, sensitive data)
- Error handling requirements
- Documentation requirements
- Refactoring protocol
- LOC reporting

#### QA Level (`agents/qa/BASE-AGENT.md`)
- Testing philosophy (prevent bugs, user-centric)
- Memory-efficient testing (strategic sampling)
- Test coverage standards (critical paths 100%)
- Test types (unit, integration, E2E, performance)
- Test quality standards (naming, structure, independence)
- JavaScript/TypeScript testing (watch mode prevention)
- Bug reporting standards (severity levels)
- Test automation best practices
- Regression testing coordination
- Performance validation
- Quality gates

#### Ops Level (`agents/ops/BASE-AGENT.md`)
- Infrastructure as Code (IaC) principles
- Deployment philosophy (automated, reversible, monitored)
- Deployment verification (MANDATORY for all deployments)
- Security scanning (pre-push credential check)
- Container management (Docker best practices)
- Monitoring & observability (metrics, logging, alerting)
- Infrastructure patterns (environments, configuration)
- Deployment strategies (blue-green, canary, rolling)
- Disaster recovery (backups, recovery procedures)
- CI/CD pipeline requirements
- Resource optimization
- Emergency response

## Build System

### build-agent.py Script

The `build-agent.py` script flattens agents by combining them with their inheritance chain.

**Features**:
- Automatic BASE-AGENT.md discovery and combination
- YAML frontmatter preservation
- Validation of agent definitions
- Batch building of all agents
- Custom output directory support

**Usage**:
```bash
# Build single agent
./build-agent.py agents/engineer/backend/python-engineer.md

# Build all agents
./build-agent.py --all

# Build to specific directory
./build-agent.py --all --output-dir ~/.claude-mpm/agents

# Validate all agents
./build-agent.py --validate
```

### Build Output

Built agents are placed in `dist/agents/` (gitignored) with full inheritance combined:

```
dist/agents/
├── universal/
│   ├── agent-manager.md          # Flattened with root BASE-AGENT.md
│   └── ...
├── engineer/
│   ├── backend/
│   │   ├── python-engineer.md    # Flattened with engineer + root BASE-AGENT.md
│   │   └── ...
│   └── ...
└── ...
```

## Auto-Deployment System

### AUTO-DEPLOY-INDEX.md

Defines rules for automatic agent deployment based on project detection.

**Detection Triggers**:
- **Python**: `pyproject.toml`, `requirements.txt`, `setup.py`
- **JavaScript/TypeScript**: `package.json` (with dependency analysis)
- **Rust**: `Cargo.toml`
- **Go**: `go.mod`, `go.sum`
- **Java**: `pom.xml`, `build.gradle`
- **Ruby**: `Gemfile`
- **PHP**: `composer.json`
- **Dart/Flutter**: `pubspec.yaml`

**Universal Agents** (always deployed):
- agent-manager
- memory-manager
- research
- code-analyzer
- documentation
- ticketing

**Example Auto-Deploy**:

Next.js + TypeScript project:
```
Detected: package.json (with "next", "typescript", "react")

Auto-Deploy:
  - Universal agents (6)
  - nextjs-engineer
  - react-engineer
  - typescript-engineer
  - qa/qa
  - qa/web-qa
  - ops/ops
  - ops/vercel-ops (if vercel.json exists)
  - security/security
```

## Migration Steps

### Phase 1: Preparation (Completed)
- ✅ Analyze existing agents
- ✅ Design hierarchical structure
- ✅ Create reorganization plan
- ✅ Extract common instructions into BASE-AGENT.md files
- ✅ Create build-agent.py script
- ✅ Create AUTO-DEPLOY-INDEX.md
- ✅ Update README.md with documentation

### Phase 2: Execution (Next)
1. Create folder structure
2. Move and rename agent files according to map
3. Strip duplicated content from agents (now in BASE-AGENT.md)
4. Test build-agent.py with all agents
5. Validate all agents build correctly
6. Update any agent references in main Claude MPM

### Phase 3: Validation
1. Build all agents: `./build-agent.py --all`
2. Validate output: `./build-agent.py --validate`
3. Compare flattened agents to original agents
4. Verify no content loss
5. Test deployment with Claude MPM

### Phase 4: Deployment
1. Commit reorganized repository
2. Tag release with new structure
3. Update main Claude MPM to use new structure
4. Update documentation
5. Announce changes to users

## Benefits

### For Maintainers
- **80% reduction** in duplicated instructions
- **Single source of truth** for shared standards
- **Easy updates** - change BASE-AGENT.md, rebuild all
- **Clear organization** - agents grouped by function

### For Users
- **Auto-deployment** - right agents for project type
- **Consistent experience** - all agents follow same standards
- **Easy customization** - fork and modify BASE-AGENT.md files
- **Better discovery** - hierarchical structure

### For Contributors
- **Clear patterns** - BASE-AGENT.md shows common structure
- **Easy agent creation** - focus on unique content
- **Validation tools** - build-agent.py catches errors
- **Documentation** - README explains system

## Metrics

### Before Reorganization
- **Total agents**: 39
- **Average agent size**: ~400 lines
- **Duplicated content**: ~60% (git workflows, standards, etc.)
- **Organization**: Flat structure
- **Naming**: Mixed (underscores and dashes)

### After Reorganization
- **Total agents**: 39 (same count)
- **Average unique content**: ~150 lines per agent
- **Shared content**: 4 BASE-AGENT.md files (~800 lines)
- **Organization**: 7 top-level categories
- **Naming**: Consistent dash-based naming
- **Build system**: Automatic flattening
- **Auto-deployment**: Project type detection

### Content Reduction
```
Before: 39 agents × 400 lines avg = 15,600 lines total
After:  39 agents × 150 lines avg = 5,850 lines (unique)
        + 4 BASE-AGENT.md × 200 lines = 800 lines (shared)
        = 6,650 lines total

Reduction: 57% less content to maintain
Consistency: 100% (all agents use same BASE-AGENT.md)
```

## Next Steps

1. **Execute reorganization** - Move files, create structure
2. **Strip duplicated content** - Remove from agents what's now in BASE-AGENT.md
3. **Test build system** - Ensure all agents build correctly
4. **Update Claude MPM** - Integrate auto-deployment
5. **Document changes** - Update CHANGELOG.md
6. **Release** - Tag and announce new structure

## Questions & Considerations

### Backward Compatibility
- Flattened agents in `dist/` are identical to original format
- No breaking changes for users
- Deployment process unchanged

### Git History
- Consider keeping file history during moves
- Use `git mv` to preserve blame information
- Document all renames in commit message

### Future Enhancements
- Add more BASE-AGENT.md files as needed (e.g., `frontend/BASE-AGENT.md`)
- Enhanced auto-deployment rules
- Agent dependency detection
- Version-specific BASE-AGENT.md (if needed)
