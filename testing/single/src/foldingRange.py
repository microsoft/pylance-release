# Folding controls should appear automatically when this file opens.
# If they do not render immediately, use `Go to next folding range` from the
# command palette once and then continue with the scenarios below.
from typing import Callable, Type, TypeVar

_T = TypeVar("_T")

def classDecorator(cls: Type[_T]) -> Type[_T]:
    return cls

# SCENARIO: fold decorated class
# TARGET: `class DecoratedClass:` immediately below `@classDecorator`
# TRIGGER: fold the range from the gutter control on the `class DecoratedClass:` line
# EXPECT: a folding control is visible on the `class DecoratedClass:` line
# VERIFY: after folding, `@classDecorator` and `class DecoratedClass:` remain visible and the `pass` line is hidden
# RECOVER: unfold the `class DecoratedClass:` range so the `pass` line is visible again
@classDecorator
class DecoratedClass:
    pass

def functionDecorator(func: Callable[..., int]) -> Callable[..., int]:
    return func

# SCENARIO: fold decorated function
# TARGET: `def decoratedFunction() -> int:` immediately below `@functionDecorator`
# TRIGGER: fold the range from the gutter control on the `def decoratedFunction` line
# EXPECT: a folding control is visible on the `def decoratedFunction` line
# VERIFY: after folding, `@functionDecorator` and `def decoratedFunction() -> int:` remain visible and the `return 0` line is hidden
# RECOVER: unfold the `def decoratedFunction` range so the `return 0` line is visible again
@functionDecorator
def decoratedFunction() -> int:
    return 0

# SCENARIO: fold function with multi-line signature
# TARGET: `def functionWithArgsSpreadOverMultipleLines(` below `decoratedFunction`
# TRIGGER: fold the range from the gutter control on the `def functionWithArgsSpreadOverMultipleLines` line
# EXPECT: a folding control is visible on the `def functionWithArgsSpreadOverMultipleLines` line
# VERIFY: after folding, only the first `def` line remains visible and the `age: int):` line plus the `pass` line are hidden
# RECOVER: unfold the `def functionWithArgsSpreadOverMultipleLines` range so the full signature and body are visible again
def functionWithArgsSpreadOverMultipleLines(name: str,
                                            age: int):
    pass

# SCENARIO: fold enclosing class
# TARGET: `class Class:` below `functionWithArgsSpreadOverMultipleLines`
# TRIGGER: fold the range from the gutter control on the `class Class:` line
# EXPECT: a folding control is visible on the `class Class:` line
# VERIFY: after folding, only `class Class:` remains visible and the methods, grouped imports, and trailing comments inside the class are hidden
# RECOVER: unfold the `class Class:` range so the full class body is visible again
class Class:
    # Single-line ranges (such as single-line functions) are not foldable.
    def singleLineFunction(self): pass

    def function1(self, name: str, address: str, title: str):
        # SCENARIO: fold multiline docstring
        # TARGET: the `"""Doc string` line inside `function1`
        # TRIGGER: fold the range from the gutter control on the first docstring line
        # EXPECT: a folding control is visible on the first docstring line
        # VERIFY: after folding, only the first docstring line remains visible and the following docstring lines are hidden
        # RECOVER: unfold the docstring range so the full docstring is visible again
        """Doc string
        Doc string
        """
        pass

    def function2(self, x: int, char: str) -> object:
        # SCENARIO: fold simple if block
        # TARGET: the first `if x == 0:` line directly inside `function2`
        # TRIGGER: fold the range from the gutter control on that first `if x == 0:` line
        # EXPECT: a folding control is visible on that first `if x == 0:` line
        # VERIFY: after folding, only that `if x == 0:` line remains visible and the `return None` line under it is hidden
        # RECOVER: unfold that first `if x == 0:` range so the `return None` line is visible again
        if x == 0:
            return None
        
        # SCENARIO: fold if block with multi-line condition
        # TARGET: the `if (x != 0 and` block below the first simple `if`
        # TRIGGER: fold the range from the gutter control on the last line of that multi-line condition
        # EXPECT: a folding control is visible on the last line of the multi-line condition
        # VERIFY: after folding, the full conditional expression remains visible and only the `return None` body line is hidden
        # RECOVER: unfold the multi-line-condition `if` range so the `return None` line is visible again
        if (x != 0 and 
            x < 1):
            return None

        # SCENARIO: fold only the first branch of an if-elif-else chain
        # TARGET: the second `if x == 0:` line, the one immediately above `elif x == 1:`
        # TRIGGER: fold the range from the gutter control on that second `if x == 0:` line
        # EXPECT: a folding control is visible on each `if`, `elif`, and `else` line in this chain
        # VERIFY: after folding the first branch, its `return None` body is hidden while the `elif x == 1:`, `elif x == 3:`, and `else:` lines remain visible
        # RECOVER: unfold the first branch in the chain so all lines are visible again
        if x == 0:
            return None
        elif x == 1:
            return None
        elif x == 3:
            return None
        else:
            pass

        # SCENARIO: fold only the for portion of a for-else block
        # TARGET: `for i in range(x):` below the if-elif-else chain
        # TRIGGER: fold the range from the gutter control on the `for i in range(x):` line
        # EXPECT: a folding control is visible on both the `for` line and the `else:` line in this block
        # VERIFY: after folding the `for`, the `x += i` line is hidden and the `else:` line remains visible
        # RECOVER: unfold the `for i in range(x):` range so the `x += i` line is visible again
        for i in range(x):
            x += i
        else:
            x = 0
        
        # SCENARIO: fold only the while portion of a while-else block
        # TARGET: `while x < 4:` below the for-else block
        # TRIGGER: fold the range from the gutter control on the `while x < 4:` line
        # EXPECT: a folding control is visible on both the `while x < 4:` line and the `else:` line in this block
        # VERIFY: after folding the `while`, the `x += 1` line is hidden and the `else:` line remains visible
        # RECOVER: unfold the `while x < 4:` range so the `x += 1` line is visible again
        while x < 4:
            x += 1
        else:
            x = 0

        # SCENARIO: fold only the try portion of a try-except-else-finally block
        # TARGET: `try:` below the while-else block
        # TRIGGER: fold the range from the gutter control on the `try:` line
        # EXPECT: folding controls are visible on the `try:`, each `except`, the `else:`, and the `finally:` lines
        # VERIFY: after folding the `try:` section, `x = 2` is hidden while the following `except`, `else:`, and `finally:` lines remain visible
        # RECOVER: unfold the `try:` range so the `x = 2` line is visible again
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
            
        # SCENARIO: fold entire match statement
        # TARGET: `match char:` below the try-except-else-finally block
        # TRIGGER: fold the range from the gutter control on the `match char:` line
        # EXPECT: a folding control is visible on the `match char:` line
        # VERIFY: after folding the `match`, the `case "(" | "[" | "{" | "<":` and `case ")" | "]" | "}" | ">":` lines are hidden
        # RECOVER: unfold the `match char:` range so both `case` lines are visible again
        match char:
            case "(" | "[" | "{" | "<":
                x = 1
            case ")" | "]" | "}" | ">":
                x = 2

        # SCENARIO: fold one case inside an expanded match statement
        # TARGET: `case "(" | "[" | "{" | "<":` inside the `match char:` block
        # TRIGGER: with the `match` block expanded, fold the range from the gutter control on the first `case` line
        # EXPECT: a folding control is visible on the first `case` line while the `match` block is expanded
        # VERIFY: after folding that first `case`, the `x = 1` line is hidden and the second `case` line remains visible
        # RECOVER: unfold the first `case` range so the `x = 1` line is visible again

        # SCENARIO: fold with statement
        # TARGET: `with open("foo.txt"):` below the `match` block
        # TRIGGER: fold the range from the gutter control on the `with open("foo.txt"):` line
        # EXPECT: a folding control is visible on the `with open("foo.txt"):` line
        # VERIFY: after folding, the `with open("foo.txt"):` line remains visible and the `pass` line under it is hidden
        # RECOVER: unfold the `with open("foo.txt"):` range so the `pass` line is visible again
        with open("foo.txt"):
            pass

        # SCENARIO: fold multi-line function call
        # TARGET: the `self.function1("John Smith",` call below the `with` block
        # TRIGGER: fold the range from the gutter control on the first line of that call
        # EXPECT: a folding control is visible on the first line of that multi-line call
        # VERIFY: after folding, only the first call line remains visible and the `"1 Main St"` plus `"President")` lines are hidden
        # RECOVER: unfold the `self.function1` call range so all argument lines are visible again
        self.function1("John Smith",
                       "1 Main St",
                       "President")

        func: Callable[[int], str] = (lambda x: 
            'even' 
            if x % 2 == 0 
            else 
            'odd')

        # SCENARIO: fold grouped consecutive imports
        # TARGET: the first `from typing import Callable, Type` line inside `function2`
        # TRIGGER: fold the range from the gutter control on that first import line
        # EXPECT: a folding control is visible on the first import line in this consecutive import group
        # VERIFY: after folding, the first import line remains visible and the following `from typing import TypeVar` line is hidden
        # RECOVER: unfold the grouped import range so both import lines are visible again
        from typing import Callable, Type
        from typing import TypeVar

        # Trailing comments at the end of the class are covered by the `fold enclosing class`
        # scenario above and should be hidden when `class Class:` is folded.

# SCENARIO: fold multi-line list literal
# TARGET: `intList: list[int] = [` below `class Class`
# TRIGGER: fold the range from the gutter control on the `intList: list[int] = [` line
# EXPECT: a folding control is visible on the `intList: list[int] = [` line
# VERIFY: after folding, only the `intList: list[int] = [` line remains visible and the element lines are hidden
# RECOVER: unfold the `intList` range so all list elements are visible again
intList: list[int] = [
    1,
    2,
    3,
]

# SCENARIO: fold multi-line set literal
# TARGET: `intSet: set[int] = {` below `intList`
# TRIGGER: fold the range from the gutter control on the `intSet: set[int] = {` line
# EXPECT: a folding control is visible on the `intSet: set[int] = {` line
# VERIFY: after folding, only the `intSet: set[int] = {` line remains visible and the element lines are hidden
# RECOVER: unfold the `intSet` range so all set elements are visible again
intSet: set[int] = {
    1,
    2,
    3,
}

# SCENARIO: fold multi-line dict literal
# TARGET: `intStrDict: dict[int, str] = {` below `intSet`
# TRIGGER: fold the range from the gutter control on the `intStrDict: dict[int, str] = {` line
# EXPECT: a folding control is visible on the `intStrDict: dict[int, str] = {` line
# VERIFY: after folding, only the `intStrDict: dict[int, str] = {` line remains visible and the key-value lines are hidden
# RECOVER: unfold the `intStrDict` range so all dict entries are visible again
intStrDict: dict[int, str] = {
        1: "one",
        2: "two",
}

# SCENARIO: fold multi-line tuple literal
# TARGET: `myTuple = (` below `intStrDict`
# TRIGGER: fold the range from the gutter control on the `myTuple = (` line
# EXPECT: a folding control is visible on the `myTuple = (` line
# VERIFY: after folding, only the `myTuple = (` line remains visible and the element lines are hidden
# RECOVER: unfold the `myTuple` range so all tuple elements are visible again
myTuple = (
    1,
    2,
    3,
)

# SCENARIO: fold matched outer region across nested region markers
# TARGET: `#region foo1` near the end of the file
# TRIGGER: fold the range from the gutter control on the `#region foo1` line
# EXPECT: a folding control is visible on the `#region foo1` line
# VERIFY: after folding, only `#region foo1` remains visible and the folded range extends through the matching outer `#endregion with text after`
# RECOVER: unfold the `#region foo1` range so the nested region lines and function definitions are visible again

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

# SCENARIO: unmatched region markers are not foldable
# TARGET: `#endregion unmatched` and `#region unmatched` at the end of the file
# TRIGGER: inspect those two lines after the file opens
# EXPECT: no folding control appears on either unmatched region marker
# VERIFY: both unmatched region marker lines remain non-foldable
# RECOVER: none
#endregion unmatched
#region unmatched
