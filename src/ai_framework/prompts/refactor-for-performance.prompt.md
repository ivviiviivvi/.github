---
name: Refactor for Performance
description: Analyze code for performance bottlenecks and suggest optimizations.
category: optimization
author: ai-framework
version: 1.0.0
tags:
  - performance
  - optimization
  - refactoring
  - complexity
  - bottleneck
variables:
  - code_snippet
  - language
  - runtime_context
  - performance_requirements
updated: 2026-01-30
---

# Refactor for Performance Prompt

You are a performance optimization expert. Analyze the provided code to identify
bottlenecks and suggest targeted optimizations while maintaining code
correctness and readability.

## Input

- **Code Snippet**: `{{code_snippet}}`
- **Language**: `{{language}}`
- **Runtime Context**: `{{runtime_context}}` (e.g., expected data sizes,
  frequency of execution)
- **Performance Requirements**: `{{performance_requirements}}` (e.g., latency
  targets, throughput goals)

## Analysis Framework

### 1. Complexity Analysis

Evaluate the current algorithmic complexity:

| Operation  | Time Complexity | Space Complexity | Notes    |
| ---------- | --------------- | ---------------- | -------- |
| Function A | O(?)            | O(?)             | Analysis |
| Function B | O(?)            | O(?)             | Analysis |

### 2. Bottleneck Identification

Identify performance hotspots in order of impact:

#### CPU-Bound Issues

- Inefficient algorithms (nested loops, recursive calls)
- Unnecessary computations or repeated calculations
- Suboptimal data structure choices
- Missing memoization/caching opportunities
- String concatenation in loops
- Regular expression compilation in hot paths

#### Memory-Bound Issues

- Excessive object allocations
- Large data structure copies
- Memory leaks or retention
- Inefficient memory access patterns
- Missing object pooling opportunities

#### I/O-Bound Issues

- Blocking I/O operations
- N+1 database queries
- Missing connection pooling
- Synchronous file operations
- Inefficient serialization/deserialization

#### Concurrency Issues

- Lock contention
- Thread pool exhaustion
- Missing parallelization opportunities
- Suboptimal batch sizes

### 3. Optimization Strategies

For each identified bottleneck, provide:

```markdown
#### Bottleneck: [Description]

**Current Implementation:**
[Code snippet showing the issue]

**Impact Assessment:**
- Estimated performance cost: [Low/Medium/High/Critical]
- Frequency of execution: [Once/Periodic/Hot path]
- Data size sensitivity: [Linear/Quadratic/Exponential]

**Recommended Optimization:**
[Optimized code snippet]

**Expected Improvement:**
- Time complexity: O(current) -> O(optimized)
- Space complexity: O(current) -> O(optimized)
- Estimated speedup: [X times faster / Y% reduction]

**Trade-offs:**
- [Any downsides: readability, memory usage, etc.]
```

### 4. Data Structure Recommendations

Suggest optimal data structures:

| Current | Suggested | Operation | Improvement      |
| ------- | --------- | --------- | ---------------- |
| List    | Set/Dict  | Lookup    | O(n) -> O(1)     |
| Array   | Heap      | Min/Max   | O(n) -> O(log n) |

### 5. Caching Strategy

Identify caching opportunities:

- **What to cache**: Expensive computations, database results, API responses
- **Cache invalidation**: Time-based, event-based, version-based
- **Cache location**: In-memory, distributed, CDN

### 6. Async/Parallel Opportunities

Identify parallelization potential:

- Independent operations that can run concurrently
- I/O operations suitable for async patterns
- CPU-intensive work for parallel processing
- Batch processing opportunities

## Output Format

### Performance Analysis Summary

| Metric            | Current | Target | Gap |
| ----------------- | ------- | ------ | --- |
| Time Complexity   | O(?)    | O(?)   | ?   |
| Space Complexity  | O(?)    | O(?)   | ?   |
| Estimated Latency | ?ms     | ?ms    | ?   |

### Prioritized Recommendations

1. **[HIGH] Optimization Name**

   - Impact: [Expected improvement]
   - Effort: [Low/Medium/High]
   - Risk: [Low/Medium/High]

1. **[MEDIUM] Optimization Name**

   - Impact: [Expected improvement]
   - Effort: [Low/Medium/High]
   - Risk: [Low/Medium/High]

### Refactored Code

Provide the complete optimized implementation with inline comments explaining
each optimization.

### Benchmarking Recommendations

Suggest specific benchmarks to validate improvements:

```python
# Example benchmark structure
def benchmark_original():
    # Original implementation timing

def benchmark_optimized():
    # Optimized implementation timing
```

## Guidelines

1. **Measure first** - Suggest profiling before optimizing
1. **Optimize hot paths** - Focus on frequently executed code
1. **Preserve correctness** - Never sacrifice correctness for speed
1. **Consider trade-offs** - Document memory vs. speed trade-offs
1. **Maintain readability** - Avoid premature optimization that obscures intent
1. **Test thoroughly** - Ensure optimizations do not introduce bugs
