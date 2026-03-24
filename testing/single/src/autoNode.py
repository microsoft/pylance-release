# PREREQ: edit the `user` or `remote` `settings.json` that applies to this VS Code window
# PREREQ: save the settings change and reload the VS Code window before checking the Pylance process state
# SCENARIO: run Pylance with an auto-selected Node executable
# TARGET: the `"python.analysis.nodeExecutable"` setting in the active `user` or `remote` `settings.json`
# TRIGGER: set `"python.analysis.nodeExecutable": "auto"`, save `settings.json`, and reload the VS Code window
# EXPECT: the setting is saved as `"auto"` before the reload and Pylance restarts during the reload
# VERIFY: the Pylance Output window contains `(Client) Running with node:` followed by a node path, and Windows Task Manager shows the Pylance process running under `node` rather than `code` with `--max-old-space-size=8192`
# RECOVER: restore the original `python.analysis.nodeExecutable` value or remove the setting, save `settings.json`, and reload the VS Code window again