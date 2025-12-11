from kps_peli import KiviPaperiSakset
from tekoaly import Tekoaly


class KPSTekoaly(KiviPaperiSakset):
    def __init__(self):
        self._tekoaly = Tekoaly()

    def _toisen_siirto(self, ensimmaisen_siirto):
        return self._tekoaly.anna_siirto()

    def _tulosta_toisen_siirto(self, siirto):
        print(f"Tietokone valitsi: {siirto}")
