# you can trigger suggestion (completion) explicitly using `Trigger Suggestion` command
# use `command palette` to find the command and its short cut
# also make sure to expand completion item tooltip (>) to see them
from typing import Literal, TypedDict

# bring up completion after `os` and confirm tooltip and `os` is added as `auto import` 
os

class MyDict(TypedDict):
    """ doc comment """
    name: str
    age: int

a = MyDict()

# bring up typed dict key completion inside of `[]` and confirm `name` and `age` are suggested
a[]


d = { "some key": 1, "another#2": "#2" }
d["#3 key"] = 3

# bring up regular dict completion inside of `[]` and confirm all keys are suggested
d[]

# bring up string literal completion inside of `""` and confirm 2 literals are suggested
e: Literal["Hello", "There"] = ""

# bring up symbol completion after `My` and confirm tooltip and `MyDict` is suggested
My

