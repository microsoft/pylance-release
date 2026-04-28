# Use `Developer: Force Retokenize` from the command palette when you need to
# refresh semantic token coloring before checking the scenario below.

from typing import Generic, TypeVar

# SCENARIO: semantic token coloring survives a forced retokenize
# TARGET: the `TypeVar`, `Box`, arithmetic, comparison, decorator, and string literal tokens in this file
# TRIGGER: run `Developer: Force Retokenize` with this file focused
# EXPECT: semantic token coloring remains active after the retokenize completes
# VERIFY: visual-only check that `class`, `def`, `if`, and `else` stay tokenized as keywords; `Box`, `value`, and `_value` stay tokenized as identifiers; `+` and `==` stay tokenized as operators; `@property` stays tokenized as a decorator; and `"Yay"` plus `"hmmm"` stay tokenized as string literals
# RECOVER: none
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