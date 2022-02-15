# Ygggdrasil

A simplistic bot designed to streamline your server experience.

Design Ideas

- Seperate commands into submodules
- Nothing too fancy -> Descriptive commands, recurring command structure, embeds responses only if not possible otherwise

## Disclaimer

This bot is currently in development and probably won't work fine just now.
Try at your own risk!

## Features

Restrictions (by Discord)

- An app can have up to 50 top-level global commands (50 commands with unique names)
- An app can have up to an additional 50 guild commands per guild
- An app can have up to 10 subcommand groups on a top-level command
- An app can have up to 10 subcommands within a subcommand group
- Choices can have up to 10 values per option
- Commands can have up to 10 options per command

Limitations on [command names](https://discord.com/developers/docs/interactions/slashCommand-commands#registering-a-command)

Limitations on [nesting subcommands and groups](https://discord.com/developers/docs/interactions/slashCommand-commands#nested-subcommands-and-groups)

### Command Structure

#### Base

``` txt
base # base
|
|__ reload_extension # command
-> Reloads an extension by name.
|
|__ purge_application_commands # command
-> Purge all slashCommands for this application.
```

#### Admin

```txt
admin # extension
|
|__ bot # command (prefixCommand slashCommand)
    |
    |__ restart # subcommand (prefixCommand) (bot owner only)
    -> Restarts the bot.
    |
    |__ shutdown # subcommand (prefixCommand) (bot owner only)
    -> Shuts down the bot.
    |
    |__ ping # subcommand (slashCommand)
    -> Lets the bot ping Discord and prints the Ping to the current channel.
|
|__ admin # command (prefixCommand)
    |
    |__ kick # subcommand (prefixCommand) (KICK_MEMBERS only)
    -> Kicks a specified user.
    |
    |__ ban # subcommand (prefixCommand) (BAN_MEMBERS only)
    -> Kicks a specified user.
    |
    |__ unban # subcommand (prefixCommand) (BAN_MEMBERS only)
    -> Kicks a specified user.
|
|__ server # command (prefixCommand)
    |
    |__ announce # subcommand (prefixCommand) (ADMINISTRATOR only)
    -> Takes an Embed as Webhook embed json as text and sends it to the announcement channel.
    |
    |__ clear # subcommand (prefixCommand) (MANAGE_MESSAGES only)
    -> Purges the current channel by 1 message, unless specified otherwise (Admin only).
```

#### Dice

```txt
dice # extension
|
|__ dice # command (prefixCommand, slashCommand)
    |
    |__ roll # subcommand (prefixCommand, slashCommand)
    -> Throws dice eg.: 3d6
    |
    |__ hroll # subcommand (prefixCommand)
    -> Throws dice eg.: 3d6, responds with epemeral message
```

Should we allow prefixCommand here?

#### Experience

```txt
experience # extension
|
|__ experience # command (prefixCommand, slashCommand)
    |
    |__ xp # subcommand (slashCommand)
    -> Prints the current stats of the user.
    |
    |__ leaderboard # subcommand (slashCommand)
    -> Print the top-ten members of the guild and the users relation to them.
    |
    |__ updateUser # subcommand (prefixCommand) (ADMINISTRATOR only)
    -> Overwrites the data of a given user in the database, or creates new if not present.
```

Will later receive an update with role/permission changes based on level of members.

#### Misc

```txt
misc # extension
|
|__ misc # command
    |
    |__ datecounter # subcommand (slashCommand)
    -> Prints the number of days from or to a given date.
    |
    |__ echo # subcommand (slashCommand)
    -> Echos text as Embed title.
    |
    |__ embed # subcommand (slashCommand)
    -> Echos text as Embed.
    |
    |__ fibonacci # subcommand (slashCommand)
    -> Prints the n-Fibonacci number.
    |
    |__ reverse # subcommand (slashCommand)
    -> Reverses the letter order of the text given and print it.
```

#### Voice

```txt
voice # extension
|
|__ setCategoryId # command (prefixCommand) (ADMINISTRATOR only)
-> Sets the category id of the Category for temporary voicechannel to be created in.
|
|__ setChannelId # command (prefixCommand) (ADMINISTRATOR only)
-> Sets the channel id of the channel to listen to for user join.
|
|__ voice # command
    |
    |__ claim # subcommand (slashCommand)
    -> Lets the user claim the current channel.
    |
    |__ limit # subcommand (slashCommand)
    -> Lets the user limit the number of member in their channel.
    |
    |__ lock # subcommand (slashCommand)
    -> Locks the users channel.
    |
    |__ name # subcommand (slashCommand)
    -> Changes the channelname of the users channel.
    |
    |__ permit # subcommand (slashCommand)
    -> Permits a given user to join the users channel, even if it's locked.
    |
    |__ reject # subcommand (slashCommand)
    -> Revokes the permission given to a user to join the users channel.
    |
    |__ unlock # subcommand (slashCommand)
    -> Unlocks the users channel.
    |
    |__ bitrate # subcommand (slashCommand)
    -> Changes the users channels bitrate.
```

#### Wolfram

```txt
wolfram # extension
|
|__ wolfram # command
    |
    |__ ask # subcommand (prefixCommand, slashCommand)
    -> Send a Wolframalpha query.
```

Should we allow prefixCommand here?

## Running the bot

Run the bot:
`docker-compose up -d`

View the current logs:
`docker-compose logs -f`

Stop the bot:
`docker-compose down`

### Debugging commands

Connect to Postgres (Yggdrasil DB):
`docker exec -it PostgreSQL psql -U postgres yggdrasil`

Backup Postgres (Yggdrasil DB):
`docker exec -it postgres pg_dump -U postgres yggdrasil > outfile`
