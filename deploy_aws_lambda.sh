#!/bin/bash

# clean up previous deploy content if it exists
if [ -d "./deploy" ]; then
  rm -rf deploy;
fi

if [ -f "./pystonk-slack-receive-package.zip" ]; then
  rm -f pystonk-slack-receive-package.zip
fi

# prepare deployment folder
mkdir deploy;
export PYSTONK_LAMBDA_DEPLOY=1;
pip install --target deploy .;
unset PYSTONK_LAMBDA_DEPLOY;

# create package & deploy
cd deploy;
rm -rf pystonk/conf/app.conf;
zip -r ../pystonk-slack-receive-package.zip .;
cd ../;
aws lambda update-function-code --function-name pystonk-slack-receive --zip-file fileb://pystonk-slack-receive-package.zip;