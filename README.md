# Exchange Bot

- Supported: OKCoinKR

## Install

1. `pip install requests` 

2. Unittest: `python -m unittest tests.test_okcoin`

## How to make a configfile?

- **You should set your config file first** on `conf/config.ini`

    - `mkdir conf` first

    - then make a config file named `config.ini`

    - and Write like this

    ```ini
    [DAYBIT]
    daybit_access_key = 
    daybit_secret_key = 

    [OKCOIN]
    okcoin_api_key = 
    okcoin_secret_key = 

    # If you're using MongoDB, You don't need to write information on SQLITE section
    [MONGODB]
    DB_IP = 
    DB_PORT = 
    DB_NAME = 
    DB_COL = 

    [SQLITE]
    FILENAME = 
    TABLENAME = 

    [LOGGING]
    directory = 
    logging = 
    ```