from __future__ import annotations
import os
from pathlib import Path


class Lib:
    @staticmethod
    def GET_ROOT() -> str:
        cwd = os.getcwd()
        root = os.path.join(cwd, "..", "..")
        return root

    PROJECT_ROOT = GET_ROOT()
