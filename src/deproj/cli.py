#!/usr/bin/env python
"""Console script for deproj."""
import argparse
from functools import partial

from deproj.utils import get_current_mlb_date, BRANDS, JSON_INDENT
from deproj.cards import build, Output


DEFAULT_BRAND = BRANDS[0]
DEFAULT_YEAR = get_current_mlb_date().year - 1
# pitcher vs hitter cards?
DEFAULT_BATTER = 605113
DEFAULT_PITCHER = 605135
DEFAULT_PERSON_ID = DEFAULT_PITCHER


def parse_args():
    """Console script for deproj."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-B', '--brand', type=str, default=DEFAULT_BRAND)
    parser.add_argument('-Y', '--year', type=int, default=DEFAULT_YEAR)
    parser.add_argument('-P', '--person-id', type=int, default=DEFAULT_PERSON_ID)
    parser.add_argument('-O', '--output', type=Output, default=Output.JSON)
    parser.add_argument('-F', '--file', type=str, default=None)  # todo

    return parser.parse_args()


def main() -> int:
    try:
        args = parse_args()
        card = build(args.brand, args.year, args.person_id)
        if args.output == Output.JSON:
            to_output = partial(card.to_json, indent=JSON_INDENT)
        elif args.output == Output.CONSOLE:
            to_output = partial(card.to_console, indent=JSON_INDENT)
        # elif args.output == Output.CSV:
        #     to_output = card.to_csv
        # elif args.output == Output.PNG:
        #     to_output = card.to_png
        else:
            raise ValueError(f"unrecognized output format: {args.output}")
        to_output(args.brand, args.year, args.person_id)
        return 0
    except Exception as e:
        raise e


if __name__ == "__main__":
    import sys
    sys.exit(main())
