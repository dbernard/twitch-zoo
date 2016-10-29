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
    app = Flask(__name__)
    Bootstrap(app)

    return app


app = create_app()


def get_twitch_stream(user):
    headers = {'Accept': 'application/vnd.twitchtv.v3+json'}

    url = 'https://api.twitch.tv/kraken/streams/{}?client_id={}'.format(user,
                                                                      client_id)
    r = requests.get(url, headers=headers)

    return json.loads(r.text)


def build_streamer_json(user, stream):
    s = {
        'username': user,
        'playing': 'Offline',
        'viewers': 0,
        'url': '#',
        'preview': 'http://placehold.it/640x360'
    }

    if not stream['stream']:
        return s

    s['username'] = stream['stream']['channel']['display_name']
    s['playing'] = stream['stream']['game']
    s['viewers'] = stream['stream']['viewers']
    s['url'] = stream['stream']['channel']['url']
    s['preview'] = stream['stream']['preview']['large']

    return s


def get_streams(streamers):
    streams = []

    for user in streamers:
        stream = get_twitch_stream(user)
        info = build_streamer_json(user, stream)
        streams.append(info)

    return streams


@app.route('/')
def index():
    streams = get_streams(users)
    return render_template('index.html', streams=streams)


@app.route('/streamers')
def streamers():
    streams = get_streams(users)

    return jsonify(streams)


if __name__ == '__main__':
    app.run()

