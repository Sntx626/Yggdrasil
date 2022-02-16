#!/usr/bin/env python3

# replace 'base' with your module name
# replace 'Base' with the lightbulb plugin name

import json
import os

import hikari
import lightbulb


with open(os.path.normpath(f"{os.getcwd()}/src/extensions/base/config.json"), "r") as f:
    config = json.load(f)

base_plugin = lightbulb.Plugin("Base")

@base_plugin.command
@lightbulb.command("base", "Includes all of the core modules of the bot!")
@lightbulb.implements(lightbulb.SlashCommandGroup, lightbulb.PrefixCommandGroup)
async def base_group(ctx: lightbulb.Context) -> None:
    pass  # as slash commands cannot have their top-level command ran, we simply pass here

@base_group.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.option(
    "extension_name", "The extension to be reloaded.", required=False
)
@lightbulb.command("reload_extension", description="Reloads a specific extension of the bot.")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def reload_extension(ctx: lightbulb.Context) -> None:
    if ctx.options.extension_name is None:
        await ctx.respond('Please specify an extension to be reloaded!')
        return

    try:
        is_first_load = False

        try:
            ctx.bot.unload_extensions(
                f'src.extensions.{ctx.options.extension_name}.{ctx.options.extension_name}'
            )
        except lightbulb.errors.ExtensionNotLoaded:
            is_first_load = True

        ctx.bot.load_extensions(
            f'src.extensions.{ctx.options.extension_name}.{ctx.options.extension_name}'
        )

        if is_first_load:
            await ctx.respond(f"Loaded extension: {ctx.options.extension_name}!")
        else:
            await ctx.respond(f"Reloaded extension: {ctx.options.extension_name}!")

    except lightbulb.errors.ExtensionNotFound:
        await ctx.respond("Extension not found!")

@base_group.child
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("purge_application_commands", "Purges all commands of this application.")
@lightbulb.implements(lightbulb.PrefixSubCommand)
async def purge_application_commands(ctx: lightbulb.Context) -> None:
    await ctx.bot.purge_application_commands(ctx.guild_id)
    await ctx.respond("ok")

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(base_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(base_plugin)
