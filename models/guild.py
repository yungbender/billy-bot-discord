import peewee as pw 
from models.base_model import BaseModel

class Guild(BaseModel):
    id = pw.CharField(primary_key=True)
    guild_name = pw.CharField(null=False)
