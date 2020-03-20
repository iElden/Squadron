from typing import List

from Match import Match

class GlobalHistory:
    def __init__(self, matchs, division):
        self.matchs : List[Match] = matchs
        self.division = division

    def get_history_for(self, squadron):
        return [match for match in self.matchs if squadron == match.team_1.squadron or squadron == match.team_2.squadron]

