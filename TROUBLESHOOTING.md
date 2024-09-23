# Troubleshooting

If you're having trouble with the language server, check the below for information which
may help. If something isn't covered here, please file an issue with the information given
in [Filing an issue](#filing-an-issue).

## Known issues

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
by the language server, so no configuration is necessary in that particular case.

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

Note that if you are coming to Pylance from using the Microsoft Python Language Server, this setting has changed from `python.autoComplete.extraPaths` to `python.analysis.extraPaths`.

### Editable install modules not found

If you want to use static analysis tools with an editable install, you should configure the editable install to use `.pth` files that contain file paths rather than executable lines (prefixed with `import`) that install import hooks. See your package manager’s documentation for details on how to do this. We have provided some basic information for common package managers below.

Import hooks can provide an editable installation that is a more accurate representation of your real installation. However, because resolving module locations using an import hook requires executing Python code, they are not usable by Pylance and other static analysis tools. Therefore, if your editable install is configured to use import hooks, Pylance will be unable to find the corresponding source files.

#### pip / setuptools
`pip` (`setuptools`) supports two ways to avoid import hooks:
- [compat mode](https://setuptools.pypa.io/en/latest/userguide/development_mode.html#legacy-behavior)
- [strict mode](https://setuptools.pypa.io/en/latest/userguide/development_mode.html#strict-editable-installs)

#### Hatch / Hatchling
[Hatchling](https://hatch.pypa.io/latest/config/build/#dev-mode) uses path-based `.pth` files by
default. It will only use import hooks if you set `dev-mode-exact` to `true`.

#### PDM
[PDM](https://pdm.fming.dev/latest/pyproject/build/#editable-build-backend) uses path-based `.pth`
files by default. It will only use import hooks if you set `editable-backend` to
`"editables"`.

### Migrating from the Microsoft Python Language Server to Pylance

If you are moving from the Microsoft Python Language Server over to Pylance, a good place to start is by reading [our migration doc](MIGRATING_TO_PYLANCE.md) which outlines a couple notable changes between the language servers.

### Minimum VS Code version

To use Pylance, you will need to be using VS Code version 1.57 or above.

### Pylance does not start up, or shows an error on startup

To use Pylance, you must be running an official build of VS Code. If you've verified that
you are running an official build and are still running into issues, please file a bug report.

### Packages do not resolve on install when using WSL

If you are using Pylance in a WSL environment, make sure your workspace is located under a WSL folder (`/home/...`) and not shared with Windows (`/mnt/...`).
See issues [#1443](https://github.com/microsoft/pylance-release/issues/1443#issuecomment-867863124) and [vscode-remote-release#5000](https://github.com/microsoft/vscode-remote-release/issues/5000).

### Pylance is crashing

Although we attempt to prevent Pylance from crashing, sometimes certain configurations can cause problems for Pylance. One particular problem is the amount of memory that Pylance is allowed to allocate when running inside of VS Code. VS Code ships with [pointer compression](https://www.electronjs.org/blog/v8-memory-cage) enabled. This makes VS Code run faster, but limits the amount of memory that Pylance can use. With some configurations, we may need more than 4GB of memory in order to analyze your project. 

If you think you're hitting an out-of-memory situation, you can alleviate this problem in a number of ways:

#### Provide your own [Node.js](https://nodejs.org/en/download/) executable to run Pylance with. 

Pylance (by default) runs using VS Code's Node.js executable (which has the 4GB limit). 

To specify your own Node.js executable, set this setting in your User settings.json and restart VS Code:

```json
"python.analysis.nodeExecutable": "<path to node.js exe>"
```

The location of your User settings.json depends upon how you're connecting:

- Local - Stored in a [local](https://code.visualstudio.com/docs/getstarted/settings#_settingsjson) file. This can be found with the command `Preferences: Open User Settings.json`.
- Remote - Stored on the remote machine. Example `/home/user/.vscode-server/data/Machine/settings.json`

You should make sure to use a version of node that is greater than or equal to what VS Code is using. You can determine the version of VS Code's node in the `Help | About` menu.

#### Increase memory limit for VS code (remote only)

For those using `vscode-server` remotely, you can increase the memory limit by setting the `NODE_OPTIONS` environment variable in your shell configuration.

On Linux or Mac, add `export NODE_OPTIONS="--max-old-space-size=8192"` to either your `.xxx_profile` or `.xxxrc` file. On Windows, add `set NODE_OPTIONS=--max-old-space-size=8192` to your batch file to update your system environment variable, or open the `System Properties` window and add `NODE_OPTIONS=--max-old-space-size=8192`.

For more details, visit [--max-old-space-size](https://nodejs.org/api/cli.html#--max-old-space-sizesize-in-megabytes)

#### Exclude unneeded `*.py` files from analysis

To minimize memory usage by Pylance, exclude unneeded `*.py` files using `python.analysis.exclude`. For instance, you can add `"python.analysis.exclude": ["**/testFiles/*.py"]` to your `.vscode/settings.json`.

For environments with multiple root workspaces, place the `.vscode/settings.json` in the root directory of each workspace instead of using `settings` section in a `*.code-workspace` file.

## Filing an issue

When filing an issue, make sure you do the following:

-   Check existing issues for the same problem (also see the "Known Issues" section above for widespread problems).
-   Enable trace logging by adding `"python.analysis.logLevel": "Trace"` to your settings.json configuration file or by using the `Pylance: Start Logging` command.
    -   Adding this will cause a large amount of info to be printed to the Python output panel.
        This should not be left long term, as the performance impact of the logging is significant.
        Use `Pylance: Stop Logging` to turn off the additional info.
-   Select "View: Toggle Output" from the command palette (Ctrl+Shift+P on Windows/Linux, Command+Shift+P on macOS), then select "__Python Language Server__" in the dropdown on the right.  
-   Copy the entire log starting with "Pylance language server XXX (pyright xxx) starting"
    
-   State the environment where your code is running; i.e. Python version, the virtual environment type, etc.
    -   If using a virtual environment, please include the requirements.txt file.
    -   If working with a conda environment, attach the environment.yml file.
-   A code example (or any other additional information) we can use to reproduce the issue.
