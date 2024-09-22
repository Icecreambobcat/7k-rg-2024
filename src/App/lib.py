# Move nonspecific functions here once implemented
import os
from pathlib import Path


class Lib:
    @staticmethod
    def GET_ROOT() -> str:
        cwd = os.getcwd()
        root = os.path.join(cwd, "..", "..")
        return root

    @staticmethod
    def load_images() -> dict[str, list[Path | None]]:
        """
        This function is intended to load all the images unrelated to the rhythm game section of the app.
        Images are sorted into a dictionary with key representing image use and a list of path objects as its values.
        """
        image_dir = Path(f"{Lib.PROJECT_ROOT}/Assets/Images")
        out = {
            "char_sprite": [],
            "background": [],
            "menu": [],
            "button": [],
            "misc": [],
        }
        for img in image_dir.iterdir():
            if img.name.startswith("char_sprite"):
                out["char_sprite"].append(img)
            elif img.name.startswith("background"):
                out["background"].append(img)
            elif img.name.startswith("menu"):
                out["menu"].append(img)
            elif img.name.startswith("button"):
                out["button"].append(img)
            else:
                out["misc"].append(img)

        return out

    PROJECT_ROOT = GET_ROOT()
    IMAGES = load_images()
