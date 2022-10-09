import sys


from parser.parser import Parser


def handle_args(args):
    if len(args) > 1:
        if args[1] == '-c':
            if len(args) > 2:
                p = Parser(args[2])
                print(p.parse().value)
                return
        elif args[1] == '-h' or args[1] == '--help':
            print("-c <expression> Calculate the specified expression and output the result to the standard output stream!!!")
            print("-h, --help  Show help message.")
            print()
            # print copyright
            print("no-division-calculator Copyright (C) 2022 May the force be with you!")
            return
    interactive()


def interactive():
    print("Welcome to the calculator!")
    print("calculator Copyright (C) 2022 May the force be with you!")
    while True:
        try:
            expression = input(">")
            if not expression.strip():
                continue  
            p = Parser(expression)
            print(p.parse().value)
        except KeyboardInterrupt as ex:
            exit(0)
        except Exception as ex:
            print(ex)

def calculate():
    print("Welcome to the calculator!")
    print("calculator Copyright (C) 2022 May the force be with you!")
    while True:
        try:
            expression = input("")
            if expression.len() == 0:
                 print("No input was entered.")
            if not expression.strip():
                continue  
            p = Parser(expression)
            print(p.parse().value)
        except KeyboardInterrupt as ex:
            exit(0)
        except Exception as ex:
            print(ex)
