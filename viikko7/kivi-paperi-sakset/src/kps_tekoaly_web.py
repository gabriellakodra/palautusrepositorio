from kps_web import KiviPaperiSaksetWeb
from tekoaly import Tekoaly


class KPSTekoalyWeb(KiviPaperiSaksetWeb):
    def __init__(self):
        super().__init__()
        self._tekoaly = Tekoaly()

    def _toisen_siirto(self, ensimmaisen_siirto, pelaaja2_siirto=None):
        return self._tekoaly.anna_siirto()
