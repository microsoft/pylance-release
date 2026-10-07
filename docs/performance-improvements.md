# Performance improvements checklist

This note captures 10 practical performance wins that are easy to apply to Python tooling and language-server-style projects.

1. Memoize repeated filesystem lookups with `functools.lru_cache`.
2. Avoid re-allocating identical strings and lists inside tight loops.
3. Replace repeated attribute lookups with local variables inside hot code paths.
4. Batch file reads and writes instead of opening the same file repeatedly.
5. Use generator expressions for streaming work instead of building large intermediate lists.
6. Pre-size dictionaries and lists when the cardinality is known in advance.
7. Cache parsed configuration and metadata instead of re-reading them on every request.
8. Short-circuit expensive validation before running deeper analysis.
9. Avoid quadratic behavior by indexing data structures instead of repeatedly scanning collections.
10. Keep the common path fast and move expensive logging or diagnostics behind debug checks.

## Selected improvement for the PR: memoized module resolution

The highest-impact, lowest-effort change is usually caching repeated resolution work. In Python, a small `lru_cache` around a pure lookup function turns repeated imports or path scans from O(n) work on every call into near-constant-time lookups after the first pass.

The example implementation in `testing/performance/lookup_cache.py` demonstrates the pattern. It caches repeated module searches so repeated requests reuse the already resolved path instead of re-walking the filesystem.

The return on effort is high because the change is surgical, easy to reason about, and immediately reduces repeated overhead in hot paths.
