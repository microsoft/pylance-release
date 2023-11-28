from typing import TypedDict


def foo(a: int) -> str:
    """ doc comment """
    pass

# hover on `foo`` and confirm signature and doc comment
foo()

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