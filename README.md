# Billy Bot - A discord bot with simple karma system and functions
Billy bot is simple bot which has some functions and can handle karma for server and global karma. Karma is stored using PSQL.

## Running own instance / developing.
Billy uses 3 enviroment variables.
- ```LOGGING_CHANNEL_ID``` - Discord channel ID where Billy will propagate every exception, please export at least random int .
- ```OWNER_ID``` - Discord user ID, who can turn on or turn off cogs (see ```admin.py```).
- ```BOT_TOKEN``` - [MANDATORY] Discord bot unique TOKEN, which can be requested by Discord developer site, visit it and request a token if you dont have one. Otherwise you cannot run bot.

Export it then with.
```
export BOT_TOKEN=123456
```

Billy uses PostgreSQL database, on beggining of run Billy searches for enviroment variables to which he will TRY to connect.

- ```DB_HOST``` - Database host (default ```localhost```).
- ```DB_NAME``` - Database name (default ```billy-db```).
- ```DB_PORT``` - Database port (default ```5432```)
- ```DB_PWD``` - Database password. (default ```billy_pwd```).
- ```DB_USER``` - Database account (default ```billy_bot```).

Export it or leave it default if you are running database instance locally.

Bot uses custom modules, you can install them with.
```
pipenv install
```
This will create virtual enviroment, then you can run the bot.
```
pipenv run python3 billy.py
```
Or you can exec to the pipenv shell.
```
pipenv shell
python3 billy.py
```

### Local database instance
#### First initialization and sql scripts exeuction
You can have your own local database instance. To start it run.
```
docker-compose up --build
```
(You need ```docker``` and ```docker-compose```).

There is SQL schema which you NEED to intialize on FIRST run of the database. In ```/database``` folder. There is SQL schema script ```db.sql```. 

When the previous command is running (database container is running), execute this script inside the container by running.
```
bash exec_script.sh db.sql
```
That will initialize the database schema.

## Making PR
If you want to contribute, make a PR explaining what does it do, how did you tested it.

### New feature
If its new feature, increment the version number in ```/utils/constants.py```. For ex.
```
CURRENT_VERSION = "1.1.2" -> CURRENT_VERSION = "1.2.2".
```

### Bugfix, minor changes
For these changes in PR increment the same number, but the lowest part. Ex.
```
CURRENT_VERSION = "1.1.2" -> CURRENT_VERSION = "1.1.3".
```
