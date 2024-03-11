import sys
from models import Grammar, AF

def main():
    gr = Grammar(sys.argv[1])
    while True:
        print('Chose an option:\n'
              '1.Display grammar and productions\n'
              '2.Show productions of nonterminal\n'
              '3.Check if grammar is regular\n'
              '4.Transform grammar in AF\n'
              '0.Exit\n')
        command = int(input())
        if command == 1:
            gr.show_grammar_elements()
        elif command == 2:
            nonterminal = input('Choose nonterminal:\n')
            gr.show_nonterminal_productions(nonterminal)
        elif command == 3:
            if gr.is_regular():
                print('Grammar is regular')
            else:
                print('Grammar is not regular')
        elif command == 4:
            gr.to_AF().show_elements()
        elif command == 0:
            break
        else:
            print('Non-existent command')


if __name__ == '__main__':
    main()