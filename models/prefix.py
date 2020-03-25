import peewee as pw 
from models.base_model import BaseModel
from models.guild import Guild

class Prefix_Guild(BaseModel):
    id = pw.IntegerField(primary_key=True)
    prefix = pw.CharField(null=False)
    guild = pw.ForeignKeyField(Guild)
