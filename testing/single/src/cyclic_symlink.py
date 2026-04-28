# SCENARIO: verify recursive-cyclic symlinks are skipped during analysis
# TARGET: a new cyclic symlink rooted under `src/linked/a/b/c/a`
# TRIGGER: create `src/linked/a/b/c`, create a symlink from `c/a` back to `../../../a`, then run `Reload Window`
# EXPECT: the host OS allows the symlink to be created successfully before reload
# VERIFY: the Output surface reports a `Skipping recursive symlink` entry for the created cycle rather than recursing indefinitely
# RECOVER: delete `src/linked/a` after the check so the workspace returns to its original layout

# Windows setup recipe (run from `src/linked/a/b/c` in an elevated PowerShell session):
#   New-Item -ItemType SymbolicLink -Path "$PWD/a" -Target "$PWD/../../../a"
# Linux/macOS setup recipe (run from `src/linked/a/b/c`):
#   ln -s ../../../a a
