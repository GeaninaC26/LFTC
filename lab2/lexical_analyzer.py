import sys
import re
#indentifier length < 250
#unique TS for indentifiers and constants
#bab

FIP = []
TS = []


other_atoms = {
    "identifier":0,
    "constant":1
}

keywords = { 
    "else":2,
    "if":3,
    "int":4,
    "while":5,
    "print":6,
    "float":7,
    "import":8,
    "and":9,
    "or":10,
    "not":11
}
separators = {
    "(":12,
    ")":13,
    "[":14,
    "]":15,
    ":":30
}

operators = {
    ">":16,
    "<":17,
    "<=":18,
    ">=":19,
    "==":20,
    "!=":21,
    "+":22,
    "-":23,
    "*":24,
    "/":25,
    "%":26,
    "//":27,
    "**":28,
    "=":29
}

lexical_atoms = {**keywords, **separators, **operators}
identifier_pattern = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]{0,249}$') 

def organize_symbol_table_lexicographically(source_code): 
    symbol_elements = set() 
    for line in source_code: 
        tokens = line.split() 
        for token in tokens: 
            if re.match(identifier_pattern, token) and token not in keywords: 
                symbol_elements.add(token) 
            elif token.isdigit():
                symbol_elements.add(f"const_{token}")

    symbol_elements = sorted(symbol_elements) 
    symbol_table = {} 

    for index, element in enumerate(symbol_elements): 

        symbol_table[element] = index 

    return symbol_table 

def classify_token(token, symbol_table, FIP): 

    if token in lexical_atoms: 
        FIP.append((lexical_atoms[token], -1)) 
    elif identifier_pattern.match(token): 
        if token in symbol_table: 
            code = symbol_table[token] 
        else: 
            code = len(symbol_table) 
            symbol_table[token] = code 
        FIP.append((0, symbol_table[token])) 

    elif token.isdigit(): 
        if f"const_{token}" in symbol_table: 
            code = symbol_table[f"const_{token}"] 
        else: 
            code = symbol_table[f"const_{token}"]

            symbol_table[f"const_{token}"] = code 
        FIP.append((1, code)) 
    else: 
        return False
    return True

def main():  

    FIP = [] 
    filename = sys.argv[1]
    fin = open(filename, "r")
    source_code = fin.readlines()
    line_nr = 0
   


    for line in source_code: 
        line_nr+=1
        tokens = line.split() 

        for token in tokens: 
            
            if not classify_token(token, symbol_table, FIP): 
                print("Lexical error on line " + str(line_nr) + ": " + line)



    print("TS:") 

    for key, value in symbol_table.items(): 

        print(f"{key}: {value}") 


    print("\nFIP:") 

    for item in FIP: 
        print(item, end=" ") 

if __name__ == "__main__": 

    main() 