from kps_web import KiviPaperiSaksetWeb
from tekoaly_parannettu import TekoalyParannettu


class KPSParempiTekoalyWeb(KiviPaperiSaksetWeb):
    def __init__(self):
        super().__init__()
        self._tekoaly = TekoalyParannettu(10)

    def _toisen_siirto(self, ensimmaisen_siirto, pelaaja2_siirto=None):
        siirto = self._tekoaly.anna_siirto()
        self._tekoaly.aseta_siirto(ensimmaisen_siirto)
        return siirto
