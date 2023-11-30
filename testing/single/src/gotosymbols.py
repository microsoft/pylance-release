# you can trigger go to symbol using `Go to symbols in workspace` command
# use `command palette` to find the command and its short cut
from typing import TypedDict


# run `Go to symbols in workspace` and type `MyDict` and verify it finds all
# `MyDict` type defined
class MyDict(TypedDict):
    pass

# run `Go to symbols in workspace` and type `var` and verify it finds all
# symbol that has `var` in them
var = 1


# run `Go to symbols in workspace` and type `foo` and verify it finds all
# symbol that has `f``o``o` in them
def foo():
    pass