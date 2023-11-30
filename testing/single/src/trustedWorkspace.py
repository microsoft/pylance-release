# you can change trusted workspace mode using `Workspaces: Manage Workspace Trust` command
# use `command palette` to find the command and its short cut

from pathlib import Path
from pytest import Cache, Config, PytestPluginManager

# open `Workspace Trust` window and put vscode in `restricted mode`
# and confirm `pytest` and anything under it is no longer resolved.
# but one we bundled is still working
# you can confirm by hover `Path` and `Config` and etc
# after that, put vscode back into `trusted mode` and confirm everything works again.
c = Cache(Path("path"), Config(PytestPluginManager()))