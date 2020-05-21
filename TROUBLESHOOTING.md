# Troubleshooting

If you're having trouble with the langauge server, check the below for information which
may help. If something isn't covered here, please file an issue with the information given
in [Filing an issue](#filing-an-issue).


## Known issues

None at this time.


## Requirements

Python is a requirement for the language server to run. In VS Code, an interpreter
_must_ be selected in order for the language server to properly initialize. If your
language server fails to start, be sure that you have selected an interpreter.


## Common questions and issues

### Unresolved import warnings

If you're getting a warning about an unresolved import, first ensure that the
package is installed into your environment if it is a library (`pip`, `pipenv`, etc).
If the warning is about importing _your own_ code (and not a library), continue reading.

The language server treats the workspace root (i.e. folder you have opened) as
the main root of user module imports. This means that if your imports are not relative
to this path, the language server will not be able to find them. This is common
for users who have a `src` directory which contains their code, a directory for
an installable package, etc. Note that the `src` scenario is automatically detected
by the language server, so no configuration is necessary in that case.

These extra roots must be specified to the language server. The easiest way to
do this (with the VS Code Python extension) is to create a workspace configuration
which sets `python.analysis.extraPaths`. For example, if a project uses a
`sources` directory, then create a file `.vscode/settings.json` in the workspace
with the contents:


```json
{
    "python.analysis.extraPaths": ["./sources"]
}
```

This list can be extended to other paths within the workspace (or even with
code outside the workspace in more complicated setups). Relative paths will
be taken as relative to the workspace root.


### "Server initialization failed"

If you see this message, ensure that an interpreter has been selected. (See [Requirements](#requirements)).


## Filing an issue

When filing an issue, make sure you do the following:

- Check existing issues for the same problem (also see the "Known Issues" section above for widespread problems).
- Enable trace logging by adding `"python.analysis.logLevel": "Trace"` to your settings.json configuration file.
    - Adding this will cause a large amount of info to be printed to the Python output panel.
    This should not be left long term, as the performance impact of the logging is significant.
- State which language server version you are using: 
    -   To find your version: Select "View: Toggle Output" from the command palette (Ctrl+Shift+P on Windows/Linux, Command+Shift+P on macOS), then select "Python" in the dropdown on the right ("Python Language Server" if running Insiders build of VS Code). Look for the line Microsoft Python Language Server version X in the console.
- State the environment where your code is running; i.e. Python version, the virtual environment type, etc.
    - If using a virtual environment, please include the requirements.txt file.
    - If working with a conda environment, attach the environment.yml file.
- A code example (or any other additional information) we can use to reproduce the issue.
