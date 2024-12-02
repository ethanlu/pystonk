#!/usr/bin/env python3
import aws_cdk as cdk

from pystonk.pystonk_stack import config, PystonkStack


app = cdk.App()
PystonkStack(app, "PystonkStack",
    env=cdk.Environment(account=config["aws"]["account"], region=config["aws"]["region"])
)

app.synth()
