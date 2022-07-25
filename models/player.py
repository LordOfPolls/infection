import logging

from attrs import define, field
from naff import Snowflake_Type, Timestamp, MISSING, Embed

__all__ = ("Player",)

from models.base_item import BaseItem

log = logging.getLogger("player")
log.setLevel(logging.DEBUG)


@define()
class Player:
    id: Snowflake_Type = field()

    start_time: Timestamp = field(default=Timestamp.now())

    xp: float = field(default=0.0)

    health: float = field(default=100.0)
    max_health: float = field(default=100.0)

    zombie: bool = field(default=False)

    inventory: dict[BaseItem, int] = field(factory=dict)

    @property
    def stats_embed(self) -> Embed:
        """Returns an embed with the player's stats."""
        embed = Embed(
            title=f"{self.id}'s stats",
            description=f"**XP**: {self.xp}\n",
        )
        embed.add_field(name="Health", value=f"{self.health} / {self.max_health}")

        embed.add_field(name="Infected", value=f"Yes" if self.zombie else "No")

        embed.add_field(
            name="Inventory",
            value="\n-".join([item.name for item in self.inventory])
            if self.inventory
            else "Empty",
        )

        embed.set_footer("Start Time")
        embed.timestamp = self.start_time

        if self.zombie:
            embed.color = 0x51BF6D
        else:
            embed.color = 0x6D51BF

        return embed

    def heal(self, amount: float, with_multiplier: bool = True) -> float:
        """
        Heals the player by the given amount.

        Args:
            amount: The amount to heal the player by.
            with_multiplier: Whether to apply item's health multiplier.

        Returns:
            The new health of the player.
        """
        multiplier: float = 1.0

        if with_multiplier:
            for item, quantity in self.inventory.items():
                if item.health_multiplier != 1:
                    multiplier += item.health_multiplier * quantity

        heal_amount = min(amount * multiplier, self.max_health - self.health)
        self.health += heal_amount
        log.info(
            f"Healing {self.id} for {heal_amount} [{amount} * {multiplier}] ({self.health} / {self.max_health})"
        )
        return self.health

    def add_xp(self, amount: float, with_multiplier: bool = True) -> float:
        """
        Adds XP to the player.

        Args:
            amount: The amount of XP to add.
            with_multiplier: Whether to apply item's XP multiplier.
        """
        multiplier: float = 1.0

        if with_multiplier:
            for item, quantity in self.inventory.items():
                if item.xp_multiplier != 1:
                    multiplier += item.xp_multiplier * quantity

        xp_amount = amount * multiplier
        self.xp += xp_amount
        log.info(f"Adding {xp_amount} XP to {self.id} [{amount} * {multiplier}]")
        return self.xp

    def infect(self) -> None:
        """Infects the player."""
        log.info(f"Infecting {self.id}")
        self.zombie = True
        self.health = self.max_health

    def recover(self) -> None:
        """Recovers the player."""
        log.info(f"Recovering {self.id}")
        self.zombie = False
        self.health = self.max_health

    def attempt_infection(self) -> bool:
        """Attempts to infect the player. Will only succeed if the player's health is at 0"""
        if self.zombie:
            return False

        if self.health > 0:
            return False

        self.infect()
        return True

    def attempt_recovery(self) -> bool:
        """Attempts to recover the player. Will only succeed if the player's health is at 0"""
        if not self.zombie:
            return False

        if self.health > 0:
            return False

        self.recover()
        return True

    def reset_inventory(self) -> None:
        """Resets the player's inventory."""
        log.info(f"Resetting {self.id}'s inventory")
        self.inventory = {}

    def clean_inventory(self) -> None:
        """Cleans the player's inventory."""
        log.info(f"Cleaning {self.id}'s inventory")
        self.inventory = {
            item: quantity
            for item, quantity in self.inventory.items()
            if quantity > 0 and not item.destroyed
        }
