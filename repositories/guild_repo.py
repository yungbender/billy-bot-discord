from models.guild import Guild

class GuildRepo:

    def check_guild(self, guildId):
        result = Guild.select().where(Guild.id == guildId).exists()
        return result

    def insert_guild(self, guildId, guildName):
        Guild.create(id=guildId, guild_name=guildName)
