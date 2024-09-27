from pathlib import Path
import sys
from ..App.App import App
from ..App.Conf import Conf

from argparse import ArgumentParser
import os
from ..App.lib import Lib


def main() -> None:
    log = False

    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{Conf.VERSION}",
        help="Returns the version of the program",
    )
    group.add_argument(
        "-l",
        "--log",
        action="store_true",
        help="Logs events to a file",
    )
    group.add_argument(
        "-c",
        "--clean",
        action="store_true",
        help="Cleans extra files",
    )

    args = parser.parse_args()
    log = False

    if args.log:
        log = True
        dir = Path(Lib.PROJECT_ROOT, "STO", "LOG", "log")
        if not dir.is_file():
            dir.touch()
        else:
            os.remove(dir)
            dir.touch()

    elif args.clean:
        log_path = Path(Lib.PROJECT_ROOT, "STO", "LOG", "log")

        if log_path.is_file():
            os.remove(log_path)

            print(f"All contents of {log_path.absolute()} have been deleted.")
        else:
            print(f"Log directory {log_path.absolute()} does not exist.")

        sys.exit(0)

    App.init_game(log)
    App.run()


if __name__ == "__main__":
    main()
