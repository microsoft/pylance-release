# SCENARIO: show only concrete implementations for an abstract method
# TARGET: `method` in `BaseWithAbstractMethod.method` below
# TRIGGER: Go To Implementations or Find All Implementations
# EXPECT: the cursor is on `method` in the abstract base declaration below
# VERIFY: the navigation or results surface shows only `Derived1.method`
from abc import ABC, abstractmethod
class BaseWithAbstractMethod(ABC):
    @abstractmethod
    def method(self):
        ...

class Derived1(BaseWithAbstractMethod):
    def method(self):
        pass

# SCENARIO: include the full implementation chain for a concrete base method
# TARGET: `method` in `BaseWithConcreteMethod.method` below
# TRIGGER: Go To Implementations or Find All Implementations
# EXPECT: the cursor is on `method` in the concrete base declaration below
# VERIFY: the navigation or results surface shows `BaseWithConcreteMethod.method`, `Intermediate.method`, and `Derived2.method`
class BaseWithConcreteMethod(ABC):
    def method(self):
        ...

class Intermediate(BaseWithConcreteMethod):
    def method(self):
        pass

class Derived2(Intermediate):
    def method(self):
        pass


# SCENARIO: include each override in a simple inheritance chain
# TARGET: `method` in `A.method` below
# TRIGGER: Go To Implementations or Find All Implementations
# EXPECT: the cursor is on `method` in `class A`
# VERIFY: the navigation or results surface shows `A.method`, `B.method`, and `C.method`
class A:
    def method(self): pass

class B(A):
    def method(self): pass

class C(B):
    def method(self): pass

x = B()
x.method()

# SCENARIO: include protocol declarations and matching implementations
# TARGET: `protocolMethod` in `MyProtocol.protocolMethod` below
# TRIGGER: Go To Implementations or Find All Implementations
# EXPECT: the cursor is on `protocolMethod` in the protocol declaration below
# VERIFY: the navigation or results surface shows `MyProtocol.protocolMethod` and `Implementation.protocolMethod`
from typing import Protocol
class MyProtocol(Protocol):
    def protocolMethod(self):
        ...

class Implementation:
    def protocolMethod(self):
        pass


# SCENARIO: exclude protocol members with mismatched implementation signatures
# TARGET: `methodWithMismatchedSignature` in `MyProtocol2.methodWithMismatchedSignature` below
# TRIGGER: Go To Implementations or Find All Implementations
# EXPECT: the cursor is on `methodWithMismatchedSignature` in the protocol declaration below
# VERIFY: the navigation or results surface shows only `MyProtocol2.methodWithMismatchedSignature`
from typing import Protocol
class MyProtocol2(Protocol):
    def methodWithMismatchedSignature(self):
        ...

class Implementation2:
    def methodWithMismatchedSignature(self, a: int):
        pass



