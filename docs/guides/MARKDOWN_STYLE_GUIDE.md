# Markdown Style Guide

Living style bible for English language patterns, best practices, and markdown
formatting standards.

## Table of Contents

- [Purpose](#purpose)
- [Core Principles](#core-principles)
- [Language Standards](#language-standards)
- [Markdown Formatting](#markdown-formatting)
- [Document Structure](#document-structure)
- [Writing Style](#writing-style)
- [Technical Writing](#technical-writing)
- [Code Examples](#code-examples)
- [File Naming](#file-naming)
- [Version Control](#version-control)

---

## Purpose

This document serves as the **authoritative style bible** for all markdown
documentation in this organization. It defines:

- English language usage patterns
- Markdown formatting standards
- Writing style conventions
- Best practices for technical documentation
- Consistency rules across all repositories

This is a **living document** that evolves with our needs while maintaining
backward compatibility.

---

## Core Principles

### 1. Clarity Over Cleverness

Write to be understood, not to impress.

**Good**:

```markdown
Use semantic versioning for all releases.
```

**Bad**:

```markdown
Leverage semver paradigms to facilitate release management synergies.
```

### 2. Consistency

Use the same terms, formats, and structures throughout all documentation.

### 3. Accessibility

Write for diverse audiences: beginners, experts, non-native English speakers.

### 4. Maintainability

Write documentation that is easy to update and refactor.

### 5. No Visual Embellishments

**DO NOT use emoji or decorative Unicode characters** in documentation.

**Prohibited**:

```markdown
## Key Features

- Feature A
- Feature B
- Feature C
```

**Correct**:

```markdown
## Key Features

- Feature A
- Feature B
- Feature C
```

---

## Language Standards

### English Variant

Use **American English** spelling and conventions throughout.

**Examples**:

- color (not colour)
- organize (not organise)
- analyze (not analyse)
- center (not centre)

### Grammar Rules

#### 1. Active Voice Preferred

**Good**: "The system processes requests" **Avoid**: "Requests are processed by
the system"

Exception: Use passive voice when the actor is unknown or irrelevant.

#### 2. Present Tense for Documentation

**Good**: "The function returns a value" **Avoid**: "The function will return a
value"

Exception: Use future tense for roadmap items.

#### 3. Second Person for Instructions

**Good**: "Configure your environment" **Avoid**: "One should configure the
environment"

#### 4. Oxford Comma

Always use the serial comma.

**Good**: "Configure, build, and test" **Avoid**: "Configure, build and test"

#### 5. Sentence Case for Headings

Use sentence case, not title case.

**Good**: "Installing the application" **Avoid**: "Installing The Application"

### Terminology

#### Consistent Terms

Use the same term throughout documentation:

| Preferred      | Avoid                                                    |
| -------------- | -------------------------------------------------------- |
| repository     | repo (in formal docs)                                    |
| pull request   | PR (in formal docs)                                      |
| commit message | commit msg                                               |
| command line   | terminal, console, shell (use specific term when needed) |
| filename       | file name                                                |
| codebase       | code base                                                |
| email          | e-mail                                                   |
| setup (noun)   | set-up                                                   |
| set up (verb)  | setup                                                    |

#### Technical Terms

Use proper capitalization for proper nouns:

- Git (not git)
- GitHub (not Github)
- JavaScript (not Javascript, javascript)
- TypeScript (not Typescript)
- Node.js (not NodeJS, Node)
- Docker (not docker)
- Kubernetes (not kubernetes)

### Abbreviations and Acronyms

#### First Use

Spell out acronyms on first use in each document:

```markdown
Use Continuous Integration/Continuous Deployment (CI/CD) for automated testing.
```

#### Common Exceptions

These can be used without spelling out:

- API
- URL
- HTTP/HTTPS
- HTML/CSS
- JSON/XML
- SQL
- PDF

#### Latin Abbreviations

Avoid Latin abbreviations; use English equivalents:

| Avoid | Use                |
| ----- | ------------------ |
| i.e.  | that is            |
| e.g.  | for example        |
| etc.  | and so on          |
| via   | through, by way of |

---

## Markdown Formatting

### Headings

#### Hierarchy

```markdown
# Document Title (H1) - One per document

## Major Section (H2)

### Subsection (H3)

#### Minor Section (H4)
```

**Rules**:

1. Only one H1 per document (the title)
1. Do not skip heading levels
1. Use sentence case
1. No punctuation at end of headings
1. Add blank line before and after headings

**Good**:

```markdown
## Installation instructions

Follow these steps to install.
```

**Bad**:

```markdown
## Installation Instructions:

Follow these steps to install.
```

### Paragraphs

#### Spacing

- Use blank lines between paragraphs
- Do not indent paragraphs
- Limit paragraphs to 3-4 sentences

```markdown
This is the first paragraph. It contains related sentences.

This is the second paragraph. It introduces a new idea.
```

#### Line Length

- Wrap lines at 80-100 characters (soft limit)
- Or use one sentence per line for easier diff review

```markdown
# One sentence per line (recommended for version control)

This is the first sentence.
This is the second sentence.
This is the third sentence.

# Or wrapped at ~80 characters

This is a longer paragraph that wraps at approximately eighty characters
to maintain readability while also working well with version control systems.
```

### Lists

#### Unordered Lists

Use hyphens for consistency:

```markdown
- First item
- Second item
  - Nested item
  - Another nested item
- Third item
```

**Rules**:

1. Use hyphens (-), not asterisks (\*) or plus signs (+)
1. Indent nested items with 2 spaces
1. Add blank line before and after list
1. Add blank line between list items if any item is multi-paragraph

```markdown
Text before list.

- Item one
- Item two
  - Nested item
- Item three

Text after list.
```

#### Ordered Lists

```markdown
1. First step
2. Second step
3. Third step
```

**Rules**:

1. Use sequential numbers (not all "1.")
1. Use actual numbers for better readability in raw markdown
1. End each item with period if items are complete sentences
1. No period if items are fragments

**Complete sentences**:

```markdown
1. Install the dependencies.
2. Configure the environment.
3. Run the application.
```

**Fragments**:

```markdown
1. Install dependencies
2. Configure environment
3. Run application
```

#### Task Lists

```markdown
- [ ] Incomplete task
- [x] Complete task
- [ ] Another incomplete task
```

### Emphasis

#### Bold

Use double asterisks:

```markdown
**This is bold text**
```

Use for:

- Important terms on first mention
- Warnings and cautions
- Strong emphasis

#### Italic

Use single asterisks:

```markdown
_This is italic text_
```

Use for:

- Emphasis
- Variable names in prose
- Book titles

#### Combined

```markdown
**_This is bold and italic_**
```

Use sparingly.

#### Code

Use backticks for inline code:

```markdown
Use the `git commit` command to commit changes.
```

Use for:

- Command names
- Function names
- Variable names
- File names
- Code snippets in prose

### Links

#### Inline Links

```markdown
See the [documentation](https://example.com/docs) for details.
```

#### Reference Links

For repeated or long URLs:

```markdown
See the [documentation][docs] for details.

More information in the [API reference][api].

[docs]: https://example.com/docs
[api]: https://example.com/api
```

#### Internal Links

```markdown
See [Installation](#installation) section.

See [Contributing Guide](../CONTRIBUTING.md).
```

#### Managed Links

For links that should stay consistent across the repo, add a link key comment:

```markdown
[GitHub Discussions](https://github.com/ivviiviivvi/.github/discussions)<!-- link:github.discussions -->
```

Update all managed links with:

```bash
python automation/scripts/resolve_link_placeholders.py --write --annotate
```

**Rules**:

1. Use descriptive link text (not "click here")
1. Ensure links work (test them)
1. Use relative paths for internal links
1. Use reference links for repeated URLs

**Good**:

```markdown
Read the [installation guide](../WORKSPACE_QUICK_START.md) for setup instructions.
```

**Bad**:

```markdown
Click [here](../WORKSPACE_QUICK_START.md) to install.
```

### Code Blocks

#### Fenced Code Blocks

Always specify language for syntax highlighting:

````markdown
```bash
git commit -m "feat: add new feature"
```

```javascript
function example() {
  return true;
}
```

```python
def example():
    return True
```
````

#### Common Language Identifiers

```
bash, sh, shell
javascript, js
typescript, ts
python, py
java
go
rust
ruby, rb
php
html
css
json
yaml, yml
xml
sql
markdown, md
diff
plaintext, text
```

#### No Language Identifier

For terminal output or when language doesn't matter:

````markdown
```
output without syntax highlighting
```
````

### Tables

#### Basic Tables

```markdown
| Header 1 | Header 2 | Header 3 |
| -------- | -------- | -------- |
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

#### Alignment

```markdown
| Left Aligned | Center Aligned | Right Aligned |
| :----------- | :------------: | ------------: |
| Left         |     Center     |         Right |
```

**Rules**:

1. Use pipes to align columns visually in raw markdown
1. Add blank line before and after table
1. Keep headers simple
1. Use sentence case for headers

### Blockquotes

```markdown
> This is a blockquote.
> It can span multiple lines.
>
> It can have multiple paragraphs.
```

Use for:

- Important notes
- Quotes from external sources
- Callouts

### Horizontal Rules

Use three hyphens with blank lines:

```markdown
Text before rule.

---

Text after rule.
```

Use sparingly to separate major sections.

---

## Document Structure

### Front Matter

Every document should begin with:

```markdown
# Document Title

Brief description of what this document covers.

## Table of Contents

- [Section 1](#section-1)
- [Section 2](#section-2)
- [Section 3](#section-3)

---
```

### Standard Sections

#### README.md Structure

```markdown
# Project Name

Brief project description.

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

Installation instructions.

## Usage

Usage examples.

## Configuration

Configuration options.

## Contributing

Link to CONTRIBUTING.md

## License

License information.
```

#### Guide Document Structure

```markdown
# Guide Title

Overview of guide purpose.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Step 1](#step-1)
- [Step 2](#step-2)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

---

## Prerequisites

What users need before starting.

## Step 1

First step instructions.

## Step 2

Second step instructions.

## Troubleshooting

Common issues and solutions.

## Next Steps

What to do after completing guide.

---

**Last Updated**: YYYY-MM-DD
```

### Footer

Include at end of long-lived documents:

```markdown
---

**Last Updated**: 2025-11-25
```

---

## Writing Style

### Tone

#### Professional but Approachable

**Good**: "Configure the environment before running tests." **Avoid**: "You
better configure the environment first!"

#### Direct and Clear

**Good**: "Delete the file." **Avoid**: "You might want to consider possibly
deleting the file."

#### Respectful

**Good**: "Ensure you have admin permissions." **Avoid**: "Obviously, you need
admin permissions."

### Instructions

#### Use Imperative Mood

```markdown
1. Install dependencies
2. Configure environment
3. Run application
```

Not:

```markdown
1. You should install dependencies
2. Please configure environment
3. Try running the application
```

#### Number Multi-Step Procedures

```markdown
1. First step
2. Second step
3. Third step
```

#### Provide Context

Explain why, not just what:

````markdown
## Set environment variables

Configure environment variables to customize application behavior:

```bash
export API_KEY=your_key_here
```
````

This allows the application to authenticate with external services.

````

### Examples

Always provide concrete examples:

```markdown
## Branch naming

Use descriptive branch names following this pattern:

```bash
develop/feature/component-name
````

For example:

```bash
develop/feature/user-authentication
develop/feature/payment-gateway
production/hotfix/security-patch
```

````

---

## Technical Writing

### Commands

Format commands consistently:

```markdown
Run the following command:

```bash
git commit -m "feat: add feature"
````

````

For multiple commands:

```markdown
```bash
# Install dependencies
npm install

# Run tests
npm test

# Build application
npm run build
````

````

### File Paths

Use backticks for file paths:

```markdown
Edit the `config/settings.yaml` file.

Add the following to `src/main.js`:
````

Use forward slashes even for Windows:

```markdown
`src/components/Header.js` (not `src\components\Header.js`)
```

### Placeholders

Use clear placeholders:

````markdown
```bash
git clone https://github.com/<username>/<repository>
cd <repository>
```
````

````

Or with more description:

```markdown
Replace `<your-api-key>` with your actual API key:

```javascript
const apiKey = '<your-api-key>';
````

````

### Prerequisites

Always list prerequisites clearly:

```markdown
## Prerequisites

Before starting, ensure you have:

- Node.js 18 or later
- npm 9 or later
- Git 2.30 or later
- Admin permissions on your system
````

---

## Code Examples

### Complete and Runnable

Provide complete, working examples:

**Good**:

````markdown
```javascript
// server.js
const express = require("express");
const app = express();
const port = 3000;

app.get("/", (req, res) => {
  res.send("Hello World");
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
```
````

````

**Avoid fragments without context**.

### Comments

Use comments to explain:

```markdown
```javascript
// Initialize the database connection
const db = await initDatabase();

// Set up middleware
app.use(express.json());

// Define routes
app.get('/users', getUsers);
````

`````

### Syntax Highlighting

Always specify language:

````markdown
```javascript
// JavaScript code
`````

```python
# Python code
```

```bash
# Shell commands
```

`````

---

## File Naming

### Documentation Files

Use uppercase for top-level docs:

```
README.md
CONTRIBUTING.md
LICENSE
CHANGELOG.md
```

Use sentence case for specific guides:

```
installation-guide.md
api-reference.md
troubleshooting.md
```

### Directories

Use lowercase with hyphens:

```
user-guides/
api-docs/
getting-started/
```

---

## Version Control

### Commit Messages for Documentation

Follow conventional commits:

```bash
docs: update installation guide
docs(api): add authentication examples
docs: fix typo in README
docs(guide): improve troubleshooting section
```

### Reviewing Documentation

Check for:

1. **Accuracy**: Information is correct and current
2. **Clarity**: Easy to understand
3. **Completeness**: No missing steps
4. **Consistency**: Follows this style guide
5. **Links**: All links work
6. **Code**: All examples work

---

## Common Mistakes to Avoid

### 1. Using Emoji

**Wrong**:
```markdown
## Installation
Follow these steps to install.
```

**Right**:
```markdown
## Installation
Follow these steps to install.
```

### 2. Inconsistent Terminology

**Wrong**: Using "repository", "repo", and "code base" interchangeably

**Right**: Use "repository" consistently in formal documentation

### 3. Missing Language Identifiers

**Wrong**:
````markdown
```
git commit -m "message"
```
`````

**Right**:

````markdown
```bash
git commit -m "message"
```
````

### 4. Poor Link Text

**Wrong**: "Click [here](../WORKSPACE_QUICK_START.md) for more information"

**Right**: "See the [installation guide](../WORKSPACE_QUICK_START.md) for more
information"

### 5. Walls of Text

**Wrong**: Single paragraph with 15 sentences

**Right**: Break into multiple paragraphs (3-4 sentences each)

---

## Checklist for New Documents

Before publishing documentation:

- [ ] Document has clear title (H1)
- [ ] Table of contents included (for documents >3 sections)
- [ ] All headings follow hierarchy (no skipped levels)
- [ ] No emoji or decorative characters used
- [ ] Consistent terminology throughout
- [ ] All code blocks have language identifiers
- [ ] All links tested and working
- [ ] Examples are complete and tested
- [ ] Grammar and spelling checked
- [ ] Follows sentence case for headings
- [ ] Uses hyphens for lists
- [ ] Last updated date included
- [ ] Appropriate front matter included

---

## Evolution of This Guide

This is a **living document**. To propose changes:

1. Open an issue describing the proposed change
1. Discuss rationale and impact
1. Submit PR updating this guide
1. Get approval from documentation team
1. Update existing docs to conform (if needed)

---

## Related Documentation

- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contributing guidelines
- [VERSION_CONTROL_STANDARDS.md](../reference/VERSION_CONTROL_STANDARDS.md) -
  Version control standards
- [README.md](../../README.md) - Repository overview

---

**Last Updated**: 2025-11-25
