#!/usr/bin/env python
"""Console script for deproj."""
import argparse

from deproj.utils import BRANDS, Output

DEFAULT_BRAND = BRANDS[0]
DEFAULT_YEAR = 2023  # deproj.utils.get_current_mlb_date().year

# pitcher vs hitter cards?
DEFAULT_BATTER = 605113
DEFAULT_PITCHER = 605135
DEFAULT_PERSON_ID = DEFAULT_PITCHER

DEFAULT_CONSOLE_OUTPUT = Output.JSON


def parse_args():
    """Console script for deproj."""
    parser = argparse.ArgumentParser()
    choose_brands = ", ".join(BRANDS)
    parser.add_argument(
        "-B",
        "--brand",
        type=str,
        required=True,
        help=f"Card brand. Choose from {choose_brands}",
    )
    parser.add_argument(
        "-Y", "--year", type=int, default=DEFAULT_YEAR, help="Year of card release"
    )
    parser.add_argument("-P", "--person-id", type=int, required=True)
    parser.add_argument("-LL", "--log-level", type=str, default=None)

    output_parsers = {}
    choose_outputs = ", ".join([o.value for o in Output])
    subparsers = parser.add_subparsers(
        help=f"output type. choose from {choose_outputs}",
        dest="output",
        required=True,
    )
    for o in Output:
        output_parsers[o] = subparsers.add_parser(o.value)
        if o != Output.CONSOLE:
            output_parsers[o].add_argument("-S", "--short", type=bool, default=True)
    output_parsers[Output.CONSOLE].add_argument(
        "-O",
        "--output-as",
        help=f"Output to console as. Choose from {choose_outputs}",
        type=Output,
    )

    return parser.parse_args()
