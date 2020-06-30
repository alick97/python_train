import sys
import logging
from lex import TokenType, Lexer
from emit import Emitter


logger = logging.getLogger("parse")


class Parser:
    '''Parser object keeps track of current token and checks if the code matches the grammar
       and emits code along the way
    '''
    def __init__(self, lexer: Lexer, emitter: Emitter):
        self.lexer = lexer
        self.emitter = emitter

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

    def isComparisonOperator(self):
        '''Return true if the current token is a comparison operator.'''
        return (self.checkToken(TokenType.GT) or self.checkPeek(TokenType.GTEQ)
                or self.checkToken(TokenType.LT) or self.checkToken(TokenType.LTEQ)
                or self.checkToken(TokenType.EQEQ) or self.checkToken(TokenType.NOTEQ))

    def abort(self, message):
        sys.exit("Error. " + message)

    # Production rules.

    def program(self):
        '''program ::= {statement}'''
        logger.debug("PROGRAM")

        self.emitter.headerLine('#include <stdio.h>')
        self.emitter.headerLine('int main(void) {')
        # Since some newlines are required in out grammar, need to skip the excess.
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        # Parse all the statements in the program.
        while not self.checkToken(TokenType.EOF):
            self.statement()

        # Wrap things up.
        self.emitter.emitLine("return 0;")
        self.emitter.emitLine("}")

        # Check that each label referenced in a GOTO is decalred.
        for label in self.labelsGotoed:
            if label not in self.labelsGotoed:
                self.abort("Attempting to GOTO to undeclared label: " + label)

    def statement(self):
        '''One of the following statements...'''

        # Check the first token to see what kind of statement this is.

        # "PRINT" (express | string)
        if self.checkToken(TokenType.PRINT):
            logger.debug("STATEMENT-PRINT")
            self.nextToken()

            if self.checkToken(TokenType.STRING):
                # Simple string, so print it.
                self.emitter.emitLine(r'printf("{}\n");'.format(self.curToken.text))
                self.nextToken()
            else:
                # Expect an expression and print the result as a float.
                self.emitter.emit(r'printf("%.2f\n", (float)(')
                self.expression()
                self.emitter.emitLine('));')
        # "IF" comparison "THEN" {statement} "ENDIF"
        elif self.checkToken(TokenType.IF):
            logger.debug("STATEMENT-IF")
            self.nextToken()
            self.emitter.emit('if(')
            self.comparison()

            self.match(TokenType.THEN)
            self.nl()
            self.emitter.emitLine(') {')

            # Zero or more statements in the body.
            while not self.checkToken(TokenType.ENDIF):
                self.statement()

            self.match(TokenType.ENDIF)
            self.emitter.emitLine('}')
        # "WHILE" comparison "REPEAT" {statement} "ENDWHILE"
        elif self.checkToken(TokenType.WHILE):
            logger.debug("STATEMENT-WHILE")
            self.nextToken()
            self.emitter.emit('while (')
            self.comparison()

            self.match(TokenType.REPEAT)
            self.nl()
            self.emitter.emitLine(') {')

            # Zero or more statements in the loop body.
            while not self.checkToken(TokenType.ENDWHILE):
                self.statement()

            self.match(TokenType.ENDWHILE)
            self.emitter.emitLine('}')
        # "LABEL" ident
        elif self.checkToken(TokenType.LABEL):
            logger.debug("STATEMENT-LABEL")
            self.nextToken()

            # Make sure this label doesn't already exist.
            if self.curToken.text in self.labelsDeclared:
                self.abort("Label already exists: " + self.curToken.text)
            self.labelsDeclared.add(self.curToken.text)

            self.emitter.emitLine(self.curToken.text + ':')
            self.match(TokenType.IDENT)
        # "GOTO" ident
        elif self.checkToken(TokenType.GOTO):
            logger.debug("STATEMENT-GOTO")
            self.nextToken()
            self.labelsGotoed.add(self.curToken.text)
            self.emitter.emitLine('goto {};'.format(self.curToken.text))
            self.match(TokenType.IDENT)
        # "LET" ident "=" expression
        elif self.checkToken(TokenType.LET):
            logger.info("STATEMENT-LET")
            self.nextToken()

            # Check if ident exists in symbol table. If not, declare it.
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)
                self.emitter.headerLine('float {};'.format(self.curToken.text))

            self.emitter.emit('{} = '.format(self.curToken.text))
            self.match(TokenType.IDENT)
            self.match(TokenType.EQ)

            self.expression()
            self.emitter.emitLine(';')
        # "INPUT" ident
        elif self.checkToken(TokenType.INPUT):
            logger.debug("STATEMENT-INPUT")
            self.nextToken()
            # If variable doesn't already exist, declare it.
            if self.curToken.text not in self.symbols:
                self.symbols.add(self.curToken.text)
                self.emitter.headerLine('float {};'.format(self.curToken.text))

            # Emit scanf but also validate the input. If invalid, set the variable to 0 and clear the input.
            self.emitter.emitLine('''
if (0 == scanf("%f", &{0})) {{
    {0} = 0;
    scanf("%s");
}}'''.format(self.curToken.text))
            self.match(TokenType.IDENT)
        # This is not a valid statement. Error!
        else:
            self.abort("Invalid statement at " + self.curToken.text + " (" + self.curToken.kind.name + ")")

        # Newline.
        self.nl()

    def comparison(self):
        '''comparison :;= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+'''
        logger.debug("COMPARISON")

        self.expression()
        # Must be at least one comparison operator and another expression.
        if self.isComparisonOperator():
            self.emitter.emit(' {} '.format(self.curToken.text))
            self.nextToken()
            self.expression()
        else:
            self.abort("Expected comparison operator at: " + self.curToken.text)

        # Can have 0 or more comparison operator and expressions.
        while self.isComparisonOperator():
            self.emitter.emit(' {} '.format(self.curToken.text))
            self.nextToken()
            self.expression()

    def expression(self):
        '''expression ::= trem {( "-" | "+" ) term}'''
        logger.debug("EXPRESSION")

        self.term()
        # Can have 0 or more +/- and exprssions.
        while self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(' {} '.format(self.curToken.text))
            self.nextToken()
            self.term()

    def term(self):
        '''term ::= unary {( "/" | "*" ) unary}'''
        logger.debug("TERM")

        self.unary()
        # Can have 0 or more *// and expressions.
        while self.checkToken(TokenType.ASTERISK) or self.checkToken(TokenType.SLASH):
            self.emitter.emit(' {} '.format(self.curToken.text))
            self.nextToken()
            self.unary()

    def unary(self):
        '''unary ::= ["+" | "-" ] primary'''
        logger.debug("UNARY")
        # Optional unary +/-
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
        self.primary()

    def primary(self):
        '''primary ::= number | ident'''
        logger.debug("PRIMARY (" + self.curToken.text + ")")

        if self.checkToken(TokenType.NUMBER):
            self.emitter.emit(self.curToken.text)
            self.nextToken()
        elif self.checkToken(TokenType.IDENT):
            # Ensure the variable already exists.
            if self.curToken.text not in self.symbols:
                self.abort("Referencing variable before assignment: " + self.curToken.text)

            self.emitter.emit(self.curToken.text)
            self.nextToken()
        else:
            # Error!
            self.abort("Unexpected token at " + self.curToken.text)

    def nl(self):
        '''nl ::= "\n"'''
        logger.debug("NEWLINE")

        # Require at least one newline.
        self.match(TokenType.NEWLINE)
        # But we will allow extra newlines too, of course.
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()
