# SCENARIO: trigger signature help for `print()`
# TARGET: the cursor position between `(` and `)` in `print()` below
# TRIGGER: Trigger Parameter Hints
# EXPECT: the cursor is between the empty parentheses in `print()`
# VERIFY: signature help opens for `print` and shows the tooltip, overload information, and an active parameter highlight
# RECOVER: none
print()

# SCENARIO: trigger signature help after a named argument
# TARGET: the cursor position immediately after `sep=` in the call below
# TRIGGER: Trigger Parameter Hints
# EXPECT: the cursor is after `sep=` in `print("hello", sep=)`
# VERIFY: signature help opens for `print` and the active parameter highlight is on `sep`
# RECOVER: none
print("hello", sep=)