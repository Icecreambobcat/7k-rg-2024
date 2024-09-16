import pickle


class Conf:
    """
    The conf class is used to handle fixed and custom variables that define the application
    Fixed configs are typically used for debugging and compatability
    If there is no set of config files then the default will be used and saved
    Otherwise the custom configs will be loaded memory and used
    """

    VERSION = "VERSION PLACEHOLDER"

    WINDOW = {"PLACEHOLDER": "PLACEHOLDER"}

    KEYS = {"PLACEHOLDER": "PLACEHOLDER"}

    DEFAULTS = {"PLACEHOLDER": "PLACEHOLDER"}

    def __init__(self):
        # call this from somewhere else if there is no loadconf
        pass


def loadConf():
    pass


def saveConf():
    pass
