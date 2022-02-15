#!/usr/bin/env python3

import json
import os

import hikari
import lightbulb
import wolframalpha


with open(os.path.normpath(f"{os.getcwd()}/src/extensions/wolframalpha/config.json"), "r") as f:
    config = json.load(f)

wolfram_client = wolframalpha.Client(config["app_id"])

wolframalpha_plugin = lightbulb.Plugin("WolframAlpha")

@wolframalpha_plugin.command
@lightbulb.command("wolframalpha", "Compute expert-level answers using Wolfram’s breakthrough algorithms, knowledgebase & AI technology.")
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def wolframalpha_group(ctx: lightbulb.Context) -> None:
    pass  # as slash commands cannot have their top-level command ran, we simply pass here

@wolframalpha_group.child
@lightbulb.option("question", "Your question to the almighty WolframAlpha.")
@lightbulb.command("ask", "Query a question to WolframAlpha.", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def ask(ctx: lightbulb.Context) -> None:
    await ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE)
    try:
        res = wolfram_client.query(ctx.options.question)
        answer = next(res.results).text
    except:
        answer = None

    if answer is None or answer == "":
        await ctx.respond("You Question returned no answer...")
        return

    assert type(answer) is str, "Wolframalpha did not return answer as str!"
    await ctx.respond(f'WolframAlpha returned:\n`{str(answer)}`')

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(wolframalpha_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(wolframalpha_plugin)
