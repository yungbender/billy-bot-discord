import peewee_async as pw
import peewee
from models.copypasta import Copypasta

class CopypastaRepo:

    def get_pasta_by_name(self, name):
        pasta = Copypasta.select(Copypasta.content).where(Copypasta.pasta_name == name).first()

        return pasta

    def get_all_pastas(self):
        pastaNames = Copypasta.select(Copypasta.pasta_name).execute()

        return pastaNames

    def insert_pasta(self, pastaName, pasta):
        Copypasta.create(pasta_name=pastaName, content=pasta)
