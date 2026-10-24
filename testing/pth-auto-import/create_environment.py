import argparse
import os
from pathlib import Path
import subprocess
import venv


def get_venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--remove-pth", action="store_true")
    args = parser.parse_args()

    workspace_root = Path(__file__).resolve().parent
    venv_dir = workspace_root / ".venv"
    if not venv_dir.exists():
        venv.EnvBuilder(with_pip=False).create(venv_dir)

    python_path = get_venv_python(venv_dir)
    site_packages = Path(
        subprocess.check_output(
            [
                python_path,
                "-c",
                "import site; print(site.getsitepackages()[0])",
            ],
            text=True,
        ).strip()
    )
    pth_path = site_packages / "portfolio.pth"

    if args.remove_pth:
        pth_path.unlink(missing_ok=True)
        print(f"Removed {pth_path}")
        return

    pth_path.write_text(f"{workspace_root}\n", encoding="utf-8")
    print(f"Wrote {pth_path}")
    print(f"Contents: {workspace_root}")


if __name__ == "__main__":
    main()
