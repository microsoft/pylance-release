# SCENARIO: find all references for an imported stdlib symbol
# TARGET: `Path` in the import line below
# TRIGGER: Find All References
# EXPECT: the cursor is on the imported `Path` symbol in `from zipfile import Path`
# VERIFY: the references view includes this import site and the `Path("path")` constructor call in `m.method(v=Path("path"))`
from zipfile import Path
from lib.userModule import Derived, MyType

# SCENARIO: find all references for an imported user type
# TARGET: `MyType` in the construction below
# TRIGGER: Find All References
# EXPECT: the cursor is on `MyType` in `m = MyType()`
# VERIFY: the references view includes the declaration in `lib/userModule.py`, the import in this file, and the construction below
m = MyType()

# SCENARIO: find all references for a user-defined method call
# TARGET: `method` in the call below
# TRIGGER: Find All References
# EXPECT: the cursor is on `method` in `m.method(v=Path("path"))`
# VERIFY: the references view includes the declaration in `lib/userModule.py` and this call site
m.method(v=Path("path"))

class FindConstructor:
    # SCENARIO: find all references for a constructor includes object creation
    # TARGET: `__init__` in the definition below
    # TRIGGER: Find All References
    # EXPECT: the cursor is on `__init__` in `def __init__(self) -> None:`
    # VERIFY: the references view includes this constructor definition and the `FindConstructor()` instantiation at `c = FindConstructor()`
    def __init__(self) -> None:
        pass

c = FindConstructor()

d = Derived()

# SCENARIO: find all references for an override-aware method symbol
# TARGET: `method` in the call below
# TRIGGER: Find All References
# EXPECT: the cursor is on `method` in `d.method()`
# VERIFY: the references view includes `Base.method`, `Derived.method`, and this call site so the override chain is represented
d.method()