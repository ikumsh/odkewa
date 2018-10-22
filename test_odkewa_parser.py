import unittest
from odkewa_parser import *
import ply.lex as lex

class TestParser(unittest.TestCase):

   def setUp(self):
      self.lexer = ODKewaLexer()
      self.lexer.build()

   def test_PLUS(self):
      self.lexer.input("+ -")
      tok = self.lexer.token()
      self.assertEqual("PLUS", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("PLUS", tok.type)


   def test_MINUS(self):
      self.lexer.input("-+")
      tok = self.lexer.token()
      self.assertEqual("MINUS", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("MINUS", tok.type)


   def test_TIMES(self):
      self.lexer.input("*+")
      tok = self.lexer.token()
      self.assertEqual("TIMES", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("TIMES", tok.type)

   def test_DIVIDE(self):
      self.lexer.input("/+")
      tok = self.lexer.token()
      self.assertEqual("DIVIDE", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("DIVIDE", tok.type)

   def test_LPAREN(self):
      self.lexer.input("(+")
      tok = self.lexer.token()
      self.assertEqual("LPAREN", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("LPAREN", tok.type)

   def test_RPAREN(self):
      self.lexer.input(")+")
      tok = self.lexer.token()
      self.assertEqual("RPAREN", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("RPAREN", tok.type)

   def test_COMMA(self):
      self.lexer.input(",+")
      tok = self.lexer.token()
      self.assertEqual("COMMA", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("COMMA", tok.type)


   def test_DOT(self):
      self.lexer.input(".+")
      tok = self.lexer.token()
      self.assertEqual("DOT", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("DOT", tok.type)


   # def test_DOTDOT(self):
   #    self.lexer.input("..x")
   #    tok = self.lexer.token()
   #    self.assertEqual("DOTDOT", tok.type)
   #    tok = self.lexer.token()
   #    self.assertNotEqual("DOTDOT", tok.type)

   def test_EQUAL(self):
      self.lexer.input("=x")
      tok = self.lexer.token()
      self.assertEqual("EQUAL", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("EQUAL", tok.type)

   def test_GREATER(self):
      self.lexer.input(">x")
      tok = self.lexer.token()
      self.assertEqual("GREATER", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("GREATER", tok.type)

   def test_LESS(self):
      self.lexer.input("<x")
      tok = self.lexer.token()
      self.assertEqual("LESS", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("LESS", tok.type)

   def test_GREATEROREQ(self):
      self.lexer.input(">=x")
      tok = self.lexer.token()
      self.assertEqual("GREATEROREQ", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("GREATEROREQ", tok.type)

   def test_LESSOREQ(self):
      self.lexer.input("<=x")
      tok = self.lexer.token()
      self.assertEqual("LESSOREQ", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("LESSOREQ", tok.type)

   def test_IDENTIFIER(self):
      self.lexer.input("abcde,")
      tok = self.lexer.token()
      self.assertEqual("IDENTIFIER", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("IDENTIFIER", tok.type)

   def test_NUMBER(self):
      self.lexer.input("10 1.0 -10 -1.0 abc")
      tok = self.lexer.token()
      self.assertEqual("NUMBER", tok.type)
      tok = self.lexer.token()
      self.assertEqual("NUMBER", tok.type)
      tok = self.lexer.token()
      self.assertEqual("NUMBER", tok.type)
      tok = self.lexer.token()
      self.assertEqual("NUMBER", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("NUMBER", tok.type)

   def test_STRING(self):
      self.lexer.input("'abcde',")
      tok = self.lexer.token()
      self.assertEqual("STRING", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("STRING", tok.type)

   def test_VAR(self):
      self.lexer.input("${abcde}abcde")
      tok = self.lexer.token()
      self.assertEqual("VAR", tok.type)
      tok = self.lexer.token()
      self.assertNotEqual("VAR", tok.type)

if __name__ == '__main__':
   unittest.main()