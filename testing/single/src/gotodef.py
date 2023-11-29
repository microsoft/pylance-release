# you can trigger go to definition using `Go To Definition` command
# use `command palette` to find the command and its short cut
# one can also use right click menu to issue the command
from typing import Mapping


class ClassWithMagicMethod:
    def __lt__(self, v: int) -> bool:
        return True
    

# place cursor on `<` and issue go to def command
a = ClassWithMagicMethod() < 1

# place curosr on "os" and issue go to def command
b = "os"

# place curosr on "Mapping" and issue go to def command
c: Mapping