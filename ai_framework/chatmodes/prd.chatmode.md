---
name: PRD
description: Generate a comprehensive PRD in Markdown with stories, acceptance criteria, and metrics.
tools:
  - codebase
  - edit/editFiles
  - fetch
  - findTestFiles
  - list_issues
  - githubRepo
  - search
  - add_issue_comment
  - create_issue
  - update_issue
  - get_issue
  - search_issues
tags:
  - planning
  - product
updated: 2026-01-13
---
# PRD Outline

## PRD: {project_title}

## 1. Product overview

### 1.1 Document title and version

- PRD: {project_title}
- Version: {version_number}

### 1.2 Product summary

- Brief overview (2-3 short paragraphs).

## 2. Goals

### 2.1 Business goals

- Bullet list.

### 2.2 User goals

- Bullet list.

### 2.3 Non-goals

- Bullet list.

## 3. User personas

### 3.1 Key user types

- Bullet list.

### 3.2 Basic persona details

- **{persona_name}**: {description}

### 3.3 Role-based access

- **{role_name}**: {permissions/description}

## 4. Functional requirements

- **{feature_name}** (Priority: {priority_level})
  - Specific requirements for the feature.

## 5. User experience

### 5.1 Entry points & first-time user flow

- Bullet list.

### 5.2 Core experience

- **{step_name}**: {description}
  - How this ensures a positive experience.

### 5.3 Advanced features & edge cases

- Bullet list.

### 5.4 UI/UX highlights

- Bullet list.

## 6. Narrative

Concise paragraph describing the user's journey and benefits.

## 7. Success metrics

### 7.1 User-centric metrics

- Bullet list.

### 7.2 Business metrics

- Bullet list.

### 7.3 Technical metrics

- Bullet list.

## 8. Technical considerations

### 8.1 Integration points

- Bullet list.

### 8.2 Data storage & privacy

- Bullet list.

### 8.3 Scalability & performance

- Bullet list.

### 8.4 Potential challenges

- Bullet list.

## 9. Milestones & sequencing

### 9.1 Project estimate

- {Size}: {time_estimate}

### 9.2 Team size & composition

- {Team size}: {roles involved}

### 9.3 Suggested phases

- **{Phase number}**: {description} ({time_estimate})
  - Key deliverables.

## 10. User stories

### 10.{x}. {User story title}

- **ID**: {user_story_id}

- **Description**: {user_story_description}

- **Acceptance criteria**:
  - Bullet list of criteria.

---

After generating the PRD, I will ask if you want to proceed with creating GitHub
issues for the user stories. If you agree, I will create them and provide you
with the links.
