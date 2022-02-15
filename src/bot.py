#!/usr/bin/env python3

import os
import json

import asyncpg
import hikari
import lightbulb


class Yggdrasil(lightbulb.BotApp):
    # Load extensions from extension packages
    # Add extensions.json for enabling extensions
    def init_extensions(self, extension_dir:str) -> None:

        extension_config_dir = os.path.normpath(f'{extension_dir}/enabled_extensions.json')

        assert os.path.exists(
           extension_config_dir
        ), f"No extension config in {extension_config_dir} present!"

        with open(extension_config_dir, "r") as extension_file:
            extensions_config = json.load(extension_file)

        for extension in extensions_config:
            if extensions_config[extension]:
                self.load_extensions_from(
                    os.path.normpath(f'{extension_dir}/{extension}'),
                    must_exist=True
                )

    async def init_database(self) -> None:
        try:
            self.conn = await asyncpg.create_pool(
                user='postgres',
                password='pwd',
                database='yggdrasil',
                host='db'
            )
        except asyncpg.exceptions.InvalidCatalogNameError as e:
            self.conn = await asyncpg.create_pool(
                user='postgres',
                password='pwd',
                host='db'
            )
            #self.conn.execute() # add seeding if db is not present
            self.conn.close()
            self.conn = await asyncpg.create_pool(
                user='postgres',
                password='pwd',
                database='yggdrasil',
                host='db'
            )

def get_bot() -> Yggdrasil:
    bot = Yggdrasil(
        os.environ['bot_token'],
        prefix=":",
        intents=hikari.Intents.ALL,
        default_enabled_guilds=(int(os.environ['default_guild']))
    )

    @bot.command
    @lightbulb.add_checks(lightbulb.owner_only)
    @lightbulb.option(
        "extension_name", "The extension to be reloaded.", required=False
    )
    @lightbulb.command("reload_extension", description="Reloads a specific extension of the bot.")
    @lightbulb.implements(lightbulb.PrefixCommand)
    async def reload_extension(ctx: lightbulb.Context) -> None:

        if ctx.options.extension_name is None:
            await ctx.respond('Please specify an extension to be reloaded!')
            return

        try:
            is_first_load = False

            try:
                bot.unload_extensions(
                    f'src.extensions.{ctx.options.extension_name}.{ctx.options.extension_name}'
                )
            except lightbulb.errors.ExtensionNotLoaded:
                is_first_load = True

            bot.load_extensions(
                f'src.extensions.{ctx.options.extension_name}.{ctx.options.extension_name}'
            )

            if is_first_load:
                await ctx.respond(f"Loaded extension: {ctx.options.extension_name}!")
            else:
                await ctx.respond(f"Reloaded extension: {ctx.options.extension_name}!")

        except lightbulb.errors.ExtensionNotFound:
            await ctx.respond("Extension not found!")

    @bot.command
    @lightbulb.add_checks(lightbulb.owner_only)
    @lightbulb.command("purge_application_commands", "Purges all commands of this application.")
    @lightbulb.implements(lightbulb.PrefixCommand)
    async def purge_application_commands(ctx):
        await bot.purge_application_commands(ctx.guild_id)
        await ctx.respond("ok")

    bot.init_extensions(os.path.normpath(f"{os.getcwd()}/src/extensions"))
    hikari.internal.aio.get_or_make_loop().run_until_complete(bot.init_database())
    return bot
