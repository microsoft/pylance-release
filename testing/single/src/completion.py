# you can trigger suggestion (completion) explicitly using `Trigger Suggestion` command
# use `command palette` to find the command and its short cut
# also make sure to expand completion item tooltip (>) to see them
from typing import Literal, TypedDict

from altair import overload

# bring up completion after `os` and confirm tooltip and `os` is added as `auto import` 
os

class MyDict(TypedDict):
    """ doc comment """
    name: str
    age: int

a = MyDict(name="Hello", age=10)

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

# bring up symbol completion after `import` and confirm all top level modules are suggested
import 

# bring up symbol completion after `import` and confirm all symbols under pandas 
# including sub modules are suggested
from pandas import 

from lib.userModule import MyType

# bring up override completion after `me` and confirm `method` is suggested
# commit the completion and confirm all necessary imports are inserted.
class Derived(MyType):
    def me


# bring up overload completion after `ha` and confirm `handle` is suggested
class TypeWithOverload:
    @overload
    def handle(self, a: int) -> str:
        return "Hello"
    
    @overload
    def ha