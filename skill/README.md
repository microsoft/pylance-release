# Pylance / Pyright Type-Checking Skills

A package of Claude Code skills for Python type checking with **Pylance** and **Pyright**. This repo is the `pylance-release` docs corpus, so every skill here is a thin, triggered entry point that **links into the real documentation** under [`../docs/`](../docs/INDEX.md) rather than duplicating it. Read the skill, then follow the relative links to the authoritative page.

## Skills

| Skill | Use when |
| ----- | -------- |
| [pylance-type-checking-setup](pylance-type-checking-setup/SKILL.md) | Configuring strictness/scope: `typeCheckingMode`, `diagnosticSeverityOverrides`, `languageServerMode`, `pyrightVersion`, config-file precedence |
| [pylance-import-resolution](pylance-import-resolution/SKILL.md) | `Import "..." could not be resolved`, missing stubs, `extraPaths`/`stubPath`/`useLibraryCodeForTypes`, editable installs, interpreter selection |
| [pylance-diagnostics-triage](pylance-diagnostics-triage/SKILL.md) | Decoding or suppressing a specific `report*` rule; `# pyright: ignore` / `# type: ignore`; per-rule severity |
| [pylance-strict-migration](pylance-strict-migration/SKILL.md) | Moving from `off`/`basic` to `strict` incrementally; per-file/per-directory strict; quieting `reportUnknown*` |
| [pylance-type-system-patterns](pylance-type-system-patterns/SKILL.md) | Authoring typing: type narrowing, `TypeGuard`/`TypeIs`, generics/`TypeVar`, `Protocol`, `TypedDict`, `Literal`, overloads, overrides |
| [pylance-workspace-perf](pylance-workspace-perf/SKILL.md) | `diagnosticMode` (open files vs workspace), `include`/`exclude`/`ignore`, monorepo setup, performance/memory, logs, notebooks, remote |
| [pylance-type-server-protocol](pylance-type-server-protocol/SKILL.md) | Building tooling that speaks the Type Server Protocol (`typeServer/*` JSON-RPC) |

The authoritative master index of all docs is [`../docs/INDEX.md`](../docs/INDEX.md).

## Installation / discovery

Claude Code auto-discovers skills from `~/.claude/skills/` (user) or `.claude/skills/` (project). To install this package for your user, symlink each skill directory into `~/.claude/skills/`:

```bash
REPO=/opt/repo/pylance-agent-skill
for s in "$REPO"/skill/pylance-*; do
  ln -sf "$s" "$HOME/.claude/skills/$(basename "$s")"
done
```

Because the symlinks point at `skill/` in this repo, the `SKILL.md` relative links (`../../docs/...`) keep resolving to the authoritative doc pages here. If you move or delete this repo, the links break — in that case copy each `skill/<name>` directory into `~/.claude/skills/<name>` instead and adjust the `../../docs/...` paths to absolute or repo-relative.

## Conventions used in these skills

- Bodies stay lean (progressive disclosure). Deeper detail lives in the linked doc pages.
- Relative links to in-repo docs are written from the skill's `SKILL.md`: `../../docs/...` (two levels up to the repo root) and `../docs/...` from this `README.md`.
- The deprecated root file `DIAGNOSTIC_SEVERITY_RULES.md` is **not** used as a rule source; the live rule set is `docs/diagnostics/` plus the mode table in `docs/settings/python_analysis_typeCheckingMode.md`.
