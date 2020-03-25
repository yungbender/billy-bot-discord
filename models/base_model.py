import peewee as pw
import os

# TODO: Think about async peewee or aiopg2
#       If the db will be too slow (many data, slow network)
#       The nonasync requests will totally slow
#       down Billy response to requests.

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "billy-db")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_PWD = os.getenv("DB_PWD", "billy_pwd")
DB_USER = os.getenv("DB_USER", "billy_bot")

DB = pw.PostgresqlDatabase(DB_NAME, user=DB_USER,
                           password=DB_PWD,
                           host=DB_HOST,
                           autorollback=True
                           )

class BaseModel(pw.Model):
    class Meta:
        database = DB
