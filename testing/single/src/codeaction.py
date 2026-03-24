# SCENARIO: quick-fix driven code actions
# TARGET: use the exact token or selection named in each scenario block below
# TRIGGER: Quick Fix, either from the lightbulb or the explicit Quick Fix command
# EXPECT: the named code-action entry is visible before execution
# VERIFY: when execution is requested, verify the real file, settings, or created-artifact change
# RECOVER: when the action mutates state, undo or revert until the workspace returns to its original state before the next scenario

# SCENARIO: offer missing stdlib import for os
# TARGET: `os` on the standalone line below
# TRIGGER: Quick Fix
# EXPECT: menu contains `Add "import os"`
# VERIFY: no execution for this scenario; menu visibility is the pass condition
# RECOVER: none
os

# SCENARIO: offer missing stdlib import for Path
# TARGET: `Path` on the standalone line below
# TRIGGER: Quick Fix
# EXPECT: menu contains `Add "from pathlib import Path"`
# VERIFY: no execution for this scenario; menu visibility is the pass condition
# RECOVER: none
Path

# SCENARIO: offer missing user-module import
# TARGET: `userModule` on the standalone line below
# TRIGGER: Quick Fix
# EXPECT: menu contains `Add "from lib import userModule"`
# VERIFY: no execution for this scenario; menu visibility is the pass condition
# RECOVER: none
userModule

# SCENARIO: offer missing symbol import from nested module
# TARGET: `MyType` in the constructor call below
# TRIGGER: Quick Fix
# EXPECT: menu contains `Add "from lib.userModule import MyType"`
# VERIFY: no execution for this scenario; menu visibility is the pass condition
# RECOVER: none
MyType()


# SCENARIO: remove unused import
# TARGET: `sys` on the import line below
# TRIGGER: Quick Fix
# EXPECT: menu contains `Remove unused import`
# VERIFY: after execution, the `import sys` line is removed from editor text
# RECOVER: undo until the original `import sys` line is restored
import sys


# SCENARIO: move symbol refactor is offered and can be executed
# TARGET: `TypeToMove` in the class declaration below
# TRIGGER: Quick Fix
# EXPECT: menu contains a move-symbol entry such as `Move symbol` or `Move symbol to...`
# VERIFY: after execution, the move-symbol flow applies a refactor and updates editor state instead of leaving the file unchanged
# RECOVER: undo or revert until the original class declaration is restored
class TypeToMove:
    pass


# SCENARIO: add workspace extraPaths entry
# TARGET: `outerModule` on the import line below
# TRIGGER: Quick Fix
# EXPECT: menu contains `Add "./outsideLib" to extraPaths`
# VERIFY: after execution, `pyrightconfig.json` contains `"extraPaths": ["./outsideLib"]` under the `./src` execution environment
# RECOVER: revert `pyrightconfig.json` before the next scenario; do not rely only on undo
import outerModule


# SCENARIO: add type-ignore suppression comment
# TARGET: `hello` in the assignment line below
# TRIGGER: Quick Fix
# EXPECT: menu contains an `Add '# type: ignore' to suppress warning` entry for this assignment
# VERIFY: after execution, the assignment line includes `# type: ignore`
# RECOVER: undo until the original assignment line is restored
a: int = "hello"


# SCENARIO: unresolved import interpreter picker opens
# TARGET: `unknownModule` on the import line below
# TRIGGER: Quick Fix
# EXPECT: menu contains `Select a different interpreter`
# VERIFY: executing `Select a different interpreter` opens the interpreter picker
# RECOVER: dismiss the picker before the next scenario
import unknownModule


# SCENARIO: unresolved import help action is offered
# TARGET: `unknownModule` on the import line above
# TRIGGER: Quick Fix
# EXPECT: menu contains `Learn more about resolving imports`
# VERIFY: no execution for this scenario; menu visibility is the pass condition until the exact help surface is part of the contract
# RECOVER: none


# SCENARIO: extract method refactor
# TARGET: select the two statements inside `function` from `codeToExtract = 1` through `print(codeToExtract)`
# TRIGGER: Quick Fix and `Refactoring...`
# EXPECT: menu contains `Extract method`
# VERIFY: after execution, a helper method is created and the selected statements are replaced by a call to that helper
# RECOVER: undo until the original function body is restored
def function():
    codeToExtract = 1
    print(codeToExtract)


# SCENARIO: extract variable refactor
# TARGET: select `1 + 2 + 3` in the print call below
# TRIGGER: Quick Fix and `Refactoring...`
# EXPECT: menu contains `Extract variable`
# VERIFY: after execution, the expression is replaced by a named variable and a new assignment is inserted into editor text
# RECOVER: undo until the original print expression is restored
print(1 + 2 + 3)


# SCENARIO: convert import to relative path
# TARGET: `userModule` in the import statement below
# TRIGGER: Quick Fix
# EXPECT: menu contains `Convert to relative path`
# VERIFY: after execution, the import statement changes from an absolute import to the equivalent relative import
# RECOVER: undo until the original absolute import is restored
from lib.userModule import ConvertImportPath


# SCENARIO: create type stub for missing stub package
# TARGET: `event` in the import statement below
# TRIGGER: Quick Fix
# EXPECT-PRECONDITION: `zope.event` is installed in the selected interpreter and does not already have a workspace stub
# EXPECT: menu contains `Create Type Stub`
# VERIFY: after execution, a new stub file for `zope.event` is created under the workspace stub path and opened or otherwise surfaced in the workspace
# RECOVER: remove or revert the created stub artifact before the next scenario
import zope.event
