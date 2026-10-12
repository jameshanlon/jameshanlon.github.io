"""
Command line entry point.
"""

import argparse
import functools
import http.server
import logging
import socketserver
import sys
import time
from pathlib import Path

from ssg import config
from ssg.site import Site

WATCH_DIRS = [config.CONTENT_DIR, config.THEME_DIR, Path("ssg")]


def build(args):
    """
    Generate the site.
    """
    Site(args.output).build()
    return 0


def serve(args):
    """
    Generate the site and serve it over HTTP.
    """
    Site(args.output).build()
    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(args.output)
    )
    with socketserver.TCPServer((args.bind, args.port), handler) as server:
        print(f"Serving {args.output} at http://{args.bind}:{args.port}")
        if args.watch:
            _watch(args)
        server.serve_forever()
    return 0


def _watch(args):
    """
    Rebuild in a background thread whenever a source file changes.
    """
    import threading

    def snapshot():
        return {
            path: path.stat().st_mtime_ns
            for directory in WATCH_DIRS
            for path in directory.rglob("*")
            if path.is_file()
        }

    def loop():
        previous = snapshot()
        while True:
            time.sleep(1)
            current = snapshot()
            if current != previous:
                previous = current
                try:
                    Site(args.output).build()
                    print("Rebuilt")
                except Exception as error:
                    print(f"Build failed: {error}")

    threading.Thread(target=loop, daemon=True).start()


def main(argv=None):
    """
    Parse arguments and dispatch to a subcommand.
    """
    parser = argparse.ArgumentParser(prog="ssg")
    parser.add_argument("-o", "--output", type=Path, default=config.OUTPUT_DIR)
    parser.add_argument("-v", "--verbose", action="store_true")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("build", help="generate the site").set_defaults(func=build)

    serve_parser = subparsers.add_parser("serve", help="generate and serve the site")
    serve_parser.add_argument("-p", "--port", type=int, default=8000)
    serve_parser.add_argument("-b", "--bind", default="0.0.0.0")
    serve_parser.add_argument("--watch", action="store_true")
    serve_parser.set_defaults(func=serve)

    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO if args.verbose else logging.WARNING)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
