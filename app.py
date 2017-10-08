import json
import requests
import configparser
from flask import Flask, render_template, jsonify
from flask_bootstrap import Bootstrap

config = configparser.ConfigParser()
config.read('config/config.ini')

client_id = config['APP']['CLIENT_ID']
users = config['APP']['USERS'].split(',')


def create_app():
    """Create the Flask app with Bootstrap requirements.

    :return: The Flask app object
    """
    app = Flask(__name__)
    Bootstrap(app)

    return app


app = create_app()


def get_twitch_stream(user):
    """Request a user's stream information from the Twitch API.

    :param user: The streamer's username to query
    :return: An object representing the user's stream / information
    """
    headers = {'Accept': 'application/vnd.twitchtv.v3+json'}

    url = 'https://api.twitch.tv/kraken/streams/{}?client_id={}'.format(user,
                                                                      client_id)
    r = requests.get(url, headers=headers)

    r.raise_for_status()
    return json.loads(r.text)


def build_streamer_json(user, stream, participant_id):
    """Compile useful streamer information from a stream object.

    :param user: The username of the streamer
    :param stream: The complete stream JSON object
    :param participant_id: The user's Extra Life participant ID
    :return: A subset object of relevant streamer info
    """
    donate_url = 'http://www.extra-life.org/index.cfm?fuseaction=donorDrive.' \
                 'participant&participantID={}'.format(participant_id)
    s = {
        'username': user,
        'playing': 'Offline',
        'viewers': 0,
        'url': 'https://www.twitch.tv/{}'.format(user),
        'preview': 'http://placehold.it/640x360',
        'participant_id': participant_id,
        'donate': donate_url if participant_id else None,
        'fps': 0,
        'views': 0
    }

    if not stream['stream']:
        return s

    s['username'] = stream['stream']['channel']['display_name']
    s['playing'] = stream['stream']['game'][:20]
    s['viewers'] = stream['stream']['viewers']
    s['preview'] = stream['stream']['preview']['large']
    s['fps'] = stream['stream']['average_fps']
    s['views'] = stream['stream']['channel']['views']

    return s


def get_streams(streamers):
    """Get stream information about each streamer provided.

    :param streamers: A list of streamer usernames and their Extra Life
                      participant ID's if applicable
    :return: A list of relevant streamer info for each streamer
    """
    streams = []

    for user in streamers:
        if '|' in user:
            user, participant_id = user.split('|')
        else:
            participant_id = None
        try:
            stream = get_twitch_stream(user)
            info = build_streamer_json(user, stream, participant_id)
            streams.append(info)
        except requests.exceptions.HTTPError as htp:
            app.logger.error("Couldn't load user '%s': %s", user, htp)

    return filter(lambda s: s['playing'] != 'Offline', streams)


@app.route('/')
def index():
    """Render the main index page with stream information.
    """
    streams = get_streams(users)
    return render_template('index.html', streams=streams)


@app.route('/streamers')
def streamers():
    """Get the JSON representation of stream information (useful for debugging).
    """
    streams = get_streams(users)

    return jsonify(streams)


if __name__ == '__main__':
    app.run(debug=True)

