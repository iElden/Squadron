import logging
import csv
import re
from Global import Global

logger = logging.getLogger("Leaders")

NON_WORD = re.compile(r"[^\wÀ-ú]+")

class Leaders:
    def __init__(self, leaders):
        self.leaders = leaders

    def __getitem__(self, item):
        return self.leaders[item]

    def __iter__(self):
        for i in self.leaders:
            yield i

    def _get_leader_named(self, name):
        result = [leader for leader in self if leader == name]
        if len(result) > 1:
            logger.warning(f"{len(result)} results found for name \"{name}\"")
            return None
        if result:
            return result[0]
        result = [leader for leader in self if leader.is_in(name)]
        if len(result) == 1:
            return result[0]
        return None

    def get_leader_named(self, name):
        if name is None:
            return None
        name = name.lower()
        leader = self._get_leader_named(name)
        if leader:
            return leader
        for i in NON_WORD.split(name):
            leader = self._get_leader_named(i)
            if leader:
                return leader
        return None

class Leader:
    def __init__(self, emoji_id, uuname, name, civ, *alias):
        self.emoji_id = int(emoji_id)
        self.uuname = uuname
        self.name = name
        self.civ = civ
        self.alias = alias
        self.all_name = [i.lower() for i in [uuname, name, civ, *alias]]

    def __repr__(self):
        return f"<Leader: {self.uuname}>"

    def __eq__(self, other):
        if isinstance(other, str):
            return other.lower() in self.all_name
        return self.uuname == other.uuname

    def is_in(self, other : str) -> bool:
        other = other.lower()
        for i in self.all_name:
            if other in i:
                return True
        return False

def load_leaders():
    with open("leaders.csv", "r") as fd:
        leaders_array = csv.reader(fd, delimiter=',')
        leaders = Leaders([Leader(*leader_array) for leader_array in leaders_array])
        Global.leaders = leaders
        return leaders