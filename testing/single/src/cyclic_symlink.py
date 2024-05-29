# test cyclic symbolic link handling

# open vscode terminal (`View: Toggle Terminal`) and go to `src/linked` folder
# and create folder `a/b/c` and create a symlink back to `a` in `c`

# powershell command
# mkdir a/b/c
# or someting equivalent in linux, mac

# for windows, run this from terminal
# make sure you are in `src/linked/a/b/c` folder using (> pwd)
#
# powershell command
# $currentLocation = Get-Location; Start-Process powershell -Verb RunAs -ArgumentList "-Command", "New-Item -ItemType SymbolicLink -Path '$currentLocation/a' -Target '$currentLocation/../../../a'"

# for linux (WSL) and mac, run this from terminal
# make sure you are in `src/linked/a/b/c` folder using (> pwd)
#
# ln -s ../../../a a

# once it is done, `Reload Window`

# output window should have entry saying
# `Skipping recursive symlink "..../a/b/c/a" -> ".../a"`

# once all test are done. delete `a` in `src/linked`
# for window, do `Remove-Item "a" -Recurse`
# for linux and mac, do `rm -r a`
