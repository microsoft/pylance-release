from typing import TypedDict


def foo(a: int) -> str:
    """ doc comment """
    return "hello"

# hover on `foo`` and confirm signature and doc comment
foo(10)

class MyDict(TypedDict):
    name: str

# hover on `name` and confirm signature
a = MyDict(name="hello")

# hover on `name` and confirm signature
b: MyDict = { "name": "hello"}

# hover on `os` and confirm it shows tooltip for `os` module
c = "os"

# hover on `typing` and `TypedDict` and confirm it shows tooltip for `typing` and `TypedDict`
d = "typing.TypedDict"

class MyNumber:
    def __init__(self, v: int):
        self._value = v

    def __add__(self, v: "MyNumber") -> "MyNumber":
        return MyNumber(self._value + v._value)
    

# hover on `+` and confirm it shows tooltip for `__add__`
e = MyNumber(0) + MyNumber(1)