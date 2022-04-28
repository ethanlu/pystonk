#!/bin/bash

# clean up previous deploy content if it exists
if [ -d "./deploy" ]; then
  rm -rf deploy;
fi

if [ -f "./pystonk-package.zip" ]; then
  rm -f pystonk-package.zip
fi

# prepare deployment folder
mkdir deploy;
pip install . --target deploy;
cp -rf pystonk deploy/;
rm -rf deploy/pystonk/conf/app.conf;

# create package & deploy
cd deploy;
zip -r ../pystonk-package.zip .;
cd ../;
aws lambda update-function-code --function-name pystonk --zip-file fileb://pystonk-package.zip;