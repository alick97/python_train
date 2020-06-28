import sys
from lex import *


class Parser:
    '''# Parser object keeps track of current token and checks if the code matches the grammar.'''
    def __init__(self, lexer):
        self.lexer = lexer

        self.symbols = set()  # All variables we have declared so far.
        self.labelsDeclared = set()  # Keep track of all labels declared.
        self.labelsGotoed = set()  # All labels goto'ed, so we know if they exist or not.

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()  # Call this twice to initialize current and peek.

    def checkToken(self, kind):
        '''Return true if the current token matches.'''
        return kind == self.curToken.kind

    def checkPeek(self, kind):
        '''Return true if the next token matches.'''
        return kind == self.peekToken.kind

    def match(self, kind):
        '''Try to match current token. If not, error. Advances the current token.'''
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)
        self.nextToken()

    def nextToken(self):
    '''Advances the current token.'''
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()
        # No need to worry about passing the EOF, lexer handles that.