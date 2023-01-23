#!/usr/bin/env python
"""Console script for deproj."""
import sys

from functools import partial

from deproj.cli import parse_args
from deproj.cards import build
from deproj.utils import set_log_level, Output


def main() -> int:
    try:
        args = parse_args()
        set_log_level(args.log_level)
        card = build(args.brand, args.year, args.person_id)
        if args.output == Output.JSON.value:
            to_output = partial(card.write_json, short=args.short)
        elif args.output == Output.CSV.value:
            to_output = partial(card.write_csvs, short=args.short)
        elif args.output == Output.CONSOLE.value:
            to_output = partial(card.to_console, output=args.output_as)
        # elif (args.output == Output.PNG.value) or True:
        #     to_output = card.to_png
        else:
            raise ValueError(f"output {args.output} not configured")  # if not in Output enum, argparse would fail
        out = to_output()
        sys.stdout.write(out)
        return 0
    except Exception as e:
        raise e


if __name__ == "__main__":
    sys.exit(main())
