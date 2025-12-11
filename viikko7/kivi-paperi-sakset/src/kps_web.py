from abc import ABC, abstractmethod
from tuomari import Tuomari


class KiviPaperiSaksetWeb(ABC):
    """Web version of the game that doesn't use input() but returns results"""

    def __init__(self):
        self.tuomari = Tuomari()
        self.game_over = False

    def make_move(self, pelaaja1_siirto, pelaaja2_siirto=None):
        """
        Make a move in the game.
        Returns dict with game state information.
        """
        if self.game_over:
            return {
                "error": "Game is over",
                "game_over": True,
                "tilanne": str(self.tuomari),
            }

        if not self._onko_ok_siirto(pelaaja1_siirto):
            self.game_over = True
            return {
                "pelaaja1_siirto": pelaaja1_siirto,
                "pelaaja2_siirto": None,
                "error": "Virheellinen siirto",
                "game_over": True,
                "tilanne": str(self.tuomari),
            }

        tokan_siirto = self._toisen_siirto(pelaaja1_siirto, pelaaja2_siirto)

        if not self._onko_ok_siirto(tokan_siirto):
            self.game_over = True
            return {
                "pelaaja1_siirto": pelaaja1_siirto,
                "pelaaja2_siirto": tokan_siirto,
                "error": "Virheellinen siirto",
                "game_over": True,
                "tilanne": str(self.tuomari),
            }

        self.tuomari.kirjaa_siirto(pelaaja1_siirto, tokan_siirto)

        # Check if either player has won 3 times
        if self.tuomari.ekan_pisteet >= 3 or self.tuomari.tokan_pisteet >= 3:
            self.game_over = True
            winner = None
            if self.tuomari.ekan_pisteet >= 3:
                winner = "Pelaaja 1"
            elif self.tuomari.tokan_pisteet >= 3:
                winner = "Pelaaja 2"

            return {
                "pelaaja1_siirto": pelaaja1_siirto,
                "pelaaja2_siirto": tokan_siirto,
                "game_over": True,
                "winner": winner,
                "tilanne": str(self.tuomari),
                "ekan_pisteet": self.tuomari.ekan_pisteet,
                "tokan_pisteet": self.tuomari.tokan_pisteet,
                "tasapelit": self.tuomari.tasapelit,
            }

        return {
            "pelaaja1_siirto": pelaaja1_siirto,
            "pelaaja2_siirto": tokan_siirto,
            "game_over": False,
            "tilanne": str(self.tuomari),
            "ekan_pisteet": self.tuomari.ekan_pisteet,
            "tokan_pisteet": self.tuomari.tokan_pisteet,
            "tasapelit": self.tuomari.tasapelit,
        }

    def end_game(self):
        """End the game and return final results"""
        self.game_over = True
        return {
            "game_over": True,
            "tilanne": str(self.tuomari),
            "ekan_pisteet": self.tuomari.ekan_pisteet,
            "tokan_pisteet": self.tuomari.tokan_pisteet,
            "tasapelit": self.tuomari.tasapelit,
        }

    @abstractmethod
    def _toisen_siirto(self, ensimmaisen_siirto, pelaaja2_siirto=None):
        pass

    def _onko_ok_siirto(self, siirto):
        return siirto == "k" or siirto == "p" or siirto == "s"
