#! /usr/bin/env python

import argparse
import sys
import pydot
import os

from preciceconfigvisualizer.common import configFileToDotCode


SUPPORTED_FORMATS = [
    "jpeg",
    "jpg",
    "pdf",
    "png",
    "svg",
]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--outfile",
        nargs="?",
        type=argparse.FileType("wb"),
        default=sys.stdout,
        help=f"The output file. Files with extensions {', '.join(SUPPORTED_FORMATS)} will be rendered using graphviz. Omit to output dot to stdout.",
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
        "--no-watchpoints",
        action="store_false",
        dest="watchpoints",
        help="Do not display watchpoints.",
    )
    parser.add_argument(
        "--no-colors",
        action="store_false",
        dest="colors",
        help="Disable colors in the output.",
    )
    parser.add_argument(
        "--margin", default=0, type=int, help="Margin around cluster borders in points."
    )
    parser.add_argument("infile", type=str, help="The XML configuration file.")
    return parser.parse_args()


def main():
    args = parse_args()
    dot = configFileToDotCode(args.infile, **vars(args))

    ext = os.path.splitext(args.outfile.name)[1].lower().lstrip(".")
    if ext in SUPPORTED_FORMATS:
        g = pydot.graph_from_dot_data(dot)[0]
        args.outfile.write(g.create(format=ext))
    else:
        args.outfile.write(dot.encode())


if __name__ == "__main__":
    main()
