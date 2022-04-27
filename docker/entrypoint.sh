#!/bin/bash

if [ "$PYSTONK_MODE" == "slack" ]
then
  python slack_app.py
else
  python terminal_app.py
fi