pystonk
=======

Python tool that leverages publically available stock data to do some simple calculations that I often perform when
trading stocks and options.

Uses [TD Amertrade's API](https://developer.tdameritrade.com/apis) data to generate stock and option reports.

# Table of Contents
* [Install/Run](#install-run)
* [TODO](#todo)

## Install/Run
Setup your virtual environment
```shell script
virtualenv <path to env>
source <path to env>/bin/activate
```

Install project from source
```shell script
git clone <repository>
python setup.py develop
```

Create a TD Ameritrade API key and assign it to `PYSTONK_API_KEY` environment variable
```shell script
export PYSTONK_API_KEY={key from td ameritrade}
```

Run project
```shell script
pystonk_pcr {stock symbol} {percent threshold}
```

## TODO
- Docker
- Kivy desktop app