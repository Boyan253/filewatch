#!/usr/bin/env python3
"""Watch a directory and run a command when anything changes."""

import argparse
import os
import subprocess
import sys
import time

__version__ = "0.1.0"

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist",
             "build", ".pytest_cache", ".mypy_cache"}


def snapshot(root, extensions=(), skip_dirs=SKIP_DIRS):
    """Map every watched file to its mtime and size."""
    state = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for name in filenames:
            if extensions and not name.endswith(tuple(extensions)):
                continue
            path = os.path.join(dirpath, name)
            try:
                stat = os.stat(path)
            except OSError:
                continue
            state[path] = (stat.st_mtime_ns, stat.st_size)
    return state


def diff(before, after):
    """Return (added, removed, changed) path lists."""
    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed = sorted(p for p in set(before) & set(after) if before[p] != after[p])
    return added, removed, changed


def describe(added, removed, changed, limit=3):
    parts = []
    for label, paths in (("+", added), ("-", removed), ("~", changed)):
        for path in paths[:limit]:
            parts.append("%s%s" % (label, os.path.basename(path)))
    total = len(added) + len(removed) + len(changed)
    if total > limit:
        parts.append("(%d more)" % (total - limit))
    return " ".join(parts)


def run(command, shell=False):
    print("\n--- %s ---" % time.strftime("%H:%M:%S"), file=sys.stderr)
    return subprocess.run(command, shell=shell).returncode


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", action="version",
                    version="%(prog)s " + __version__)
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("-e", "--ext", action="append", default=[],
                    help="only watch these extensions, e.g. -e .py -e .toml")
    ap.add_argument("-i", "--interval", type=float, default=0.6, help="poll interval")
    ap.add_argument("--debounce", type=float, default=0.3,
                    help="wait for changes to settle before running")
    ap.add_argument("--initial", action="store_true", help="run once at startup")
    ap.add_argument("--shell", action="store_true")
    ap.add_argument("command", nargs=argparse.REMAINDER)
    args = ap.parse_args(argv)

    command = [c for c in args.command if c != "--"]
    if not command:
        ap.error("give a command after --, e.g. filewatch.py src -e .py -- pytest")
    if args.shell:
        command = " ".join(command)

    root = os.path.abspath(args.path)
    state = snapshot(root, args.ext)
    print("watching %s (%d files), ctrl-c to stop" % (root, len(state)), file=sys.stderr)
    if args.initial:
        run(command, args.shell)

    try:
        while True:
            time.sleep(args.interval)
            current = snapshot(root, args.ext)
            added, removed, changed = diff(state, current)
            if not (added or removed or changed):
                continue
            time.sleep(args.debounce)
            current = snapshot(root, args.ext)
            added, removed, changed = diff(state, current)
            state = current
            print(describe(added, removed, changed), file=sys.stderr)
            run(command, args.shell)
    except KeyboardInterrupt:
        print("\nstopped", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
