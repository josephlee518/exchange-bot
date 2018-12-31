# Exchange Bot

- Supported: OKCoinKR

## Install

1. `pip install requests` 

2. Unittest: `python -m unittest tests.test_okcoin`

3. And Import!

**NOTE**: It's Made on Python 3.7 (x64, Ubuntu Linux 18)

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

## Python Test in VSCode

- To run test in Python, You should change some file (`settings.json`) in VSCode (or other editor can be used).

```json
{
    "python.unitTest.unittestEnabled": true, // If you're using unittest, Set true
    "python.unitTest.pyTestEnabled": false, // If you're using pyTest, Set true
    "python.unitTest.nosetestsEnabled": false, // If you're using nosetests, Set true 
    "python.unitTest.cwd": "~/exchange-bot", // Currently Working Directory
    "python.unitTest.unittestArgs": [
        "-v", // give verbosity options
        "-s", "tests", // Selecting folder to gather with
        "-p", "*test_*.py" // test file named *test_* 
    ]
}
```