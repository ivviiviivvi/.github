## 2025-11-16 - Visual Consistency in Markdown Reports
**Learning:** Using emojis in data tables that match section headers significantly improves visual scannability and consistency in generated Markdown reports. Users can quickly identify categories when visual cues (icons) are present alongside text.
**Action:** When generating Markdown reports, apply consistent emoji prefixes to data categories that align with the overall report theme and header style.

## 2025-12-30 - Standardized Legend Management
**Learning:** Hardcoding legend strings in multiple places leads to inconsistency and clutter (redundant displays). Defining a single source of truth (e.g., a dictionary map) for categories and emojis ensures consistency and allows for dynamic legend generation.
**Action:** Use a central configuration object for category-to-emoji mappings and generate legends programmatically in all report sections.
