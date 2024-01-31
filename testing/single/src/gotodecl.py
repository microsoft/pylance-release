# you can trigger go to declaration using `Go To Declaration` command
# use `command palette` to find the command and its short cut
# one can also use right click menu to issue the command
from typing import Mapping

   

# place cursor on `==` and issue go to decl command
# it should go to pyi file.
a = 1 == 1

# place cursor on "os" and issue go to decl command
# it should go to pyi file.
b = "os"

# place cursor on "Mapping" and issue go to decl command
# it should go to pyi file instead of py file.
c: Mapping