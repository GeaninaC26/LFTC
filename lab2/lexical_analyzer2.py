import sys
import re

# identifier length < 250
# unique TS for identifiers and constants
# lexicographically ordered dictionary

FIP = []
TS = {}
other_atoms = {
    "identifier": 0,
    "constant": 1
}

keywords = {
    "else": 2,
    "if": 3,
    "int": 4,
    "while": 5,
    "print": 6,
    "float": 7,
    "import": 8,
    "and": 9,
    "or": 10,
    "not": 11
}

separators = {
    "(": 12,
    ")": 13,
    "[": 14,
    "]": 15,
    ":": 30
}

operators = {
    ">": 16,
    "<": 17,
    "<=": 18,
    ">=": 19,
    "==": 20,
    "!=": 21,
    "+": 22,
    "-": 23,
    "*": 24,
    "/": 25,
    "%": 26,
    "//": 27,
    "**": 28,
    "=": 29
}

lexical_atoms = {**keywords, **separators, **operators}

def insert_reserved(symbol):
    FIP.append((lexical_atoms[symbol], "-1"))


def insert_identifier(identifier):
    if len(identifier) > 250:
        return False
    else:
        if identifier not in TS:
            TS[identifier] = len(TS)
        FIP.append((other_atoms["identifier"], TS[identifier]))
        return True

def insert_constant(constant):
    test_mat = re.match(r"^-?[0-9]+(\.[0-9]+)?[_a-zA-Z]", constant)
    if test_mat is None:
        if constant not in TS:
            TS[constant] = len(TS)
        FIP.append((other_atoms["constant"], TS[constant]))

def main():
    filename = sys.argv[1]
    fin = open(filename, "r")
    source_code = fin.readlines()
    line_nr = 0

    for line in source_code:
        line_nr = line_nr + 1
        tokens = line.split(" ")
        for token in tokens:
            token = token.strip("\n")
            while token != "":
                found = False
                mat = None
                for keyword in keywords:
                    rez = re.match('^' + re.escape(keyword), token)
                    if rez is not None:
                        found = True
                        mat = rez
                if found:
                    insert_reserved(mat.group(0))
                    token = token[mat.end(0):len(token)]
                    continue
                for separator in separators:
                    rez = re.match('^' + re.escape(separator), token)
                    if rez is not None:
                        found = True
                        mat = rez
                if found:
                    insert_reserved(mat.group(0))
                    token = token[mat.end(0):len(token)]
                    continue
                for operator in operators:
                    rez = re.match('^' + re.escape(operator), token)
                    if rez is not None:
                        found = True
                        mat = rez
                if found:
                    insert_reserved(mat.group(0))
                    token = token[mat.end(0):len(token)]
                    continue

                mat = re.match(r"^[_a-zA-Z][_a-zA-Z0-9]*", token)
                if mat is not None:
                    if insert_identifier(mat.group(0)):
                        token = token[mat.end(0):len(token)]
                        continue
                    else:
                        print("Lexical error on line " + str(line_nr) + "(identifier too long): " + line)
                        break
                    
                mat = re.match(r"^-?[0-9]+(\.[0-9]+)?", token)
                if mat is not None:
                    test_mat = re.match(r"^-?[0-9]+(\.[0-9]+)?[_a-zA-Z]", token)
                    if test_mat is None:
                        insert_constant(mat.group(0))
                        token = token[mat.end(0):len(token)]
                        continue
                    else:
                        print("Lexical error on line " + str(line_nr) + "(invalid identifier): " + line)
                        break
                print("Lexical error on line " + str(line_nr) + ": " + line)
                break

if __name__ == "__main__":
    main()
    
    for key, value in dict(sorted(TS.items())).items():
        print(f"{key}: {value}")
    print("FIP:\n", FIP)
