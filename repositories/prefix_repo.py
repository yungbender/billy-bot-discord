from models.prefix import Prefix_Guild

class PrefixRepo:
    def get_prefix(self, guildId):
        return Prefix_Guild.select() \
                          .where(Prefix_Guild.guild_id == guildId) \
                          .first()

    def insert_prefix(self, prefix, guildId):
        prefixGuild = Prefix_Guild.select().where(Prefix_Guild.guild_id == guildId).first()
        if not prefixGuild:
            Prefix_Guild.create(guild_id=guildId, prefix=prefix)
        else:
            prefixGuild.prefix = prefix
            prefixGuild.save()
