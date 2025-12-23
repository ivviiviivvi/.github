# Bolt's Journal

## 2024-05-22 - [Optimization] Premature Regex Compilation
**Learning:** In Python, `re.findall(pattern, string)` internally caches compiled regex objects. Pre-compiling regexes (`re.compile(pattern)`) for a small set of constant patterns provided NO performance benefit (and was negligibly slower) in a benchmark of 5000 iterations.
**Action:** Do not refactor for `re.compile` unless using `re.VERBOSE` for readability or if patterns are dynamically generated/evicted from cache.

## 2024-05-22 - [Anti-Pattern] Unnecessary Sleep in Local Loops
**Learning:** Found a `time.sleep(0.3)` inside a loop iterating over API results (`analyze_repository_health`), but the loop body performs NO network requests (only local data processing). This artificially slows down the script by 0.3s per repository (30s for 100 repos) for no reason.
**Action:** Always verify if a loop actually performs I/O before adding rate-limiting sleeps.

## 2025-12-20 - [Optimization] Efficient String Construction
**Learning:** In `scripts/ecosystem_visualizer.py`, identified the use of inefficient string concatenation (`+=`) in loops, which also led to `UnboundLocalError` due to undefined variables.
**Action:** Replaced string concatenation with list accumulation (`parts.append()`) and `''.join()`. This is the preferred method in Python for building large strings, avoiding quadratic time complexity associated with repeated string copying.
