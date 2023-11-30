# you can trigger type hierarchy using `Types: Show Type Hierarchy` command
# use `command palette` to find the command and its short cut
# one can use both command or menu to issue the command.
from typing import Generic, TypeVar
from lib.userModule import Base, Derived2, Derived3


# place cursor on `Derived3` and see type hierarchy
# check supertypes
a = Derived3()

# place cursor on `method` and see type hierarchy
# check supertypes
a.method()

# place cursor on `Base` and see type hierarchy
# check subtypes
b = Base()

# place cursor on `method` and see type hierarchy
# check subtypes
b.method()

# place cursor on `Derived2` and see type hierarchy
# check subtypes and supertypes
c = Derived2()

# place cursor on `method` and see type hierarchy
# check subtypes and supertypes
c.method()


T = TypeVar("T")

# place cursor on `TypeHierarchyBase` and see type hierarchy
# check subtypes
class TypeHierarchyBase(Generic[T]):
    pass

# place cursor on `TypeHierarchyType` and see type hierarchy
# check supertypes
class TypeHierarchyType(TypeHierarchyBase[int]):
    pass