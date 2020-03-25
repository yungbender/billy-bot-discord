import peewee as pw 
from models.base_model import BaseModel
from models.guild import Guild
from models.client import Client

class Karma(BaseModel):
    id = pw.IntegerField(primary_key=True)
    karma = pw.IntegerField(null=False, default=0)
    avaiable_karma = pw.IntegerField(null=False, default=10)
    guild = pw.ForeignKeyField(Guild)
    client = pw.ForeignKeyField(Client)
