import requests
from typing import List


class Player:
    def __init__(self, data: dict):
        self.name = data.get('name')
        self.nationality = data.get('nationality')
        self.assists = data.get('assists', 0)
        self.goals = data.get('goals', 0)
        self.team = data.get('team')
        self.games = data.get('games', 0)
        self.id = data.get('id')

    def __str__(self) -> str:
        return f"{self.name:20} {self.team:>8} {self.goals:>2} + {self.assists:>2} = {self.goals + self.assists:>2}"


class PlayerReader:
    def __init__(self, url: str = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"):
        self.url = url

    def get_players(self) -> List[Player]:
        resp = requests.get(self.url)
        resp.raise_for_status()
        data = resp.json()
        return [Player(d) for d in data]


class PlayerStats:
    def __init__(self, reader: PlayerReader):
        self.reader = reader

    def players_by_nationality(self, players: List[Player], nationality: str) -> List[Player]:
        return [p for p in players if p.nationality == nationality]

    def top_scorers_by_nationality(self, nationality: str, n: int | None = None) -> List[Player]:
        players = self.reader.get_players()
        filtered = self.players_by_nationality(players, nationality)
        filtered.sort(key=lambda p: p.goals + p.assists, reverse=True)
        if n is not None:
            return filtered[:n]
        return filtered
