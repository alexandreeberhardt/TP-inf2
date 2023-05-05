import pickle
from TP4EXO2 import Groupe

groupe = Groupe()

with open("TP4EXO2.py", "wb") as f:
    pickle.dump(groupe, f)

with open("TP4EXO2.py", "rb") as f:
    groupe = pickle.load(f)

assert str(Groupe) == str(groupe)
for i in range(len(Groupe)):
    assert str(Groupe[i]) == str(groupe[i])

