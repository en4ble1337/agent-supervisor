# Systematic Debugging Guide

When a bug is encountered, do not immediately start changing code. Follow this 4-phase systematic process.

## Phase 1: Root Cause Investigation
1. **Reproduce:** Create a minimal test case or script that consistently triggers the bug.
2. **Isolate:** Determine if the issue is in the Frontend, Backend API, SSH Service, or the remote Agent runtime.
3. **Inspect:** Check logs (FastAPI logs, Browser console, SSH session logs).
4. **Trace:** Follow the data flow from the UI through the API to the database or remote host.

## Phase 2: Pattern Analysis
1. **Scope:** Is this a one-off bug or a systemic pattern?
2. **Context:** Did this work before? What changed recently?
3. **Assumptions:** What assumptions did we make about the external APIs (Hermes/OpenClaw) or SSH behavior that might be wrong?

## Phase 3: Hypothesis and Testing
1. **Formulate:** State exactly why you think the bug is happening.
2. **Verify Hypothesis:** Use a debugger or temporary logging to confirm the hypothesis.
3. **Failed Hypotheses:** Document what you tried and why it *wasn't* the cause.

## Phase 4: Implementation & Verification
1. **Fix:** Apply the minimal fix required to resolve the root cause.
2. **TDD:** Add a regression test to the test suite to ensure this bug never returns.
3. **Verify:** Run the full test suite and verify the fix in the actual environment.
4. **Cleanup:** Remove any temporary logging or debugging artifacts.
