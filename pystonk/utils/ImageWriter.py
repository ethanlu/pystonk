from pystonk import configuration
from io import BytesIO

import boto3


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
            s3_client = boto3.client('s3')
            s3_client.put_object(
                Bucket=f"pystonk-images-{configuration['aws']['s3_hash']}",
                Key=fname,
                Body=data.getvalue(),
                ContentType='image/png'
            )
            url = f"https://pystonk-images-{configuration['aws']['s3_hash']}.s3.{configuration['aws']['region']}.amazonaws.com/{fname}"
        return url
