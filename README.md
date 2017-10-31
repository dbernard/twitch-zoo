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
and collection of users to monitor. Each user has their own block, prefixed
with `USER_`.  If an Extra Life ID is associated with a username, a donation
link will appear alongside the stream.

Example:
```
[APP]
CLIENT_ID=[TWITCH_CLIENT_ID]
TEAM_ID=[EXTRA_LIFE_TEAM_ID]
PAGE_TITLE=[YOUR_PAGE_TITLE]

[USER_KWONSTANT]
NAME=Justin
TWITCH=kwonstant
EXTRALIFE=266807
PUBG=kwonstant
BLIZZARD=JayKwon#1164
```

