#!/usr/bin/env python3
import os

import aws_cdk as cdk

from dotenv import load_dotenv
from os import path
from pystonk.pystonk_stack import PyStonkStack


load_dotenv(path.abspath(path.dirname(__file__)) + "/.env")
app = cdk.App()
PyStonkStack(app, "PyStonkStack",
             env=cdk.Environment(account=os.getenv('PYSTONK_AWS_ACCOUNT'), region=os.getenv('PYSTONK_AWS_REGION'))
)

app.synth()
