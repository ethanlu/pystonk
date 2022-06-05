#!/bin/bash

# clean up previous deploy content if it exists
if [ -d "./deploy" ]; then
  rm -rf deploy;
fi

if [ -f "./pystonk-package.zip" ]; then
  rm -f pystonk-slack-receive-package.zip
fi

# prepare deployment folder
mkdir deploy;
export PYSTONK_LAMBDA_DEPLOY=1;
pip install --target deploy .;
unset PYSTONK_LAMBDA_DEPLOY;
cp -rf pystonk/__init__.py deploy/;
cp -rf pystonk/slack_lambda_app.py deploy/;
cp -rf pystonk/conf deploy/;
cp -rf pystonk/utils deploy/;
rm -rf deploy/pystonk/conf/app.conf;

# create package & deploy
cd deploy;
zip -r ../pystonk-slack-receive-package.zip .;
cd ../;
aws lambda update-function-code --function-name pystonk-slack-receive --zip-file fileb://pystonk-slack-receive-package.zip;