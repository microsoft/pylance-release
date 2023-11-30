# you can trigger find all reference using `References: Find All Reference` command 
# use `command palette` to find the command and its short cut
# or the command can be issued using right-click menu

# put cursor on `Path` and run find all references
from zipfile import Path
from lib.userModule import Derived, MyType

# put cursor on `MyType` and run find all references
m = MyType()

# put cursor on `method` and run find all references
m.method(v=Path("path"))

class FindConstructor:
    # put cursor on `__init__` and run find all references
    # and confirm all object instantiation expressions are found as well
    # such as FindConstructor()
    def __init__(self) -> None:
        pass

c = FindConstructor()

d = Derived()

# put cursor on `method` and run find all references
# and confirm that it found all overriden methods
d.method()