# How to Use Glob Patterns in Extra Paths with Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) resolves imports by searching a list of directories you provide through [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md) (and the equivalent `extraPaths` entries in `pyrightconfig.json` / `pyproject.toml`). In large repositories — especially generated dependency trees like Bazel's `rules_python` output — that list can grow to hundreds of nearly identical entries that must be kept in sync by hand.

Glob patterns let you describe those directories with a wildcard instead of listing each one. This guide explains the wildcard syntax, the **deterministic** order in which matches are added, how to configure it, what you see in the editor, and the performance trade-offs to keep in mind.

> **Note**: Earlier versions of Pylance did **not** support wildcards in `extraPaths`, because a naïve glob would make import order depend on filesystem enumeration (non-deterministic) and could silently slow down every import lookup. Glob support removes both problems: expansion is fully deterministic (see [Deterministic Ordering and Precedence](#deterministic-ordering-and-precedence)) and happens once when configuration loads. The performance cost is still real for very broad globs — see [Performance and Memory Considerations](#performance-and-memory-considerations).

---

## Table of Contents

- [How Glob Extra Paths Work](#how-glob-extra-paths-work)
- [Glob Syntax](#glob-syntax)
- [Deterministic Ordering and Precedence](#deterministic-ordering-and-precedence)
- [Configuring Glob Extra Paths](#configuring-glob-extra-paths)
- [What You See in Pylance](#what-you-see-in-pylance)
- [Performance and Memory Considerations](#performance-and-memory-considerations)
- [How Glob Extra Paths Work for Copilot and AI Tools](#how-glob-extra-paths-work-for-copilot-and-ai-tools)
- [Edge Cases and Special Behavior](#edge-cases-and-special-behavior)
- [Diagnostic Checklist](#diagnostic-checklist)
- [FAQ](#faq)
- [Related Guides](#related-guides)

---

## How Glob Extra Paths Work

An `extraPaths` list is an **ordered** set of import search roots. When you use a wildcard in an entry, Pylance treats that entry as a **glob** and expands it, _in place_, to every directory that matches — then continues resolving imports using the resulting concrete list.

- A **literal entry** (no wildcard) behaves exactly as before: it is a single search root, kept at its position in the list, and is not required to exist.
- A **glob entry** (contains `*`, `**`, or `?`) is replaced, at its position, by the directories it matches, sorted into a stable order.

Only **directories** are matched — a glob never adds a file as a search root. Expansion happens once, when your configuration is loaded (at startup and whenever the relevant settings or config file change), not on every import.

This applies to every source of extra paths:

- The [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md) VS Code setting
- The top-level `extraPaths` in `pyrightconfig.json` / `pyproject.toml`
- Each execution environment's `extraPaths` (see [Monorepo Setup — Execution Environments](monorepo-setup.md#execution-environments))

---

## Glob Syntax

Glob entries use the same wildcard syntax as `include`, `exclude`, and `ignore`:

| Wildcard | Matches                                                     | Example                     |
| -------- | ----------------------------------------------------------- | --------------------------- |
| `*`      | Any sequence of characters **within a single path segment** | `libs/*/src`                |
| `**`     | Any number of path segments, including none (recursive)     | `external/**/site-packages` |
| `?`      | A single character                                          | `pkg_31?/site-packages`     |

Relative globs resolve from the same base directory as literal extra paths: the **workspace root** for the VS Code setting, or the **config file's directory** for `pyrightconfig.json` / `pyproject.toml`. Path variables such as `${workspaceFolder}` are substituted first, then the glob is expanded (see [What You See in Pylance](#what-you-see-in-pylance)).

---

## Deterministic Ordering and Precedence

Because `extraPaths` is order-sensitive (the first matching root wins during import resolution), glob expansion is designed to produce the **same ordered list on every machine**, regardless of how the filesystem enumerates directories.

Two rules govern the result:

1. **Sort within a glob.** The directories a single glob matches are inserted at that glob's position, sorted in **ascending order** by their resolved path. The comparison is case-sensitive and **ordinal** (it compares Unicode code points and normalizes to NFC), so it never depends on your locale, language, or operating system — Windows, macOS, and Linux produce an identical order.
2. **Precedence on duplicates.** When the same directory would appear more than once, the winner is chosen by this priority:
    - **An explicit (literal) entry always wins** and keeps _its own_ position — even if a glob earlier in the list also matched that directory.
    - **Among globs, the earlier glob wins.**
    - A duplicate contributed by the loser is dropped. Two identical literal entries keep the first occurrence.

### Worked examples

The first two examples use this directory layout:

```text
libs/
├── auth/src/
├── core/src/
└── shared/src/
```

**Single glob** — `["libs/*/src"]`
Expands to every matching directory, sorted ascending:

```text
libs/auth/src
libs/core/src
libs/shared/src
```

**Literal plus a glob that covers it** — `["libs/shared/src", "libs/*/src"]`
`libs/shared/src` is a literal entry and keeps its position at the front. `libs/*/src` also matches `libs/shared/src`, but that copy is dropped because the literal entry already owns the path. Result:

```text
libs/shared/src
libs/auth/src
libs/core/src
```

**Two globs that overlap** — over a tree containing `external/pip310_numpy/site-packages`, `external/pip310_pandas/site-packages`, and `external/pip311_numpy/site-packages`, with `["external/pip310_*/site-packages", "external/pip3??_numpy/site-packages"]`:
Both globs match `external/pip310_numpy/site-packages`. The earlier glob keeps it; the later glob drops that overlap. Result:

```text
external/pip310_numpy/site-packages     ← first glob
external/pip310_pandas/site-packages    ← first glob
external/pip311_numpy/site-packages     ← second glob (pip310_numpy already taken)
```

**Multiple literals mixed with multiple globs** — this is the common real-world shape. Given this tree:

```text
stubs/
packages/
├── api/src/
├── auth/src/
├── core/src/
└── shared/src/
vendor/
├── grpc/python/
├── legacy/python/
└── proto/python/
```

and this configuration:

```json
{
    "python.analysis.extraPaths": [
        "stubs",
        "packages/core/src",
        "packages/*/src",
        "vendor/proto/python",
        "vendor/*/python"
    ]
}
```

Pylance processes each entry at its position, expanding globs in place and dropping any directory already owned by an explicit entry:

| #   | Entry                 | Contributes                                                                                                   |
| --- | --------------------- | ------------------------------------------------------------------------------------------------------------- |
| 1   | `stubs`               | `stubs` (literal)                                                                                             |
| 2   | `packages/core/src`   | `packages/core/src` (literal — kept here, ahead of the glob below)                                            |
| 3   | `packages/*/src`      | `packages/api/src`, `packages/auth/src`, `packages/shared/src` (sorted; `core` dropped — the literal owns it) |
| 4   | `vendor/proto/python` | `vendor/proto/python` (literal — kept here, ahead of the glob below)                                          |
| 5   | `vendor/*/python`     | `vendor/grpc/python`, `vendor/legacy/python` (sorted; `proto` dropped — the literal owns it)                  |

Final resolved order:

```text
stubs
packages/core/src
packages/api/src
packages/auth/src
packages/shared/src
vendor/proto/python
vendor/grpc/python
vendor/legacy/python
```

Notice that `packages/core/src` and `vendor/proto/python` appear at **their own positions** (2 and 6), not inside the sorted block of the glob that also matched them — an explicit entry always keeps the slot where you wrote it.

**Literal _after_ a glob keeps its own (later) slot** — position is authoritative. If you reorder the first pair to put the literal last, `["packages/*/src", "packages/core/src"]`, the result is:

```text
packages/api/src
packages/auth/src
packages/shared/src
packages/core/src
```

The glob expands first (sorted, without `core`, because the explicit `packages/core/src` owns that path), then `packages/core/src` appears at the end where you placed it — so a literal can "pull" its directory out of a glob's sorted block to a later position.

### The Bazel case

A Bazel `rules_python` tree produces one directory per dependency, e.g. `external/rules_python~~pip~pip_310_<name>/site-packages`. Instead of hundreds of literal entries, one glob covers them all deterministically:

```json
{
    "python.analysis.extraPaths": ["external/rules_python~~pip~pip_310_*/site-packages"]
}
```

Every matching `site-packages` directory is added, sorted ascending, and the list is identical for every developer who checks out the repository.

---

## Configuring Glob Extra Paths

Glob entries work everywhere a literal `extraPaths` entry works. Mix literals and globs freely — literals keep their position, globs expand around them.

**VS Code settings (`.vscode/settings.json`)** — resolved from the workspace root:

```json
{
    "python.analysis.extraPaths": ["./src", "./packages/*/src", "external/rules_python~~pip~pip_310_*/site-packages"]
}
```

**`pyrightconfig.json`** — resolved from the config file's directory:

```json
{
    "extraPaths": ["libs/*/src", "generated/**/python"]
}
```

**`pyproject.toml`**:

```toml
[tool.pyright]
extraPaths = ["libs/*/src", "generated/**/python"]
```

**Per–execution environment** — each environment's `extraPaths` overrides (does not merge with) the global list, and is expanded independently:

```jsonc
// pyrightconfig.json
{
    "executionEnvironments": [
        { "root": "packages/api", "extraPaths": ["packages/*/src"] },
        { "root": "packages/worker", "extraPaths": ["packages/*/src", "vendor/**/python"] },
    ],
}
```

> **Tip**: Point globs at the directory that should be **on the import path** (the parent of the top-level package), just like literal extra paths. See [Extra Paths — path specifications](../settings/python_analysis_extraPaths.md).

---

## What You See in Pylance

Because Pylance is the language server you interact with, glob expansion surfaces in a few places:

- **The resolved paths appear in the log.** Enable [`"python.analysis.logLevel": "Trace"`](../settings/python_analysis_logLevel.md) and open **Output → Pylance**. Each expanded directory is logged as an individual, fully resolved `Looking in extraPath '...'` line during import resolution — so you can confirm exactly which directories a glob produced and in what order. See [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md).
- **A glob that matches nothing is silent.** It contributes zero entries and is not an error. If an import is unresolved, check the log to see whether the glob expanded to the directories you expected.
- **Restart after configuration changes.** Expansion runs when configuration loads. After editing `extraPaths` (or adding/removing directories a glob covers), run **Python: Restart Language Server** to force re-expansion.
- **The config-vs-settings rule still applies.** If a `pyrightconfig.json` / `pyproject.toml` exists, its `extraPaths` takes precedence and the VS Code [`python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md) setting is ignored (Pylance shows the usual _"python.analysis.extraPaths cannot be set when a pyrightconfig.json or pyproject.toml is being used"_ warning). Put your globs where your other `extraPaths` live.
- **Variables expand first.** `${workspaceFolder}` and the other supported path variables are substituted before the glob is matched, so `"${workspaceFolder:shared}/packages/*/src"` works as expected.
- **Very broad globs are flagged.** If expanding a single glob has to walk an unusually large directory tree (more than ~10,000 directories), Pylance writes a one-time warning to **Output → Pylance** suggesting you narrow the pattern. Expansion still completes; treat the warning as a prompt to scope the glob.

---

## Performance and Memory Considerations

Every directory a glob expands to becomes a real import search root **and** a file-watch root. A broad glob that matches hundreds of directories therefore has a measurable cost, and this is the main thing to tune.

**What costs what:**

- **Import lookups.** Each unresolved import is checked against every extra path in order. More expanded roots means more directories to probe per lookup. A tightly scoped glob (`external/rules_python~~pip~pip_310_*/site-packages`) is far cheaper than a greedy one (`**/site-packages`).
- **File watching.** Each expanded root is watched for changes so analysis stays current. Hundreds of watched roots increase watcher overhead and memory.
- **Symbol search.** If you enable [`includeExtraPathSymbolsInSymbolSearch`](../settings/python_analysis_includeExtraPathSymbolsInSymbolSearch.md), workspace symbol search also scans expanded extra-path directories, which grows with the number of matches.

**Mitigations:**

- **Be specific.** Prefer the narrowest glob that matches what you need. Anchor it to a known prefix and avoid a leading `**` when a fixed segment works.
- **Scope with execution environments.** Put per-subtree globs in [`executionEnvironments`](monorepo-setup.md#execution-environments) so a file only pays for the roots relevant to its subtree, rather than one giant global list.
- **Reduce watching if you don't need live updates.** Exclude generated dependency trees from file watching (for example via VS Code's `files.watcherExclude`) when they don't change during a session; expansion still resolves imports, you just stop watching those roots for changes.
- **Combine with performance presets.** For very large repositories, pair glob extra paths with the guidance in [How to Tune Pylance Performance](performance-tuning.md) and the monorepo presets in [Monorepo Setup — Performance Tuning](monorepo-setup.md#performance-tuning-for-monorepos) (`languageServerMode`, `diagnosticMode`, indexing controls).

> For complete performance guidance (language server mode, indexing, heap limits, presets), see [How to Tune Pylance Performance](performance-tuning.md). This section covers the extra-paths-specific cost.

> **Pylance warns when a glob walks a very large tree.** If expanding a single glob scans more than ~10,000 directories, a one-time warning appears in **Output → Pylance**. It does not stop expansion, but it is a strong signal to narrow the pattern (anchor it to a fixed prefix and avoid a bare `**` at a large root) or to move it into an execution environment.

---

## How Glob Extra Paths Work for Copilot and AI Tools

GitHub Copilot and other AI tools reason about your project through the same resolved import paths Pylance uses. The key property they can rely on is the **deterministic contract**:

- Given the same directory tree, a glob always expands to the **same ordered list** of search roots on every machine — there is no hidden dependence on filesystem order.
- Precedence is stable: an explicit entry always wins over a glob-discovered duplicate, and an earlier glob wins over a later one.
- The winning root for any importable module is therefore reproducible. When Copilot suggests or fixes an import, the module it points at is the one Pylance would resolve — not a guess that might differ between checkouts.

If you use [Pylance's MCP tools with Copilot](copilot-pylance-workflow.md), the resolved (expanded) extra paths are what those tools see, so their answers reflect the same order described in [Deterministic Ordering and Precedence](#deterministic-ordering-and-precedence).

---

## Edge Cases and Special Behavior

| Case                                   | Behavior                                                                                                                                          |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Glob matches no directory              | Contributes nothing; not an error. Check the Trace log to confirm what expanded.                                                                  |
| Glob matches a file                    | Ignored — only directories become search roots.                                                                                                   |
| Empty or whitespace-only entry         | Ignored (an empty entry would otherwise resolve to the project root and silently pollute the search path).                                        |
| Duplicate via a literal entry          | The literal wins and keeps its own position; the glob-discovered copy is dropped.                                                                 |
| Duplicate across two globs             | The earlier glob wins; the later glob drops the overlap.                                                                                          |
| Two entries differ only in letter case | Treated as **distinct** roots (case-sensitive), because case affects the resolved module name. Both survive even on case-insensitive filesystems. |
| Symbolic links                         | Not resolved — the matched path is used as-is so it maps to the intended module name. Symlink cycles are guarded against during expansion.        |
| Execution environment `extraPaths`     | Overrides (does not merge with) the global `extraPaths`; expanded independently per environment.                                                  |
| `.pth` files and auto-detected `src/`  | Unchanged. These conveniences still apply where they did before and operate on the expanded directories; globbing does not alter that behavior.   |

---

## Diagnostic Checklist

When a glob-based `extraPaths` isn't resolving imports as expected:

- [ ] **Correct location**: Are your `extraPaths` in the file that takes effect? A `pyrightconfig.json` / `pyproject.toml` overrides the VS Code setting.
- [ ] **Restarted**: Did you run **Python: Restart Language Server** after editing the glob or changing the directories it covers?
- [ ] **Expanded as expected**: With `"python.analysis.logLevel": "Trace"`, does **Output → Pylance** show the directories you expected as `Looking in extraPath '...'` lines?
- [ ] **Right level**: Does the glob point at the import root (the parent of the top-level package), not one level too high or too low?
- [ ] **Order**: If the wrong copy of a module resolves, check ordering — an explicit entry or an earlier glob may be winning. See [Deterministic Ordering and Precedence](#deterministic-ordering-and-precedence).
- [ ] **Scope/perf**: Is the glob broader than it needs to be? Narrow it or move it into an execution environment.

---

## FAQ

### Q: Weren't wildcards unsupported in `extraPaths`?

They were, for two reasons: a naïve glob made import order non-deterministic, and broad globs could silently slow every import lookup. Glob support addresses both — expansion is fully deterministic (sorted, with stable precedence) and happens once at configuration load. The lookup cost is still real for very broad globs, which is why [Performance and Memory Considerations](#performance-and-memory-considerations) matters.

### Q: Is the expansion order the same on every machine?

Yes. Matches are sorted with a case-sensitive, platform-independent comparison, and precedence (explicit > earlier glob > later glob) is fixed. The same tree yields the same ordered list on Windows, macOS, and Linux.

### Q: Will this slow Pylance down?

Only in proportion to how many directories your globs expand to. A specific glob is cheap; a greedy one like `**/site-packages` can add many roots to every import lookup and file-watch. Keep globs narrow and consider execution environments — see [Performance and Memory Considerations](#performance-and-memory-considerations).

### Q: Do globs work in `pyrightconfig.json` and `pyproject.toml`, not just VS Code settings?

Yes — globs are supported in every source of extra paths, including per–execution-environment `extraPaths`. Config-file entries resolve relative to the config file's directory.

### Q: Can I mix literal paths and globs?

Yes. Literals keep their exact position; globs expand around them. If a glob rediscovers a literal path, the literal wins and keeps its position.

### Q: A glob matches nothing — is that an error?

No. It simply contributes no entries. Use Trace logging to see what a glob expanded to.

### Q: How do I see exactly which directories a glob added?

Enable `"python.analysis.logLevel": "Trace"` and read **Output → Pylance**; each expanded directory appears as a `Looking in extraPath '...'` line. See [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md).

---

## Related Guides

- [How to Set Up a Python Monorepo with Pylance](monorepo-setup.md) — extra paths, execution environments, and multi-package layouts
- [How to Fix Unresolved Import Errors in Pylance](unresolved-imports.md) — when imports don't resolve at all
- [How to Read Pylance Import Resolution Logs](reading-pylance-logs.md) — trace logging, search order, and log interpretation
- [How to Tune Pylance Performance](performance-tuning.md) — language server mode, indexing, heap limits, and presets
- [How to Troubleshoot Pylance Settings](settings-troubleshooting.md) — setting precedence and config file overrides
- [Understanding `python.analysis.extraPaths`](../settings/python_analysis_extraPaths.md) — the extra paths setting reference

---

_For more information on Pylance settings and customization, refer to the **[Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference)** documentation._

---

_This document was generated with the assistance of AI and has been reviewed by humans for accuracy and completeness._
