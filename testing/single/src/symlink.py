# SCENARIO: verify navigation resolves both sides of the linked shared-module pair correctly
# TARGET: `shared` and `SharedType` in the imports below
# TRIGGER: create `src/linked/shared_link.py` as a symlink to `src/linked/shared.py`, then use Go to Definition and Find All References on the linked symbols
# EXPECT: the symlink exists before navigation starts
# VERIFY: navigation opens the correct underlying paths for each symbol and Find All References stays scoped to the selected declaration rather than merging both copies indiscriminately
# RECOVER: delete `src/linked/shared_link.py` after the check
from linked.shared import SharedType as shared1
from linked.shared_link import SharedType as shared2


import linked.shared as shared

# SCENARIO: rename `RenameType` through the shared module alias
# TARGET: `RenameType` in `shared.RenameType()` below
# TRIGGER: Rename Symbol
# EXPECT: rename is available on the selected symbol
# VERIFY: the rename updates the selected symbol and undo restores the original text
# RECOVER: undo until the file matches its original text
a = shared.RenameType()


# SCENARIO: rename `SharedType` and observe symlink-backed propagation
# TARGET: `SharedType` in `shared.SharedType()` below
# TRIGGER: Rename Symbol
# EXPECT: rename is available on the selected symbol
# VERIFY: the source declaration is renamed first and the symlinked twin reflects the saved change once the backing file is written
# RECOVER: undo until the file matches its original text and remove the created symlink if needed
b = shared.SharedType()

# SCENARIO: inspect rename availability on the imported module alias `shared`
# TARGET: `shared` in the import below
# TRIGGER: Rename Symbol
# EXPECT: rename availability can be inspected on the imported module alias
# VERIFY: record whether rename remains available even though the alias points at a symlink-backed module path
# RECOVER: undo if any rename is committed
import linked.shared

# SCENARIO: inspect rename availability on the symlinked module import
# TARGET: `shared_link` in the import below
# TRIGGER: Rename Symbol
# EXPECT: rename availability can be inspected on the imported symlink target
# VERIFY: the symlinked module import remains renameable when the underlying workspace flow supports it
# RECOVER: undo if any rename is committed
import linked.shared_link
