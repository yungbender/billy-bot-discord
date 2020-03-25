from models.karma import Karma
from models.client import Client
from models.base_model import DB
from peewee import fn

from utils.constants import DEFAULT_AVAIABLE_KARMA


class KarmaRepo:

    def _fetch_karma(self, clientId, guildId):
        karma = Karma.select() \
<<<<<<< HEAD
             .where((Karma.client == clientId) & (Karma.guildId == guildId)) \
=======
             .where((Karma.client == clientId) & (Karma.guild == guildId)) \
>>>>>>> Add V1.2.4
             .first()

        return karma

    def check_user_has_karma(self, userId, guildId):
        result = Karma.select().where((Karma.guild == guildId) & (Karma.client == userId)) \
                      .exists()
        return result

    def get_user_avaiable_karma(self, clientId, guildId):
        karma = Karma.select(Karma.avaiable_karma) \
                     .where((Karma.client_id == clientId) & (Karma.guild == guildId)) \
                     .first()

        return karma.avaiable_karma

    def get_top_karma_server(self, guildId, pageSize, page):
        karma = Karma.select() \
                     .where(Karma.guild == guildId) \
                     .order_by(Karma.karma.desc()) \
                     .paginate(page, paginate_by=pageSize) \
                     .execute()

        return karma

    def get_user_karma(self, guildId, clientId):
        karma = Karma.select() \
                     .where((Karma.guild == guildId) & (Karma.client == clientId)) \
                     .first()

        return karma
    
    def get_user_karma_all(self, clientId):
        karma = Karma.select(fn.SUM(Karma.karma).alias("karmaSum")) \
                     .where((Karma.client == clientId)) \
                     .first()

        return karma

    def give_karma(self, giverId, givenId, guildId):
        with DB.atomic() as transaction:
            try:
                given = self._fetch_karma(givenId, guildId)
                giver = self._fetch_karma(giverId, guildId)

                given.karma += 1
                giver.avaiable_karma -= 1

                given.save()
                giver.save()

            except Exception as e:
                transaction.rollback()
                raise e
        
        return True

    def take_karma(self, giverId, givenId, guildId):
        with DB.atomic() as transaction:
            try:
                given = self._fetch_karma(givenId, guildId)
                giver = self._fetch_karma(giverId, guildId)

                given.karma -= 1
                giver.avaiable_karma -= 1

                given.save()
                giver.save()
            except Exception as e:
                transaction.rollback()
                raise e

        return True

    def restart_avaiable_karma(self):
        with DB.atomic() as transaction:
            try:
                Karma.update(avaiable_karma = DEFAULT_AVAIABLE_KARMA) \
                     .execute()
            except Exception as e:
                transaction.rollback()
                raise e

        return True

    def reset_server_karma(self, guildId):
        with DB.atomic() as transaction:
            try:
                Karma.update(karma = 0).where(Karma.guild == guildId) \
                     .execute()
            except Exception as e:
                transaction.rollback()
                raise e

        return True

    def create_karma(self, userId, guildId):
        Karma.create(guild=guildId, client=userId)
