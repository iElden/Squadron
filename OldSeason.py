import json
from Squadron import OldSquadron, Division
from History import GlobalHistory

class OldSeason:
    def __init__(self, squadrons, histories):
        self.squadrons = squadrons
        self.histories = histories
        self.update_players_stats()

    @classmethod
    def from_json(cls, json_file):
        with open(json_file) as fd:
            js = json.load(fd)
        squadrons = [OldSquadron(s) for s in js['squadrons']]
        mapuche_history = GlobalHistory.from_json(js['matchs']['mapuche'], Division.MAPUCHE, squadrons)
        didons_hisory = GlobalHistory.from_json(js['matchs']['didon'], Division.DIDON, squadrons)
        return cls(squadrons, [mapuche_history, didons_hisory])

    def get_history_for(self, squadron):
        return sum([[match for match in history if squadron == match.team_1.squadron or squadron == match.team_2.squadron] for history in self.histories], [])

    def update_players_stats(self):
        for squadron in self.squadrons:
            for player in squadron.players:
                player.stats.reset()
        for history in self.histories:
            for match in history:
                for igteam in match.team_1, match.team_2:
                    for igplayer in igteam:
                        player = igteam.squadron.find_player(igplayer)
                        if player is None:
                            continue
                        if igteam.win:
                            player.stats.win += 1
                        else:
                            player.stats.lose += 1