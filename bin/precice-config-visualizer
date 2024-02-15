#! /usr/bin/env python

import argparse
import sys

from preciceconfigvisualizer.common import configFileToDotCode


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--outfile",
        nargs="?",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="The resulting dot file. Omit to output to stdout.",
    )
    displayChoices = ["full", "merged", "hide"]
    parser.add_argument(
        "--data-access",
        choices=displayChoices,
        default="full",
        help="Verbosity of the displayed read/write access between mesh and participant.",
    )
    parser.add_argument(
        "--data-exchange",
        choices=displayChoices,
        default="full",
        help="Verbosity of the displayed data exchange between meshes.",
    )
    parser.add_argument(
        "--communicators",
        choices=displayChoices,
        default="full",
        help="Verbosity of the displayed of communicators.",
    )
    parser.add_argument(
        "--cplschemes",
        choices=displayChoices,
        default="full",
        help="Verbosity of the displayed of coupling schemes.",
    )
    parser.add_argument(
        "--mappings",
        choices=displayChoices,
        default="full",
        help="Verbosity of the displayed of mappings.",
    )
    parser.add_argument(
        "--no-watchpoints", action="store_true", help="Do not display watchpoints."
    )
    parser.add_argument(
        "--no-colors", action="store_true", help="Disable colors in the output."
    )
    parser.add_argument(
        "--margin", default=8, type=int, help="Margin around cluster borders in points."
    )
    parser.add_argument("infile", type=str, help="The XML configuration file.")
    return parser.parse_args()


def main():
    args = parse_args()
    dot = configFileToDotCode(args.infile, args)
    args.outfile.write(dot)


if __name__ == "__main__":
    main()
