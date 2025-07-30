#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Update Avatar animation state")
    parser.add_argument(
        "--ani", help="Animation name (e.g. walk, idle)", metavar="ANIMATION"
    )
    parser.add_argument(
        "--dir", help="Direction (e.g. side, down)", metavar="DIRECTION"
    )
    args = parser.parse_args()

    state_file = Path("state.json")

    # load existing state (if any)
    state = {}
    if state_file.exists():
        try:
            state = json.loads(state_file.read_text())
        except json.JSONDecodeError:
            state = {}

    # merge in any provided flags
    if args.ani:
        state["ani"] = args.ani
    if args.dir:
        state["dir"] = args.dir

    # write back (one‐line JSON)
    state_file.write_text(json.dumps(state))


if __name__ == "__main__":
    main()
