# SCENARIO: inspect an import-resolution diagnostic in the Problems view
# TARGET: `unknownModule` on the import line below
# TRIGGER: Run `View: Focus Problems` from the Command Palette after this file is analyzed
# EXPECT: Pylance has already published diagnostics for this file, including an editor squiggle on `unknownModule`
# VERIFY: the Problems view contains a diagnostic for the unresolved `unknownModule` import, and the editor still shows the squiggle on that token
# RECOVER: leave file text unchanged; close or move focus away from the Problems view before the next scenario

# SCENARIO: confirm the import error remains visible in the editor
# TARGET: `unknownModule` on the import line below
# TRIGGER: inspect the line after analysis completes
# EXPECT: `unknownModule` is marked as an unresolved import
# VERIFY: the import line shows a diagnostic squiggle on `unknownModule`
# RECOVER: leave file text unchanged
import unknownModule

# SCENARIO: confirm an unknown-identifier diagnostic is reported
# TARGET: `unknownIdentifier` on the standalone line below
# TRIGGER: inspect the line after analysis completes
# EXPECT: Pylance reports `unknownIdentifier` as undefined
# VERIFY: the standalone `unknownIdentifier` line shows a diagnostic squiggle and is listed as a problem
# RECOVER: leave file text unchanged
unknownIdentifier

# SCENARIO: confirm a syntax diagnostic is reported
# TARGET: the `:""` line below
# TRIGGER: inspect the line after analysis completes
# EXPECT: Pylance reports invalid Python syntax on this line
# VERIFY: the `:""` line shows a syntax-error squiggle and is listed as a problem
# RECOVER: leave file text unchanged
:""

# SCENARIO: confirm a type-mismatch diagnostic exposes code-action UI
# TARGET: `"Hello"` in the annotated assignment below
# TRIGGER: hover the diagnostic in the editor, or open the Problems view and use the code-action affordance for this diagnostic
# EXPECT: the assignment is reported as a type mismatch for `a: int`
# VERIFY: a code-action entry is available for this diagnostic from the editor hover or from the Problems entry without applying any edit
# RECOVER: dismiss the hover or code-action UI without changing file text
a: int = "Hello"

# SCENARIO: confirm an unused import is faded but not listed as a problem
# TARGET: `os` on the import line below
# TRIGGER: inspect the editor and Problems view after analysis completes
# EXPECT: Pylance classifies `os` as unused
# VERIFY: the `import os` line is faded in the editor and there is no Problems entry for that line
# RECOVER: leave file text unchanged
import os


def foo():
    # SCENARIO: confirm an unused local symbol is faded but not listed as a problem
    # TARGET: `a` in the assignment below inside `foo`
    # TRIGGER: inspect the editor and Problems view after analysis completes
    # EXPECT: Pylance classifies `a` as an unused local symbol
    # VERIFY: the `a = 1` line is faded in the editor and there is no Problems entry for that line
    # RECOVER: leave file text unchanged
    a = 1


if False:
    # SCENARIO: confirm unreachable code is faded but not listed as a problem
    # TARGET: `print("unreachable code")` inside the `if False` block below
    # TRIGGER: inspect the editor and Problems view after analysis completes
    # EXPECT: Pylance classifies this statement as unreachable code
    # VERIFY: the `print("unreachable code")` line is faded in the editor and there is no Problems entry for that line
    # RECOVER: leave file text unchanged
    print("unreachable code")