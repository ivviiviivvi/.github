# Chaos Zone 🌪️

## Purpose

This is a **temporary holding area** for unorganized, unstructured, or
work-in-progress content. Think of it as the repository's "inbox" or "dumping
ground" where you can quickly upload content without worrying about organization
or structure.

## What Goes Here?

- Raw chat transcripts from AI conversations
- Draft documents before they're refined
- Brainstorming notes and ideas
- Screenshots and temporary files
- Anything that doesn't have a clear home yet
- Content that needs to be reviewed and organized later

## Structure

```
chaos-zone/
├── chats/          # AI chat transcripts, conversation logs
├── drafts/         # Work-in-progress documents and drafts
├── ideas/          # Brainstorming notes, quick ideas
└── misc/           # Everything else that doesn't fit elsewhere
```

## Guidelines

### ✅ DO:

- Upload content quickly without worrying about formatting
- Use descriptive filenames when possible (e.g.,
  `chat-2025-11-18-feature-discussion.md`)
- Add dates to filenames for context (YYYY-MM-DD format)
- Dump content here first, organize later

### ❌ DON'T:

- Let content sit here indefinitely - periodically review and organize
- Upload sensitive information (API keys, passwords, etc.)
- Store large binary files (use Git LFS or external storage)

## Periodic Cleanup

The chaos zone should be reviewed periodically (suggested: monthly) to:

1. Move relevant content to appropriate directories
1. Archive or delete outdated material
1. Extract useful insights into proper documentation
1. Keep the chaos zone manageable

## Quick Start

To add content:

```bash
# Navigate to the appropriate subdirectory
cd chaos-zone/chats

# Add your file
cp /path/to/your/file.md .

# Or create a new file directly
cat > new-chat-$(date +%Y-%m-%d).md << 'EOF'
[Paste your content here]
EOF
```

______________________________________________________________________

**Remember:** The chaos zone is meant to be temporary. Content here is raw and
unvetted. Always review and organize before referencing in official
documentation.
