import logging

from naff import Client, listen, Context
from naff.api.events import MessageCreate

from models import Player

log = logging.getLogger("client")
log.setLevel(logging.DEBUG)


class Bot(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.players: dict[int, Player] = {}

    @listen()
    async def on_startup(self):
        print(f"Logged in as {self.user.username}")
        print(
            f"https://discord.com/oauth2/authorize?client_id={self.app.id}&scope=bot&permissions=8"
        )

    @listen()
    async def on_message_create(self, event: MessageCreate):
        if event.message.author.bot:
            return
        player = self.get_player(event.message.author.id)
        player.add_xp(1)

    async def on_command(self, ctx: Context):
        await super().on_command(ctx)
        player = self.get_player(ctx.author.id)
        player.add_xp(2)

    def get_player(self, user_id: int) -> Player:
        """
        Get the player for the given user id.

        Args:
            user_id: The user ID

        Returns:
            The player for the given user id.
        """
        player = self.players.get(user_id)
        if not player:
            log.info(f"Creating new player ({user_id})")
            player = Player(user_id)
            self.players[user_id] = player
        return player
