import argparse as arg
from LoxInterpreter import panic, Lox

def main() -> None:
    parser = arg.ArgumentParser(description='Crafting a Compiler')
    parser.add_argument("filepath", help="Path to the input file", type=str, default=None, nargs="?")
    parser.add_argument('--version', action='version', version='Crafting a Compiler 1.0')
    args = parser.parse_args()

    if not args.filepath:
        panic("No input file provided")

    Lox(args.filepath)

if __name__ == '__main__':
    main()
