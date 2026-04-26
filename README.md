# Single-Pane-of-Glass Supervisor Dashboard

A single-pane-of-glass supervisor dashboard acting as a thin layer on top of agent runtimes like OpenClaw and Hermes

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
/opt/hermes/workspace
backend/
backend/api/
backend/models/
backend/schemas/
backend/services/
backend/core/
frontend/
frontend/src/components/
frontend/src/pages/
frontend/src/services/
docs/
```
