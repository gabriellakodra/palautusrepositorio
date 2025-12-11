import pytest
from kps_pelaaja_vs_pelaaja_web import KPSPelaajaVsPelaajaWeb
from kps_tekoaly_web import KPSTekoalyWeb
from kps_parempi_tekoaly_web import KPSParempiTekoalyWeb


class TestKPSPelaajaVsPelaajaWeb:
    def setup_method(self):
        self.peli = KPSPelaajaVsPelaajaWeb()

    def test_alustus(self):
        assert self.peli.game_over == False
        assert self.peli.tuomari.ekan_pisteet == 0
        assert self.peli.tuomari.tokan_pisteet == 0
        assert self.peli.tuomari.tasapelit == 0

    def test_make_move_tasapeli(self):
        result = self.peli.make_move("k", "k")

        assert result["game_over"] == False
        assert result["pelaaja1_siirto"] == "k"
        assert result["pelaaja2_siirto"] == "k"
        assert result["tasapelit"] == 1
        assert result["ekan_pisteet"] == 0
        assert result["tokan_pisteet"] == 0

    def test_make_move_eka_voittaa(self):
        result = self.peli.make_move("k", "s")

        assert result["game_over"] == False
        assert result["ekan_pisteet"] == 1
        assert result["tokan_pisteet"] == 0
        assert result["tasapelit"] == 0

    def test_make_move_toka_voittaa(self):
        result = self.peli.make_move("s", "k")

        assert result["game_over"] == False
        assert result["ekan_pisteet"] == 0
        assert result["tokan_pisteet"] == 1
        assert result["tasapelit"] == 0

    def test_make_move_virheellinen_pelaaja1_siirto(self):
        result = self.peli.make_move("x", "k")

        assert result["game_over"] == True
        assert "error" in result
        assert self.peli.game_over == True

    def test_make_move_virheellinen_pelaaja2_siirto(self):
        result = self.peli.make_move("k", "x")

        assert result["game_over"] == True
        assert "error" in result
        assert self.peli.game_over == True

    def test_make_move_after_game_over(self):
        self.peli.end_game()
        result = self.peli.make_move("k", "k")

        assert result["game_over"] == True
        assert "error" in result

    def test_end_game(self):
        self.peli.make_move("k", "s")
        self.peli.make_move("p", "p")

        result = self.peli.end_game()

        assert result["game_over"] == True
        assert result["ekan_pisteet"] == 1
        assert result["tasapelit"] == 1
        assert self.peli.game_over == True

    def test_useita_kierroksia(self):
        self.peli.make_move("k", "k")
        self.peli.make_move("k", "s")
        self.peli.make_move("s", "k")

        assert self.peli.tuomari.ekan_pisteet == 1
        assert self.peli.tuomari.tokan_pisteet == 1
        assert self.peli.tuomari.tasapelit == 1

    def test_peli_paattyy_kun_pelaaja1_voittaa_3_kertaa(self):
        # Pelaaja 1 voittaa 3 kertaa
        for i in range(3):
            result = self.peli.make_move("k", "s")
            if i < 2:
                assert result["game_over"] == False
            else:
                assert result["game_over"] == True
                assert result["winner"] == "Pelaaja 1"
                assert result["ekan_pisteet"] == 3

    def test_peli_paattyy_kun_pelaaja2_voittaa_3_kertaa(self):
        # Pelaaja 2 voittaa 3 kertaa
        for i in range(3):
            result = self.peli.make_move("s", "k")
            if i < 2:
                assert result["game_over"] == False
            else:
                assert result["game_over"] == True
                assert result["winner"] == "Pelaaja 2"
                assert result["tokan_pisteet"] == 3

    def test_peli_jatkuu_ennen_3_voittoa(self):
        # Pelataan 2 kierrosta, peli ei pääty
        for _ in range(2):
            result = self.peli.make_move("k", "s")
            assert result["game_over"] == False

        assert self.peli.tuomari.ekan_pisteet == 2
        assert self.peli.game_over == False

    def test_tasapelit_eivat_paata_pelia(self):
        # Pelataan 10 tasapeliä, peli ei pääty
        for _ in range(10):
            result = self.peli.make_move("k", "k")
            assert result["game_over"] == False

        assert self.peli.tuomari.tasapelit == 10
        assert self.peli.game_over == False


class TestKPSTekoalyWeb:
    def setup_method(self):
        self.peli = KPSTekoalyWeb()

    def test_alustus(self):
        assert self.peli.game_over == False
        assert self.peli._tekoaly is not None

    def test_make_move_tekoaly_tekee_siirron(self):
        result = self.peli.make_move("k")

        assert result["game_over"] == False
        assert result["pelaaja1_siirto"] == "k"
        assert result["pelaaja2_siirto"] in ["k", "p", "s"]

    def test_make_move_tekoaly_sarja(self):
        # Tekoälyn pitäisi pelata p, s, k -sykli (aloittaa 0:sta, 0+1=1 -> p)
        result1 = self.peli.make_move("k")
        assert result1["pelaaja2_siirto"] == "p"

        result2 = self.peli.make_move("k")
        assert result2["pelaaja2_siirto"] == "s"

        result3 = self.peli.make_move("k")
        assert result3["pelaaja2_siirto"] == "k"

    def test_make_move_ilman_pelaaja2_siirtoa(self):
        # Tekoälypeliä vastaan ei tarvita pelaaja2_siirtoa
        result = self.peli.make_move("p", None)

        assert result["game_over"] == False
        assert result["pelaaja2_siirto"] in ["k", "p", "s"]


class TestKPSParempiTekoalyWeb:
    def setup_method(self):
        self.peli = KPSParempiTekoalyWeb()

    def test_alustus(self):
        assert self.peli.game_over == False
        assert self.peli._tekoaly is not None

    def test_make_move_parannettu_tekoaly_tekee_siirron(self):
        result = self.peli.make_move("k")

        assert result["game_over"] == False
        assert result["pelaaja1_siirto"] == "k"
        assert result["pelaaja2_siirto"] in ["k", "p", "s"]

    def test_make_move_parannettu_tekoaly_oppii(self):
        # Pelataan useita kierroksia (mutta ei 3 voittoa)
        for i in range(2):
            result = self.peli.make_move("k")
            assert result["pelaaja2_siirto"] in ["k", "p", "s"]
            # Peli ei pääty ennen 2 voittoa
            if result["game_over"]:
                # Jos peli päättyi, tarkista että jompikumpi voitti 3
                assert result["ekan_pisteet"] >= 3 or result["tokan_pisteet"] >= 3
            else:
                assert result["ekan_pisteet"] < 3 and result["tokan_pisteet"] < 3

    def test_make_move_eri_siirroilla(self):
        siirrot = ["k", "p", "s", "k", "p"]

        for siirto in siirrot:
            result = self.peli.make_move(siirto)
            # Peli voi päättyä jos jompikumpi voittaa 3 kertaa
            if result["game_over"]:
                assert result["ekan_pisteet"] >= 3 or result["tokan_pisteet"] >= 3
                break
            assert result["pelaaja2_siirto"] in ["k", "p", "s"]
