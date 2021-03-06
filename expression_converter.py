import hashlib
from odkewa_parser import *

class ExpressionConverter():

   def __init__(self, question):
      self.lexer = ODKewaLexer()
      self.lexer.build()
      self.q = question
      self.tokenized = {}
      self.calculation = ''
      self.constraint = ''
      self.relevant = ''
      self.choice_filter = ''
      self.cf_vars = ''

   def tokenize(self, ex_type):
      self.tokenized[ex_type] = []
      self.lexer.input(self.q[ex_type])
      while True:
         tok = self.lexer.token()
         if not tok: 
            break
         self.tokenized[ex_type].append({ "type": tok.type, "value": tok.value})

   def to_ng_function(self, ex_type):
      if ex_type == "calculation":
         return self.calculation

      if ex_type == "constraint":
         if self.q.get("constraint",'') != '':
            for tok in self.q["constraint"]["tokenized"]:
               if tok["type"] == "IDENTIFIER":
                  self.constraint += "" # TODO: THROW EXCEPTION
               elif tok["type"] == "DOT":
                  self.constraint += "value "
               # if tok["type"] == "DOTDOT":
               #    pass
               elif tok["type"] == "EQUAL":
                  self.constraint += "== "
               elif tok["type"] == "AND":
                  self.constraint += "&& "
               elif tok["type"] == "OR":
                  self.constraint += "|| "
               elif tok["type"] == "NOT":
                  self.constraint += "!"
               elif tok["type"] == "VAR":
                  self.constraint += "scope.data."+tok["value"]+" " if tok["value"] != self.q["name"] else "value "
               elif tok["type"] == "STRING":
                  self.constraint += '\''+tok["value"]+'\''
               else:
                  self.constraint += str(tok["value"])+" "

         if self.constraint != '':
            c_name = hashlib.sha1(self.q['name']).hexdigest()
            self.constraint = """
               ODKewa.directive(\'"""+c_name+"""\', function() {
                   return {
                       require: \'ngModel\',
                       link: function(scope, element, attr, mCtrl) {
                           function validation(value) 
                           {
                              // """+self.q['name']+""" validation
                              mCtrl.$setValidity(\'"""+c_name+"""Error\', """+self.constraint+""");
                              return value;
                           }
                           mCtrl.$parsers.push(validation);
                       }
                   };
               });\n
            """
         return self.constraint

      if ex_type == "relevant":
         if self.q.get("relevant",'') != '':
            for tok in self.q["relevant"]["tokenized"]:
               if tok["type"] == "IDENTIFIER":
                  self.relevant += "" # TODO: THROW EXCEPTION
               elif tok["type"] == "DOT":
                  self.relevant += "document.getElementById(\""+self.q['name']+"\").value "
               # if tok["type"] == "DOTDOT":
               #    pass
               elif tok["type"] == "EQUAL":
                  self.relevant += "== "
               elif tok["type"] == "AND":
                  self.relevant += "&& "
               elif tok["type"] == "OR":
                  self.relevant += "|| "
               elif tok["type"] == "NOT":
                  self.relevant += "!"
               elif tok["type"] == "VAR":
                  self.relevant += "document.getElementById(\""+tok["value"]+"\").value "
               elif tok["type"] == "STRING":
                  self.relevant += '\''+tok["value"]+'\''
               else:
                  self.relevant += str(tok["value"])+" "

         if self.relevant != '':
            self.relevant = """
               $scope.relevant__"""+self.q["name"]+""" = function relevant__"""+self.q["name"]+"""() {
                  return """+self.relevant+""";
               };\n
            """
         return self.relevant

      if ex_type == "choice_filter" and (self.q["type"] == "select_one" or self.q["type"] == "select_multiple"):
         if self.q.get("choice_filter",'') != '':
            for tok in self.q["choice_filter"]["tokenized"]:
               if tok["type"] == "DOT":
                  self.choice_filter += "$scope.data."+self.q['name']+" "
               # if tok["type"] == "DOTDOT":
               #    pass
               elif tok["type"] == "EQUAL":
                  self.choice_filter += "== "
               elif tok["type"] == "VAR":
                  self.choice_filter += "vars."+tok["value"]+" "
                  self.cf_vars += tok["value"]+": data."+tok["value"]+", "
               elif tok["type"] == "STRING":
                  self.choice_filter += '\''+tok["value"]+'\''
               elif tok["type"] == "IDENTIFIER":
                  self.choice_filter += "choice."+tok["value"]+" "
               else:
                  self.choice_filter += str(tok["value"])+" "
         if self.choice_filter != '':
            self.choice_filter = """
               $scope."""+self.q["name"]+"""__filter = function(vars) {
                     rs = $scope.choices."""+self.q["list_name"]+""".filter(function(choice) { return """+self.choice_filter+"""})
                     // if (rs.length > 0){
                     //    $scope.data."""+self.q["name"]+""" = rs[0].name
                     // }
                     return rs;
               };\n
            """
         return {"filter": self.choice_filter, "vars": self.cf_vars}

if __name__ == '__main__':
      print('tok')
