import sys

class GIC:
    def __init__(self, filename):
        self.__terminals = set()
        self.__non_terminals = set()
        self.__productions = []

        for line in open(filename, 'r').readlines():
            lhs, rhs = line.strip().split('->')
            self.__productions.append((lhs, rhs))
            self.__non_terminals.add(lhs)
            for symbol in rhs:
                if symbol != '@':
                    if symbol.isupper():
                        self.__non_terminals.add(symbol)
                    else:
                        self.__terminals.add(symbol)
    
    def get_terminals(self):
        return self.__terminals
    
    def get_non_terminals(self):
        return self.__non_terminals
    
    def get_productions(self):
        return self.__productions
    

def first(grammar: GIC):
    first = {}
    for terminal in grammar.get_terminals():
        first[terminal] = {terminal}
    for non_terminal in grammar.get_non_terminals():
        first[non_terminal] = set()
    for lhs, rhs in grammar.get_productions():
        if rhs == '@':
            first[lhs].add('@')

    while True:
        updated = False
        for lhs, rhs in grammar.get_productions():
            if rhs == '@':
                continue
            for symbol in rhs:
                if symbol in grammar.get_terminals():
                    if symbol not in first[lhs]:
                        first[lhs].add(symbol)
                        updated = True
                    break
                else:
                    for terminal in first[symbol]:
                        if terminal not in first[lhs] and terminal != '@':
                            first[lhs].add(terminal)
                            updated = True
                    if '@' not in first[symbol]:
                        break
            else:
                if '@' not in first[lhs]:
                    first[lhs].add('@')
                    updated = True
        if not updated:
            break 
    return first


def follow(grammar: GIC, first_set):
    follow = {}
    for non_terminal in grammar.get_non_terminals():
        follow[non_terminal] = set()
    follow['S'].add('$')
    
    while True:
        updated = False
        for lhs, rhs in grammar.get_productions():
            for i in range(len(rhs)):
                if rhs[i] in grammar.get_terminals() or rhs[i] == '@':
                    continue
                for j in range(i + 1, len(rhs)):
                    for terminal in first_set[rhs[j]]:
                        if terminal != '@' and terminal not in follow[rhs[i]]:
                            follow[rhs[i]].add(terminal)
                            updated = True
                    if '@' not in first_set[rhs[j]]:
                        break
                else:
                    for terminal in follow[lhs]:
                        if terminal not in follow[rhs[i]]:
                            follow[rhs[i]].add(terminal)
                            updated = True
        if not updated:
            break
    return follow


def ll_table(grammar: GIC, first_set, follow_set):
    table = {}
    for non_terminal in grammar.get_non_terminals():
        table[non_terminal] = {}
    for terminal in grammar.get_terminals():
        table[terminal] = {}
    table['$'] = {}

    for line in table.keys():
        for terminal in grammar.get_terminals():
            table[line][terminal] = []
        table[line]['$'] = []

    for i in range(len(grammar.get_productions())):
        lhs, rhs = grammar.get_productions()[i]

        if rhs == '@' or '@' in first_set[rhs[0]]:
            for terminal in follow_set[lhs]:
                table[lhs][terminal].append((rhs, i+1))
        else:
            for terminal in first_set[rhs[0]]:
                table[lhs][terminal].append((rhs,i+1))

    for terminal in grammar.get_terminals():
        table[terminal][terminal].append(('pop', -1))

    table['$']['$'].append(('acc', -1))


    for line in table.keys():
        for column in table[line].keys():
            if table[line][column] == []:
                table[line][column].append(('err', -1))
    
    return table


def print_ll1_table(table):
    print('Table:')
    for line in table.keys():
        for column in table[line].keys():
            print(line, column, table[line][column])
        print()

def analyze(table, input):
    working_stack = 'S$'
    input_stack = input + '$'
    output = ''

    while True:
        print(f"({input_stack}, {working_stack}, {output})", end=" |-")

        if working_stack[0] == '@':
            working_stack = working_stack[1:]
            continue 
        if table[working_stack[0]][input_stack[0]][0][0] == 'acc':
            print('acc')
            print('Accepted')
            print(output)
            break
        elif table[working_stack[0]][input_stack[0]][0][0] == 'pop':
            working_stack = working_stack[1:]
            input_stack = input_stack[1:]
            print('pop')
        elif table[working_stack[0]][input_stack[0]][0][0] == 'err':
            print('err')
            print('Error')
            break
        else:
            output = output + ' ' + str(table[working_stack[0]][input_stack[0]][0][1]) 
            working_stack = table[working_stack[0]][input_stack[0]][0][0] + working_stack[1:]
            print()



def main():
    gic = GIC(sys.argv[1])
    first_set = first(gic)
    follow_set = follow(gic, first_set)
    print('First:', first_set)
    print('Follow: ', follow_set)
    table = ll_table(gic, first_set, follow_set)
    analyze(table, sys.argv[2])

if __name__ == "__main__":
    main()