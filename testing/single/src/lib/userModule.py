# this file contains types that are used by other test files.

from zipfile import Path

from requests import ConnectTimeout


class MyType:
    def method(self, v: Path) -> ConnectTimeout:
        raise Exception("Hello")
    
    def worktree_method(self):
        pass

class ConvertImportPath:
    pass

class Base:
    def method(self):
        pass

class Derived(Base):
    def method(self):
        return super().method()
    
class Derived2(Base):
    def method(self):
        return super().method()
    
class Derived3(Derived, Derived2):
    def method(self):
        return super().method()