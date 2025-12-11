import pytest
from tekoaly import Tekoaly


class TestTekoaly:
    def setup_method(self):
        self.tekoaly = Tekoaly()

    def test_anna_siirto_palauttaa_paperin_alussa(self):
        # Tekoäly aloittaa 0:sta, lisää 1, jolloin _siirto = 1 -> "p"
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "p"

    def test_anna_siirto_palauttaa_sakset_toisella_kerralla(self):
        self.tekoaly.anna_siirto()  # p
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "s"

    def test_anna_siirto_palauttaa_kiven_kolmannella_kerralla(self):
        self.tekoaly.anna_siirto()  # p
        self.tekoaly.anna_siirto()  # s
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "k"

    def test_anna_siirto_toistaa_kierron(self):
        siirrot = []
        for _ in range(6):
            siirrot.append(self.tekoaly.anna_siirto())

        assert siirrot == ["p", "s", "k", "p", "s", "k"]

    def test_aseta_siirto_ei_vaikuta(self):
        # aseta_siirto ei tee mitään tavallisessa tekoälyssä
        self.tekoaly.aseta_siirto("k")
        siirto = self.tekoaly.anna_siirto()
        assert siirto == "p"  # Edelleen palautetaan p koska _siirto on 0 alussa
