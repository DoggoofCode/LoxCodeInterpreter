from LoxInterpreter.token import Token
from LoxInterpreter.scanner import Scanner

class Lox:
    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath
        self.runFile()

    def runFile(self) -> None:
        with open(self.filepath, 'r') as file:
            self.run(file.read())

    def run(self, source: str) -> None:
        scanner: Scanner = Scanner(source)
        tokens: list[Token] = scanner.scanTokens()

        for token in tokens:
            print(token)
