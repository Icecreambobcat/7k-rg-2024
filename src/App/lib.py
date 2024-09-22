# Move nonspecific functions here once implemented
import os

def GET_ROOT() -> str:
    cwd = os.getcwd() 
    root = os.path.join(cwd, "..", "..")
    return root
