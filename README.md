# Twitch Zoo

A simple Twitch.tv stream aggregator for a list of users. Initially intended for
use during the Extra Life charity event.

## Example

A sample result given the names of 3 popular streamers (streamers shown below
are not associated with HumanGeo).

![Sample webpage][example]


[example]: static/images/example.png

## Configuration

Edit the `config.ini` file with your Twitch API client ID
([generated here](https://www.twitch.tv/settings/connections)), your Extra Life
team ID (in the URL for your team page:
`https://www.extra-life.org/index.cfm?fuseaction=donorDrive.team&teamID=[THIS_IS_YOUR_TEAM_ID]`,
and collection of users to monitor. The users collection can be either plain
Twitch user names, or a pipe-delimited collection of Twitch usernames and Extra
Life participant ID numbers (i.e. `user|participantId`).  If an Extra Life ID
is associated with a username, a donation link will appear alongside the
stream.

Example:
```
[APP]
CLIENT_ID=[TWITCH_CLIENT_ID]
TEAM_ID=[EXTRA_LIFE_TEAM_ID]
USERS=USER1|214742,USER2,USER3|214742
```

