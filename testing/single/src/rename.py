# Use `Rename Symbol` to trigger these scenarios.
# The command may be invoked from the command palette, its keyboard shortcut, or the right-click menu.

from zipfile import Path
from lib.userModule import Derived, MyType

# SCENARIO: rename an imported type reference
# TARGET: `MyType` in `m = MyType()` below
# TRIGGER: Rename Symbol and rename `MyType` to `MyType2`
# EXPECT: rename is available on the `MyType` reference
# VERIFY: after execution, this line becomes `m = MyType2()`
# RECOVER: undo until this line returns to `m = MyType()`
m = MyType()

# SCENARIO: rename a method call on a local instance
# TARGET: `method` in `m.method(v=Path("path"))` below
# TRIGGER: Rename Symbol and rename `method` to `method2`
# EXPECT: rename is available on the `method` call
# VERIFY: after execution, this line becomes `m.method2(v=Path("path"))`
# RECOVER: undo until this line returns to `m.method(v=Path("path"))`
m.method(v=Path("path"))

class RenameConstructor:
    # SCENARIO: rename a constructor method without renaming unrelated symbols
    # TARGET: `__init__` in the definition below
    # TRIGGER: Rename Symbol and rename `__init__` to a distinct replacement name
    # EXPECT: rename is available on the `__init__` definition
    # VERIFY: only the method name in this definition changes, and unrelated symbols such as `RenameConstructor` and `c = RenameConstructor()` remain unchanged
    # RECOVER: undo until the method name returns to `__init__`
    def __init__(self) -> None:
        pass

c = RenameConstructor()

d = Derived()

# SCENARIO: rename an overridden method across the inheritance chain
# TARGET: `method` in `d.method()` below
# TRIGGER: Rename Symbol and rename `method` to `method2`
# EXPECT: rename is available on the overridden `method` call
# VERIFY: after execution, this line becomes `d.method2()`, and all overridden method declarations and references in the inheritance chain are renamed consistently
# RECOVER: undo until this line returns to `d.method()` and the overridden method names are restored
d.method()