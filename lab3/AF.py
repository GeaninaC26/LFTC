# fiser = alfabet "\n" multime_stari "\n" stare_initiala "\n" multime_stari_finale "\n" tranzitii 
# alfabet = simbol {" ", simbol}
# multime_stari = stare {" " stare}
# multime_stari_finale = stare {" " stare}
# tranzitii = tranzitie {"\n" tranzitie}
# stare_initiala = stare
# tranzitie = stare " " simbol " " stare
# simbol = litera | cifra | _ | .
# litera = litera_mare | litera_mica
# litera_mica = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z"
# litera_mare = "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
# cifra = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
# stare = simbol {simbol}

import sys

class AF:
    def __init__(self, file):
        f = open(file, "r")
        lines = f.readlines()
        alfabet = lines[0].strip("\n").split(" ")
        multime_stari = lines[1].strip("\n").split(" ")
        stare_initiala = lines[2].strip("\n")
        multime_stari_finale = lines[3].strip("\n").split(" ")
        tranzitii = []
        for tranzitie in lines[4:]:
            tranzitii.append(tranzitie.strip("\n").split(" "))

        self.alfabet = alfabet
        self.multime_stari = multime_stari
        self.multime_stari_finale = multime_stari_finale
        self.stare_initiala = stare_initiala
        self.tranzitii = tranzitii

    def verifica_secventa(self, secventa):
        stare_curenta = self.stare_initiala
        for simbol in secventa:
            found = False
            if simbol not in self.alfabet:
                return False
            print(stare_curenta, simbol)
            for tranzitie in self.tranzitii:
                if tranzitie[0] == stare_curenta and simbol == tranzitie[1]:
                    print(tranzitie, stare_curenta, simbol)
                    stare_curenta = tranzitie[2]
                    found = True
                    break
            if not found:
                return False
        if stare_curenta in self.multime_stari_finale:
            return True
        return False

def main():
    af = AF(sys.argv[1])
    while True:
        print("Alegeti o optiune:\n1.Afiseaza elemente automat\n2.Verifica secventa acceptata\n3.Afisare starea in care ajunge o stare printr-un simbol.\n0.Exit\n")
        command = int(input())
        if command == 1:
            print("\nAlfabetul:\n" + str(af.alfabet) + "\n\nMultimea starilor:\n" + str(af.multime_stari) + "\n\nStare initiala:\n" + af.stare_initiala + "\n\nMultimea starilor finale:\n" + str(af.multime_stari_finale) + "\n\nTranzitii:")
            for tranzitie in af.tranzitii:
                print(tranzitie)
            print("\n")
        elif command == 2:
            print("Introduceti secventa:")
            print('REZULTAT: ', af.verifica_secventa(input().strip("\n")))
        elif command == 3:
            print("Introduceti starea:")
            stare_curenta = input().strip("\n")
            print("Introduceti simbolul: ")
            simbol = input().strip("\n")
            stare_urm = ""
            found = False
            for tranzitie in af.tranzitii:
                if tranzitie[0] == stare_curenta and simbol == tranzitie[1]:
                    print(tranzitie)
                    stare_urm = tranzitie[2]
                    found = True
                    break
            if found == False:
                print("Nu exista o tranzitie pentru aceasta stare si acest simbol.")
        elif command == 0:
            break
        else:
            print("Comanda inexistenta")

if __name__ == "__main__":
    main()
