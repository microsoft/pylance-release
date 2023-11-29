# you can trigger quick fix explicitly using `QuickFix` command
# use `command palette` to find the command and its short cut

# place cursor on `os` and confirm lightbulb shows up
# and trigger quick fix and confirm `Add 'import os'` is listed
os

# place cursor on `Path` and confirm lightbulb shows up
# and trigger quick fix and confirm `Add 'from pathlib import Path'` is listed
Path

# place cursor on `userModule` and confirm lightbulb shows up
# and trigger quick fix and confirm `Add 'from lib import userModule'` is listed
userModule

# place cursor on `MyType` and confirm lightbulb shows up
# and trigger quick fix and confirm `Add 'from lib.userModule import MyType'` is listed
MyType


# place cursor on `sys` and confirm lightbulb shows up
# and trigger quick fix and confirm `remove unused import` is listed
# execute the code action and confirm it works as expected
import sys


# place cursor on `TypeToMove` and confirm lightbulb shows up
# and trigger quick fix and confirm `move symbol` is listed
# execute the code action and confirm it works as expected
# and undo to make sure undo works as expected
class TypeToMove:
    pass


# place cursor on `outerModule` and confirm lightbulb shows up
# and trigger quick fix and confirm `Add "./outsideLib" to extraPaths` is listed
# execute the code action and confirm `extraPaths` is added to `settings.json`
import outerModule


# place cursor on `hello` and confirm lightbulb shows up
# and trigger quick fix and confirm `type ignore` entry is listed
# execute the code action and confirm it added #type: ignore
a: int = "hello"


# place cursor on `unknownModule` and confirm lightbulb shows up
# and trigger quick fix and confirm `select a different interpreter` and 
# `learn more about resolving import` entry is listed
# execute the code action and confirm it works as expected
import unknownModule


# select code between `codeToExtract` and `print(codeToExtract)` and confirm lightbulb shows up
# and trigger quick fix and confirm `extract method` is listed
# execute the code action and confirm it works as expected
def function():
    codeToExtract = 1
    print(codeToExtract)