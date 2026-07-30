# Pylance Type-Checking Skill

A [Claude Code](https://docs.claude.com/en/docs/claude-code) skill that helps you **write Python code that passes Pylance/Pyright type checking** — adding type annotations, fixing `report*` diagnostics in the source, applying type narrowing, using `TYPE_CHECKING` imports and type stubs, and suppressing with `# pyright: ignore`.

This skill is about the Python source you produce. It does **not** cover editor/CI configuration (`.vscode/settings.json`, `pyrightconfig.json`, `languageServerMode`, GitHub Actions) — for that, see the [Pylance settings docs](https://github.com/microsoft/pylance-release/tree/main/docs/settings) and [how-to guides](https://github.com/microsoft/pylance-release/tree/main/docs/howto).

Distilled from the official Pylance documentation in the [pylance-release](https://github.com/microsoft/pylance-release) repo.

## What's inside

```
pylance-type-checking/
├── SKILL.md                         # main entry — quick reference + decision flow + write-to conventions
├── README.md                       # this file
└── references/
    ├── type-checking-levels.md     # off/basic/standard/strict: what each catches + write-toward guidance + per-file overrides
    ├── fixing-type-errors.md       # problem→fix pairs for common report* diagnostics (in the code)
    ├── type-narrowing.md           # isinstance, is None, TypeGuard/TypeIs, narrowing gotchas
    ├── typed-imports-and-stubs.md  # types-* stubs, TYPE_CHECKING imports, py.typed, .pyi stubs
    └── diagnostics-reference.md    # compact lookup table of all report* rules
```

## Install

### Option A: Copy into your personal skills directory

Copy (or symlink) this folder into your Claude Code skills directory:

```bash
# macOS / Linux
cp -R pylance-type-checking ~/.claude/skills/

# or symlink (stays in sync if you clone/update the repo)
ln -s "$(pwd)/pylance-type-checking" ~/.claude/skills/pylance-type-checking
```

### Option B: Install for a single project

Copy into the project's `.claude/skills/`:

```bash
mkdir -p .claude/skills
cp -R pylance-type-checking .claude/skills/
```

Restart Claude Code (or reload the session) after installing. The skill appears as `pylance-type-checking` and is auto-suggested when you ask about Python type annotations, narrowing union/optional types, resolving Pylance/Pyright `report*` errors, or what level of type checking to write toward.

## Usage

Just ask naturally — the skill triggers on relevant prompts:

- "Write a function that takes `str | None` and returns `str`, type-safe."
- "Fix this Pylance `reportOptionalMemberAccess` error."
- "How do I narrow `str | None`?"
- "What does strict mode require me to annotate?"
- "Add type stubs / annotations so this import stops reporting `Unknown`."

You can also invoke it directly with `/pylance-type-checking` (Claude Code slash command).

## Source

Distilled from the official Pylance documentation: <https://github.com/microsoft/pylance-release/tree/main/docs>. For full detail on any topic, the references link back to the original docs.
