# you can trigger source code action explicitly using `Source Action` 
# use `command palette` to find the command and its short cut
# one can also use right-click menu to run them as well.
# since code action usually modify code, make sure `undo` work as expected.

import os
import sys

from .lib.userModule import MyType

m = MyType()

# source action can be run through fix all as well
# add these in the .vscode/setting.json
#  "editor.codeActionsOnSave": { "source.fixAll": true },
#  "python.analysis.fixAll": [
#     "source.unusedImports",
#     "source.convertImportFormat"
#  ]
# and run either `Fix All` command from the command palette or
# modify this file and save