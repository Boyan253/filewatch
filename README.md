# filewatch

> Run a command whenever files change - a dependency-free watch loop with debouncing.

## Why

You want `pytest` to run every time you save. The usual answers install a
watcher package with a native extension. This is one stdlib file that polls,
which is fast enough for any repo you would edit by hand.

## Usage

```
python filewatch.py src -e .py -- pytest -q
python filewatch.py . -e .go -- go build ./...
python filewatch.py docs -e .md --initial -- python mdtoc.py README.md --write
python filewatch.py . --shell -- "npm run build && npm test"
```

Stop with ctrl-c.

## How it works

Every `--interval` seconds it takes a snapshot of mtime and size for every
watched file and compares it with the previous one. When something differs it
waits `--debounce` seconds and re-checks, so a save that touches twenty files
triggers one run, not twenty.

## Options

| flag | effect |
|------|--------|
| `-e .py` | only watch these extensions (repeatable) |
| `-i 0.6` | poll interval in seconds |
| `--debounce 0.3` | settle time before running |
| `--initial` | run once at startup instead of waiting for a change |
| `--shell` | run the command through the shell, for pipes and `&&` |

`.git`, `node_modules`, `__pycache__`, virtualenvs and build directories are
never watched.
