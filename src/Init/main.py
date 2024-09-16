from ..App.App import App
# from ..App.Conf import Conf
# # from sys import exit
# from argparse import ArgumentParser
# import os.path as path
# import subprocess


def main() -> None:
    # parser = ArgumentParser()
    # group = parser.add_mutually_exclusive_group()
    #
    # group.add_argument(
    #     "--version",
    #     action="version",
    #     version=f"{Conf.VERSION}",
    #     help="Returns the version of the program",
    # )
    # group.add_argument(
    #     "-l",
    #     "--log",
    #     action="store_true",
    #     help="Logs events to a file",
    # )
    # group.add_argument(
    #     "-c",
    #     "--clean",
    #     action="store_true",
    #     help="Cleans extra files",
    # )
    #
    # args = parser.parse_args()
    #
    # if args.log:
    #     pass
    #
    # if args.clean:
    #     pass

    Game = App()
    Game.run()


if __name__ == "__main__":
    main()
