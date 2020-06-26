from lex import Lexer, TokenType, Token
import unittest


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


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TokenTestCase))
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
