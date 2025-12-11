from kps_web import KiviPaperiSaksetWeb


class KPSPelaajaVsPelaajaWeb(KiviPaperiSaksetWeb):
    def _toisen_siirto(self, ensimmaisen_siirto, pelaaja2_siirto=None):
        return pelaaja2_siirto
