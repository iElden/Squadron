import gspread
from oauth2client.service_account import ServiceAccountCredentials as sac
from typing import List, Tuple
from enum import Enum

GDOC_KEY = "1sbYm75v8lg4qerV6PlCm2i-7EEkUokjZ-AdArik6Vak"

credentials = sac.from_json_keyfile_name("private/googlekey.json", ["https://spreadsheets.google.com/feeds"])
gc = gspread.authorize(credentials)

class Division(Enum):
    MAPUCHE = "Mapuche"
    DIDON = "Didon"

class Squadron:
    def __init__(self, div, name, players):
        self.division: Division = div
        self.name : str = name
        self.formated_name : str = name.lower().replace(' ', '')
        self.players : List[str] = players
    def __str__(self):
        return f"{self.name} ({self.division}): {', '.join(self.players)}"

def get_squadron() -> Tuple[List[Squadron], List[Squadron]]:
    wb = gc.open_by_key(GDOC_KEY)
    squadron_sheet = wb.get_worksheet(1).get_all_values()

    mapuche = [Squadron(Division.MAPUCHE, squadron_sheet[21][j], [squadron_sheet[i][j] for i in range(22, 33) if squadron_sheet[i][j]]) for j in range(1, 6)]
    didon = [Squadron(Division.DIDON, squadron_sheet[34][j], [squadron_sheet[i][j] for i in range(35, 46) if squadron_sheet[i][j]]) for j in range(1, 6)]
    return mapuche, didon
