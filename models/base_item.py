from attrs import define, field
from naff import Snowflake_Type, MISSING

from models.exceptions import NotRepairable, NotDamageable

__all__ = ("BaseItem",)


@define()
class BaseItem:
    name: str = field()

    repairable: bool = field(default=False)
    invulnerable: bool = field(default=False)

    integrity: float = field(default=1.0)
    max_integrity: float = field(default=1.0)

    xp_multiplier: int = field(default=1)
    health_multiplier: int = field(default=1)

    emoji_id: Snowflake_Type = field(default=MISSING)

    @property
    def integrity_percentage(self) -> float:
        """Returns the integrity percentage of the item."""
        return self.integrity / self.max_integrity

    @property
    def destroyed(self) -> bool:
        """Returns whether the item is destroyed."""
        return self.integrity <= 0.0

    def damage(self, amount: float) -> float:
        """
        Damages the item by the given amount.
        Args:
            amount: The amount to damage the item by.

        Returns:
            The new integrity of the item.
        """
        if not self.invulnerable:
            self.integrity -= amount
            return self.integrity
        raise NotDamageable()

    def repair(self, amount: float) -> float:
        """
        Repairs the item by the given amount.
        Args:
            amount: The amount to repair the item by.

        Returns:
            The new integrity of the item.
        """
        if self.repairable:
            self.integrity += amount
            return self.integrity
        raise NotRepairable()
