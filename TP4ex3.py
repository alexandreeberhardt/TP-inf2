import pickle
from TP4EXO2 import Groupe

groupe1 = Groupe()
def main():
    with open("TP4EXO2.pickle", "ab") as f:
        pickle.dump(groupe1,f)

    with open("TP4EXO2.pickle", "rb") as f:
        groupe2 = pickle.load(f)

        print(groupe2)

if __name__== "__main__":
    main()


