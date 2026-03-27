def func1():
    pass


# SCENARIO: show call hierarchy for a local function with both incoming and outgoing calls
# TARGET: `func2` in the function definition below
# TRIGGER: Show Call Hierarchy
# EXPECT: the cursor is on `func2` in `def func2():`
# VERIFY: the Call Hierarchy view opens on `func2`, incoming calls include `func3`, and toggling to outgoing calls shows `func1`
# RECOVER: none
def func2():
    func1()


def func3():
    func2()


from math import sqrt as s
from math import sqrt


# SCENARIO: show call hierarchy for an aliased import
# TARGET: `s` in `from math import sqrt as s`
# TRIGGER: Show Call Hierarchy
# EXPECT: the cursor is on the alias binding `s` in the import above
# VERIFY: the Call Hierarchy view opens for the aliased symbol and incoming calls include `callByAlias`
# RECOVER: none
def callByAlias():
    s(1)


# SCENARIO: show call hierarchy for the original imported name
# TARGET: `sqrt` in `from math import sqrt`
# TRIGGER: Show Call Hierarchy
# EXPECT: the cursor is on `sqrt` in the non-aliased import above
# VERIFY: the Call Hierarchy view opens for `sqrt` and incoming calls include `callByName`
# RECOVER: none
def callByName():
    sqrt(1)


import abc


class Base(abc.ABC):
    @abc.abstractmethod
    def method(self):
        pass


class Derived(Base):
    # SCENARIO: show call hierarchy for an overridden method across the hierarchy
    # TARGET: `method` in the override below
    # TRIGGER: Show Call Hierarchy
    # EXPECT: the cursor is on `method` in `def method(self):` within `Derived`
    # VERIFY: the Call Hierarchy view treats the override set as one symbol family and surfaces callers from both `BaseConsumer.consumer` and `DerivedConsumer.consumer`
    # RECOVER: none
    def method(self):
        pass


class BaseConsumer:
    def consumer(self, base: Base):
        base.method()
        return base


class DerivedConsumer(BaseConsumer):
    def consumer(self, derived: Derived):
        derived.method()
        return derived
