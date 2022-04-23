pystonk
=======

Python tool that leverages publically available stock data to do some simple calculations that I often perform when
trading stocks and options.

# Table of Contents
* [Prerequisite](#prerequisite)
* [Local Run](#local-run)
* [Slack App](#slack-app)
* [TODO](#todo)

## Prerequisite
This tool uses [TD Amertrade's API](https://developer.tdameritrade.com/apis) data:
* [create an account](https://developer.tdameritrade.com/content/getting-started#createAccount)
* [register an app](https://developer.tdameritrade.com/content/getting-started#registerApp) to get an API key.

## Local Run
### With Docker
Create a `.env` file and add `PYSTONK_API_KEY` environment variable to it 
```shell script
echo "PYSTONK_API_KEY={key from td ameritrade}" > .env
```

Build and run project
```shell script
docker-compose build
docker-compose run pystonk
```
### Without Docker
Setup your virtual environment
```shell script
virtualenv <path to env>
source <path to env>/bin/activate
```

Install project
```shell script
python setup.py install
```

Create a TD Ameritrade API key (see prerequisites) and assign it to `PYSTONK_API_KEY` environment variable
```shell script
export PYSTONK_API_KEY={key from td ameritrade}
```

Run project
```shell script
pystonk_terminal
```

## Slack App
PyStonk can be setup as a Slack application! It is not distributed publicly, so will need to be manually installed into your
desired Slack workspace.
* [Create an app in desired workspace](https://api.slack.com/apps?new_app=1)
  * Once created, a signing secret will be available and this will need to be exported as `PYSTONK_SLACK_SECRET`
  ```shell script
  export PYSTONK_SLACK_SECRET={slack app signing secret}
  ```
* [Create a bot oauth token and ](https://api.slack.com/legacy/oauth):
  * Once created, the Bot User Oauth Token will be accessible in the Oauth & Permissions section of Slack app admin page. Export this token to `PYSTONK_SLACK_TOKEN`
  ```shell script
  export PYSTONK_SLACK_TOKEN={bot user oauth token}
  ```
* In OAuth & Permissions section of your Slack app admin page, add the following bot token scopes:
  * `app_mention:read`
  * `chat:write`
  * `commands`
* In Event Subscriptions section of your Slack app admin page, enable events and set the request endpoint to your server that will host this project
* In Slash Commands section of your Slack app admin page, create a `/pystonk` command and set the endpoint url to your server that will host this project

### Deploy
```shell script
pip install python-lambda
lambda deploy --config-file=aws_lambda.yaml --requirements=requirements.txt
```

## TODO
- More reports & slack commands
- Kivy desktop app