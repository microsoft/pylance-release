# SCENARIO: source-action driven whole-file fixes
# TARGET: use the exact file state named in each scenario block below
# TRIGGER: Source Action, from the command palette, its shortcut, or the editor context menu
# EXPECT: the named source-action entry is visible before execution
# VERIFY: when execution is requested, verify the resulting editor or settings text instead of relying on menu visibility alone
# RECOVER: when the action mutates state, undo or revert until the workspace returns to its original state before the next scenario

# SCENARIO: run Fix All through Source Action
# TARGET: place the cursor anywhere in this file while the import block below still contains both unused imports and the relative `from .lib.userModule import MyType` statement
# TRIGGER: Source Action, then choose `Fix All`; before execution, set `python.analysis.fixAll` to include `source.unusedImports` and `source.convertImportFormat`, and set `python.analysis.importFormat` to `absolute` so the import-format rewrite is observable
# EXPECT: the Source Action picker contains `Fix All`
# VERIFY: after execution, editor text removes `import os` and `import sys`, and rewrites `from .lib.userModule import MyType` to `from lib.userModule import MyType`
# RECOVER: undo until the original unused imports and the original relative import are restored

import os
import sys

from .lib.userModule import MyType

m = MyType()

# SCENARIO: run source.fixAll on save
# TARGET: restore this file to its original imports first, then make a harmless edit anywhere in the file so Save has a pending change to apply
# TRIGGER: save the file after configuring `.vscode/settings.json` with `"editor.codeActionsOnSave": { "source.fixAll": true }`, `"python.analysis.fixAll": ["source.unusedImports", "source.convertImportFormat"]`, and `"python.analysis.importFormat": "absolute"`
# EXPECT: workspace settings are in place so Save runs `source.fixAll` for this Python file instead of requiring the explicit Source Action picker
# VERIFY: after Save, editor text removes `import os` and `import sys`, rewrites `from .lib.userModule import MyType` to `from lib.userModule import MyType`, and leaves the file saved with no pending dirty state from the same edit
# RECOVER: undo until the file matches its original text, and revert `.vscode/settings.json` if those settings were added only for this scenario