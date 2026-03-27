# ENV: reuse ../.venv
# DEPS: bootstrap from ../requirements.txt when pytest-backed trust checks need the selected interpreter populated
# SCENARIO: verify analysis changes between trusted and restricted workspace modes
# TARGET: the `pytest` and bundled symbols referenced in the construction below
# TRIGGER: run `Workspaces: Manage Workspace Trust`, switch to restricted mode, inspect symbol resolution, then switch back to trusted mode
# EXPECT: the workspace trust flow can be opened from the command palette
# VERIFY: `pytest`-provided symbols stop resolving in restricted mode while bundled symbols such as `Path` still remain inspectable, then full resolution returns after switching back to trusted mode
# RECOVER: return the workspace to trusted mode before leaving the scenario

from pathlib import Path
from pytest import Cache, Config, PytestPluginManager

c = Cache(Path("path"), Config(PytestPluginManager()))