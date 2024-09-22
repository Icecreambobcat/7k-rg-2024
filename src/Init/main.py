from App.App import App
from App.Conf import Conf

from argparse import ArgumentParser
import os
import shutil
from App.lib import Lib


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

    if args.log:
        log = True

    elif args.clean:
        root = Lib.PROJECT_ROOT
        log_path = os.path.join(root, "STO/log")

        if os.path.exists(log_path):
            for item in os.listdir(log_path):
                item_path = os.path.join(log_path, item)

                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)

            print(f"All contents of {log_path} have been deleted.")
        else:
            print(f"Log directory {log_path} does not exist.")

        exit()

    Game = App(log)
    Game.run()


if __name__ == "__main__":
    main()
