#!/usr/bin/env python3

# replace 'placeholder' with your module name
# replace 'Placeholder' with the lightbulb plugin name

import json
import os

import hikari
import lightbulb


with open(os.path.normpath(f"{os.getcwd()}/src/extensions/placeholder/config.json"), "r") as f:
    config = json.load(f)

placeholder_plugin = lightbulb.Plugin("Placeholder")

@placeholder_plugin.command
@lightbulb.command("placeholder", "bar")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def placeholder_group(ctx: lightbulb.Context) -> None:
    pass  # as slash commands cannot have their top-level command ran, we simply pass here

@placeholder_group.child
@lightbulb.option("optionname", "description")
@lightbulb.command("commandname", "description", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def commandname(ctx: lightbulb.Context) -> None:
    await ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE) # temporary fix as auto_defer doesn't work rn
    await ctx.respond('This is a response!')

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(placeholder_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(placeholder_plugin)
