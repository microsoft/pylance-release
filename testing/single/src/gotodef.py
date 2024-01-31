# you can trigger go to definition using `Go To Definition` command
# use `command palette` to find the command and its short cut
# one can also use right click menu to issue the command
from typing import Mapping


class ClassWithMagicMethod:
    def __lt__(self, v: int) -> bool:
        return True
    def __len__(self) -> int:
        return 1
    

# place cursor on `<` and issue go to def command
a = ClassWithMagicMethod() < 1

# place cursor on "os" and issue go to def command
b = "os"

# place cursor on "Mapping" and issue go to def command
c: Mapping

# place cursor on `len` and issue go to def
# and confirm it shows both len and __len__ as def
print(len(ClassWithMagicMethod()))
