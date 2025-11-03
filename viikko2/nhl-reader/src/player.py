from typing import List, Optional

import requests


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
        # Keep the formatted string under 100 characters for linters
        points = self.goals + self.assists
        name_part = f"{self.name:20}"
        team_part = f"{self.team:>8}"
        score_part = f"{self.goals:>2} + {self.assists:>2} = {points:>2}"
        return f"{name_part} {team_part} {score_part}"

    def points(self) -> int:
        """Return total points (goals + assists). Keeps class with at least two public methods."""
        return self.goals + self.assists


class PlayerReader:
    def __init__(self, url: str = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"):
        self.url = url

    def get_players(self) -> List[Player]:
        # Add a timeout to avoid hanging indefinitely
        resp = requests.get(self.url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return [Player(d) for d in data]

    def get_player_by_id(self, player_id: int) -> Optional[Player]:
        """Return a Player with the given id or None if not found.

        This provides a second public method so the class meets pylint's
        minimum-public-methods rule without changing existing behaviour.
        """
        players = self.get_players()
        for player in players:
            if player.id == player_id:
                return player
        return None


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
