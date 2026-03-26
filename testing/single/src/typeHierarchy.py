from typing import Generic, TypeVar
from lib.userModule import Base, Derived2, Derived3


# SCENARIO: show supertypes for a multiply-inherited class
# TARGET: `Derived3` in the construction below
# TRIGGER: Show Type Hierarchy
# EXPECT: the cursor is on `Derived3` in `a = Derived3()`
# VERIFY: the Type Hierarchy view opens on `Derived3` and the supertypes tree includes `Derived` and `Derived2`
# RECOVER: none
a = Derived3()

# SCENARIO: show supertypes for an overridden method on a multiply-inherited class
# TARGET: `method` in the call below
# TRIGGER: Show Type Hierarchy
# EXPECT: the cursor is on `method` in `a.method()`
# VERIFY: the Type Hierarchy view opens on `Derived3.method` and the supertypes tree includes `Derived.method` and `Derived2.method`
# RECOVER: none
a.method()

# SCENARIO: show subtypes for a base class
# TARGET: `Base` in the construction below
# TRIGGER: Show Type Hierarchy
# EXPECT: the cursor is on `Base` in `b = Base()`
# VERIFY: the Type Hierarchy view opens on `Base` and the subtypes tree includes `Derived`, `Derived2`, and `Derived3`
# RECOVER: none
b = Base()

# SCENARIO: show subtypes for a base-class method
# TARGET: `method` in the call below
# TRIGGER: Show Type Hierarchy
# EXPECT: the cursor is on `method` in `b.method()`
# VERIFY: the Type Hierarchy view opens on `Base.method` and the subtypes tree includes the overrides on `Derived`, `Derived2`, and `Derived3`
# RECOVER: none
b.method()

# SCENARIO: show hierarchy for a class with a known subtype gap
# TARGET: `Derived2` in the construction below
# TRIGGER: Show Type Hierarchy
# EXPECT: the cursor is on `Derived2` in `c = Derived2()`
# VERIFY: the Type Hierarchy view opens on `Derived2` and includes `Base` as a supertype; keep the subtype half skip-ready because `Derived3` may still be absent due to the known limitation tracked at https://github.com/microsoft/pylance-release/issues/5403
# RECOVER: none
c = Derived2()

# SCENARIO: show hierarchy for a method with the same known subtype gap
# TARGET: `method` in the call below
# TRIGGER: Show Type Hierarchy
# EXPECT: the cursor is on `method` in `c.method()`
# VERIFY: the Type Hierarchy view opens on `Derived2.method` and includes `Base.method` as a supertype; keep the subtype half skip-ready because the matching `Derived3.method` subtype may still be absent under the same known limitation
# RECOVER: none
c.method()


T = TypeVar("T")


# SCENARIO: show subtypes for a generic base class
# TARGET: `TypeHierarchyBase` in the class definition below
# TRIGGER: Show Type Hierarchy
# EXPECT: the cursor is on `TypeHierarchyBase` in the class declaration below
# VERIFY: the Type Hierarchy view opens on `TypeHierarchyBase` and the subtypes tree includes `TypeHierarchyType`
# RECOVER: none
class TypeHierarchyBase(Generic[T]):
    pass


# SCENARIO: show supertypes for a specialized generic subclass
# TARGET: `TypeHierarchyType` in the class definition below
# TRIGGER: Show Type Hierarchy
# EXPECT: the cursor is on `TypeHierarchyType` in the class declaration below
# VERIFY: the Type Hierarchy view opens on `TypeHierarchyType` and the supertypes tree includes `TypeHierarchyBase[int]`
# RECOVER: none
class TypeHierarchyType(TypeHierarchyBase[int]):
    pass
