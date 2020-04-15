#
#	Billy-Bot (Version: 1.0)
#	Made by YungBender
#

import asyncio
import random
import secrets
import os
import sys
import traceback
from asyncio import ensure_future

import discord
from discord.ext import commands

from utils.logger import LOGGER
from repositories.prefix_repo import PrefixRepo
from cogs.admin import Admin, OWNER_ID
from cogs.rng import RNG
from cogs.memes import Memes
from cogs.nsfw import Nsfw
from cogs.interaction import Interaction
from cogs.copypasta import Copypasta
from cogs.karma import Karma
from cogs.stats import Stats
from libs.sniff import Sniffer
from utils.common import get_git_hash
from utils.constants import CURRENT_VERSION


DEFAULT_PREFIX = "!"
PREFIX_REPO = PrefixRepo()
BOT_TOKEN = os.getenv("BOT_TOKEN", None)
LOGGING_CHANNEL = int(os.getenv("LOGGING_CHANNEL_ID", None))


class Billy(commands.Bot):

	logging_channel = None
	sniffer = None

	def __init__(self, token):
		super().__init__(command_prefix=self._get_prefix, owner_id=OWNER_ID, help_command=None)
		self.sniffer = Sniffer()
		self.run(token)

	def _get_prefix(self, bot, message):
		try:
			prefix = PREFIX_REPO.get_prefix(str(message.guild.id))
		except Exception as _: # should be peewee error
			return DEFAULT_PREFIX

		if prefix:
			return prefix.prefix
		else:
			return DEFAULT_PREFIX

	async def _set_presence(self):
		format_ = f"v{CURRENT_VERSION}"
		presence = discord.Game(format_)
		await self.change_presence(activity=presence)

	async def _fetch_logging_channel(self):
		if not LOGGING_CHANNEL:
			return

		self.logging_channel = self.get_channel(LOGGING_CHANNEL)
		LOGGER.info("Channel fetched.")

	async def _init_timers(self):
		ensure_future(self.karma.start_cooldown())
		ensure_future(self.interaction.start_corona_cooldown())		

	async def on_ready(self):
		LOGGER.info("Billy ready and running.")

		self.add_cog(Admin(self))
		self.add_cog(RNG(self))
		self.add_cog(Memes(self))
		self.add_cog(Nsfw(self))
		self.add_cog(Copypasta(self))
		self.add_cog(Stats(self))

		# TODO: this is ugly
		self.add_cog(Karma(self))
		self.karma = self.get_cog("Karma")

		self.add_cog(Interaction(self))
		self.interaction = self.get_cog("Interaction")

		await self._fetch_logging_channel()

		await self._set_presence()
		await self._init_timers()

	async def on_message(self, msg):
		ctx = await self.get_context(msg)
		channel = ctx.message.channel

		isThere, content = await self.sniffer.sniff(ctx)

		if isThere == "crack":
			await ctx.send(content)

		elif isThere == "karma":
			async with channel.typing():
				await self.karma.behave(ctx)
				return

		elif ctx.valid:
			async with channel.typing(): # simulate calculation
				await self.invoke(ctx)

	async def on_command_error(self, ctx, error):
		""" Command error handler. """
		if isinstance(error, commands.BadArgument):
			await ctx.send("Wrong input given!")
		if isinstance(error, commands.errors.CommandInvokeError):
			await self._handle_internal_error(ctx, error.original)

	async def on_error(self, event, *args, **kwargs):
		""" Overall exception handler. """
		type_, value, tb = sys.exc_info()
		ex_content = traceback.format_exception(type_, value, tb)
		ex_content = " ".join(e for e in ex_content)

		# Check for the stupid restart of cogs.
		# TODO: fix this
		if "is already registered." in ex_content:
			return

		LOGGER.exception(f"Unexpected exception on event: {event}. Args: {args} Kwargs: {kwargs}. Content: {ex_content}")

		if not self.logging_channel:
			return

		await self.logging_channel.send(content="```" + ex_content + "```")

	async def _handle_internal_error(self, ctx, ex):
		""" Handler for internal errors for logging into server text room. """
		ex_content = traceback.format_exception(type(ex), ex, ex.__traceback__)
		ex_content = " ".join(e for e in ex_content)

		# Check for the stupid restart of cogs.
		# TODO: fix this
		if "is already registered." in ex_content:
			return

		LOGGER.exception(f"Unexpected exception on event: {ctx.message.content}. Args: {ctx.args} Kwargs: {ctx.kwargs}. Content: {ex_content}")

		if not self.logging_channel:
			return

		await self.logging_channel.send(content="```" + ex_content + "```")

if __name__ == "__main__":
	BILLY = Billy(BOT_TOKEN)
