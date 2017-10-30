from overwatch import Overwatch


def translate_stats(stats):
    """Translate the Overwatch stats into something more easy to digest."""
    i = 0
    return {stats[i]: stats[i + 1] for i in range(0, len(stats), 2)}


def simple_stats(translated_stats):
    """Reduce the full stat readout to 4 major ones."""
    return {
        'most_elims': translated_stats['Eliminations - Most in Game'],
        'most_dmg': translated_stats['All Damage Done - Most in Game'],
        'most_assists': translated_stats['Defensive Assists - Most in Game'] + '/' +
                        translated_stats['Offensive Assists - Most in Game'],
        'most_fire': translated_stats['Time Spent on Fire - Most in Game']
    }


def stats(name):
    """Retrieve the stats for Overwatch."""
    info = Overwatch(battletag=name, hero='all')
    stats = info()
    translated = translate_stats(stats)
    return simple_stats(translated)
