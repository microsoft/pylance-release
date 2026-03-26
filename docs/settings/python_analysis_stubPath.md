# Understanding `python.analysis.stubPath` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It provides type checking, completions, navigation, and import resolution features that depend on accurate type information.

The `python.analysis.stubPath` setting tells Pylance where to look for custom package stub files that you maintain in your workspace.

## What `python.analysis.stubPath` does

`python.analysis.stubPath` points to a directory that contains custom type stub files (`.pyi`).

These stubs let you provide type information for packages that:

- do not ship with usable type information
- need local corrections or supplements
- expose compiled modules that are hard to analyze from source

The default value is `typings`.

This default does not generate any stubs for you. It simply means Pylance looks for custom stubs in a workspace folder named `typings` if you create one.

## When to use `stubPath`

Use `python.analysis.stubPath` when you want to add or override type information for specific packages in your project.

Common cases include:

- adding stubs for an internal library
- supplementing a third-party package that is missing some annotations
- providing stubs for compiled extensions
- correcting package-specific typing without replacing the full typeshed tree

If you need to override the full typeshed source for standard-library or typeshed fallback stubs, use [`python.analysis.typeshedPaths`](python_analysis_typeshedPaths.md) instead.

## How paths are resolved

If you provide a relative path, Pylance resolves it relative to the workspace root.

For example:

```json
"python.analysis.stubPath": "typings"
```

means Pylance looks in the workspace-root `typings` directory.

This is important when you edit `.vscode/settings.json`: the path is not resolved relative to the `.vscode` folder itself.

## Expected directory structure

Each package should have its own subdirectory under the stub path, mirroring the package layout that Python imports.

Example:

```text
my_project/
├── src/
├── typings/
│   ├── requests/
│   │   └── __init__.pyi
│   └── my_internal_lib/
│       ├── __init__.pyi
│       └── api.pyi
```

Example setting:

```json
"python.analysis.stubPath": "typings"
```

## Workflow: add custom stubs for a package

1. Create the stub root directory, such as `typings`.
2. Add a subdirectory for the package you want to describe.
3. Add `.pyi` files that mirror the package's module structure.
4. Point `python.analysis.stubPath` at that directory if you are not using the default `typings` location.
5. Reload the window or restart the language server if Pylance does not pick up the new stubs immediately.

Example:

```json
"python.analysis.stubPath": "./typings"
```

And a matching stub file:

```python
# typings/examplelib/__init__.pyi

def process(data: bytes) -> str: ...
```

## Partial stubs

`python.analysis.stubPath` also supports PEP 561 partial stub packages.

A partial stub package lets you provide stubs for only part of a package instead of replacing the whole package surface.

This is useful when:

- a package already has some usable inline typing, but parts of it are missing
- you want to patch only a few modules or symbols
- generated stubs are incomplete and you want to layer manual fixes on top

In a partial stub package, the directory name ends with `-stubs`, and the package contains a `py.typed` file whose contents include `partial`.

Example:

```text
typings/
└── examplelib-stubs/
	├── __init__.pyi
	├── api.pyi
	└── py.typed
```

Example `py.typed` contents:

```text
partial
```

With that structure, Pylance can merge the partial stub package with the installed library rather than requiring you to stub every module up front.

Use a partial stub package when you want to fill gaps. Use a regular full stub package when you want the stub package to define the package entirely.

## How `stubPath` relates to `useLibraryCodeForTypes`

If a library has weak or missing type information, a focused fix is often to add custom stubs through `python.analysis.stubPath` rather than disabling [`python.analysis.useLibraryCodeForTypes`](python_analysis_useLibraryCodeForTypes.md) for every library.

In many cases, a better fix is to add the missing package stubs under `python.analysis.stubPath` so Pylance can use explicit type information instead of falling back to source-code inference.

This approach is usually more targeted than turning off library-code analysis for every library.

## How `stubPath` differs from `typeshedPaths`

Use [`python.analysis.stubPath`](python_analysis_stubPath.md) for package-specific custom stubs that live in a stub directory such as `typings`.

Use [`python.analysis.typeshedPaths`](python_analysis_typeshedPaths.md) when you want Pylance to use a custom typeshed tree for standard-library stubs or typeshed fallback stubs.

In practice:

- `stubPath` is the normal choice for project-local or package-local stub work
- `typeshedPaths` is an advanced setting for replacing the typeshed source tree that Pylance consults

## Common problems

### Pylance does not seem to use my stubs

Check the following:

- the path resolves from the workspace root
- the package directory name matches the import name
- the stub file names mirror the real module structure
- the setting points at the stub root, not directly at one package subdirectory

### My stubs work for one package but not another

Make sure each package has its own subdirectory under the configured stub root.

For example, this is correct:

```text
typings/
├── package_a/
└── package_b/
```

### Should I use `stubPath` or `typeshedPaths`?

If the problem is a specific package, use `stubPath`.

If the problem is your custom copy of typeshed or you need to replace standard-library/typeshed fallback stubs, use `typeshedPaths`.

## Frequently asked questions

### Does `stubPath` support multiple directories?

No. `python.analysis.stubPath` accepts a single directory path.

### Does `stubPath` replace the full bundled typeshed?

No. It is for custom package stubs. It does not replace the full typeshed tree.

### Can I use an absolute path?

Yes. You can use either an absolute path or a workspace-relative path.

### What if I leave the setting alone?

By default, Pylance uses `typings` as the stub directory name. If that directory does not exist in your workspace, there are simply no extra custom stubs to load.

---

For more information on Pylance settings and customization, refer to the [Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference) documentation.
