import pytest
from tuomari import Tuomari


class TestTuomari:
    def setup_method(self):
        self.tuomari = Tuomari()

    def test_alkutila(self):
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0

    def test_tasapeli(self):
        self.tuomari.kirjaa_siirto("k", "k")
        assert self.tuomari.tasapelit == 1
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 0

    def test_eka_voittaa_kivi_sakset(self):
        self.tuomari.kirjaa_siirto("k", "s")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0

    def test_eka_voittaa_sakset_paperi(self):
        self.tuomari.kirjaa_siirto("s", "p")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0

    def test_eka_voittaa_paperi_kivi(self):
        self.tuomari.kirjaa_siirto("p", "k")
        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 0
        assert self.tuomari.tasapelit == 0

    def test_toka_voittaa_kivi_sakset(self):
        self.tuomari.kirjaa_siirto("s", "k")
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 0

    def test_toka_voittaa_sakset_paperi(self):
        self.tuomari.kirjaa_siirto("p", "s")
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 0

    def test_toka_voittaa_paperi_kivi(self):
        self.tuomari.kirjaa_siirto("k", "p")
        assert self.tuomari.ekan_pisteet == 0
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 0

    def test_useita_kierroksia(self):
        self.tuomari.kirjaa_siirto("k", "k")  # tasapeli
        self.tuomari.kirjaa_siirto("k", "s")  # eka voittaa
        self.tuomari.kirjaa_siirto("s", "k")  # toka voittaa
        self.tuomari.kirjaa_siirto("p", "p")  # tasapeli

        assert self.tuomari.ekan_pisteet == 1
        assert self.tuomari.tokan_pisteet == 1
        assert self.tuomari.tasapelit == 2

    def test_str_representation(self):
        self.tuomari.kirjaa_siirto("k", "s")
        self.tuomari.kirjaa_siirto("p", "p")

        result = str(self.tuomari)
        assert "1 - 0" in result
        assert "Tasapelit: 1" in result
