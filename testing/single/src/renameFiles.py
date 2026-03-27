# SCENARIO: rename this top-level module file from the VS Code explorer
# TARGET: the top-level `renameFiles.py` file entry for this file in `src`
# TRIGGER: rename the file from the VS Code explorer to `renameFiles1.py`
# EXPECT: the explorer allows the rename on this file entry
# VERIFY: after execution, the explorer shows this file at `src/renameFiles1.py` and `src/renameFolders/__init__.py` updates `from renameFiles import RenameFileType` to import from `renameFiles1`
# RECOVER: undo the rename until the explorer shows this file back at `src/renameFiles.py` and `src/renameFolders/__init__.py` returns to `from renameFiles import RenameFileType`

# SCENARIO: rename the imported package from the VS Code explorer
# TARGET: the `renameFolders` folder entry under `src`
# TRIGGER: rename the folder from the VS Code explorer to `renameFolders1`
# EXPECT: the explorer allows the package folder rename
# VERIFY: after execution, the explorer shows the package at `src/renameFolders1`, `import renameFolders` updates to `import renameFolders1`, and `import renameFolders.renameByModule` updates to `import renameFolders1.renameByModule`
# RECOVER: undo the rename until the explorer shows the package back at `src/renameFolders` and both import lines in this file return to `renameFolders`

# SCENARIO: rename an imported package reference with Rename Symbol
# TARGET: `renameFolders` in `import renameFolders` below
# TRIGGER: Rename Symbol and rename `renameFolders` to `renameFolders1`
# EXPECT: rename is available on the imported package reference
# VERIFY: after execution, this line becomes `import renameFolders1`, the next import becomes `import renameFolders1.renameByModule`, and the explorer shows the package folder renamed to `src/renameFolders1`
# RECOVER: undo the rename until this line returns to `import renameFolders`, the next import returns to `import renameFolders.renameByModule`, and the explorer shows the package back at `src/renameFolders`
import renameFolders

# SCENARIO: rename an imported submodule reference with Rename Symbol
# TARGET: `renameByModule` in `import renameFolders.renameByModule` below
# TRIGGER: Rename Symbol and rename `renameByModule` to `renameByModule1`
# EXPECT: rename is available on the imported submodule reference
# VERIFY: after execution, this line becomes `import renameFolders.renameByModule1`, the explorer shows the module file at `src/renameFolders/renameByModule1.py`, and `src/renameFolders/__init__.py` updates `from . import renameByModule` to `from . import renameByModule1`
# RECOVER: undo the rename until this line returns to `import renameFolders.renameByModule`, the explorer shows the module file back at `src/renameFolders/renameByModule.py`, and `src/renameFolders/__init__.py` returns to `from . import renameByModule`
import renameFolders.renameByModule


class RenameFileType:
    pass