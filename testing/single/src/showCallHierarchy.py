def func1():
    pass


# Right click on func2 and select `Show Call Hierarchy` to view incoming calls,
# func3 is expected to show up.
# Toggle the phone icon on the top right to view outgoing calls,
# func1 is expected to show up.
def func2():
    func1()


def func3():
    func2()


# Right click on sqrt and s to view that the `Show Call Hierarchy` also works for alias
from math import sqrt as s
from math import sqrt


def callByAlias():
    s(1)


def callByName():
    sqrt(1)


# Right click on method to view that the `Show Call Hierarchy` considers all overriden methods as a match
import abc


class Base(abc.ABC):
    @abc.abstractmethod
    def method(self):
        pass


class Derived(Base):
    def method(self):
        pass


class BaseConsumer:
    def consumer(self, base: Base):
        base.method()


class DerivedConsumer:
    def consumer(self, derived: Derived):
        derived.method()
