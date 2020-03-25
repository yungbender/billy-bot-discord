import peewee as pw 
from models.base_model import BaseModel

class Client(BaseModel):
    id = pw.CharField(max_length=255,primary_key=True)
    current_name = pw.CharField(null=False)
