import os
import sys

def resource_path(relative_path):
    """ 
    Get absolute path to resource, works for dev and for PyInstaller.
    This version assumes resources are in an 'assets' subdirectory.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, 'assets', relative_path)
