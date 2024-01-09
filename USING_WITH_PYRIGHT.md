# Pyright and Pylance Together

[Pyright](https://github.com/Microsoft/pyright) is an open source version of a Python type checker that forms the basis for Pylance. Both Pyright and Pylance can be used inside of an IDE to provide a [language server](https://code.visualstudio.com/api/language-extensions/language-server-extension-guide#why-language-server) for Python code.

Pyright can also be used on the [command line](https://github.com/microsoft/pyright/blob/main/docs/command-line.md) to produce json or text output. This can be used in a variety of situations, like a [pre-commit hook](https://github.com/microsoft/pyright/blob/main/docs/ci-integration.md#running-pyright-as-a-pre-commit-hook), or a [github action](https://github.com/jakebailey/pyright-action).

However, Pylance and Pyright don't always produce the same results. There are several reasons why this may happen.

## Pyright version and Pylance's underlying Pyright version are different

Since Pyright and Pylance have different release cadences, there are many times when the latest version of Pylance (even Pylance prerelease) is not based on the latest version of Pyright. If you're using one of the following tools to run Pyright, you can specify your Pylance version (`latest-release`, `latest-prerelease`, or version number) and the tool will use the matching version of Pyright:

- [pyright-action](https://github.com/jakebailey/pyright-action): In v1.8.0+, provide the `pylance-version` option instead of `version`. For more details, see [their documentation](https://github.com/jakebailey/pyright-action#keeping-pyright-and-pylance-in-sync).
- [pyright-python](https://github.com/RobertCraigie/pyright-python): In v1.1.338+, set the `PYRIGHT_PYTHON_PYLANCE_VERSION` environment variable and do not set `PYRIGHT_PYTHON_FORCE_VERSION`. For more details, see [their documentation](https://github.com/RobertCraigie/pyright-python#keeping-pyright-and-pylance-in-sync).

If you are aware of other similar tools that could benefit from having the same behavior, please let us know.

## Type stub differences

Pylance comes bundled with a number of stubs, usually found here in the installation:

```
<pylance-extension-install>/dist/bundled
<pylance-extension-install>/dist/native-stubs
```

For Pyright to produce the same errors as Pylance, it needs to use the same stub files. 

This might be done by copying the contents of each of the bundled Pylance stub folders to a new folder. 

You'd then reference that new folder in your [pyrightconfig.json](https://microsoft.github.io/pyright/#/configuration)

```json
{
    "stubPath": "./pylanceStubs"
}
```

or pyproject.toml

```ini
[tool.pyright]
stubPath="./pylanceStubs"
```

Where `pylanceStubs` contains the contents of the `bundled` and `native-stubs` folders.

We have plans to make this easier in the [future](https://github.com/microsoft/pylance-release/discussions/3638).

## Settings differences

Both Pylance and Pyright have [settings](https://github.com/microsoft/pylance-release#settings-and-customization) to control behavior. For the most part, they use the same values, but the few differences, described below, do have an impact on the analysis.


| Setting | Pylance default | Pyright default | Description | Potential Impact |
|----|----|----|----|----|
| autoSearchPaths | true | false|  Adds 'src' to the list of search paths. | This may change what files are found when analyzing. So if you're getting missing imports for modules in your 'src' tree, this might be why. |
| extraPaths | `PYTHONPATH` | [ ] | Additional search paths that will be used when searching for modules imported by files. | Pylance includes paths found in the `PYTHONPATH` environment variable and the `PYTHONPATH` definition from your [`.env` file](https://code.visualstudio.com/docs/python/environments#_environment-variable-definitions-file). Pyright ignores `.env` files and treats paths from the `PYTHONPATH` environment variable as third party library paths. This results in a difference in prioritization of these paths when resolving imports. |
| typeCheckingMode | off | standard | Determines what diagnostics are shown. | Pylance defaults to `off`. If you want to guarantee this is the same as Pyright, set it to `standard` (or whatever you want to enforce) by specifying it in your settings.json. |

Here's an example `pyrightconfig.json` you would use to ensure Pylance and Pyright both picked up the same settings:

```json
{
    "autoSearchPaths": false,
    "extraPaths": [], // Include paths from PYTHONPATH env var and .env definition
    "typeCheckingMode": "standard"
}
```

or pyproject.toml

```ini
[tool.pyright]
autoSearchPaths=false
extraPaths=[] # Include paths from PYTHONPATH env var and .env definition
typeCheckingMode="standard"
```


## Diagnostic severity overrides

Both Pylance and Pyright support a [`python.analysis.diagnosticSeverityOverrides`](https://microsoft.github.io/pyright/#/configuration?id=diagnostic-rule-defaults) setting. Differences in this setting have a direct impact on the diagnostics returned. If you were attempting to get the same error output from both Pylance and Pyright, ensure that they are using the same value for this setting.

By default they are the same except for one value:  `reportShadowedImports`.

In order to have Pylance and Pyright behave the same, you would set this value in a `pyrightconfig.json`

```json
{
    "reportShadowedImports": "warning"
}
```

or pyproject.toml

```ini
[tool.pyright]
reportShadowedImports="warning"
```
