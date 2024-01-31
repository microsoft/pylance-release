# you can trigger folding range using `Go to next folding range` command
# use `command palette` to find the command and its short cut
# but that said, folding range should automatically run when a file is opened.
from typing import Callable, Type, TypeVar

_T = TypeVar("_T")

def classDecorator(cls: Type[_T]) -> Type[_T]:
    return cls

# Folding control for decorated class should appear on the `class` line.
# Folding the class should leave the `class` line and decorator visible.
@classDecorator
class DecoratedClass:
    pass

def functionDecorator(func: Callable[..., int]) -> Callable[..., int]:
    return func

# Folding control for decorated function should appear on the `def` line.
# Folding the function should leave the `def` line and decorator visible.
@functionDecorator
def decoratedFunction() -> int:
    return 0

# Folding this function should only leave the `def` line visible. The line
# with the `age` parameter will be hidden along with the function body.
def functionWithArgsSpreadOverMultipleLines(name: str,
                                            age: int):
    pass

# Folding this class should leave only the `class` line visible.
# In addition to the methods within, the trailing comments at the end of
# the class should also be folded.
class Class:
    # Single-line ranges (such as single-line functions) are not foldable.
    def singleLineFunction(self): pass

    def function1(self, name: str, address: str, title: str):
        # Multiline strings can be folded, leaving only the first line visible.
        """Doc string
        Doc string
        """
        pass

    def function2(self, x: int, char: str) -> object:
        # Folding a simple `if` statement should leave only the `if` line visible.
        if x == 0:
            return None
        
        # The folding control for an `if` statement with a multi-line conditional
        # expression should be on the last line of the expression. Therefore, when
        # folded, the entire expression is still visible.
        if (x != 0 and 
            x < 1):
            return None

        # When folding within an if/elif/else statement. Each section (ex. `elif`)
        # has its own folding control and folds separately. For example, folding the
        # `if` only collapses the body of the `if` without affecting the `elif` and
        # `else` statements that follow it.
        if x == 0:
            return None
        elif x == 1:
            return None
        elif x == 3:
            return None
        else:
            pass

        # Similarly, in a `for` loop, the `for` and `else` fold separately.
        for i in range(x):
            x += i
        else:
            x = 0
        
        # `while` loops behave the same way.
        while x < 4:
            x += 1
        else:
            x = 0

        # Similarly, in a `try` statement, the `try`, `except`, `else`, and `finally`
        # all fold separately.
        try:
            x = 2
        except ZeroDivisionError:
            x = 3
        except:
            x = 6
        else:
            x = 4
        finally:
            x = 5
            
        # Folding a `match` statement collapses the entire statement (all of the `cases`).
        # However, the `case` statements can be folded on their own if the `match` is
        # not folded.
        match char:
            case "(" | "[" | "{" | "<":
                x = 1
            case ")" | "]" | "}" | ">":
                x = 2

        # Folding a `with` statement collapses the entire statement.
        with open("foo.txt"):
            pass

        # When a multi-line function call is folded, only the first line is visible.
        self.function1("John Smith",
                       "1 Main St",
                       "President")

        func: Callable[[int], str] = (lambda x: 
            'even' 
            if x % 2 == 0 
            else 
            'odd')

        # Groups of consecutive `import` statements can be folded leaving only the first
        # line visible.
        #
        # These imports should be hidden when the enclosing `class` is folded.
        from typing import Callable, Type
        from typing import TypeVar

        # Comments at the end of a folding range, such as this comment which is at the end
        # of a `class`, should be hidden when the preceding range (the `class` in this case)
        # is folded.

# Folding multi-line lists, sets, dicts, and tuples leaves just the first line.
intList: list[int] = [
    1,
    2,
    3,
]

intSet: set[int] = {
    1,
    2,
    3,
}

intStrDict: dict[int, str] = {
        1: "one",
        2: "two",
}

myTuple = (
    1,
    2,
    3,
)

# If a `#region` comment has a matching `#endregion` comment, folding the
# `#region` will collapse everything from the `#region` to the matching
# `#endregion` leaving just the `#region` line visible. Note that regions
# can be nested so the matching `#endregion` is not necessarily the next one.

#region foo1
def foo1(): pass #region not on its own line is ignored
# region foo2
def foo2(): pass
 #region foo3
def foo3(): pass
# endregion
 #endregion
def foo4(): pass
#endregion with text after

# Unmatched `#region` and `#endregion` comments are not foldable.
#endregion unmatched
#region unmatched
