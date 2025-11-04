# tehdään alussa importit

from logger import logger
from summa import summa
from erotus import erotus
from tulo import tulo

print("toinen testi")

logger("aloitetaan ohjelma")

x = int(input("luku 1: "))
y = int(input("luku 2: "))
print(f"{x} + {y} = {summa(x, y)}") # tehdään sama muutos kuin main
print(f"{x} - {y} = {erotus(x, y)}") 
print(f"{x} * {y} = {tulo(x, y)}") 

logger("lopetetaan ohjelma")
print("goodbye!")
print("testi")

# tehdään tännekin jokin muutos
