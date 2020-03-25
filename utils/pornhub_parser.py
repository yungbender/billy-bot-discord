import httpx


class PornhubParser():

	requestClient = None

	def __init__(self):
		self.requestClient = httpx.AsyncClient()

	async def get_pornhub_link(self, orientation):
		if orientation == "gay":
			pornhub = await self.requestClient.get("https://www.pornhub.com/gay/random")
		else:
			pornhub = await self.requestClient.get("https://pornhub.com/random")	

		link = pornhub.url
		return link
