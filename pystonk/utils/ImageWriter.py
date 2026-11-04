from pystonk import configuration
from io import BytesIO


class ImageWriter(object):
    def __init__(self):
        pass

    @classmethod
    def write(cls, name: str, data: BytesIO) -> str:
        fname = f"{name}.png"
        if not configuration['slack']['lambda']:
            with open(f"pystonk/images/{fname}", "wb") as f:
                f.write(data.getbuffer())
            url = f"{configuration['slack']['images']['domain']}/pystonk-images/{fname}"
        else:
            url = ''
        return url
