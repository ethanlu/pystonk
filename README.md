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

For running this as a Slack app locally, it will need an Ngrok auth token:
* [create an account and get an auth token](https://ngrok.com/)

## Local Run
### Ngrok
Setup a Ngrok access point so that traffic from Slack can reach your local app. The request URL that is needed for Slack events and 
slash commands should use:
`https://{ngrok endpoint}/slack/events`

### Configure Slack App
PyStonk can be setup as a Slack application! It is not distributed publicly, so will need to be manually installed into your
desired Slack workspace.
* [Create an app in desired workspace](https://api.slack.com/apps?new_app=1)
  * Once created, a signing secret will be available and this will need to be exported as `PYSTONK_SLACK_SECRET`
* [Create a bot oauth token and ](https://api.slack.com/legacy/oauth):
  * Once created, the Bot User Oauth Token will be accessible in the Oauth & Permissions section of Slack app admin page. Export this token to `PYSTONK_SLACK_TOKEN`
* In OAuth & Permissions section of your Slack app admin page, add the following bot token scopes:
  * `app_mention:read`
  * `chat:write`
  * `commands`
* In Event Subscriptions section of your Slack app admin page, enable events and set the request endpoint to your server that will host this project
* In Slash Commands section of your Slack app admin page, create a `/pystonk` command and set the endpoint url to your server that will host this project

### Docker
Create a `.env` file and add these environment variables to it:
```shell script
PYSTONK_API_KEY={key from td ameritrade}
PYSTONK_SLACK_TOKEN={slack bot user oauth token}
PYSTONK_SLACK_SECRET={slack app signing secret}
NGROK_AUTHTOKEN={ngrok auth token}
```

Build and run project
```shell script
docker-compose build
docker-compose up -d
```

## TODO
- More reports & slack commands
- Kivy desktop app