#!/usr/bin/env python3
import os

import aws_cdk as cdk

from pystonk.pystonk_stack import PystonkStack


app = cdk.App()
PystonkStack(app, "PystonkStack",
    env=cdk.Environment(account='', region='us-east-1')
)

app.synth()
