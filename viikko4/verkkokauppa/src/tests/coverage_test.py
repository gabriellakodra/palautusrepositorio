import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestCoverage(unittest.TestCase):   

    def test_tyhja_ostoskori_hinta_nolla(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()
        viitegeneraattori_mock.uusi.return_value = 42
        varasto_mock = Mock()

        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)
        
        kauppa.aloita_asiointi()
        kauppa.tilimaksu("pekka", "12345")
        
        pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 0)

    def test_ei_lisaa_tuotetta_jos_ei_saldoa(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()
        viitegeneraattori_mock.uusi.return_value = 42
        varasto_mock = Mock()

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 0  

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)
        
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)  
        kauppa.tilimaksu("pekka", "12345")
        
        pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 0)
        varasto_mock.ota_varastosta.assert_not_called()

    def test_tuote_equality_and_hash(self):
        tuote1 = Tuote(1, "maito", 5)
        tuote2 = Tuote(1, "maito", 5)
        tuote3 = Tuote(2, "leipä", 3)
        
        self.assertEqual(tuote1, tuote2)
        self.assertNotEqual(tuote1, tuote3)
     
        self.assertEqual(hash(tuote1), hash(tuote2))
        self.assertNotEqual(hash(tuote1), hash(tuote3))
      
        self.assertEqual(str(tuote1), "maito")

    def test_perakkaisten_ostosten_viitteet_erilaisia(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()
        
        viitegeneraattori_mock.uusi.side_effect = [42, 43]
        
        varasto_mock = Mock()

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)
      
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")
     
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")
        
        expected_calls = [
            unittest.mock.call("pekka", 42, "12345", "33333-44455", 5),
            unittest.mock.call("pekka", 43, "12345", "33333-44455", 5)
        ]
        pankki_mock.tilisiirto.assert_has_calls(expected_calls)

    def test_varasto_hae_olematon_tuote(self):
        from varasto import Varasto
        from kirjanpito import Kirjanpito
        
        kirjanpito_mock = Mock()
        varasto = Varasto(kirjanpito_mock)
        
        tuote = varasto.hae_tuote(999)
        
        self.assertIsNone(tuote)

    def test_ostoskori_poista_tuote(self):
        from ostoskori import Ostoskori
        
        ostoskori = Ostoskori()
        tuote1 = Tuote(1, "maito", 5)
        tuote2 = Tuote(2, "leipä", 3)
       
        ostoskori.lisaa(tuote1)
        ostoskori.lisaa(tuote2)
      
        self.assertEqual(ostoskori.hinta(), 8)
       
        ostoskori.poista(tuote1)
     
        self.assertEqual(ostoskori.hinta(), 3)

    def test_viitegeneraattori_uusi(self):
        from viitegeneraattori import Viitegeneraattori
        
        gen = Viitegeneraattori()
        
        viite1 = gen.uusi()
        viite2 = gen.uusi()
        viite3 = gen.uusi()
        
        self.assertEqual(viite1, 2) 
        self.assertEqual(viite2, 3)
        self.assertEqual(viite3, 4)

    def test_pankki_tilisiirto(self):
        from pankki import Pankki
        from kirjanpito import Kirjanpito
        
        kirjanpito_mock = Mock()
        pankki = Pankki(kirjanpito_mock)
        
        result = pankki.tilisiirto("pekka", 42, "12345", "67890", 100)
      
        self.assertTrue(result)
       
        kirjanpito_mock.lisaa_tapahtuma.assert_called_with(
            "tilisiirto: tililtä 12345 tilille 67890 viite 42 summa 100e"
        )

    def test_kirjanpito_lisaa_tapahtuma(self):
        from kirjanpito import Kirjanpito
        
        kirjanpito = Kirjanpito()
        
        kirjanpito.lisaa_tapahtuma("test event")
        kirjanpito.lisaa_tapahtuma("another event")
        
        self.assertEqual(len(kirjanpito.tapahtumat), 2)
        self.assertEqual(kirjanpito.tapahtumat[0], "test event")
        self.assertEqual(kirjanpito.tapahtumat[1], "another event")
 