# PREREQ: set `editor.autoIndent` to `none` before running the indentation scenarios in this file
# PREREQ: set `autoFormatStrings` to `true` before running the string-prefix scenarios in this file

# SCENARIO: press Enter after a `for` header and confirm the next line is indented
# TARGET: the `:` in `for a in range(10):` below
# TRIGGER: place the cursor immediately after the `:` and press Enter
# EXPECT: the `for` statement is not yet followed by a body line
# VERIFY: a new blank line is inserted under the `for` header and the cursor lands one indentation level inside the loop body
# RECOVER: undo until the file matches its original text
for a in range(10):

__break_for_statement_ # its here so that code after this is not recognized as body of the for statement.

# SCENARIO: press Enter after a simple assignment and confirm no extra indentation is added
# TARGET: the closing `"` in `ch = "a"` below
# TRIGGER: place the cursor immediately after the string literal and press Enter
# EXPECT: the assignment line is complete and not inside an unfinished block
# VERIFY: a new blank line is inserted directly below `ch = "a"` and the cursor lands at the same indentation level as the assignment line
# RECOVER: undo until the file matches its original text
ch = "a"

# SCENARIO: press Enter after a `match` header and confirm the next line is indented
# TARGET: the `:` in `match ch:` below
# TRIGGER: place the cursor immediately after the `:` and press Enter
# EXPECT: the `match` statement is not yet followed by a case line
# VERIFY: a new blank line is inserted under `match ch:` and the cursor lands one indentation level inside the `match` block
# RECOVER: undo until the file matches its original text
match ch:
    # SCENARIO: press Enter after a `case` header and confirm the next line is indented
    # TARGET: the `:` in `case "a":` below
    # TRIGGER: place the cursor immediately after the `:` and press Enter
    # EXPECT: the `case` statement is not yet followed by a body line
    # VERIFY: a new blank line is inserted under `case "a":` and the cursor lands one indentation level inside that case body
    # RECOVER: undo until the file matches its original text
    case "a":

__break_for_case_ # its here so that code after this is not recognized as body of the case statement.


if ch == "a":
    pass
    # SCENARIO: type `:` after `else` and confirm the clause is dedented into the correct position
    # TARGET: `else` on the line below
    # TRIGGER: place the cursor immediately after `else` and type `:`
    # EXPECT: the line starts as an incorrectly indented `else` directly under `pass`
    # VERIFY: the line becomes `else:` and is moved to align with the matching `if ch == "a":` line
    # RECOVER: undo until the file matches its original text
    else

# SCENARIO: typing `{` in a plain string adds an `f` prefix when auto-format-strings is enabled
# TARGET: each empty string literal in `x`, `y`, `z`, and `w` below, one literal at a time
# TRIGGER: with `autoFormatStrings` enabled, place the cursor inside the literal and type `{`
# EXPECT: each target literal starts without an `f` prefix before typing `{`
# VERIFY: the edited literal gains a leading `f` automatically as soon as `{` is typed
# RECOVER: undo after each trial until the file matches its original text
x = ""
y = ''
z = """""""
w = ''''''

# SCENARIO: typing `{` in an existing f-string does not add a second `f`
# TARGET: each prefixed string literal in `a`, `b`, `c`, and `d` below, one literal at a time
# TRIGGER: with `autoFormatStrings` enabled, place the cursor inside the literal and type `{`
# EXPECT: each target literal already starts with exactly one `f` prefix before typing `{`
# VERIFY: the edited literal still has exactly one `f` prefix after `{` is typed
# RECOVER: undo after each trial until the file matches its original text
# NOTE: this covers the known issue tracked at https://github.com/microsoft/pylance-release/issues/5703
a = f""
b = f''
c = f"""""""
d = f''''''

# SCENARIO: typing `{` in an `r` or `b` string does not replace the existing prefix with `f`
# TARGET: the prefixed string literals in `e` and `f` below
# TRIGGER: with `autoFormatStrings` enabled, place the cursor inside each literal and type `{`
# EXPECT: `e` starts with `r` and `f` starts with `b` before typing `{`
# VERIFY: the edited literals keep their original `r` or `b` prefix and do not gain an additional `f` prefix
# RECOVER: undo after each trial until the file matches its original text
e = r""
f = b''
