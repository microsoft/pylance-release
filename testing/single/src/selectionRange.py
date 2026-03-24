from typing import Literal


def foo(ch: Literal["a", "b", "c"]):
    match ch:
        case "a":
            pass
        case "b":
            for i in range(10):
                # SCENARIO: expand selection from a nested print call
                # TARGET: `print` in `print(f"{ch}{i}")` inside the `case "b"` loop
                # TRIGGER: Expand Selection, then repeat the same command
                # EXPECT: the cursor starts on the `print` token in the nested call below
                # VERIFY: skip-ready because the legacy checklist says only that the selection should expand "as expected" and does not define the required selection sequence or final range
                print(f"{ch}{i}")
        case "c":
            pass