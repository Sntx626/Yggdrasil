#!/usr/bin/env python3

# replace 'data_test' with your module name
# replace 'Data_Test' with the lightbulb plugin name

import json
import os

import hikari
import lightbulb


with open(os.path.normpath(f"{os.getcwd()}/src/extensions/data_test/config.json"), "r") as f:
    config = json.load(f)

data_test_plugin = lightbulb.Plugin("Data_Test")

@data_test_plugin.command
@lightbulb.command("data_test", "bar")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def data_test_group(ctx: lightbulb.Context) -> None:
    pass  # as slash commands cannot have their top-level command ran, we simply pass here

@data_test_group.child
@lightbulb.option("query", "description")
@lightbulb.command("execute", "description", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def execute(ctx: lightbulb.Context) -> None:
    await ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE) # temporary fix as auto_defer doesn't work rn

    response = ctx.bot.database.execute(ctx.options.query)

    await ctx.respond(str(response))

@data_test_group.child
@lightbulb.command("commit", "description", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def commit(ctx: lightbulb.Context) -> None:
    await ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE) # temporary fix as auto_defer doesn't work rn

    ctx.bot.database.commit()

    await ctx.respond("Commited changes")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(data_test_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(data_test_plugin)
