from __future__ import annotations

from functools import lru_cache
from pathlib import Path


def _search_roots(module_name: str, roots: tuple[str, ...]) -> str | None:
    """Look up a module by walking a small set of known roots."""
    module_path = Path(*module_name.split("."))
    for root in roots:
        candidate = Path(root) / module_path
        for suffix in (".py", "/__init__.py"):
            target = candidate.with_suffix(suffix) if suffix == ".py" else candidate / "__init__.py"
            if target.exists():
                return str(target)
    return None


@lru_cache(maxsize=2048)
def resolve_module_path(module_name: str, roots: tuple[str, ...]) -> str | None:
    """Memoize expensive filesystem lookups for repeated imports."""
    return _search_roots(module_name, roots)


def resolve_many(module_names: list[str], roots: tuple[str, ...]) -> list[str | None]:
    return [resolve_module_path(module_name, roots) for module_name in module_names]


if __name__ == "__main__":
    demo_roots = ("C:/workspace/project", "C:/workspace/vendor")
    module_names = ["pkg.core", "pkg.core", "pkg.util", "pkg.helper"]
    print(resolve_many(module_names, demo_roots))
