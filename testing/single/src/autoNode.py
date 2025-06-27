# in `user` or `remote` `settings.json`, add `"python.analysis.nodeExecutable": "auto"`
# and `reload` the vscode. Confirm that pylance runs as expected. `output window`` should have a log entry
# saying `(Client) Running with node: path to node`
# Also, you can use `task manager` to confirm `pylance` is running with `node` not `code` and it is running
# with `--max-old-space-size=8192`