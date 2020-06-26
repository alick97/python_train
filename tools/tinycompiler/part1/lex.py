import enum
import sys


class TokenType(enum.Enum):
    '''TokenType is our enum for all the types of tokens.'''
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords, range 101-200.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
    # Operators.
    EQ = 201
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211


class Token:
    ''''Token contains the original text and the type of token.'''
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText   # The token's actual text. Used for identifiers, strings, and numbers.
        self.kind = tokenKind   # The TokenType that this token is classified as.

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # Relies on all keyword enum values being 1XX.
            if kind.name == tokenText and kind.value > 100 and kind.value < 200:
                return kind
        return None

    def __repr__(self):
        return '{}, token text:{}, token kind:{}'.format(super().__repr__(), self.text, self.kind)

    def __eq__(self, other):
        return self.text == other.text and self.kind == other.kind


class Lexer:
    def __init__(self, input):
        self.source = input + '\n'  # Source code to lex as a string. Append a newline to simplify lexing/parsing the last token/statement.
        self.curChar = ''  # Current character in the string.
        self.curPos = -1  # Current position in the string.
        self.nextChar()

    def nextChar(self):
        '''Process the next character.'''
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'  # EOF
        else:
            self.curChar = self.source[self.curPos]

    def peek(self):
        '''Return the lookahead character.'''
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos+1]

    def abort(self, message):
        '''Invalid token found, print error message and exit.'''
        sys.exit('Lexing error. ' + message)

    def skipWhitespace(self):
        '''Skip whitespace except newlines, which we will use to indicate the end of a statement.'''
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()

    def skipComment(self):
        '''Skip comments in the code.'''
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    def getToken(self):
        '''Return the next token.'''
        self.skipWhitespace()
        self.skipComment()
        token = None

        # Check the first character of this token to see if we can decide what it is.
        # If it is a multiple character operator (e.g., !=), number, identifier,
        # or keyword then we will process the rest.
        # TODO: Add other token parse.
        if self.curChar == '+':
            token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token('', TokenType.EOF)
        else:
            # Unknow token.
            print("Unknow token")
            pass

        self.nextChar()
        return token


    
    




