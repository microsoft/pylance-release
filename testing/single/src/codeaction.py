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


