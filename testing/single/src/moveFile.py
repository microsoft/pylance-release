# SCENARIO: move this file into the sibling `renameFolders` package from the VS Code explorer
# TARGET: the top-level `moveFile.py` file entry for this file in `src`, moved into the sibling `renameFolders` folder
# TRIGGER: drag and drop this file from the VS Code explorer into `renameFolders`
# EXPECT: the explorer allows the move and targets `renameFolders` as the destination package
# VERIFY: after execution, the explorer shows this file at `src/renameFolders/moveFile.py`, `src/renameFolders/__init__.py` updates its `moveFile` import to point at the moved in-package module, and `src/renameFolders/renameByModule.py` updates its `moveFile` import to the moved sibling module while `m = moveFile.MovedFile()` still refers to that moved module
# RECOVER: undo the move until the explorer shows this file back at `src/moveFile.py`, `src/renameFolders/__init__.py` returns to `from .. import moveFile`, and `src/renameFolders/renameByModule.py` returns to `import moveFile`


class MovedFile:
    pass