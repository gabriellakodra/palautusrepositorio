import unittest
from laskin import Laskin


class StubIO:
    def __init__(self, inputs):
        self.inputs = inputs
        self.outputs = []

    def lue(self, teksti):
        return self.inputs.pop(0)

    def kirjoita(self, teksti):
        self.outputs.append(teksti)


class TestLaskinKaksiLaskua(unittest.TestCase):
    def test_kaksi_summaa_peräkkäin(self):
        io = StubIO(["1", "3", "2", "5", "-9999"])
        laskin = Laskin(io)
        laskin.suorita()

        self.assertEqual(io.outputs[0], "Summa: 4")  
        self.assertEqual(io.outputs[1], "Summa: 7")  
