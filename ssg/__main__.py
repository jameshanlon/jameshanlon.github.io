"""
Command line entry point for the site generator.
"""

import argparse
import logging

from ssg.site import Site


def main():
    """
    Parse arguments and run the requested command.
    """
    parser = argparse.ArgumentParser(prog="ssg", description="Build the site.")
    parser.add_argument("command", choices=["build"])
    parser.add_argument("-o", "--output-dir", help="Where to write the site.")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    Site(args.output_dir).build()


if __name__ == "__main__":
    main()
