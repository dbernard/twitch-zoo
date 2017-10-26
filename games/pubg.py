"""Module to ease interaction with PlayerUnknown's Battlegrounds."""

from functools import lru_cache

from pypubg import core

from games import config


API = core.PUBGAPI(config['GAMES']['PUBG_API_KEY'])


def get_stats(name, api=API):
    """Get the full stats for a given player name.

    :param name: the account name of the player to retrieve
    :param api: (optional) an instance of `pypubg.core.PUBGAPI` to use
    :returns: the full stats dict for a given player

    """
    return api.player(name)


def extract_stat(region, desired_field):
    """Safely extract a statistic from a region's stats.

    :param region: the region block from the full stats lookup
    :param desired_field: the name of the field to retrieve
    :returns: the given stat, or -1 if not found

    """
    for stat in region['Stats']:
        if stat['field'] == desired_field:
            return stat['value']
    return '-1'


def extract_region(stats, region_name='agg', match='squad'):
    """Safely extract a region from the full stat rollup.

    :param stats: the full stats lookup for a player
    :param region: the region to extract from the full lookup, defaults to `agg`
    :param match: the type of game to extract from the lookup, defaults to `squad`
    :returns: the region block if located, an empty `dict` if not found

    """
    for region in stats['Stats']:
        if region['Region'] == region_name and region['Match'] == match:
            return region
    return {}


def get_agg_simplified(stats):
    """Get a simplified version with more compact data representing the player.

    :param stats: the full stats lookup for a player.
    :returns: a simplified dict containing the information

    """
    region = extract_region(stats, 'agg')
    return {
        'kd': extract_stat(region, 'KillDeathRatio'),
        'rounds': extract_stat(region, 'RoundsPlayed'),
        'wins': extract_stat(region, 'Wins'),
        'kills': extract_stat(region, 'Kills')
    }


@lru_cache(24)
def get_stats_simple(name):
    """Helper function to quickly retrieve stats from all regions.

    :param name: the account name to retrieve
    :returns: the simplified stats for the provided account name

    """
    stats = get_stats(name)
    return get_agg_simplified(stats)


def stats(name):
    """Get the full stats for a given player name.

    :param name: the account name to pull stats for
    :returns: the simplified stats for a given account name

    """
    return get_stats_simple(name)
