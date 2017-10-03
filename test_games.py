import asyncio

from games import pubg, overwatch

async def test():
    print(pubg.stats('kwonstant'))
    ow = await overwatch.stats('JayKwon#1164')
    print(ow)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())
