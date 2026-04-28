# PREREQ: this file has two valid workspace-mode outcomes; use the scenario that matches how the workspace was opened
# PREREQ: use `testing/test.code-workspace` for the multiroot scenario, or open only `testing/single` for the single-folder scenario

# SCENARIO: in multiroot mode, resolve the `日本` module successfully
# TARGET: `日本` on the import line below and on the attribute-access line after it
# TRIGGER: open this file from the multiroot workspace defined by `testing/test.code-workspace` and wait for analysis
# EXPECT: the sibling workspace root that contains the `日本` module is part of the opened workspace
# VERIFY: `import 日本` has no import-resolution diagnostic and `日本.` resolves without an unresolved-import error
# RECOVER: leave file text unchanged

# SCENARIO: in single-folder mode, report the missing `日本` import as unresolved
# TARGET: `日本` on the import line below
# TRIGGER: open only the `testing/single` folder and wait for analysis
# EXPECT: the workspace does not include the root that contains the `日本` module
# VERIFY: `import 日本` shows an import-resolution diagnostic in the editor
# RECOVER: leave file text unchanged

import 日本
日本.