import os

PYSTONK_ROOT = os.path.abspath(os.path.dirname(__file__))


def get_conf_path(filename: str = 'app.conf') -> str:
    filepath = os.path.join(PYSTONK_ROOT, 'conf', filename)
    if os.path.exists(filepath):
        return filepath
    else:
        return os.path.join(PYSTONK_ROOT, 'conf', 'default.conf')
