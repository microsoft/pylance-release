# test symbolic link handling

# open vscode terminal (`View: Toggle Terminal`) and go to `src/linked` folder
# and create symbolic link `shared_link.py` to `shared.py`

# for windows, run this from terminal
# make sure you are in `src/linked` folder using (> pwd)
#
# powershell command
# $currentLocation = Get-Location; Start-Process powershell -Verb RunAs -ArgumentList "-Command", "New-Item -ItemType SymbolicLink -Path '$currentLocation/shared_link.py' -Target '$currentLocation/shared.py'"

# for linux (WSL) and mac, run this from terminal
# make sure you are in `src/linked` folder using (> pwd)
#
# ln -s shared.py shared_link.py

# go to def on `shared` and `SharedType` and confirm both opened its own
# editor with correct path.
# and change content in one of them and make sure the other see the changes as well
#
# also, run find all references on `SharedType` and confirm it finds only corresponding one but not both
from linked.shared import SharedType as shared1
from linked.shared_link import SharedType as shared2


import linked.shared as shared

# rename `RenameType` to `RenameType1` and undo
a = shared.RenameType()


# rename `SharedType` to `SharedType1` and undo
# confirm only `SharedType` from `from linked.shared` is renamed.
b = shared.SharedType()

# try to rename `shared`, we need to decide whether we should allow it or not since it will break
# symlink. (currently allowed)
import linked.shared

# try to rename `shared_link1`, it should work
import linked.shared_link

# once all test are done. delete `shared_link.py`
# for window, do `del shared_link.py`
# for linux and mac, do `rm shared_link.py`
