<!--
CHECKPOINT RULES (from session-management.md):
- Quick update: After any todo completion
- Full checkpoint: After ~20 tool calls or decisions
- Archive: End of session or major feature complete

After each task, ask: Decision made? >10 tool calls? Feature done?
-->

# Current Session State

*Last updated: 2026-03-07*

## Active Task
Project initialization and core CLI tool creation

## Current Status
- **Phase**: implementing
- **Progress**: Core tool complete, project structure set up
- **Blocking Issues**: None

## Context Summary
Created map_seg.py — a CLI tool that reads a NIfTI file, validates pixel values are in [0,255], prompts user for remapping, and writes output. Project initialized with uv, nibabel, and numpy.

## Files Being Modified
| File | Status | Notes |
|------|--------|-------|
| map_seg.py | complete | Core CLI tool |
| CLAUDE.md | complete | Project config |

## Next Steps
1. [ ] Set up GitHub repo (pending user decision)
2. [ ] Add tests
3. [ ] Add ruff/mypy dev dependencies

## Key Context to Preserve
- Using uv for package management (user preference)
- SSL requires system keychain export for uv on this machine (Zscaler proxy)

## Resume Instructions
To continue this work:
1. Check if GitHub repo was created
2. Review map_seg.py for any requested changes
