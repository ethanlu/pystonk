pystonk
=======

Python tool that leverages publically available stock data to do some simple calculations that I often perform when
trading stocks and options.

# Table of Contents
* [Prerequisite](#prerequisite)
* [Local Run](#local-run)
* [TODO](#todo)

## Prerequisite
This tool uses [TD Amertrade's API](https://developer.tdameritrade.com/apis) data:
* [create an account](https://developer.tdameritrade.com/content/getting-started#createAccount)
* [register an app](https://developer.tdameritrade.com/content/getting-started#registerApp) to get an API key.

## Local Run
### With Docker
Clone project
```shell script
git clone <repository>
```

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

Install project from source
```shell script
git clone <repository>
python setup.py install
```

Create a TD Ameritrade API key and assign it to `PYSTONK_API_KEY` environment variable
```shell script
export PYSTONK_API_KEY={key from td ameritrade}
```

Run project
```shell script
pystonk_terminal
```

## TODO
- Slack plugin
- Kivy desktop app