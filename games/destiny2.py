import pydest
import asyncio
import datetime

from games import config

membership_types = {
    'xbox': 1,
    'playstation': 2,
    'pc': 3
}

api_key = config['GAMES']['DESTINY2_API_KEY']

def parse_date(value):
    return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")

def clean_stats(stats):
    pvpStats = stats['Response']['allPvP']['allTime']

    return {
        'bestKills': pvpStats['bestSingleGameKills']['basic']['displayValue'],
        'bestScore': pvpStats['bestSingleGameScore']['basic']['displayValue'],
        'kd': pvpStats['killsDeathsRatio']['basic']['displayValue'],
        'kda': pvpStats['killsDeathsAssists']['basic']['displayValue'],
        'combatRating': pvpStats['combatRating']['basic']['displayValue'],
        'winLoss': pvpStats['winLossRatio']['basic']['displayValue'],
        'weapon': pvpStats['weaponBestType']['basic']['displayValue'],
        'spree': pvpStats['longestKillSpree']['basic']['displayValue']
    }

async def get_character_id(destiny, membership_type, membership_id):
    profile = await destiny.api.get_profile(membership_type, membership_id, ['200'])

    characters = [character for id, character in profile['Response']['characters']['data'].items()]

    most_recent_character = sorted(characters, key=lambda x: parse_date(x['dateLastPlayed']), reverse=True)[0]

    return most_recent_character['characterId']

async def get_membership_id(destiny, username, membership_type):
    
    res = await destiny.api.search_destiny_player(membership_type, username)

    return res['Response'][0]['membershipId']

async def get_stats(user_platform):
    destiny = pydest.Pydest(api_key)

    username, platform = user_platform.split(',')

    membership_type = membership_types[platform]
    
    membership_id = await get_membership_id(destiny, username, membership_type)
    
    character_id = await get_character_id(destiny, membership_type, membership_id)

    stats = await destiny.api.get_historical_stats(membership_type, membership_id, character_id)

    stats = clean_stats(stats)

    destiny.close()

    return stats

def stats(user_platform):
    loop = asyncio.new_event_loop()

    stats = loop.run_until_complete(get_stats(user_platform))

    loop.close()

    return stats