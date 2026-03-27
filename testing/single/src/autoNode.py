# PREREQ: edit the `user` or `remote` `settings.json` that applies to this VS Code window
# PREREQ: save the settings change and reload the VS Code window before checking the Pylance process state
# SCENARIO: run Pylance with an auto-selected Node executable
# TARGET: the `"python.analysis.nodeExecutable"` setting in the active `user` or `remote` `settings.json`
# TRIGGER: set `"python.analysis.nodeExecutable": "auto"`, save `settings.json`, and reload the VS Code window
# EXPECT: the setting is saved as `"auto"` before the reload and Pylance restarts during the reload
# VERIFY: open the `ms-python.python.Python Language Server` log file after the reload and confirm it contains `(Client) Running with node:` followed by a node path; use this log-backed VS Code surface as the folder-mode proof that auto node selection took effect
# RECOVER: restore the original `python.analysis.nodeExecutable` value or remove the setting, save `settings.json`, and reload the VS Code window again