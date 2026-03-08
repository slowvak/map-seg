# Code Landmarks

## Entry Points
| Location | Purpose |
|----------|---------|
| map_seg.py:main() | CLI entry point, argparse |

## Core Business Logic
| Location | Purpose |
|----------|---------|
| map_seg.py:load_nifti() | Load and validate NIfTI |
| map_seg.py:get_mapping() | Interactive user prompts |
| map_seg.py:remap() | LUT-based pixel remapping |

## Configuration
| Location | Purpose |
|----------|---------|
| pyproject.toml | Project deps and metadata |

## Gotchas & Non-Obvious Behavior
| Location | Issue | Notes |
|----------|-------|-------|
| uv | SSL/TLS | Zscaler proxy requires `SSL_CERT_FILE` from system keychain export |
