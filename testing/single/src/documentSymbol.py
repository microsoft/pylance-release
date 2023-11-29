# you can trigger document symbol using `Explorer: Focus on Outline View` 
# or `Go to Symbol in Editor ...` commands
# use `command palette` to find the command and its short cut

# confirm the `OUTLINE` view shows symbol hierarchy of the code view
# click entries in the view to make sure correct symbols are highlighted
# and double click to jump to the code

# confirm the `Go to symbol in Editor` also works as expected
class A:
    def __init__(self, v: int):
        self.v = v

    def getValue(self) -> int:
        return self.v
    

def createA(v: int) -> A:
    return A(v)

aInstance = createA(10)