from typing import Optional

import Squadron

class Global:
    squadrons = []

    @classmethod
    def get_squadron_by_id(cls, target):
        for squad in cls.squadrons:
            if squad.id == target:
                return squad
        return None
