import logging
import discord
from asyncio import sleep
from enum import Enum
from typing import List, Tuple

from Player import Player

logger = logging.getLogger(__name__)

class Division(Enum):
    MAPUCHE = "Mapuche"
    DIDON = "Didon"

class Squadron:
    def __init__(self, div, role, players):
        self.division: Division = div
        self.role : discord.Role = role
        self.id : int = role.id
        self.name : str = role.name
        self.formated_name : str = self.name.lower().replace(' ', '')
        self.players : List[Player] = players
    def __str__(self):
        return f"{self.name} ({self.division}): {', '.join([str(i) for i in self.players])}"

    def __int__(self):
        return self.id

    def get_player(self, discord_id):
        for player in self.players:
            if player.member and player.member.id == discord_id:
                return player
        return None
