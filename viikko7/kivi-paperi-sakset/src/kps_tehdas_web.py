from kps_pelaaja_vs_pelaaja_web import KPSPelaajaVsPelaajaWeb
from kps_tekoaly_web import KPSTekoalyWeb
from kps_parempi_tekoaly_web import KPSParempiTekoalyWeb


class KPSTehdas:
    @staticmethod
    def luo_peli_web(tyyppi):
        if tyyppi == "a":
            return KPSPelaajaVsPelaajaWeb()
        elif tyyppi == "b":
            return KPSTekoalyWeb()
        elif tyyppi == "c":
            return KPSParempiTekoalyWeb()
        else:
            return None
