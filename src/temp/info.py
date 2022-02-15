import hikari
import lightbulb

from datetime import datetime
from lightbulb import commands, context

info_plugin = lightbulb.Plugin("Info")


@info_plugin.command
@lightbulb.option("target", "The member to get information about.", hikari.User, required=False)
@lightbulb.command("userinfo", "Get info on a server member.")
@lightbulb.implements(commands.PrefixCommand, commands.SlashCommand)
async def userinfo(ctx: context.Context) -> None:
    target = ctx.options.target if ctx.options.target is not None else ctx.user
    target = ctx.get_guild().get_member(target)

    if not target:
        await ctx.respond("That user is not in the server.")
        return

    created_at = int(target.created_at.timestamp())
    joined_at = int(target.joined_at.timestamp())

    roles = (await target.fetch_roles())[1:]  # All but @everyone

    embed = (
        hikari.Embed(
            title=f"User Info - {target.display_name}",
            description=f"ID: `{target.id}`",
            colour=0x000000,
            timestamp=datetime.now().astimezone(),
        )
        .set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
        .set_thumbnail(target.avatar_url)
        .add_field(
            "Bot?",
            target.is_bot,
            inline=True,
        )
        .add_field(
            "Created account on",
            f"<t:{created_at}:d> (<t:{created_at}:R>)",
            inline=True,
        )
        .add_field(
            "Joined server on",
            f"<t:{joined_at}:d> (<t:{joined_at}:R>)",
            inline=True,
        )
        .add_field(
            "Roles",
            ", ".join(r.mention for r in roles),
            inline=False,
        )
    )

    await ctx.respond(embed)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(info_plugin)
