#!/usr/bin/env python3

# replace 'placeholder' with your module name
# replace 'Placeholder' with the lightbulb plugin name

import json
import os

import hikari
import lightbulb


with open(os.path.normpath(f"{os.getcwd()}/src/extensions/welcome/config.json"), "r") as f:
    config = json.load(f)   #auf config kann per config["3"]

welcome_plugin = lightbulb.Plugin("Welcome") #Plugin generieren um welcome einzeln deaktivieren zu können ohne Bot funktionalitäten zu beinflussen.

@welcome_plugin.command #Z18-22 Erstellt Gruppe /welcome mit Beschreibung
@lightbulb.command("welcome", "Module for welcome messages") #Beschreibt Modul, erster Wert Blockbezeichnung im Slash Command, zweiter Beschreibung.
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def welcome_group(ctx: lightbulb.Context) -> None:
    pass  # as slash commands cannot have their top-level command ran, we simply pass here

@welcome_group.child #Unterordnung unter welcome Group aus 18-22
#@lightbulb.option("optionname", "description")
@lightbulb.command("send", "description", auto_defer=True)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def send(ctx: lightbulb.Context) -> None: #Command wird als Methode erstellt
    await ctx.respond(hikari.ResponseType.DEFERRED_MESSAGE_CREATE) # temporary fix as auto_defer doesn't work rn
    await ctx.respond(config["interaction"]["welcome message 1"]) #Bot Antwort aus config

def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(welcome_plugin)

def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(welcome_plugin)
