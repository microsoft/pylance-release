# SCENARIO: verify transient `pyright-*` temp folders are cleaned up after normal VS Code shutdown
# TARGET: the OS temp directory entries created by this workspace session
# TRIGGER: clear existing `pyright-*` temp folders, reopen the workspace, observe a new temp folder appear, then close VS Code normally
# EXPECT: a fresh `pyright-*` temp folder is created while the workspace is open
# VERIFY: the created temp folder is removed after VS Code exits normally instead of being left behind
# RECOVER: none; this is an observational host-level lifecycle check