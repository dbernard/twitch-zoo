from functools import lru_cache

from pypubg import core

from games import config


api = core.PUBGAPI(config['GAMES']['PUBG_API_KEY'])


def get_stats(name):
    return api.player(name)


def extract_stat(region, desired_field):
    for stat in region['Stats']:
        if stat['field'] == desired_field:
            return stat['value']
    return '-1'


def extract_region(stats, region_name='agg', match='squad'):
    for region in stats['Stats']:
        if region['Region'] == region_name and region['Match'] == match:
            return region
    return {}


def get_agg_simplified(stats):
    region = extract_region(stats, 'agg')
    return {
        'kd': extract_stat(region, 'KillDeathRatio'),
        'rounds': extract_stat(region, 'RoundsPlayed'),
        'wins': extract_stat(region, 'Wins'),
        'kills': extract_stat(region, 'Kills')
    }


@lru_cache(24)
def get_stats_simple(name):
    stats = get_stats(name)
    return get_agg_simplified(stats)
