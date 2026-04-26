#!/usr/bin/env python3
"""
setup_launchpad.py - Project Scaffolding & Environment Initialization
---------------------------------------------------------------------
This script initializes the project environment by reading the PRD, ARCH, and
RESEARCH documents in the docs/ folder. It creates the directory structure,
standard configuration files, methodology guides, and the AGENTS.md "kernel".

Usage:
    python setup_launchpad.py
"""

import os
import re
from pathlib import Path

# Paths to input documents
DOCS_DIR = Path("docs")
PRD_PATH = DOCS_DIR / "PRD.md"
ARCH_PATH = DOCS_DIR / "ARCH.md"
RESEARCH_PATH = DOCS_DIR / "RESEARCH.md"


def extract_from_docs():
    """Extracts project-specific metadata from documentation files."""
    data = {
        "name": "Project Name",
        "description": "One-line description.",
        "tech_stack": [],
        "directories": [],
        "dictionary": [],
        "secrets": [],
    }

    if not PRD_PATH.exists() or not ARCH_PATH.exists():
        print("Error: PRD.md or ARCH.md not found in docs/")
        return data

    # Read PRD
    prd_content = PRD_PATH.read_text(encoding="utf-8")
    name_match = re.search(r"^# PRD: (.*)", prd_content, re.MULTILINE)
    if name_match:
        data["name"] = name_match.group(1).strip()

    desc_match = re.search(r"## Executive Summary\n\n(.*?)\.", prd_content, re.DOTALL)
    if desc_match:
        data["description"] = desc_match.group(1).strip().replace("\n", " ")

    # Read ARCH
    arch_content = ARCH_PATH.read_text(encoding="utf-8")

    # Extract Tech Stack from table
    tech_matches = re.findall(r"\| (.*?) \| (.*?) \| (.*?) \|", arch_content)
    for tech in tech_matches:
        if "Layer" not in tech[0]:
            data["tech_stack"].append(f"{tech[1]} ({tech[2]})")

    # Extract Directories from table
    dir_matches = re.findall(r"\| `(.*?)` \|", arch_content)
    for d in dir_matches:
        path = d.strip()
        if (
            path
            and path != "Path"
            and not path.endswith(".py")
            and not path.endswith(".tsx")
            and not path.endswith(".ts")
            and not path.endswith(".yml")
            and not path.endswith(".md")
        ):
            # Ensure we don't treat comma separated file lists as directories
            if "," not in path:
                data["directories"].append(path)

    # Extract Dictionary Terms from table
    dict_matches = re.findall(r"\| (.*?) \| (.*?) \| (.*?) \|", arch_content)
    for term in dict_matches:
        if "Term" not in term[0] and "Definition" not in term[1]:
            data["dictionary"].append(term[0].strip())

    # Extract Secrets/Environment Variables
    secret_matches = re.findall(r"`([A-Z0-9_]+)` environment variable", arch_content)
    data["secrets"] = list(set(secret_matches))

    return data


def create_scaffold(data):
    """Creates the directory structure and files."""

    # 1. Base Folders
    base_folders = ["docs/plans", "docs/methodology", "directives", "execution", "src", "tests", ".tmp"]

    # Filter out any accidental files that got into directories
    all_folders = [f for f in set(base_folders + data["directories"]) if f and "." not in f.split("/")[-1]]
    all_folders = sorted(list(set(all_folders)))

    print(f"--- Creating Directory Structure for {data['name']} ---")
    for folder in all_folders:
        os.makedirs(folder, exist_ok=True)
        print(f"Created: {folder}")

    # 2. .gitignore
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/
env/
*.egg-info/
dist/
build/

# Environment
.env
.env.local
*.local

# IDE
.idea/
.vscode/
*.swp
*.swo

# Project
.tmp/
*.log
agents.db
"""
    Path(".gitignore").write_text(gitignore_content, encoding="utf-8")
    print("Created: .gitignore")

    # 3. .env.example
    env_content = "# Project Environment Variables\n"
    for secret in data["secrets"]:
        env_content += f"{secret}=your-{secret.lower().replace('_', '-')}-here\n"

    # Add defaults if missing
    if "DATABASE_URL" not in data["secrets"]:
        env_content += "DATABASE_URL=sqlite+aiosqlite:///./agents.db\n"

    Path(".env.example").write_text(env_content, encoding="utf-8")
    print("Created: .env.example")

    # 4. README.md
    readme_content = f"""# {data["name"]}

{data["description"]}

## Quick Start

1. Clone the repository
2. Copy `.env.example` to `.env` and configure
3. Run `python setup_launchpad.py` (if not already run)
4. Follow `directives/001_initial_setup.md`

## Documentation

- [Product Requirements](docs/PRD.md)
- [Technical Architecture](docs/ARCH.md)
- [Implementation Research](docs/RESEARCH.md)
- [Agent Instructions](AGENTS.md)

## Development Methodology

- [Implementation Planning](docs/methodology/implementation-planning.md)
- [Review Gates](docs/methodology/review-gates.md)
- [Debugging Guide](docs/methodology/debugging-guide.md)

## Project Structure

```text
{chr(10).join(data["directories"])}
```
"""
    Path("README.md").write_text(readme_content, encoding="utf-8")
    print("Created: README.md")

    # 5. requirements.txt
    requirements = [
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "sqlalchemy>=2.0.0",
        "aiosqlite>=0.19.0",
        "asyncssh>=2.14.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "cryptography>=42.0.0",
        "pytest>=8.0.0",
        "pytest-asyncio>=0.23.0",
        "httpx>=0.27.0",
    ]
    Path("requirements.txt").write_text("\n".join(requirements), encoding="utf-8")
    print("Created: requirements.txt")

    # 6. AGENTS.md
    agents_md = f"""# AGENTS.md - System Kernel

## Project Context

**Name:** {data["name"]}
**Purpose:** {data["description"]}
**Stack:** {", ".join(data["tech_stack"])}

## Core Domain Entities

{chr(10).join([f"- {term}" for term in data["dictionary"]])}

---

## 1. The Prime Directive

You are an agent operating on the {data["name"]} codebase.

**Before writing ANY code:**
1. Read `docs/PRD.md` to understand WHAT we are building
2. Read `docs/ARCH.md` to understand HOW we structure it
3. Consult `docs/RESEARCH.md` for proven patterns to follow
4. Check `directives/` for your current assignment

**Core Rules:**
- Use ONLY the technologies defined in ARCH.md Tech Stack
- Use ONLY the terms defined in ARCH.md Dictionary
- Follow ONLY the API contracts defined in ARCH.md
- Place code ONLY in the directories specified in ARCH.md

---

## 2. The 3-Layer Workflow

### Layer 1: Directives (Orders)
- Location: `directives/`
- Purpose: Task assignments with specific acceptance criteria
- Action: Read the lowest-numbered incomplete directive

### Layer 2: Orchestration (Planning)
- Location: `docs/plans/`
- Purpose: Granular implementation plans for each directive
- Action: Before coding, break the directive into tasks following `docs/methodology/implementation-planning.md`

### Layer 3: Execution (Automation)
- Location: `execution/`
- Purpose: Reusable scripts for repetitive tasks
- Examples: `run_migrations.py`, `seed_data.py`, `run_tests.py`

---

## 3. The TDD Iron Law

**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**

### The Mandatory Cycle

For every piece of functionality:

1. **RED:** Write a test in `tests/` that describes the expected behavior. Run it. Confirm it **fails** — and fails for the *right reason* (assertion failure, not import error).
2. **GREEN:** Write the **minimum** code in `src/` to make the test pass. Run all tests. Confirm they **all pass**.
3. **REFACTOR:** Clean up the code while keeping tests green. Run all tests again. Confirm they still pass.
4. **COMMIT:** Only after all tests pass.

### The Nuclear Rule

If you write production code before writing its test:
- **Delete it.** Not "keep as reference." Not "adapt it while writing tests." Delete means delete.
- Write the test first.
- Implement fresh, guided by the failing test.

### Test File Locations

Mirror the source structure:
- `backend/api/agents.py` → `tests/api/test_agents.py`

### TDD Rationalizations Table

| Excuse | Reality |
|--------|---------|
| "This is too simple to test" | Simple code breaks. The test takes 30 seconds to write. |
| "I'll write tests after" | Tests that pass immediately prove nothing — they describe what the code *does*, not what it *should* do. |
| "I already tested it manually" | Manual testing has no record and can't be re-run. |
| "Deleting my work is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt with interest. |
| "I'll keep it as reference and write tests first" | You'll adapt it. That's tests-after with extra steps. Delete means delete. |
| "I need to explore first" | Explore freely. Then throw away the exploration and start with TDD. |
| "The test is hard to write — the design isn't clear yet" | Listen to the test. Hard to test = hard to use. Redesign. |
| "TDD will slow me down" | TDD is faster than debugging. Every shortcut becomes a debugging session. |
| "TDD is dogmatic; I'm being pragmatic" | TDD IS pragmatic. "Pragmatic" shortcuts = debugging in production. |
| "This is different because..." | It's not. Delete the code. Start with the test. |

---

## 4. Implementation Planning

**Before coding any directive, create an implementation plan.**

See `docs/methodology/implementation-planning.md` for the full template.

**The rule:** Write every plan as if the implementer is an enthusiastic junior engineer with no project context and an aversion to testing.

Plans are saved to `docs/plans/YYYY-MM-DD-<feature-name>.md`.

---

## 5. Review Gates

**Every completed task goes through two review stages before moving on.**

See `docs/methodology/review-gates.md` for checklists.

### Gate 1: Spec Compliance Review
### Gate 2: Code Quality Review

### Batch Checkpoints
After every 3 completed tasks, pause and produce a progress report.

---

## 6. Verification Before Completion

**NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.**

Before marking any task, directive, or feature as "done":
1. **Run the verification command** (test suite, linter, type checker)
2. **Read the actual output** — not from memory, not assumed
3. **Include the evidence** in your completion report

---

## 7. Systematic Debugging

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

When something breaks, follow the 4-phase process:
1. Root Cause Investigation
2. Pattern Analysis
3. Hypothesis and Testing
4. Implementation

---

## 8. Anti-Rationalization Rules

- "I need more context before I can start" -> Start with the test.
- "Let me explore the codebase first" -> Read the plan.
- "I'll clean this up later" -> Clean it up now.

---

## 9. Definition of Done

- [ ] Implementation plan written before coding
- [ ] Code exists in appropriate directory
- [ ] All new code has corresponding tests in `tests/`
- [ ] Tests were written BEFORE implementation (TDD)
- [ ] All tests pass
- [ ] Spec compliance review passed
- [ ] Code quality review passed
- [ ] Directive file is marked as Complete

---

## 10. File Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Python modules | snake_case | `agent_service.py` |
| Python classes | PascalCase | `class AgentService` |
| Test files | `test_` prefix | `test_agent_service.py` |
| Directives | `NNN_description.md` | `001_initial_setup.md` |

---

## 11. Commit Message Format
`type(scope): description`

Refs: directive-NNN
"""
    Path("AGENTS.md").write_text(agents_md, encoding="utf-8")
    print("Created: AGENTS.md")

    # 7. Methodology Docs
    methodology_docs = {
        "implementation-planning.md": """# Implementation Planning Guide
Before coding any directive, break it into a detailed implementation plan.
Save to `docs/plans/YYYY-MM-DD-<feature-name>.md`.
""",
        "review-gates.md": """# Review Gates Guide
Every task must pass Spec Compliance and Code Quality reviews.
""",
        "debugging-guide.md": """# Systematic Debugging Guide
1. Root Cause Investigation
2. Pattern Analysis
3. Hypothesis and Testing
4. Implementation
""",
    }
    for filename, content in methodology_docs.items():
        Path(f"docs/methodology/{filename}").write_text(content, encoding="utf-8")
    print("Created methodology documents.")

    # 8. Initial Directive
    directive_001 = """# Directive 001: Initial Environment Setup

## Objective
Configure the development environment and verify all dependencies are working.

## Steps
1. Create virtual environment: `python -m venv .venv`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment: `cp .env.example .env`
4. Run verification: `python execution/verify_setup.py`

## Acceptance Criteria
- [ ] .venv created and active
- [ ] `pip install` success
- [ ] `.env` exists
- [ ] `verify_setup.py` passes

## Status: [ ] Incomplete / [ ] Complete
"""
    Path("directives/001_initial_setup.md").write_text(directive_001, encoding="utf-8")
    print("Created: directives/001_initial_setup.md")

    # 9. Verification Script
    verify_script = """#!/usr/bin/env python3
import sys
from pathlib import Path

def check():
    checks = [
        ("Python 3.11+", lambda: sys.version_info[:2] >= (3, 11)),
        (".env exists", lambda: Path(".env").exists()),
        ("Requirements", lambda: Path("requirements.txt").exists()),
        ("Methodology", lambda: Path("docs/methodology/review-gates.md").exists())
    ]
    all_pass = True
    for name, func in checks:
        passed = func()
        print(f"[{'✓' if passed else '✗'}] {name}")
        if not passed: all_pass = False
    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(check())
"""
    Path("execution/verify_setup.py").write_text(verify_script, encoding="utf-8")
    print("Created: execution/verify_setup.py")

    # 10. IDE Config (.cursorrules)
    cursor_rules = f"""# Cursor Rules for {data["name"]}
- Read AGENTS.md, ARCH.md, and RESEARCH.md at start of session.
- Follow TDD Iron Law.
- Create implementation plans before coding.
- Respect directory structure: {", ".join(data["directories"])}
"""
    Path(".cursorrules").write_text(cursor_rules, encoding="utf-8")
    print("Created: .cursorrules")


def main():
    data = extract_from_docs()
    create_scaffold(data)
    print(f"\n--- {data['name']} Initialization Complete! ---")
    print("Next Step: Run 'python execution/verify_setup.py' after setup.")


if __name__ == "__main__":
    main()
