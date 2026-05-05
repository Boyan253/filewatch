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
