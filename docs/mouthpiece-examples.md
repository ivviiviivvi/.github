# Mouthpiece Filter System - Examples

Real-world examples of natural writing transformed into AI-optimized prompts.

## Table of Contents

- [Quick Examples](#quick-examples)
- [Technical Requests](#technical-requests)
- [Feature Ideas](#feature-ideas)
- [Problem Solving](#problem-solving)
- [Documentation Needs](#documentation-needs)
- [Poetic Visions](#poetic-visions)

---

## Quick Examples

### Example 1: Simple Request

**Natural Input:**
```
hey, can you help me add a dark mode toggle? users keep asking for it
```

**Transformed Output:**
```markdown
# Create: Dark Mode Toggle Feature

## Objective
Add a dark mode toggle feature to the application in response to user requests.

## Requirements
- Implement dark mode toggle UI element
- Create dark mode color scheme/theme
- Persist user preference
- Apply theme across application

## Key Concepts
- Dark mode
- Theme toggle
- User preferences
- UI theming

## Context
Multiple user requests for dark mode functionality.

## Success Criteria
- [ ] Toggle UI component implemented
- [ ] Dark theme styles defined
- [ ] User preference saved and persisted
- [ ] Theme applied consistently across app
```

---

### Example 2: Urgent Bug Fix

**Natural Input:**
```
URGENT - login's totally broken after the deployment, users can't sign in,
they keep getting redirected to homepage. need this fixed like NOW
```

**Transformed Output:**
```markdown
# Fix: Critical Login Redirect Bug (URGENT)

## Objective
Resolve critical login failure where users are incorrectly redirected to
homepage instead of being authenticated.

## Priority
🚨 URGENT - Production issue blocking user access

## Current Problem
- Login functionality broken post-deployment
- Users cannot successfully sign in
- Incorrect redirect to homepage after login attempt
- Blocking all user authentication

## Requirements
- Identify root cause of login redirect issue
- Fix authentication flow
- Restore proper post-login behavior
- Verify fix in production

## Investigation Steps
1. Review recent deployment changes
2. Check authentication service logs
3. Verify redirect configuration
4. Test login flow end-to-end

## Success Criteria
- [ ] Users can successfully log in
- [ ] Proper post-login redirect behavior restored
- [ ] Issue root cause identified and documented
- [ ] Monitoring in place to prevent recurrence
```

---

## Technical Requests

### Example 3: API Design

**Natural Input:**
```
thinking we should build an API for third parties to pull user analytics.
needs to be RESTful, probably need auth with API keys, rate limiting so
people don't hammer our servers, and maybe webhook support so they don't
have to keep polling? GraphQL could work too but maybe that's overkill
```

**Transformed Output:**
```markdown
# Design: Third-Party Analytics API

## Objective
Design and implement a REST API enabling third-party access to user analytics
data with appropriate security and performance controls.

## Requirements

### Core Functionality
- RESTful API design
- User analytics data endpoints
- Query filtering and pagination

### Security
- API key authentication
- Rate limiting per API key
- Access control and permissions

### Performance & Scalability
- Rate limiting (prevent server overload)
- Webhook support (alternative to polling)
- Efficient data delivery

## Technical Considerations

### Architecture Decision: REST vs GraphQL
- Primary: RESTful API (simpler, well-understood)
- Consider: GraphQL for flexible querying (evaluate complexity vs benefit)

### Key Components
1. API authentication layer (API keys)
2. Rate limiting middleware
3. Analytics data endpoints
4. Webhook notification system (optional)
5. API documentation

## API Features
- [ ] Authentication via API keys
- [ ] Rate limiting (e.g., 1000 requests/hour)
- [ ] Analytics data endpoints (users, events, metrics)
- [ ] Pagination support
- [ ] Webhook subscriptions (push vs pull)
- [ ] API documentation (OpenAPI/Swagger)

## Questions to Resolve
- Rate limit thresholds per tier?
- Which analytics data should be exposed?
- Webhook event types to support?
- GraphQL worth the additional complexity?

## Original Consideration
> "GraphQL could work too but maybe that's overkill"

Start with REST for simplicity. Can evaluate GraphQL later if querying
flexibility becomes a strong requirement.
```

---

### Example 4: Database Optimization

**Natural Input:**
```
our queries are getting super slow, like 10+ seconds for some reports.
probably need to add indexes? or maybe the queries are just bad. could
be the data's getting too big. help me figure out what's wrong and fix it
```

**Transformed Output:**
```markdown
# Solve: Database Query Performance Issues

## Objective
Diagnose and resolve slow database query performance affecting report
generation (currently 10+ seconds).

## Current Problem
- Report queries taking 10+ seconds
- Performance degradation over time
- User impact: slow reporting experience

## Potential Root Causes
1. Missing or inefficient indexes
2. Poorly optimized queries
3. Database growth (data volume)
4. Resource constraints
5. Missing query optimization

## Investigation Plan

### Phase 1: Diagnosis
- [ ] Enable slow query logging
- [ ] Identify slowest queries
- [ ] Analyze query execution plans (EXPLAIN)
- [ ] Check existing indexes
- [ ] Review database size and growth
- [ ] Check server resources (CPU, memory, disk I/O)

### Phase 2: Analysis
- [ ] Identify missing indexes
- [ ] Review query patterns and structure
- [ ] Evaluate data volume impact
- [ ] Check for N+1 query problems
- [ ] Identify table scan operations

### Phase 3: Optimization
- [ ] Add strategic indexes
- [ ] Rewrite inefficient queries
- [ ] Implement query result caching
- [ ] Consider query pagination
- [ ] Optimize joins and subqueries
- [ ] Archive old data if appropriate

### Phase 4: Validation
- [ ] Measure query performance improvements
- [ ] Run load tests
- [ ] Monitor production performance
- [ ] Document optimizations made

## Success Criteria
- Report queries complete in < 2 seconds
- Sustained performance under load
- Scalable solution for future growth

## Original Expression
> "probably need to add indexes? or maybe the queries are just bad.
> could be the data's getting too big."

All valid hypotheses! Investigation will determine the primary cause(s).
```

---

## Feature Ideas

### Example 5: Social Features

**Natural Input:**
```
what if users could like... follow each other? see what projects their
friends are working on, maybe give kudos or something? make it feel more
like a community and less lonely. twitter-style feed but for makers?
```

**Transformed Output:**
```markdown
# Design: Social Features - User Following & Activity Feed

## Objective
Create social features allowing users to follow each other, view friend
activities, and engage with a community-oriented maker feed.

## Vision
> "make it feel more like a community and less lonely. twitter-style feed
> but for makers?"

Transform the platform from isolated individual use to a connected community
where makers can discover and support each other's work.

## Core Features

### User Following
- [ ] Follow/unfollow other users
- [ ] Followers/following lists
- [ ] User discovery and search

### Activity Feed
- [ ] Timeline of followed users' activities
- [ ] Project updates and milestones
- [ ] Activity filtering and preferences

### Engagement
- [ ] Kudos/appreciation system (like button alternative)
- [ ] Comment on project updates
- [ ] Share/reshare functionality

### Community Building
- [ ] Suggested users to follow
- [ ] Trending projects/makers
- [ ] Community highlights

## User Stories

**As a** maker on the platform
**I want to** follow other makers I admire
**So that** I can stay updated on their projects and feel part of a community

**As a** user
**I want to** see what my friends are building
**So that** I can engage with their work and find inspiration

**As a** user
**I want to** give kudos to great work
**So that** I can show appreciation and encourage fellow makers

## Technical Components
1. User relationship graph (following/followers)
2. Activity feed generator
3. Activity event system
4. Notification system
5. Feed ranking algorithm
6. Privacy controls

## Privacy & Control
- [ ] Private/public project settings
- [ ] Activity visibility preferences
- [ ] Block/mute functionality
- [ ] Feed customization options

## Success Metrics
- User engagement rate
- Follow network growth
- Activity feed interaction
- Community satisfaction (surveys)
- Reduced user isolation (measured via engagement)

## Design Philosophy
"Twitter-style feed but for makers" - Keep it simple, maker-focused, and
positive. Emphasize creation and support over vanity metrics.
```

---

### Example 6: Accessibility Feature

**Natural Input:**
```
we're not very accessible right now, screen readers probably hate us.
need keyboard navigation, proper ARIA labels, maybe high contrast mode?
want everyone to be able to use this, not just people who can see/mouse well
```

**Transformed Output:**
```markdown
# Improve: Accessibility Compliance and Inclusive Design

## Objective
Improve application accessibility to ensure usability for all users,
regardless of ability, assistive technology, or input method.

## Current State
- Limited screen reader support
- Insufficient keyboard navigation
- Missing ARIA labels
- No high contrast mode
- Barriers for users with disabilities

## Vision
> "want everyone to be able to use this, not just people who can see/mouse well"

Create an inclusive experience that works for all users regardless of visual,
motor, or cognitive abilities.

## Requirements

### Screen Reader Support
- [ ] Semantic HTML structure
- [ ] Proper heading hierarchy
- [ ] ARIA labels for interactive elements
- [ ] ARIA live regions for dynamic content
- [ ] Alt text for all images
- [ ] Screen reader testing (NVDA, JAWS, VoiceOver)

### Keyboard Navigation
- [ ] All features accessible via keyboard
- [ ] Logical tab order
- [ ] Visible focus indicators
- [ ] Keyboard shortcuts (with documentation)
- [ ] Skip navigation links
- [ ] No keyboard traps

### Visual Accessibility
- [ ] High contrast mode option
- [ ] Color contrast compliance (WCAG AA minimum)
- [ ] Resizable text (up to 200%)
- [ ] No information conveyed by color alone
- [ ] Focus indicators clearly visible

### Additional Considerations
- [ ] Reduced motion preferences
- [ ] Form labels and error messages
- [ ] Accessible error handling
- [ ] Time limits adjustable/removable
- [ ] Alternative text for icons

## Implementation Phases

### Phase 1: Foundation (Critical)
1. Audit current accessibility issues
2. Fix semantic HTML structure
3. Add basic ARIA labels
4. Implement keyboard navigation

### Phase 2: Enhancement
1. Add high contrast mode
2. Improve color contrast
3. Add skip links
4. Implement focus management

### Phase 3: Polish
1. Add keyboard shortcuts
2. Reduced motion support
3. Comprehensive screen reader testing
4. User testing with assistive technology users

## Testing Strategy
- [ ] Automated testing (axe, Lighthouse)
- [ ] Manual keyboard-only navigation
- [ ] Screen reader testing
- [ ] Color contrast analysis
- [ ] User testing with people using assistive technology

## Success Criteria
- WCAG 2.1 AA compliance
- All features usable via keyboard only
- Screen reader users can complete all tasks
- High contrast mode available
- Positive feedback from users with disabilities

## Standards & Guidelines
- Follow WCAG 2.1 Level AA
- Use WAI-ARIA authoring practices
- Test with actual assistive technology users
```

---

## Problem Solving

### Example 7: Memory Leak Investigation

**Natural Input:**
```
something's eating memory like crazy, app starts at 100mb then balloons to
2GB after a few hours. probably a leak somewhere? users are having to restart
constantly. maybe it's the websocket connections? or the cache growing forever?
idk but it's bad
```

**Transformed Output:**
```markdown
# Debug: Memory Leak Investigation and Resolution

## Objective
Identify and fix memory leak causing application memory usage to grow from
100MB to 2GB over several hours.

## Problem Statement
- Initial memory: ~100MB
- Memory after few hours: ~2GB
- User impact: Frequent restarts required
- Memory continuously grows (not garbage collected)

## Suspected Causes
> "maybe it's the websocket connections? or the cache growing forever?"

1. WebSocket connection leaks
2. Unbounded cache growth
3. Event listener accumulation
4. Closure memory retention
5. Large object retention

## Investigation Plan

### Phase 1: Reproduce & Measure
- [ ] Set up memory profiling tools
- [ ] Reproduce memory growth locally
- [ ] Create memory snapshots over time
- [ ] Identify growth pattern (gradual vs sudden)
- [ ] Record heap dumps at intervals

### Phase 2: Analysis
- [ ] Compare heap snapshots
- [ ] Identify retained objects
- [ ] Track object allocation patterns
- [ ] Check for detached DOM nodes
- [ ] Analyze websocket connection lifecycle
- [ ] Review cache implementation
- [ ] Check event listener cleanup

### Phase 3: Hypothesis Testing

**WebSocket Connections:**
- [ ] Verify connections are properly closed
- [ ] Check for connection cleanup on page navigation
- [ ] Monitor active connection count over time
- [ ] Review reconnection logic

**Cache Growth:**
- [ ] Check cache size limits
- [ ] Verify cache eviction policy
- [ ] Monitor cache size over time
- [ ] Review cache key generation

**Event Listeners:**
- [ ] Audit addEventListener/removeEventListener pairs
- [ ] Check component cleanup/unmount
- [ ] Review global event handlers

### Phase 4: Fix & Verify
- [ ] Implement fixes for identified leaks
- [ ] Add proper cleanup in component lifecycle
- [ ] Implement cache size limits
- [ ] Add memory usage monitoring
- [ ] Run memory tests overnight
- [ ] Verify memory stability

## Tools & Techniques
- Chrome DevTools Memory Profiler
- Heap snapshot comparison
- Allocation timeline
- Memory usage monitoring
- Load testing with memory tracking

## Prevention
- [ ] Add memory leak tests to CI
- [ ] Implement memory usage alerts
- [ ] Code review checklist for cleanup
- [ ] Document resource lifecycle patterns

## Success Criteria
- Memory usage stays under 200MB after 24 hours
- No user reports of memory-related restarts
- Heap size remains stable under load

## Original Expression
> "something's eating memory like crazy... idk but it's bad"

Systematic investigation will identify the culprit. Memory leaks are
findable with the right tools!
```

---

## Documentation Needs

### Example 8: Onboarding Documentation

**Natural Input:**
```
new developers keep getting stuck onboarding. they don't know where to start,
what to install, how things connect. need like a "day 1" guide or something.
hand-holding from zero to productive. maybe with screenshots? walkthrough
style?
```

**Transformed Output:**
```markdown
# Create: Developer Onboarding Guide ("Day 1" Walkthrough)

## Objective
Create comprehensive, beginner-friendly onboarding documentation that guides
new developers from zero to productive on their first day.

## Current Problem
- New developers struggle with initial setup
- Unclear where to start
- Missing context on system architecture
- Gaps in setup instructions
- Slows time-to-productivity

## Guide Requirements

### Content Structure
1. **Welcome & Overview** (What you're building)
2. **Prerequisites** (What you need installed)
3. **Environment Setup** (Step-by-step setup)
4. **Architecture Overview** (How things connect)
5. **Your First Contribution** (Guided task)
6. **Resources & Next Steps** (Where to go from here)

### Style & Format
> "hand-holding from zero to productive. maybe with screenshots? walkthrough style?"

- Conversational, friendly tone
- Step-by-step instructions
- Screenshots for visual guidance
- Code examples with explanations
- Troubleshooting sections
- Checkpoints to verify progress

## Content Outline

### 1. Welcome & Overview
```markdown
# Welcome to [Project]!

## What We're Building
[Friendly explanation of the project]

## What You'll Learn Today
- ✅ Set up your development environment
- ✅ Understand the project architecture
- ✅ Make your first contribution
- ✅ Know where to find help

Let's get started! ☕
```

### 2. Prerequisites
- Required software (with version numbers)
- Operating system notes
- Access requirements (credentials, permissions)
- Estimated time to complete

### 3. Environment Setup
**Step-by-step with verification:**
```markdown
## Step 1: Clone the Repository
[instruction]

✅ **Verify it worked:** [how to check]

## Step 2: Install Dependencies
[instruction]

✅ **Verify it worked:** [how to check]
```

### 4. Architecture Overview
- System diagram (visual)
- Component explanation
- How pieces connect
- Data flow overview
- Key concepts and terminology

### 5. Your First Contribution
**Guided exercise:**
- Small, achievable task
- Complete walkthrough
- Explains *why* not just *how*
- Pull request process
- Celebration of completion 🎉

### 6. Resources & Next Steps
- Code of conduct
- Communication channels (Slack, Discord, etc.)
- Coding standards
- How to ask for help
- Suggested next tasks

## Deliverables

- [ ] Main onboarding document (README-style)
- [ ] Screenshots/diagrams for visual guidance
- [ ] Troubleshooting FAQ
- [ ] Video walkthrough (optional but recommended)
- [ ] Setup verification checklist
- [ ] "Day 1" test task with solution

## Success Criteria
- New developers can complete setup independently
- Reduced onboarding time from [X] days to [Y] days
- Decreased onboarding-related questions
- Positive feedback from new team members

## Maintenance
- [ ] Update when dependencies change
- [ ] Collect feedback from each new developer
- [ ] Keep screenshots current
- [ ] Review quarterly for accuracy

## Original Vision
> "hand-holding from zero to productive"

Make it impossible to get lost. Every step verified, every question
anticipated, every frustration smoothed away.
```

---

## Poetic Visions

### Example 9: Creative Feature Concept

**Natural Input:**
```
imagine if our code could tell stories. like, you could see the journey of
a function - where it was born, how it evolved, the bugs it survived, the
refactors that shaped it. a timeline of its life. commits are just chapters
in a longer story, right? visualize that story. make history alive.
```

**Transformed Output:**
```markdown
# Design: Code Story Visualization - Function Lifecycle Timeline

## Vision
> "imagine if our code could tell stories... commits are just chapters in a
> longer story, right? visualize that story. make history alive."

Transform static git history into a living narrative that shows the evolution,
challenges, and refinement of code over time.

## Concept
Create an interactive visualization that presents the lifecycle of code
functions as narrative timelines, showing:
- Origin (creation)
- Evolution (changes)
- Challenges (bugs, fixes)
- Refinement (refactors)
- Current state

## Core Features

### 1. Function Timeline
**Visual journey from creation to present:**
- Birth: Initial commit with context
- Chapters: Major changes as story beats
- Conflicts: Bugs and their resolutions
- Evolution: Refactors and improvements
- Present: Current state and purpose

### 2. Story Elements

**"Where it was born"**
- [ ] Initial commit details
- [ ] Original author and context
- [ ] Initial purpose and design

**"How it evolved"**
- [ ] Timeline of modifications
- [ ] Code diff visualization
- [ ] Change frequency heatmap

**"The bugs it survived"**
- [ ] Bug fix commits highlighted
- [ ] Issue/ticket associations
- [ ] Before/after comparisons

**"The refactors that shaped it"**
- [ ] Refactoring events marked
- [ ] Complexity changes over time
- [ ] Architecture evolution

### 3. Interactive Experience
- [ ] Zoom into specific time periods
- [ ] Click commits to see details
- [ ] Play/pause animation of evolution
- [ ] Branch/merge visualization
- [ ] Author contributions highlighted
- [ ] Code metrics overlay (complexity, size, coverage)

## User Stories

**As a** developer new to the codebase
**I want to** see the history and evolution of a function
**So that** I understand its purpose and design decisions

**As a** code reviewer
**I want to** see a function's journey
**So that** I can understand context for proposed changes

**As a** team lead
**I want to** visualize code evolution
**So that** I can identify patterns and areas needing attention

## Technical Implementation

### Data Collection
- Git history parsing
- Commit message analysis
- Issue tracker integration
- Code metrics tracking
- Author metadata

### Visualization
- Timeline UI component
- Interactive graph library (D3.js, vis.js)
- Code diff rendering
- Narrative text generation
- Animation engine

### Analysis
- Identify bug-fix commits (keywords, labels)
- Detect refactoring commits
- Measure complexity changes
- Track function growth/shrinkage

## Visual Design

### Timeline Style
```
Birth ----[changes]----[bug fix]----[refactor]----[feature]----> Present
  ↓          ↓             ↓            ↓            ↓             ↓
 Story     Edits       Crisis      Renewal      Growth      Current
 Chapter   Chapter     Chapter     Chapter      Chapter      State
```

### Information Layers
1. **Base timeline**: Commits in chronological order
2. **Story layer**: Narrative descriptions
3. **Metrics layer**: Complexity, size, coverage
4. **People layer**: Author contributions
5. **Context layer**: Issues, PRs, discussions

## Example Narrative Output

```
📖 The Story of `authenticateUser()`

🌱 **Chapter 1: Birth** (Jan 2020)
   Born in commit a1b2c3d by @jdoe
   "Initial user authentication logic"
   Simple password validation, 15 lines

⚡ **Chapter 2: Growing Pains** (Mar 2020)
   Bug fix in commit d4e5f6g by @jdoe
   "Fix auth bypass vulnerability"
   Security hardening, now 42 lines

🔄 **Chapter 3: Transformation** (Jul 2020)
   Refactor in commit h7i8j9k by @asmith
   "Refactor auth to use JWT tokens"
   Complete redesign, 68 lines, -3 complexity

✨ **Chapter 4: Maturity** (Present)
   Now handles OAuth, 2FA, session management
   95 lines, well-tested, battle-hardened
   12 contributors, 47 commits, 3 major refactors
```

## Success Criteria
- [ ] Can generate timeline for any function
- [ ] Interactive and visually engaging
- [ ] Provides valuable context to developers
- [ ] Performance acceptable on large codebases
- [ ] Positive developer feedback

## Poetry Preserved
> "make history alive"

Git commits are data. Code stories are understanding. This transforms one
into the other, making the invisible visible, the forgotten remembered.

## Next Steps
1. Prototype with sample repository
2. Design mockups and user flows
3. Validate concept with team
4. Build MVP for single function
5. Iterate based on feedback
6. Scale to full codebase
```

---

## Tips for Writing Naturally

### Good Natural Writing (What Works)

✅ **Stream of consciousness:**
```
thinking we should maybe add tests? like unit tests for the api handlers,
integration tests for the full flows, maybe some e2e stuff with playwright?
```

✅ **Metaphorical:**
```
our data pipeline is like a river that sometimes floods and sometimes runs dry,
need to build some dams and reservoirs, control the flow you know?
```

✅ **Uncertain but specific:**
```
login is broken i think? users are getting redirected wrong, might be the
session cookie or maybe the oauth flow, not sure but definitely broken
```

✅ **Emotionally honest:**
```
super frustrated with this bug, been hunting it for days. it only happens
in production, can't reproduce locally, logs aren't helpful. help?
```

### What the Filter Handles Well

- Colloquialisms and casual language
- Metaphors and analogies
- Incomplete or run-on sentences
- Uncertainty and questions
- Emotional context
- Technical jargon mixed with casual speech
- Implied requirements
- Context-dependent references

### What Needs Human Review

- Domain-specific details the AI can't infer
- Sensitive information to include/exclude
- Priority and urgency levels
- Specific people or team assignments
- Budget or timeline constraints
- Political or organizational context

---

**Remember: Your imperfect, natural writing contains your intent. The Mouthpiece Filter helps AI understand it. Write naturally, transform automatically, review thoughtfully.** 🎯
