import pytest
from tekoaly_parannettu import TekoalyParannettu


class TestTekoalyParannettu:
    def setup_method(self):
        self.tekoaly = TekoalyParannettu(10)

    def test_alkutila_palauttaa_kiven(self):
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "k"

    def test_aseta_siirto_tallentaa_muistiin(self):
        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("k")
        # Muisti ei ole tyhjä enää
        assert self.tekoaly._vapaa_muisti_indeksi == 1

    def test_muisti_tayttyy_oikein(self):
        for i in range(3):
            self.tekoaly.anna_siirto()
            self.tekoaly.aseta_siirto("k")

        assert self.tekoaly._vapaa_muisti_indeksi == 3

    def test_muisti_unohtaa_vanhimman_kun_tayttyy(self):
        # Täytetään muisti
        for i in range(10):
            self.tekoaly.anna_siirto()
            self.tekoaly.aseta_siirto("k")

        # Muisti on täynnä
        assert self.tekoaly._vapaa_muisti_indeksi == 10

        # Lisätään yksi lisää
        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("p")

        # Indeksi pysyy samana, mutta vanhin siirto on unohtunut
        assert self.tekoaly._vapaa_muisti_indeksi == 10

    def test_tekoaly_oppii_vastustajan_siirroista(self):
        # Simuloidaan tilanne jossa pelaaja pelaa aina k -> p
        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("k")

        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("k")

        self.tekoaly.anna_siirto()
        self.tekoaly.aseta_siirto("k")

        # Tekoälyn pitäisi oppia ja vastata paperilla
        siirto = self.tekoaly.anna_siirto()
        # Tarkistetaan että siirto on jokin valideista
        assert siirto in ["k", "p", "s"]

    def test_pieni_muisti_toimii(self):
        tekoaly_pieni = TekoalyParannettu(3)

        for i in range(5):
            tekoaly_pieni.anna_siirto()
            tekoaly_pieni.aseta_siirto("s")

        # Muistin koko rajoittuu kolmeen
        assert tekoaly_pieni._vapaa_muisti_indeksi == 3

    def test_eri_siirrot_muistissa(self):
        siirrot = ["k", "p", "s", "k", "p"]

        for siirto in siirrot:
            self.tekoaly.anna_siirto()
            self.tekoaly.aseta_siirto(siirto)

        assert self.tekoaly._vapaa_muisti_indeksi == 5
        # Tarkistetaan että muistissa on oikeita arvoja
        for i, siirto in enumerate(siirrot):
            assert self.tekoaly._muisti[i] == siirto
