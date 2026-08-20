---
name: False Positive Report
about: Report a TorusGuard rule that incorrectly flagged safe code
title: '[False Positive]: '
labels: ['false-positive', 'rules']
assignees: ''
---

### Rule ID
<!-- e.g. TG-SSRF-001, TG-CACHE-001, TG-AUTH-006 -->

### Finding Classification
- Current Severity: [Critical / High / Medium / Low / Info]
- Confidence Assigned: [Confirmed / Likely / Manual review]

### Why is this Result Incorrect?
<!-- Explain why the flagged code is actually safe or mitigated by other controls. -->

### Relevant Stack & Framework
<!-- e.g. Express 4.19, Next.js 14 App Router, FastAPI 0.110, Supabase, Prisma -->

### Reproduction Steps
1. Include the snippet below in a project.
2. Run `/torusguard audit` or `/torusguard check <area>`.
3. Observe finding triggered for the safe pattern.

### Sanitized Sample Code (Safe Pattern Flagged as Unsafe)
```javascript
// Paste sanitized code snippet here (fake data and placeholders only)
```

### Suggested Refinement
<!-- How should the rule detection or false-positive exceptions section be updated? -->
