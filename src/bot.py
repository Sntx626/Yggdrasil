#!/usr/bin/env python3

import os
import json

import asyncpg
import hikari
import lightbulb


class Yggdrasil(lightbulb.BotApp):
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
            self.db_pool = await asyncpg.create_pool(
                user=os.environ['POSTGRES_USER'],
                password=os.environ['POSTGRES_PASSWORD'],
                database=os.environ['POSTGRES_DB'],
                host=os.environ['POSTGRES_HOST']
            )
        except asyncpg.exceptions.InvalidCatalogNameError as e:
            self.db_pool = await asyncpg.create_pool(
                user=os.environ['POSTGRES_USER'],
                password=os.environ['POSTGRES_PASSWORD'],
                host=os.environ['POSTGRES_HOST']
            )
            async with self.db_pool.acuire() as conn:
                await conn.execute("CREATE DATABASE $1", os.environ['POSTGRES_DB'])
                # seed database
            self.db_pool.close()

            self.db_pool = await asyncpg.create_pool(
                user=os.environ['POSTGRES_USER'],
                password=os.environ['POSTGRES_PASSWORD'],
                database=os.environ['POSTGRES_DB'],
                host=os.environ['POSTGRES_HOST']
            )

def get_bot() -> Yggdrasil:
    bot = Yggdrasil(
        os.environ['bot_token'],
        prefix=":",
        intents=hikari.Intents.ALL,
        default_enabled_guilds=(int(os.environ['default_guild']))
    )

    bot.init_extensions(os.path.normpath(f"{os.getcwd()}/src/extensions"))
    hikari.internal.aio.get_or_make_loop().run_until_complete(bot.init_database())

    return bot
