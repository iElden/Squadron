import discord
import logging
from typing import List, Optional
from Player import Player

CIVFR_ID = 197418659067592708
DIDON_REPORT = 682916309939519557
MAPUCHE_REPORT = 682924130181578762
CLAN_PMU = 420160838570213397

logger = logging.getLogger("DiscordClient")

class DiscordClient(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)
        self.civfr = None  # type: discord.Guild
        self.clan_pmu =  None # type: discord.TextChannel
        self.didon_report = None  # type: discord.TextChannel
        self.mapuche_report = None   # type: discord.TextChannel
        self.clan_members = None  # type: List[discord.Member]
        self.informations_loaded = False  # type: bool

    async def on_ready(self):
        self.civfr = self.get_guild(CIVFR_ID)
        self.clan_pmu = self.civfr.get_channel(CLAN_PMU)
        self.didon_report = self.civfr.get_channel(DIDON_REPORT)
        self.mapuche_report = self.civfr.get_channel(MAPUCHE_REPORT)
        self.clan_members = self.clan_pmu.members
        self.informations_loaded = True
        logger.info("ready")
        for role in self.civfr.roles:
            print(f"{role.id:>20}: {role.name}")


    async def launch(self, **kwargs):
        with open("private/token") as fd:
            _token = fd.read()
        await self.start(_token, **kwargs)

    def get_member_named(self, name) -> Optional[discord.Member]:
        member = discord.utils.find(lambda i: i.name.lower() == name.lower(), self.clan_members)
        if member:
            return member
        return discord.utils.find(lambda i: i.display_name.lower() == name.lower(), self.clan_members)

    def get_player(self, name) -> Player:
        player = Player(name)
        member = self.get_member_named(name)
        if member:
            player.fill_informations_with_discord(member)
        return player
