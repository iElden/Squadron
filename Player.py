import discord

class Player:
    def __init__(self, obj):
        self.name = str(obj)
        self.member = None
        self.avatar_url = "/img/unknown.png"
        if isinstance(obj, discord.Member):
            self.fill_informations_with_discord(obj)

    def fill_informations_with_discord(self, member):
        self.member = member
        self.name = member.name
        self.avatar_url = member.avatar_url

    def __str__(self):
        return self.name

    @property
    def win_ratio(self):
        return "W: 0 / L: 0"