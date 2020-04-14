import discord
import logging
from asyncio import sleep
from typing import List, Optional, Tuple
import re

from Player import Player
from Match import Match
from History import GlobalHistory
from Squadron import Division, Squadron
from Global import Global, Constant

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
        await self.load()
        logger.info("ready")

    async def on_message(self, message : discord.Message):
        if message.channel in [self.didon_report, self.mapuche_report] and re.match(r"<@&\d+>\s*vs\s*<@&\d+>", message.content, re.IGNORECASE):
            history = Global.mapuche_history if message.channel == self.mapuche_report else Global.didon_history
            match = Match.parse_match(message)
            history.register_match(match)

    async def load(self):
        self.civfr = self.get_guild(CIVFR_ID)
        self.clan_pmu = self.civfr.get_channel(CLAN_PMU)
        self.didon_report = self.civfr.get_channel(DIDON_REPORT)
        self.mapuche_report = self.civfr.get_channel(MAPUCHE_REPORT)
        self.clan_members = self.clan_pmu.members
        self.informations_loaded = True

        Global.clan_member = self.clan_members

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

    async def get_history_for(self, channel_id):
        channel = self.get_channel(channel_id)
        messages = await channel.history().flatten()
        history = [Match.parse_match(msg) for msg in sorted(messages, key=lambda i:i.created_at) if re.match(r"<@&\d+>\s*vs\s*<@&\d+>", msg.content, re.IGNORECASE)]
        return [i for i in history if i]

    async def get_full_histories(self) -> List[GlobalHistory]:
        return [GlobalHistory((await self.get_history_for(channel_id)), div)
                                      for channel_id, div in [(MAPUCHE_REPORT, Division.MAPUCHE), (DIDON_REPORT, Division.DIDON)]]

    async def get_squadrons(self) -> Tuple[List[Squadron], List[Squadron]]:
        logger.info("Waiting for DiscordClient to load")
        await self.wait_until_ready()
        while not self.informations_loaded:
            await sleep(0.1)

        mapuche = [Squadron(Division.MAPUCHE, squad,
                            [Player(member) for member in self.clan_members if squad in member.roles])
                   for squad in [self.civfr.get_role(i) for i in Constant.MAPUCHE_SQUADS]]
        didon = [Squadron(Division.DIDON, squad,
                          [Player(member) for member in self.clan_members if squad in member.roles])
                 for squad in [self.civfr.get_role(i) for i in Constant.DIDON_SQUADS]]
        return mapuche, didon