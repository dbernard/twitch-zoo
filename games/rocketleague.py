import requests

from games import config


def get_stats(steam64):
    """Retrieve the stats from Rocket League Stats. Requires auth."""
    url = 'https://api.rocketleaguestats.com/v1/player'
    params = {
        'unique_id': steam64,
        'platform_id': '1',
        'apikey': config['APP']['RLSTATS']
    }
    response = requests.get(url, params=params)
    return response.json()


def stats(steam64):
    """Helper method for stats retrieval."""
    stats = get_stats(steam64)
    return stats['stats']
