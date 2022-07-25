from naff import (
    Extension,
    slash_command,
    InteractionContext,
    Embed,
    slash_option,
    OptionTypes,
    User,
)


class Commands(Extension):
    @slash_command("debug")
    async def debug(self, ctx: InteractionContext):
        ...

    @debug.subcommand("infect")
    @slash_option("user", "the user in question", OptionTypes.USER, required=True)
    async def debug_infect(self, ctx: InteractionContext, user: User):
        player = self.bot.get_player(user.id)
        player.infect()
        await ctx.send(embed=player.stats_embed)

    @debug.subcommand("recover")
    @slash_option("user", "the user in question", OptionTypes.USER, required=True)
    async def debug_recover(self, ctx: InteractionContext, user: User):
        player = self.bot.get_player(user.id)
        player.recover()
        await ctx.send(embed=player.stats_embed)

    @debug.subcommand("heal")
    @slash_option("user", "the user in question", OptionTypes.USER, required=True)
    @slash_option("amount", "the amount to heal", OptionTypes.NUMBER, required=True)
    async def debug_heal(self, ctx: InteractionContext, user: User, amount: float):
        player = self.bot.get_player(user.id)
        player.heal(amount)
        await ctx.send(embed=player.stats_embed)


def setup(bot):
    Commands(bot)
