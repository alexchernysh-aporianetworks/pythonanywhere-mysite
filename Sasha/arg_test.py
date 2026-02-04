#!/usr/bin/env python3
"""
Test script for PythonAnywhere Scheduled Tasks.

Behavior:
  - No arguments: prints one message.
  - With arguments: prints a different message + parsed values.

Examples (local):
  python arg_test.py
  python arg_test.py --name Sasha
  python arg_test.py --count 3 --flag
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import socket
import sys


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="arg_test.py",
        description="Simple arg/no-arg behavior check for scheduled tasks.",
    )
    parser.add_argument("--name", default=None, help="Optional name to print.")
    parser.add_argument(
        "--count",
        type=int,
        default=0,
        help="Optional integer; influences output when provided.",
    )
    parser.add_argument(
        "--flag",
        action="store_true",
        help="Optional boolean flag; changes output when enabled.",
    )
    return parser


def main(argv: list[str]) -> int:
    parser = _build_parser()

    # Key behavior difference: no args vs args
    if len(argv) == 0:
        print("NO-ARGS MODE: launched without any CLI arguments.")
        print("Tip: try `--name Sasha` or `--count 3 --flag`.")
    else:
        args = parser.parse_args(argv)
        print("ARGS MODE: launched with CLI arguments.")
        print(
            json.dumps(
                {
                    "parsed": {"name": args.name, "count": args.count, "flag": args.flag},
                    "raw_argv": argv,
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )

    # Useful context for debugging scheduled tasks
    print("--- context ---")
    print(f"timestamp_utc={_dt.datetime.now(tz=_dt.timezone.utc).isoformat()}")
    print(f"python={sys.executable}")
    print(f"cwd={os.getcwd()}")
    print(f"host={socket.gethostname()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

