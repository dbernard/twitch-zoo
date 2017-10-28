import aiohttp

from overwatch_api import constants
from overwatch_api.core import AsyncOWAPI


async def stats(name):
    """Get the stats for an Overwatch player.

    :param name: the Blizzard tag for the player to retrieve
    :returns: the stats for the provided player

    """
    client = AsyncOWAPI()
    stats = {}

    connector = aiohttp.TCPConnector(verify_ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        stats[constants.PC] = await client.get_profile(name, session=session, platform=constants.PC)

    return stats
