import pytest
from kps_tehdas_web import KPSTehdas
from kps_pelaaja_vs_pelaaja_web import KPSPelaajaVsPelaajaWeb
from kps_tekoaly_web import KPSTekoalyWeb
from kps_parempi_tekoaly_web import KPSParempiTekoalyWeb


class TestKPSTehdas:
    def test_luo_peli_web_pelaaja_vs_pelaaja(self):
        peli = KPSTehdas.luo_peli_web("a")
        assert isinstance(peli, KPSPelaajaVsPelaajaWeb)

    def test_luo_peli_web_tekoaly(self):
        peli = KPSTehdas.luo_peli_web("b")
        assert isinstance(peli, KPSTekoalyWeb)

    def test_luo_peli_web_parempi_tekoaly(self):
        peli = KPSTehdas.luo_peli_web("c")
        assert isinstance(peli, KPSParempiTekoalyWeb)

    def test_luo_peli_web_virheellinen_tyyppi(self):
        peli = KPSTehdas.luo_peli_web("x")
        assert peli is None

    def test_luo_peli_web_tyhja_merkkijono(self):
        peli = KPSTehdas.luo_peli_web("")
        assert peli is None
