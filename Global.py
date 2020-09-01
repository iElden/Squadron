import asyncio
import json
from typing import Tuple
from shutil import copyfile
from datetime import datetime

class Constant:
    MAPUCHE_SQUADS = [682245125656805459, 682919453788471306, 682245596324823053,
                      652143977260122125, 708475861606596612, 708475862860824598]
    DIDON_SQUADS = [708475004744106024, 708475012624941107, 708475862693052438, 708475854941847665,
                    708475858486034474, 708475860348567612, 682920185547587594]
    CHRISTINE_SQUADS = [708475861292286024, 708475865314361394, 708475865494978612,
                        708475021621723137, 708475864110596107, 708475864115052635]
    CURRENT_SEASON = "5"

class Global:
    squadrons = None
    leaders = None
    clan_member = None
    discord_client = None
    loop = None
    mapuches = didons = christines = None
    mapuche_history = didon_history = christine_history = None
    histories = None
    full_history = None
    ignore_match = []
    old_season = {}

    @classmethod
    def get_squadron_by_id(cls, target):
        for squad in cls.squadrons:
            if squad.id == target:
                return squad
        return None

    @classmethod
    def get_member_by_id(cls, discord_id):
        for member in cls.clan_member:
            if member.id == discord_id:
                return member
        return None

    @classmethod
    def get_member_by_name(cls, name):
        for member in cls.clan_member:
            if name.lower() == member.name.lower():
                return member
        for member in cls.clan_member:
            if name.lower() in member.name.lower():
                return member
        return None
    
    @classmethod
    def load(cls):
        from DiscordClient import DiscordClient
        cls.discord_client = DiscordClient()
        cls.loop = asyncio.get_event_loop()
        cls.loop.create_task(cls.discord_client.launch())
        cls.reload()

    @classmethod
    def reload(cls):
        import OldSeason
        cls.mapuches, cls.didons, cls.christines = cls.loop.run_until_complete(cls.discord_client.get_squadrons())
        cls.squadrons = cls.mapuches + cls.didons + cls.christines
        # TODO: Déspaghettisifier tout ça !
        cls.histories, cls.ignore_match = cls.load_histories_from_json()
        loaded_histories = cls.loop.run_until_complete(
            cls.discord_client.get_full_histories(ignore_matchs_ids=sum([[match.id for match in history] for history in cls.histories], []))
        )
        if any(loaded_histories):
            cls.histories = [sh + lh for sh, lh in zip(cls.histories, loaded_histories)]
            cls.save_histories_to_json()
        cls.mapuche_history, cls.didon_history, cls.christine_history = cls.histories
        cls.old_season = {"3": OldSeason.OldSeason.from_json("save_squadron_season3.json"),
                          "4": OldSeason.OldSeason.from_json("save_squadron_season4.json")}
        cls.reload_full_history()
        cls.update_players_stats()

    @classmethod
    def reload_full_history(cls):
        from History import GlobalHistory
        cls.full_history = GlobalHistory(sum([i.matchs for i in cls.histories], []), None)


    @classmethod
    def load_histories_from_json(cls) -> Tuple[list, list]:
        from History import GlobalHistory
        from Squadron import Division
        with open("current_season.json") as fd:
            js = json.load(fd)
        return [GlobalHistory.from_json(histo, Division(div), cls.squadrons)
                for div, histo in js['histories'].items()], js['ignore_ids']

    @classmethod
    def save_histories_to_json(cls):
        copyfile("current_season.json", f"backup_json/{datetime.now().strftime('%Y_%m_%d-%H_%M_%S')}.json")
        with open("current_season.json", 'w') as fd:
            json.dump({'histories': {i.division.value: i.to_json() for i in cls.histories}, 'ignore_ids': cls.ignore_match}, fd, indent=4)

    @classmethod
    def reset_players_stats(cls):
        for squadron in cls.squadrons:
            for player in squadron.players:
                player.stats.reset()

    @classmethod
    def update_players_stats(cls):
        cls.reset_players_stats()
        for history in cls.histories:
            for match in history:
                for igteam in match.team_1, match.team_2:
                    for igplayer in igteam:
                        if not igteam.squadron:  # Anti-fail : should not be triggered
                            continue
                        player = igteam.squadron.find_player(igplayer)
                        if player is None:
                            continue
                        if igteam.win:
                            player.stats.win += 1
                        else:
                            player.stats.lose += 1