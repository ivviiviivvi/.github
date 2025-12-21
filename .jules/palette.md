# Palette's Journal

## 2025-12-17 - [Mermaid Diagram Styling]
**Learning:** Mermaid diagrams in GitHub Markdown can be styled using `classDef` and `:::className` syntax. This allows for creating visually distinct layers in generated documentation without needing image generation tools.
**Action:** Apply this pattern to all future script-generated Mermaid diagrams to improve readability and visual hierarchy.

## 2025-12-19 - [Markdown Table Consistency]
**Learning:** Dynamically generated Markdown tables must maintain consistent column counts across all rows, including the header separator. Partial rows at the end of a dataset can break table rendering if not padded with empty cells to match the header's column count.
**Action:** Always calculate the required number of columns from the header or expected layout and pad subsequent rows with empty cells to preserve table structure.

## 2025-12-20 - [Collapsible Sections in Reports]
**Learning:** Large lists in Markdown reports (like technology coverage or workflow lists) can overwhelm the user and make navigation difficult.
**Action:** Wrap long lists in HTML `<details>` and `<summary>` tags to make them collapsible by default, improving the initial scanability of the report.
