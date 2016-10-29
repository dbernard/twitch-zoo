# Twitch Zoo

A simple Twitch.tv stream aggregator for a list of users. Initially intended for
use during the Extra Life charity event.

## Example

A sample result given the names of 3 popular streamers (streamers shown below
are not associated with HumanGeo).

![Sample webpage][example]


[example]: img/example.png

## Configuration

Edit the `config.ini` file with your Twitch API client ID and collection of users to monitor.  THe users collection can be either plain Twitch user names, or a pipe-delimited collection of Twitch usernames and Extra Life participant ID numbers (i.e. `user|participantId`).  If an Extra Life ID is associated with a username, a donation badge will appear alongside the stream.
