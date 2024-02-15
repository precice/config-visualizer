#! /usr/bin/env python

import argparse

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from preciceconfigvisualizer.window import ConfigVisualizerWindow


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "infile",
        type=str,
        default=None,
        nargs="?",
        help="The optional preCICE XML configuration file.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    window = ConfigVisualizerWindow(args.infile)
    window.connect("delete-event", Gtk.main_quit)
    Gtk.main()


if __name__ == "__main__":
    main()
