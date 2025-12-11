import pytest
from kps_tehdas import KPSTehdas
from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly


class TestKPSTehdas:
    def test_luo_peli_pelaaja_vs_pelaaja(self):
        peli = KPSTehdas.luo_peli("a")
        assert isinstance(peli, KPSPelaajaVsPelaaja)

    def test_luo_peli_tekoaly(self):
        peli = KPSTehdas.luo_peli("b")
        assert isinstance(peli, KPSTekoaly)

    def test_luo_peli_parempi_tekoaly(self):
        peli = KPSTehdas.luo_peli("c")
        assert isinstance(peli, KPSParempiTekoaly)

    def test_luo_peli_virheellinen_tyyppi(self):
        peli = KPSTehdas.luo_peli("x")
        assert peli is None

    def test_luo_peli_tyhja_merkkijono(self):
        peli = KPSTehdas.luo_peli("")
        assert peli is None
