# you can trigger rename using `Rename Symbol` command 
# use `command palette` to find the command and its short cut
# or the command can be issued using right-click menu

from zipfile import Path
from lib.userModule import Derived, MyType

# put cursor on `MyType` and rename it to `MyType2`
# make sure undo work as well.
m = MyType()

# put cursor on `method` and rename it to `method2`
# make sure undo work as well.
m.method(v=Path("path"))

class RenameConstructor:
    # put cursor on `__init__` and rename
    # make sure it doesn't rename anything else but itself
    def __init__(self) -> None:
        pass

c = RenameConstructor()

d = Derived()

# put cursor on `method` and rename it to `method2`
# and confirm it renamed all overriden methods
d.method()