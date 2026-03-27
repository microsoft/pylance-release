# This file is used for testing the interactive window in VS Code.
# Requires the Jupyter extension to be installed before running these scenarios.

# SCENARIO: execute the first interactive-window cell
# TARGET: the first `# %%` cell containing `print("Hello world")`
# TRIGGER: run this cell in the interactive window
# EXPECT: the cell can be sent to the interactive window and run successfully
# VERIFY: the interactive window shows `Hello world` as the output from this cell
# RECOVER: leave the interactive window open for the next scenario
# %%
print("Hello world")

# SCENARIO: hover over code inside expanded interactive-window cell content
# TARGET: the `print` token from the first executed cell after expanding that cell in the interactive window
# TRIGGER: in the interactive window, double-click the first executed cell to expand its source content, then hover over `print`
# EXPECT: the executed cell source expands in-place and `print` is visible as a hover target
# VERIFY: the hover surfaces documentation for the built-in `print`
# RECOVER: collapse or close the expanded cell view if it stays open and blocks later steps

# SCENARIO: execute the working-directory cell in the interactive window
# TARGET: the second `# %%` cell containing `import os` and `print(os.getcwd())`
# TRIGGER: run this cell in the interactive window
# EXPECT: the interactive window remains available for another execution
# VERIFY: the interactive window shows a non-empty current working directory string for `os.getcwd()`
# RECOVER: leave the interactive window open for the restart-sensitive scenario below
# %%
import os
print(os.getcwd())

# SCENARIO: execute a cell after restarting the extension host
# TARGET: the third `# %%` cell containing `print("After restart")`
# TRIGGER: restart the extension host, return to this file, and then run this cell in the interactive window
# EXPECT: after the restart, the interactive-window flow is available again for this file
# VERIFY: the interactive window shows `After restart` as the output from this cell
# RECOVER: if the restart closes editors or resets UI state, reopen this file and re-establish only the state needed to run this cell before continuing
# %%
print("After restart")

# SCENARIO: hover over code inside expanded cell content after restart
# TARGET: the `print` token from the `print("After restart")` cell after expanding that cell in the interactive window
# TRIGGER: in the interactive window, double-click the post-restart executed cell to expand its source content, then hover over `print`
# EXPECT: the post-restart executed cell source expands in-place and `print` is visible as a hover target
# VERIFY: the hover surfaces documentation for the built-in `print`
# RECOVER: collapse or close the expanded cell view before moving on

# SCENARIO: interactive-window input completions and execution
# TARGET: the interactive-window input box after the restart-sensitive checks above
# TRIGGER: type `pri` in the interactive-window input box, trigger completions, commit the `print` completion, finish the line as `print("Interactive input OK")`, and execute it
# EXPECT: the completion list includes `print` for the partial `pri` input and the completed line remains executable in the interactive window
# VERIFY: committing the completion inserts `print`, and executing `print("Interactive input OK")` shows `Interactive input OK` in the interactive window output
# RECOVER: clear any leftover text from the interactive-window input box before ending the file run