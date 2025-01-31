# Right click on BaseWithAbstractMethod.method and select `Go To Implementations` or `Find All Implementations`,
# Only Derived1.method is expected to show up.
from abc import ABC, abstractmethod
class BaseWithAbstractMethod(ABC):
    @abstractmethod
    def method(self):
        ...

class Derived1(BaseWithAbstractMethod):
    def method(self):
        pass

# Right click on BaseWithConcreteMethod.method and select `Go To Implementations` or `Find All Implementations`,
# All methods are shown: BaseWithConcreteMethod.method, Intermediate.method, Derived2.method.
class BaseWithConcreteMethod(ABC):
    def method(self):
        ...

class Intermediate(BaseWithConcreteMethod):
    def method(self):
        pass

class Derived2(Intermediate):
    def method(self):
        pass


# Right click on A.method and select `Go To Implementations` or `Find All Implementations`,
# All methods are shown: A.method, B.method, C.method.
class A:
    def method(self): pass

class B(A):
    def method(self): pass

class C(B):
    def method(self): pass

x = B()
x.method()

# Right click on MyProtocol.protocolMethod and select `Go To Implementations` or `Find All Implementations`,
# MyProtocol.protocolMethod and Implementation.protocolMethod are expected to show up.
from typing import Protocol
class MyProtocol(Protocol):
    def protocolMethod(self):
        ...

class Implementation:
    def protocolMethod(self):
        pass


# Right click on MyProtocol2.methodWithMismatchedSignature and select `Go To Implementations` or `Find All Implementations`,
# Only MyProtocol2.methodWithMismatchedSignature is expected to show up.
from typing import Protocol
class MyProtocol2(Protocol):
    def methodWithMismatchedSignature(self):
        ...

class Implementation2:
    def methodWithMismatchedSignature(self, a: int):
        pass



