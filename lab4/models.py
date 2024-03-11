# class for regular grammar
class Grammar:
    def __init__(self, file="", start_symbol="", nonterminals=[], terminals=[], productions={}):
        if file != "":
            f = open(file, 'r')

            lines = f.readlines()
            start_symbol = lines[0].strip('\n')
            nonterminals = lines[1].strip('\n').split(' ')
            terminals = lines[2].strip('\n').split(' ')
            productions = {}

            for production in lines[3:]:
                left_hand_side, right_hand_side = production.strip('\n').split('->')
                productions[left_hand_side] = right_hand_side.split('|')

        self.__start_symbol = start_symbol
        self.__nonterminals = nonterminals
        self.__terminals = terminals
        self.__productions = productions

    def to_AF(self):

        if not self.is_regular():
            print("The grammar is irregular")
            return 
        
        alfabet = self.__terminals
        stare_initiala = self.__start_symbol
        multime_stari = self.__nonterminals + ['K']

        multime_stari_finale = ['K']
        tranzitii = []

        if '@' in self.__productions[self.__start_symbol]:
            multime_stari_finale.append(self.__start_symbol)
        
        for key in self.__productions:
            values = self.__productions[key]
            for value in values:
                if len(value) == 2:
                    tranzitii.append([key, value[0], value[1]])
                elif value != '@':
                    tranzitii.append([key, value[0], 'K'])

        AF(alfabet=alfabet, stare_initiala=stare_initiala, multime_stari=multime_stari, multime_stari_finale=multime_stari_finale, tranzitii=tranzitii).show_elements()
        

    def show_grammar_elements(self):
        print(f'The start symbol is: {self.__start_symbol}')
        print(f'The nonterminals are: {self.__nonterminals}')
        print(f'The terminals are: {self.__terminals}')
        for key in self.__productions:
            print(f'The productions are: {key}->{"|".join(self.__productions[key])}')

    def show_nonterminal_productions(self, nonterminal):
        if nonterminal not in self.__nonterminals:
            print(f'{nonterminal} is not a nonterminal.')
        elif nonterminal not in self.__productions:
            print(f'{nonterminal} does not have productions.')
        else:
            print(f'{nonterminal}\'s productions are:')
            for value in self.__productions[nonterminal]:
                print(f'{nonterminal}->{value}')

    def is_regular(self):
        for key in self.__productions:
            if key not in self.__nonterminals:
                return False

        if '@' in self.__productions[self.__start_symbol]:
            for key in self.__productions:
                values = self.__productions[key]
                for value in values:
                    if self.__start_symbol in value:
                        return False

        for key in self.__productions:
            values = self.__productions[key]
            for value in values:
                if value[0] not in self.__terminals and value[0] != '@':
                    return False
                elif len(value) > 1 and value[1] not in self.__nonterminals:
                    return False
                elif len(value) > 2:
                    return False
                elif '@' in value and key != self.__start_symbol:
                    return False
                
        return True

# class for AF
class AF:
    def __init__(self, file="", alfabet=[], multime_stari=[], stare_initiala="", multime_stari_finale=[], tranzitii=[]):
        
        if file != "":
            f = open(file, "r")
            lines = f.readlines()
            alfabet = lines[0].strip("\n").split(" ")
            multime_stari = lines[1].strip("\n").split(" ")
            stare_initiala = lines[2].strip("\n")
            multime_stari_finale = lines[3].strip("\n").split(" ")
            tranzitii = []
            for tranzitie in lines[4:]:
                tranzitii.append(tranzitie.strip("\n").split(" "))

        self.__alfabet = alfabet
        self.__multime_stari = multime_stari
        self.__multime_stari_finale = multime_stari_finale
        self.__stare_initiala = stare_initiala
        self.__tranzitii = tranzitii
        
    def to_grammar(self):

        terminals = self.__alfabet
        start_symbol = self.__stare_initiala
        nonterminals =  self.__multime_stari
        productions = {}

        ft = [tr[0] for tr in self.__tranzitii]
        difference = [x for x in self.__multime_stari if x in ft]
 
        for tranzitie in self.__tranzitii:
            if tranzitie[2] in difference:
                if tranzitie[0] in productions:
                    productions[tranzitie[0]].append(f'{tranzitie[1]}{tranzitie[2]}')
                else:
                    productions[tranzitie[0]] = [f'{tranzitie[1]}{tranzitie[2]}']

            if tranzitie[2] not in difference:
                if tranzitie[0] in productions and tranzitie[1] not in [x for x in productions[tranzitie[0]]]:
                    productions[tranzitie[0]].append(f'{tranzitie[1]}')
                else:
                    productions[tranzitie[0]] = [f'{tranzitie[1]}']                

        if start_symbol in self.__multime_stari_finale:
            productions[start_symbol].append('@')

        return Grammar(terminals=terminals, start_symbol=start_symbol, nonterminals=nonterminals, productions=productions)

    
    def show_elements(self):
        print("\nAlfabetul:\n" + str(self.__alfabet) + "\n\nMultimea starilor:\n" + str(self.__multime_stari) + "\n\nStare initiala:\n" + self.__stare_initiala + "\n\nMultimea starilor finale:\n" + str(self.__multime_stari_finale) + "\n\nTranzitii:")
        for tranzitie in self.__tranzitii:
            print(tranzitie)
        print("\n")

    def verifica_secventa(self, secventa):
        stare_curenta = self.__stare_initiala
        for simbol in secventa:
            found = False
            if simbol not in self.__alfabet:
                return False
            print(stare_curenta, simbol)
            for tranzitie in self.__tranzitii:
                if tranzitie[0] == stare_curenta and simbol == tranzitie[1]:
                    print(tranzitie, stare_curenta, simbol)
                    stare_curenta = tranzitie[2]
                    found = True
                    break
            if not found:
                return False
        if stare_curenta in self.__multime_stari_finale:
            return True
        return False
