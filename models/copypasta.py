import peewee as pw
from models.base_model import BaseModel

class Copypasta(BaseModel):
    pasta_name = pw.CharField(max_length=64, primary_key=True)
    content = pw.TextField(null=False)
