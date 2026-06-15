#!/bin/bash
# install.sh — Cross-platform installer for professor-fan-critique-skill
# Usage:
#   ./install.sh              # Auto-detect platform
#   ./install.sh --dry-run    # Preview without changes
#   ./install.sh --uninstall  # Remove installed links
#   ./install.sh --all        # Install to all detected platforms

set -euo pipefail

SKILL_NAME="professor-fan-critique-skill"
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DRY_RUN=false
UNINSTALL=false
ALL=false

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=true; shift ;;
        --uninstall) UNINSTALL=true; shift ;;
        --all) ALL=true; shift ;;
        --platform) PLATFORM="$2"; shift 2 ;;
        *) echo "Unknown: $1"; exit 1 ;;
    esac
done

install_to() {
    local src="$1"
    local dest="$2"
    local label="$3"

    if $UNINSTALL; then
        if [ -L "$dest/$SKILL_NAME" ] || [ -d "$dest/$SKILL_NAME" ]; then
            echo "  [REMOVE] $label: $dest/$SKILL_NAME"
            $DRY_RUN || rm -rf "$dest/$SKILL_NAME"
        fi
        return
    fi

    mkdir -p "$dest"
    if [ -e "$dest/$SKILL_NAME" ]; then
        echo "  [SKIP] $label: already exists at $dest/$SKILL_NAME"
        return
    fi

    echo "  [INSTALL] $label: $dest/$SKILL_NAME"
    $DRY_RUN || cp -R "$src" "$dest/$SKILL_NAME"
}

echo "professor-fan-critique-skill installer"
echo "======================================"

if $DRY_RUN; then
    echo "  DRY RUN — no changes will be made"
fi

# Detect and install by platform
if [ -n "${PLATFORM:-}" ]; then
    case "$PLATFORM" in
        claude) install_to "$SKILL_DIR" "$HOME/.claude/skills" "Claude Code" ;;
        opencode) install_to "$SKILL_DIR" "$HOME/.config/opencode/skills" "OpenCode" ;;
        copilot) install_to "$SKILL_DIR" "$HOME/.copilot/skills" "GitHub Copilot" ;;
        gemini) install_to "$SKILL_DIR" "$HOME/.gemini/skills" "Gemini CLI" ;;
        cursor) install_to "$SKILL_DIR" ".cursor/skills" "Cursor (project)" ;;
        universal) install_to "$SKILL_DIR" "$HOME/.agents/skills" "Universal" ;;
        *) echo "Unknown platform: $PLATFORM"; exit 1 ;;
    esac
elif $ALL; then
    echo "Installing to all detected platforms..."
    [ -d "$HOME/.claude" ] && install_to "$SKILL_DIR" "$HOME/.claude/skills" "Claude Code"
    [ -d "$HOME/.config/opencode" ] && install_to "$SKILL_DIR" "$HOME/.config/opencode/skills" "OpenCode"
    [ -d "$HOME/.copilot" ] && install_to "$SKILL_DIR" "$HOME/.copilot/skills" "GitHub Copilot"
    [ -d "$HOME/.gemini" ] && install_to "$SKILL_DIR" "$HOME/.gemini/skills" "Gemini CLI"
    # Also install to universal path
    install_to "$SKILL_DIR" "$HOME/.agents/skills" "Universal"
else
    echo "Detecting platform..."
    if [ -d "$HOME/.claude" ]; then
        install_to "$SKILL_DIR" "$HOME/.claude/skills" "Claude Code"
    elif [ -d "$HOME/.config/opencode" ]; then
        install_to "$SKILL_DIR" "$HOME/.config/opencode/skills" "OpenCode"
    elif [ -d "$HOME/.copilot" ]; then
        install_to "$SKILL_DIR" "$HOME/.copilot/skills" "GitHub Copilot"
    elif [ -d "$HOME/.gemini" ]; then
        install_to "$SKILL_DIR" "$HOME/.gemini/skills" "Gemini CLI"
    else
        echo "  No supported platform detected."
        echo "  Install manually: cp -R $SKILL_DIR <your-tool-skill-path>"
        exit 1
    fi
fi

if ! $UNINSTALL; then
    # Also create universal path symlink
    install_to "$SKILL_DIR" "$HOME/.agents/skills" "Universal (fallback)"
fi

echo ""
echo "Done! Use /$SKILL_NAME in your agent to review academic work."
