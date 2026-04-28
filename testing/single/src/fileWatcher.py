# PREREQ: keep `src/lib/changeExternally.py` closed in VS Code for the entire scenario
# PREREQ: make the helper-file edit from an external editor such as Notepad, not from VS Code
# SCENARIO: detect an external file change and clear the dependent import error
# TARGET: `TypeChangedExternally` on the import line and on the constructor call below in this file
# TRIGGER: open `src/lib/changeExternally.py` in Notepad, uncomment `class TypeChangedExternally: pass`, and save the file externally
# EXPECT: before the external save, this file shows the missing-symbol error caused by `TypeChangedExternally` being commented out in `src/lib/changeExternally.py`
# VERIFY: after the external save and file-watcher reanalysis, the import of `TypeChangedExternally` and the `TypeChangedExternally()` call below no longer show diagnostics
# RECOVER: re-comment `class TypeChangedExternally: pass` in `src/lib/changeExternally.py` from the external editor, save again, and wait for the original diagnostics to return before the next scenario
from lib.changeExternally import TypeChangedExternally

TypeChangedExternally()