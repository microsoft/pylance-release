# Understanding `python.analysis.typeshedPaths` in Pylance

[Pylance](https://marketplace.visualstudio.com/items?itemName=ms-python.vscode-pylance) is a fast, feature-rich language support extension for Python in Visual Studio Code, powered by the Pyright static type checker. It uses typeshed data for standard-library typing and for some fallback stub resolution.

The `python.analysis.typeshedPaths` setting lets you point Pylance at a custom typeshed tree instead of relying only on the bundled copy.

## What `python.analysis.typeshedPaths` does

`python.analysis.typeshedPaths` is an array of paths to search for typeshed modules.

The default value is an empty array:

```json
"python.analysis.typeshedPaths": []
```

When the setting is left empty, Pylance uses its bundled typeshed data.

When you configure the setting, Pylance uses only the first entry in the array.

## When to use `typeshedPaths`

Use `python.analysis.typeshedPaths` when you want Pylance to consult a custom typeshed tree for:

- standard-library stubs
- typeshed fallback stubs for third-party packages
- local experiments with updated or patched typeshed content

This is an advanced setting. If you only need custom stubs for a few packages in your project, [`python.analysis.stubPath`](python_analysis_stubPath.md) is usually the better choice.

## Situations where `typeshedPaths` can help

Most users do not need this setting. It becomes useful when your runtime or typing environment differs enough from bundled CPython-oriented typeshed data that you need to supply your own tree.

Examples include:

- embedded or alternate Python runtimes such as MicroPython, where available builtins and standard-library-style modules differ from normal CPython expectations
- internal or patched Python distributions where your team maintains a modified typeshed tree
- testing or validating a newer local typeshed checkout before those stubs are available in the bundled copy
- specialized environments where you need to replace typeshed fallback stubs with your own curated versions

For example, MicroPython users often work with modules and builtins that do not line up with the normal CPython standard library. In that situation, `typeshedPaths` can make sense if you maintain a complete custom typeshed-style tree for that runtime.

If you only need stubs for a few runtime-specific modules, [`python.analysis.stubPath`](python_analysis_stubPath.md) is usually simpler.

## How paths are resolved

If you provide a relative path, Pylance resolves it relative to the workspace root.

Example:

```json
"python.analysis.typeshedPaths": [
    "vendor/typeshed"
]
```

That points Pylance at the workspace-root `vendor/typeshed` directory.

## Important behavior: only the first path is used

Although the VS Code setting is an array, Pylance uses only the first configured entry.

For example:

```json
"python.analysis.typeshedPaths": [
    "vendor/typeshed",
    "other/typeshed"
]
```

Pylance uses `vendor/typeshed` and ignores the second path.

If you need multiple custom changes, put them into one typeshed tree rather than expecting multiple directories to be merged.

## Expected directory structure

The configured path should point to the root of a typeshed-style directory layout.

Typical structure:

```text
vendor/
└── typeshed/
    ├── stdlib/
    └── stubs/
```

Treat this as a full typeshed-style tree, not as a small patch folder.

If that tree is incomplete, Pylance may lose access to standard-library or fallback stub information that would otherwise come from the bundled typeshed.

In particular:

- provide the full root that contains `stdlib`
- include a `stubs` directory when you rely on third-party typeshed fallback stubs
- do not point this setting at a folder that contains only a few standalone `.pyi` files

If you only need to patch a few packages, use [`python.analysis.stubPath`](python_analysis_stubPath.md) instead of `typeshedPaths`.

## Workflow: use a custom typeshed tree

1. Create or clone a typeshed-style directory tree.
2. Apply the changes you need under `stdlib` or `stubs`.
3. Point `python.analysis.typeshedPaths` at the root of that tree.
4. Reload the window or restart the language server if Pylance does not pick up the change immediately.

Example:

```json
{
    "python.analysis.typeshedPaths": ["vendor/typeshed"]
}
```

## How `typeshedPaths` differs from `stubPath`

Use [`python.analysis.typeshedPaths`](python_analysis_typeshedPaths.md) for a custom typeshed tree.

Use [`python.analysis.stubPath`](python_analysis_stubPath.md) for package-specific custom stubs in a directory such as `typings`.

In practice:

- `typeshedPaths` changes where Pylance looks for typeshed content
- `stubPath` adds a custom package-stub directory for your own or third-party package stubs

## How `typeshedPaths` relates to `useLibraryCodeForTypes`

If a problem comes from missing or incorrect typeshed-based typing information, a custom `typeshedPaths` tree may be a better fix than disabling [`python.analysis.useLibraryCodeForTypes`](python_analysis_useLibraryCodeForTypes.md).

`useLibraryCodeForTypes` controls whether Pylance falls back to parsing library source code when stubs are missing. `typeshedPaths` instead changes the stub source that Pylance consults for typeshed content.

## Common problems

### Built-in names or standard-library modules start behaving strangely

That often means the custom typeshed tree is incomplete or points at the wrong directory level.

Make sure the configured path points at the full typeshed root that contains `stdlib` and, when needed, `stubs`.

### I configured multiple paths but only one seems to matter

That is expected. Pylance uses only the first entry in `python.analysis.typeshedPaths`.

### Should I use `typeshedPaths` for one package fix?

Usually no. For a package-specific fix, [`python.analysis.stubPath`](python_analysis_stubPath.md) is typically simpler and more targeted.

## Frequently asked questions

### Does `typeshedPaths` replace the bundled typeshed behavior?

It redirects Pylance to a custom typeshed tree for typeshed lookup rather than relying only on the bundled copy, so an incomplete custom tree can change or reduce available type information.

### Can I use more than one custom typeshed directory?

No. The setting accepts an array, but Pylance uses only the first configured path.

### Can I use an absolute path?

Yes. You can use either an absolute path or a workspace-relative path.

### When should I prefer `stubPath` instead?

Prefer `stubPath` when you are adding or correcting stubs for specific packages rather than replacing the full typeshed source tree.

### Can this help with runtimes like MicroPython?

Potentially, yes, but only if you have a complete enough typeshed-style tree for that runtime. If you point `typeshedPaths` at a partial folder that does not provide the needed `stdlib` layout, you can end up with missing or incorrect built-in and standard-library typing.

## See Also

- [How to Set Up a Python Monorepo](../howto/monorepo-setup.md) — bundled typeshed and custom typeshed paths

## Troubleshooting

If your custom typeshed isn't being picked up:

1. **Check the Output panel**: Open **Output → Pylance** for errors about missing or malformed typeshed directories.
2. **Enable trace logging**: Add `"python.analysis.logLevel": "Trace"` to settings and look for typeshed resolution messages. See [Reading Pylance Logs](../howto/reading-pylance-logs.md).
3. **Verify directory structure**: The path must point to a directory containing a `stdlib/` subdirectory with a `VERSIONS` file.
4. **Restart**: Run **"Python: Restart Language Server"** after changing this setting.
5. **Config file override**: If a `pyrightconfig.json` exists with `typeshedPath` set, the VS Code setting is ignored. See [Settings Troubleshooting](../howto/settings-troubleshooting.md).

---

For more information on Pylance settings and customization, refer to the [Pylance Settings and Customization](https://code.visualstudio.com/docs/python/settings-reference) documentation.
