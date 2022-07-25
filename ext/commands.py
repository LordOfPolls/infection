from naff import Extension, slash_command, InteractionContext, Embed


class Commands(Extension):
    @slash_command("heal")
    async def cmd_heal(self, ctx: InteractionContext):
        raise NotImplementedError

    @slash_command("stats")
    async def cmd_stats(self, ctx: InteractionContext):
        player = self.bot.get_player(ctx.author.id)
        await ctx.send(embed=player.stats_embed)

    @slash_command("infect")
    async def cmd_infect(self, ctx: InteractionContext):
        raise NotImplementedError

    @slash_command("leaderboard")
    async def cmd_leaderboard(self, ctx: InteractionContext):
        raise NotImplementedError


def setup(bot):
    Commands(bot)
