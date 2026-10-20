# Wayedits

Simple plain-text editor built with Python and PySide6 (Qt 6).

## Run from source

Requires [uv](https://docs.astral.sh/uv/) and Python 3.14+.

```bash
uv sync
uv run python main.py
```

Open a file on launch:

```bash
uv run python main.py path/to/file.txt
```

## Build single executable

```bash
uv sync --dev
uv run pyinstaller --clean --noconfirm wayedits.spec
```

The binary is written to `dist/wayedits`.
