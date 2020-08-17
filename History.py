from typing import List

from Match import Match
import Global

class GlobalHistory:
    def __init__(self, matchs, division):
        self.matchs : List[Match] = matchs
        self.division = division

    def get_history_for(self, squadron):
        return [match for match in self.matchs if squadron == match.team_1.squadron or squadron == match.team_2.squadron]

    def register_match(self, match):
        self.matchs.append(match)
        Global.Global.reload_full_history()

    def __iter__(self):
        for match in self.matchs:
            yield match

    def __add__(self, other):
        return GlobalHistory(self.matchs + other.matchs, self.division or other.division)

    def __bool__(self):
        return bool(self.matchs)

    def to_json(self):
        return [i.to_json() for i in self.matchs]

    @classmethod
    def from_json(cls, js, division, old_squadrons):
        return cls([Match.from_json(i, old_squadrons) for i in js], division)