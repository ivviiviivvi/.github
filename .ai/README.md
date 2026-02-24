# AI Guidance Files

This directory contains instruction files for various AI coding assistants.

## Files

| File        | Purpose                          | Tool Discovery    |
| ----------- | -------------------------------- | ----------------- |
| `CLAUDE.md` | Claude Code instructions         | Symlinked at root |
| `GEMINI.md` | Google Gemini instructions       | -                 |
| `AGENTS.md` | General agent/Codex instructions | -                 |

## Why This Structure?

AI coding tools (Claude Code, GitHub Copilot, Gemini, etc.) each have their own
conventions for discovering instruction files:

- **Claude Code**: Looks for `CLAUDE.md` at repository root
- **GitHub Copilot**: Uses `.github/copilot-instructions.md` (kept in standard
  location)
- **Gemini**: Looks for `GEMINI.md` at repository root (optional symlink)

This directory consolidates AI guidance files while maintaining tool
compatibility through symlinks where required.

## Symlinks

Root symlinks for tool discovery:

- `CLAUDE.md` → `.ai/CLAUDE.md` (required for Claude Code)

## Related Files

- `.github/copilot-instructions.md` - GitHub Copilot instructions (standard
  location)
