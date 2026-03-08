# CLAUDE.md

## Skills
Read and follow these skills before writing any code:
- .claude/skills/base.md
- .claude/skills/security.md
- .claude/skills/project-tooling.md
- .claude/skills/session-management.md
- .claude/skills/python.md

## Project Overview
A CLI tool that remaps pixel values in NIfTI segmentation files. Reads a NIfTI file with pixel values 0-255, prompts the user for a new value for each existing value, and writes a remapped output file.

## Tech Stack
- Language: Python 3.12
- Package manager: uv
- Libraries: nibabel (NIfTI I/O), numpy (pixel manipulation)
- Testing: pytest

## Key Commands
```bash
# Install dependencies
uv sync

# Run the tool
uv run python map_seg.py input.nii.gz output.nii.gz

# Run tests
uv run pytest

# Lint
uv run ruff check .

# Type check
uv run mypy map_seg.py

# Verify tooling
./scripts/verify-tooling.sh
```

## Documentation
- `docs/` - Technical documentation
- `_project_specs/` - Project specifications and todos

## Atomic Todos
All work is tracked in `_project_specs/todos/`:
- `active.md` - Current work
- `backlog.md` - Future work
- `completed.md` - Done (for reference)

## Session Management

### State Tracking
Maintain session state in `_project_specs/session/`:
- `current-state.md` - Live session state (update every 15-20 tool calls)
- `decisions.md` - Key architectural/implementation decisions (append-only)
- `code-landmarks.md` - Important code locations for quick reference
- `archive/` - Past session summaries

### Resuming Work
When starting a new session:
1. Read `_project_specs/session/current-state.md`
2. Check `_project_specs/todos/active.md`
3. Review recent entries in `decisions.md` if context needed
4. Continue from "Next Steps" in current-state.md

## Project-Specific Patterns
- Use lookup tables (numpy array indexing) for value remapping — fast even on large volumes
- Always preserve NIfTI affine and header when writing output files
- Validate pixel range [0, 255] on load
