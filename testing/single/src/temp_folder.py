# test whether `pyright-xxx folder`` is removed after vscode is closed
#
# Steps follow:
# 
# 1. go to temp folder (%TEMP% in windows)
# 2. delete all `pyright-xxxx` folders
# 3. close this vscode
# 4. open new vscode
# 5. open this workspace
# 6. see pyright-xxx folder is created
# 7. close vscode (close it normally rather than kill it)
# 8. see pyright-xxx folder is removed.