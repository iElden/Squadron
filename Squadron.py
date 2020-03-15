import logging
from asyncio import sleep
from enum import Enum
from typing import List, Tuple

from Player import Player

logger = logging.getLogger(__name__)

MAPUCHE_SQUADS = [652144868109582357, 682245125656805459, 682247440346513430, 682917973287239693, 682919453788471306]
DIDON_SQUADS = [682245427722190881, 682245588389200108, 682245596324823053, 682920185547587594, 652144537535512586]

class Division(Enum):
    MAPUCHE = "Mapuche"
    DIDON = "Didon"

class Squadron:
    def __init__(self, div, name, players):
        self.division: Division = div
        self.name : str = name
        self.formated_name : str = name.lower().replace(' ', '')
        self.players : List[Player] = players
    def __str__(self):
        return f"{self.name} ({self.division}): {', '.join([str(i) for i in self.players])}"

from DiscordClient import DiscordClient
async def get_squadrons(discord_client: DiscordClient) -> Tuple[List[Squadron], List[Squadron]]:
    logger.info("Waiting for DiscordClient to load")
    await discord_client.wait_until_ready()
    while not discord_client.informations_loaded:
        await sleep(0.1)

    mapuche = [Squadron(Division.MAPUCHE, squad.name,
                        [member for member in discord_client.clan_members if squad in member.roles])
               for squad in [discord_client.civfr.get_role(i) for i in MAPUCHE_SQUADS]]
    didon = [Squadron(Division.DIDON, squad.name,
                        [member for member in discord_client.clan_members if squad in member.roles])
               for squad in [discord_client.civfr.get_role(i) for i in DIDON_SQUADS]]
    return mapuche, didon
