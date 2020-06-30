from lex import Lexer, TokenType, Token
from parse import Parser
import unittest
import coverage
import logging

class TokenTestCase(unittest.TestCase):
    def get_token_list(self, input):
        token_list = list()

        lexer = Lexer(input)
        token = lexer.getToken()
        token_list.append(token)
        while token.kind != TokenType.EOF:
            token = lexer.getToken()
            token_list.append(token)
        return token_list

    def assertTokenlistEqual(self, list1, list2):
        error_msg = "\nfirstlist:{}\nsecondlist:{}".format(list1, list2)
        self.assertListEqual(list1, list2, error_msg)

    def test_token_comment(self):
        input = '#abc'
        token_list = [
            Token('\n', TokenType.NEWLINE),
            Token('', TokenType.EOF)
        ]
        self.assertTokenlistEqual(self.get_token_list(input), token_list)

    def test_token_pluse(self):
        input = '#dasds\n+'
        token_list = [
            Token('\n', TokenType.NEWLINE),
            Token('+', TokenType.PLUS),
            Token('\n', TokenType.NEWLINE),
            Token('', TokenType.EOF)
        ]
        self.assertTokenlistEqual(self.get_token_list(input), token_list)

    def test_string_illegal_character(self):
        input = '"123'
        with self.assertRaises(SystemExit):
            self.get_token_list(input)

    def test_keyword_operator_identifer(self):
        input = 'IF+-123 foo*THEN/'
        token_list = [
            Token('IF', TokenType.IF),
            Token('+', TokenType.PLUS),
            Token('-', TokenType.MINUS),
            Token('123', TokenType.NUMBER),
            Token('foo', TokenType.IDENT),
            Token('*', TokenType.ASTERISK),
            Token('THEN', TokenType.THEN),
            Token('/', TokenType.SLASH),
            Token('\n', TokenType.NEWLINE),
            Token('', TokenType.EOF)
        ]
        self.assertTokenlistEqual(self.get_token_list(input), token_list)


class ParseTestCase(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def test_parse(self):
        print("Tiny Compiler")
        with open('hello.tiny', 'r') as inputFile:
            input = inputFile.read()

        # Initialize the lexer and parser.
        lexer = Lexer(input)
        parser = Parser(lexer)

        parser.program()  # Start the parser.
        print("Parsing completed.")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TokenTestCase))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(ParseTestCase))
    return suite


if __name__ == '__main__':
    cov = coverage.Coverage(branch=True, source=['lex', 'parse'])
    cov.start()

    runner = unittest.TextTestRunner()
    runner.run(suite())

    cov.stop()
    cov.save()

    cov.report(show_missing=True)
    cov.html_report()
