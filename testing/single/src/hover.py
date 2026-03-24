from typing import TypedDict


def foo(a: int) -> str:
    """doc comment"""
    return "hello"


# SCENARIO: hover over a user-defined function call target
# TARGET: `foo` in the call expression below
# TRIGGER: Hover
# EXPECT: a hover widget opens for the function symbol
# VERIFY: the hover includes the function signature with `a: int` and `-> str`, and it includes `doc comment`
# RECOVER: move the caret away or dismiss the hover widget before the next scenario
foo(10)


class MyDict(TypedDict):
    name: str


# SCENARIO: hover over a TypedDict field used as a keyword argument
# TARGET: `name` in `MyDict(name="hello")` below
# TRIGGER: Hover
# EXPECT: a hover widget opens for the TypedDict field
# VERIFY: the hover identifies the `name` field and shows that its value type is `str`
# RECOVER: move the caret away or dismiss the hover widget before the next scenario
a = MyDict(name="hello")

# SCENARIO: hover over a TypedDict field used as a string key
# TARGET: the `"name"` key in the dict literal below
# TRIGGER: Hover
# EXPECT: a hover widget opens for the TypedDict field mapping
# VERIFY: the hover identifies the `name` field and shows that its value type is `str`
# RECOVER: move the caret away or dismiss the hover widget before the next scenario
b: MyDict = {"name": "hello"}

# SCENARIO: hover over the `os` token inside a string literal
# TARGET: `os` inside the string literal on the assignment below
# TRIGGER: Hover
# EXPECT: a hover widget opens for the `os` token
# VERIFY: the hover identifies the `os` module and shows module documentation text
# RECOVER: move the caret away or dismiss the hover widget before the next scenario
c = "os"

# SCENARIO: hover over the `typing` token inside a qualified string literal
# TARGET: `typing` inside the string literal `"typing.TypedDict"` below
# TRIGGER: Hover
# EXPECT: a hover widget opens for the `typing` token
# VERIFY: the hover identifies the `typing` module and shows module documentation text
# RECOVER: move the caret away or dismiss the hover widget before the next scenario
# SCENARIO: hover over the `TypedDict` token inside a qualified string literal
# TARGET: `TypedDict` inside the string literal `"typing.TypedDict"` below
# TRIGGER: Hover
# EXPECT: a hover widget may or may not open for this token depending on product behavior
# VERIFY: record whether `TypedDict` resolves to a class hover or reproduces the known limitation tracked by microsoft/pylance-release#5171
# RECOVER: move the caret away or dismiss the hover widget before the next scenario
d = "typing.TypedDict"


class MyNumber:
    def __init__(self, v: int):
        self._value = v

    def __add__(self, v: "MyNumber") -> "MyNumber":
        return MyNumber(self._value + v._value)


# SCENARIO: hover over an overloaded operator
# TARGET: `+` in the expression below
# TRIGGER: Hover
# EXPECT: a hover widget opens for the operator implementation
# VERIFY: the hover references `__add__` and shows that the operation returns `MyNumber`
# RECOVER: move the caret away or dismiss the hover widget before the next scenario
e = MyNumber(0) + MyNumber(1)

# SCENARIO: hover over a built-in type annotation
# TARGET: `int` in the annotation below
# TRIGGER: Hover
# EXPECT: a hover widget opens for the built-in type
# VERIFY: the hover shows the built-in `int` type header and includes documentation text beneath it
# RECOVER: move the caret away or dismiss the hover widget before the next scenario
i: int
