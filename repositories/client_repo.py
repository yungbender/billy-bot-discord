from models.client import Client
from models.karma import Karma

class ClientRepo:

    def check_user(self, userId: int):
        result = Client.select().where(Client.id == userId).exists()
        return result

    def insert_user(self, userId:int , name: str):
        client = Client.create(id=userId, current_name=name)

