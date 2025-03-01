from LoxInterpreter.token import Token, TokenType
from LoxInterpreter.utils import panic

def is_alpha(c: str) -> bool:
    return c >= 'a' and c <= 'z' or c >= 'A' and c <= 'Z' or c == '_'

def is_digit(c: str) -> bool:
    return c >= '0' and c <= '9'

class Scanner:
    _start = 0
    _current = 0
    _line = 1

    def __init__(self, source: str) -> None:
        self.source:str = source
        self.tokens:list[Token] = []

    @property
    def is_at_end(self) -> bool:
        return self._current >= len(self.source)

    def scanTokens(self) -> list[Token]:
        while not self.is_at_end:
            self._start = self._current
            self.scanToken()

        self.tokens.append(Token(TokenType.EOF, "", None, self._line))
        return self.tokens

    def match(self, expected: str) -> bool:
        if self.is_at_end or self.source[self._current] != expected:
            return False
        self._current += 1
        return True

    def scanToken(self) -> None:
        c = self.advance()
        match c:
            case '(':
                self.add_token(TokenType.LEFT_PAREN)
            case ')':
                self.add_token(TokenType.RIGHT_PAREN)
            case '{':
                self.add_token(TokenType.LEFT_BRACE)
            case '}':
                self.add_token(TokenType.RIGHT_BRACE)
            case ',':
                self.add_token(TokenType.COMMA)
            case '.':
                self.add_token(TokenType.DOT)
            case '-':
                self.add_token(TokenType.MINUS)
            case '+':
                self.add_token(TokenType.PLUS)
            case ';':
                self.add_token(TokenType.SEMICOLON)
            case '*':
                self.add_token(TokenType.STAR)
            case '!':
                if self.match("="):
                    self.add_token(TokenType.BANG_EQUAL)
                else:
                    self.add_token(TokenType.BANG)
            case '=':
                if self.match("="):
                    self.add_token(TokenType.EQUAL_EQUAL)
                else:
                    self.add_token(TokenType.EQUAL)
            case '<':
                if self.match("="):
                    self.add_token(TokenType.LESS_EQUAL)
                else:
                    self.add_token(TokenType.LESS)
            case '>':
                if self.match("="):
                    self.add_token(TokenType.GREATER_EQUAL)
                else:
                    self.add_token(TokenType.GREATER)
            case '/':
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_end:
                        self.advance()
                elif self.match("*"):
                    self.multi_line_comment()
                else:
                    self.add_token(TokenType.SLASH)
            case ' ':
                pass
            case '\t':
                pass
            case '\t':
                pass
            case '\r':
                pass
            case '\n':
                self._line += 1
            case '"':
                self.string()
            case _:
                if is_digit(c):
                    self.number()
                elif is_alpha(c):
                    self.identifier()
                else:
                    panic(f"Unexpected character '{c}'", self._line, [self.tokens])

    def multi_line_comment(self):
        while self.peek() != "*" and self.peek_next() != "/" and not self.is_at_end:
            if self.peek() == "\n":
                self._line += 1
            self.advance()
        if self.is_at_end:
            panic("Unterminated comment.", self._line)
        self.advance()
        self.advance()

    def identifier(self):
        while is_alpha(self.peek()) or is_digit(self.peek()):
            self.advance()
        text = self.source[self._start:self._current]
        type = self.keywords.get(text)
        if type is None:
            type = TokenType.IDENTIFIER
        self.add_token(type)

    def number(self):
        while is_digit(self.peek()):
            self.advance()
        if self.peek() == "." and is_digit(self.peek_next()):
            self.advance()
            while is_digit(self.peek()):
                self.advance()
        self.add_token(TokenType.NUMBER, float(self.source[self._start:self._current]))

    def peek_next(self):
        if self._current + 1 >= len(self.source):
            return "\0"
        return self.source[self._current + 1]

    def string(self) -> None:
        while self.peek() != '"' and not self.is_at_end:
            if self.peek() == "\n":
                self._line += 1
            self.advance()
        if self.is_at_end:
            panic("Unterminated string.", self._line)
        self.advance()
        self.add_token(TokenType.STRING, self.source[self._start + 1:self._current - 1])

    def peek(self) -> str:
        if self.is_at_end:
            return "\0"
        return self.source[self._current]

    def advance(self) -> str:
        self._current += 1
        return self.source[self._current - 1]

    def add_token(self, token_type: TokenType, literal: object = None) -> None:
        text = self.source[self._start:self._current]
        self.tokens.append(Token(token_type, text, literal, self._line))


    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE
    }
