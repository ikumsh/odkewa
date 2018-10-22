import ply.lex as lex

class ODKewaLexer(object):
   # List of token names.   This is always required
   reserved = {
         'and': 'AND',
         'or': 'OR',
         'not': 'NOT'
   }

   tokens = [
      'PLUS',
      'MINUS',
      'TIMES',
      'DIVIDE',
      'LPAREN',
      'RPAREN',
      'COMMA',
      'DOT',
      'DOTDOT',
      'EXCLAMATION',
      'EQUAL',
      'NOT_EQUAL',
      'GREATER',
      'LESS',
      'GREATEROREQ',
      'LESSOREQ',
      'IDENTIFIER',
      'NUMBER', 
      'STRING',
      'VAR',
   ] + list(reserved.values())

   # Regular expression rules for simple tokens
   t_PLUS         = r'\+'
   t_MINUS        = r'-'
   t_TIMES        = r'\*'
   t_DIVIDE       = r'/'
   t_LPAREN       = r'\('
   t_RPAREN       = r'\)'
   t_COMMA        = r','
   t_DOT          = r'\.'
   # t_DOTDOT       = r'\.\.'
   t_EXCLAMATION  = r'\!'
   t_EQUAL        = r'\='
   t_NOT_EQUAL    = r'\!\='
   t_GREATER      = r'\>'
   t_LESS         = r'\<'
   t_GREATEROREQ  = r'\>\='
   t_LESSOREQ     = r'\<\='
   
   def t_IDENTIFIER(self, t):
      r'[a-zA-Z_][a-zA-Z0-9_]*'
      t.type = {  'and': 'AND',
                  'or': 'OR',
                  'not': 'NOT'
               }.get(t.value,'IDENTIFIER')
      return t

   # A regular expression rule with some action code
   def t_NUMBER(self, t):
      r'-?\d+(\.\d*)?'
      try:
         t.value = int(t.value)
      except ValueError:
         t.value = float(t.value)    
      return t

   def t_STRING(self, t):
      r"'[^']*'"
      t.value = t.value[1:-1]
      return t

   def t_VAR(self, t):
      r"\$\{[a-zA-Z_]([a-zA-Z0-9_]*)?\}"
      t.value = t.value[2:-1]
      return t

   # Define a rule so we can track line numbers
   def t_newline(self, t):
      r'\n+'
      t.lexer.lineno += len(t.value)

   # A string containing ignored characters (spaces and tabs)
   t_ignore  = ' \t'

   # Error handling rule
   def t_error(self, t):
      print("Illegal character '%s'" % t.value[0])
      t.lexer.skip(1)

    # Build the lexer
   def build(self,**kwargs):
      self.lexer = lex.lex(module=self, **kwargs)

   def input(self, data):
      return self.lexer.input(data)

   def token(self):
      return self.lexer.token()

   # Test it output
   def test(self,data):
      self.input(data)
      while True:
         tok = self.token()
         if not tok: 
            break
         print(tok.type, tok.value)

if __name__ == '__main__':
   # Build the lexer and try it out
   m = ODKewaLexer()
   m.build()           # Build the lexer
   print("first a simple test:\n")
   m.test("3 + 4 abcde not")
   print("\n\nand next a list of tokens:\n")     # Test it
   m.tokenize("3 + 4 abcde != $ not")
