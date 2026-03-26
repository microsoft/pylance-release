# ENV: reuse ../.venv
# DEPS: bootstrap from ../requirements.txt when package-backed completion checks need pandas or other workspace dependencies
# SCENARIO: show auto-import completion for `os`
# TARGET: the standalone `os` line below
# TRIGGER: Trigger Suggestion
# EXPECT: the completion list opens at the standalone symbol target
# VERIFY: the suggestion list includes `os` as an auto-import completion entry
# RECOVER: dismiss the completion list without committing the item
from typing import Literal, TypedDict, overload


os

class MyDict(TypedDict):
    """ doc comment """
    name: str
    age: int

a = MyDict(name="Hello", age=10)

# SCENARIO: show TypedDict key completion inside `a[]`
# TARGET: the empty brackets in `a[]` below
# TRIGGER: Trigger Suggestion
# EXPECT: the completion list opens inside the subscript position
# VERIFY: the suggestion list includes `name` and `age`
# RECOVER: dismiss the completion list without committing the item
a[]


d = { "some key": 1, "another#2": "#2" }
d["#3 key"] = 3

# SCENARIO: show regular dict key completion inside `d[]`
# TARGET: the empty brackets in `d[]` below
# TRIGGER: Trigger Suggestion
# EXPECT: the completion list opens inside the subscript position
# VERIFY: the suggestion list includes `"some key"`, `"another#2"`, and `"#3 key"`
# RECOVER: dismiss the completion list without committing the item
d[]

# SCENARIO: show literal-string completions inside `e = ""`
# TARGET: the empty string literal in `e: Literal[...] = ""` below
# TRIGGER: Trigger Suggestion
# EXPECT: the completion list opens inside the string literal
# VERIFY: the suggestion list includes `"Hello"` and `"There"`
# RECOVER: dismiss the completion list without committing the item
e: Literal["Hello", "There"] = ""

# SCENARIO: show literal-string completions inside `case ""`
# TARGET: the empty string literal in the `case ""` pattern below
# TRIGGER: Trigger Suggestion
# EXPECT: the completion list opens inside the pattern literal
# VERIFY: the suggestion list includes `"Hello"` and `"There"`
# RECOVER: dismiss the completion list without committing the item
match e:
    case ""

# SCENARIO: show symbol completion for `MyDict`
# TARGET: `My` on the standalone line below
# TRIGGER: Trigger Suggestion
# EXPECT: the completion list opens at the symbol prefix
# VERIFY: the suggestion list includes `MyDict`
# RECOVER: dismiss the completion list without committing the item
My

# SCENARIO: show top-level module completions after `import`
# TARGET: the trailing space in `import ` below
# TRIGGER: Trigger Suggestion
# EXPECT: the completion list opens at the import target
# VERIFY: the suggestion list includes top-level modules such as `argparse`
# RECOVER: dismiss the completion list without committing the item
import 

# SCENARIO: show pandas symbol completions after `from pandas import`
# TARGET: the trailing space in `from pandas import ` below
# TRIGGER: Trigger Suggestion
# EXPECT: the completion list opens at the pandas-import target
# VERIFY: the suggestion list includes pandas symbols or submodules such as `concat`
# RECOVER: dismiss the completion list without committing the item
from pandas import 

from lib.userModule import MyType

# SCENARIO: show override completion suggestion after `def me`
# TARGET: the partial member name `me` in `def me` below
# TRIGGER: Trigger Suggestion
# EXPECT: the completion list opens at the partial member target
# VERIFY: the suggestion list includes the override entry `method`
# RECOVER: dismiss the completion list without committing the item
class Derived(MyType):
    def me


# SCENARIO: show overload completion suggestion after `def ha`
# TARGET: the partial member name `ha` in the second overload stub below
# TRIGGER: Trigger Suggestion
# EXPECT: the completion list opens at the partial member target
# VERIFY: the suggestion list includes the overload entry `handle`
# RECOVER: dismiss the completion list without committing the item
class TypeWithOverload:
    @overload
    def handle(self, a: int) -> str:
        return "Hello"
    
    @overload
    def ha

# SCENARIO: show named-parameter completion for `sep`
# TARGET: `sep` in `print("Hello", sep)` below
# TRIGGER: Trigger Suggestion
# EXPECT: the completion list opens at the named-parameter target
# VERIFY: the suggestion list includes `sep=`
# RECOVER: dismiss the completion list without committing the item
print("Hello", sep)


# SCENARIO: show built-in override completion suggestion for `__init__`
# TARGET: the partial member name `__init__` in the class below
# TRIGGER: Trigger Suggestion
# EXPECT: the completion list opens at the built-in override target
# VERIFY: the suggestion list includes the built-in override entry `__init__`
# RECOVER: dismiss the completion list without committing the item
class BuiltInMethod:
    def __init__