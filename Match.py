from Player import Player
from Global import Global

import discord
from typing import List, Optional
from enum import Enum
from datetime import timedelta, datetime
import re
import logging

logger = logging.getLogger("Match")

MATCH_REGEX = re.compile(r"<@&(?P<SquadID1>\d+)>\s*vs\s*<@&(?P<SquadID2>\d+)>\s*\n\s*map.*:\s*(?P<Map>.+)\s*bans?\s*:\s*(?P<Bans>.+?)\s*<@&(?P<SquadReportID1>\d+)> *(?P<VictoryReport1>.+?)? *\n(?P<Team1Query>[\s\S]+?)\s*<@&(?P<SquadReportID2>\d+)> *(?P<VictoryReport2>.+?)? *\n(?P<Team2Query>[\s\S]+)", re.IGNORECASE)
VICTORY_TURN = re.compile(r"(?:tours?|t)\s*(\d+)", re.IGNORECASE)

class VictoryType(Enum):
    CC = "Concédée"
    SCORE = "Score"
    SCIENCE = "Scientifique"
    CULTURE = "Culturelle"
    MILITARY = "Militaire"
    RELIGIOUS = "Religieuse"
    DIPLOMACY = "Diplomatique"
    UNKNOWN = "???"

    @classmethod
    def get_from_query(cls, query):
        query = query.lower()
        if "scien" in query: return cls.SCIENCE
        if "cultur" in query: return cls.CULTURE
        if "milit" in query or "dominat" in query: return cls.MILITARY
        if "relig" in query: return cls.RELIGIOUS
        if "diplo" in query: return cls.DIPLOMACY
        if "cc" in query or "abandon" in query or "forfait" in query: return cls.CC
        return cls.UNKNOWN

class IGPlayer(Player):
    def __init__(self, obj, civ):
        super().__init__(obj)
        self.civ = civ

    @classmethod
    def parse_player(cls, txt : str):
        return IGPlayer(None, None)

class IGTeam:
    def __init__(self, squadron, players, win):
        self.squadron = squadron
        self.players : List[Optional[IGPlayer]] = players
        self.win : Optional[bool] = win

    def __str__(self):
        return self.squadron.name

    @classmethod
    def parse_players(cls, txt : str):
        return [IGPlayer.parse_player(i) for i in [j.strip() for j in txt.split('\n')] if i]

class Match:
    def __init__(self, team_1, team_2, victory_type, turn, game_map, bans, date):
        self.team_1 : IGTeam = team_1
        self.team_2 : IGTeam = team_2
        self.victory_type : str = victory_type.value
        self.turn : int = turn
        self.map : str = game_map
        self.bans : List[...] = bans
        self._date : datetime = date - timedelta(hours=5)
        self.date : str = self._date.strftime("%d/%m/%Y")

    def __str__(self):
        return f"{self.team_1} vs {self.team_2}: {self.victory_type} turn {self.turn} on {self.map}"

    def __iter__(self) -> IGTeam:
        yield self.team_1
        yield self.team_2
        return

    @classmethod
    def parse_match(cls, message : discord.Message):
        """Parse discord message to a Match object, return None if failed"""
        txt = message.content
        match = MATCH_REGEX.match(txt)
        if not match:
            return None
        squad1 = Global.get_squadron_by_id(int(match["SquadReportID1"]))
        squad2 = Global.get_squadron_by_id(int(match["SquadReportID2"]))
        if match["VictoryReport1"] and match["VictoryReport2"]:
            logger.error("2 Victory report detected, abort parsing")
            return None
        team_1_win = bool(match["VictoryReport1"])
        victory_report = match["VictoryReport1"] or match["VictoryReport2"]
        victory_type = VictoryType.get_from_query(victory_report)
        victory_turn_match = VICTORY_TURN.findall(victory_report)
        victory_turn = int(victory_turn_match[0]) if victory_turn_match else None
        return cls(
            IGTeam(squad1, IGTeam.parse_players(match["Team1Query"]), team_1_win),
            IGTeam(squad2, IGTeam.parse_players(match["Team2Query"]), not team_1_win),
            victory_type, victory_turn, match["Map"], None, message.created_at)

    def get_player(self, target) -> Optional[IGPlayer]:
        name = target.name if isinstance(target, Player) else target
        for team in self:
            for player in team.players:
                if player.name == name:
                    return player
        return None

    def get_player_team(self, target) -> Optional[IGTeam]:
        name = target.name if isinstance(target, Player) else target
        for team in self:
            for player in team.players:
                if player.name == name:
                    return team
        return None