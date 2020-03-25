import peewee as pw 
from models.base_model import BaseModel
from models.client import Client
from models.guild import Guild

class ClientGuild(BaseModel):
    client_id = pw.ForeignKeyField(Client)
    guild_id = pw.ForeignKeyField(Guild)
