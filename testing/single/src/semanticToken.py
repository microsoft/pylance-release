# you can trigger semantic token using `Developer: Force Retokenize` command
# use `command palette` to find the command and its short cut

from typing import Generic, TypeVar

# confirm identifier, keyword, operators and etc are all colored as expected.
T = TypeVar("T", int, float)

class Box(Generic[T]):
    def __init__(self, v: T):
        self._value = v

    def __add__(self, v: "Box[T]") -> "Box[T]":
        return Box(self.value + v.value)

    def __eq__(self, value: T) -> bool:
        return self.value == value
    
    @property
    def value(self):
        return self._value
    
a = Box(10)
b = Box(20)
c = a + b

d = 1 + 2

if c == d:
    print("Yay")
else:
    print("hmmm")