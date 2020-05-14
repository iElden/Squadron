import discord
from Global import Global
from typing import Optional

class Player:
    def __init__(self, obj):
        self.name : str = str(obj)
        self.member : Optional[discord.Member] = None
        self.avatar_url : str = "/img/unknown.png"
        if isinstance(obj, discord.Member):
            self.fill_informations_with_discord(obj)
        self.stats = PlayerStats()

    def fill_informations_with_discord(self, member):
        self.member = member
        self.name = member.name
        self.avatar_url = member.avatar_url

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    @property
    def win_ratio(self):
        return f"W: {self.stats.win} / L: {self.stats.lose} ({self.stats.str_win_ratio} %)"

    def to_json(self):
        return {
            "discord_id": None if not self.member else self.member.id,
            "name": self.name
        }

    @classmethod
    def from_json(cls, js):
        member = Global.discord_client.get_member(js['discord_id'])
        return cls(member if member else js['name'])



class PlayerStats:
    def __init__(self):
        self.win = 0
        self.lose = 0
        self.scrap = 0

    @property
    def win_ratio(self) -> float:
        if not self.lose and not self.win:
            return 0
        return self.win / (self.lose + self.win)

    @property
    def str_win_ratio(self) -> str:
        if not self.lose and not self.win:
            return 'N/A'
        return str(self.win * 100 // (self.lose + self.win))

    def reset(self):
        self.__init__()