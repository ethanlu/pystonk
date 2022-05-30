#!/bin/bash

if [ "$PYSTONK_MODE" == "slack" ]
then
  python pystonk/slack_app.py
else
  python pystonk/terminal_app.py
fi