# filewatch

> Run a command whenever files change - a dependency-free watch loop with debouncing.

## Why

You want `pytest` to run every time you save. The usual answers install a
watcher package with a native extension. This is one stdlib file that polls,
which is fast enough for any repo you would edit by hand.
