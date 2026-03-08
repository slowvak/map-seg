#!/bin/bash
set -e

echo "Verifying project tooling..."

# GitHub CLI
if command -v gh &> /dev/null; then
  if gh auth status &> /dev/null; then
    echo "✓ GitHub CLI authenticated"
  else
    echo "✗ GitHub CLI not authenticated. Run: gh auth login"
    exit 1
  fi
else
  echo "⚠ GitHub CLI not installed. Run: brew install gh"
fi

# uv
if command -v uv &> /dev/null; then
  echo "✓ uv installed ($(uv --version))"
else
  echo "✗ uv not installed. Run: curl -LsSf https://astral.sh/uv/install.sh | sh"
  exit 1
fi

# Check project dependencies
if [ -f "pyproject.toml" ]; then
  if uv sync --check 2>/dev/null; then
    echo "✓ Python dependencies in sync"
  else
    echo "⚠ Dependencies may need sync. Run: uv sync"
  fi
fi

echo ""
echo "Tooling verification complete!"
