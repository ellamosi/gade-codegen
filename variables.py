import re

from token import Token

class Variable(Token):
  def __init__(self, variables, name):
    Token.__init__(self)
    self.variables = variables
    self.name = name

  def token_name(self):
    return 'Variable: ' + self.name

class MultilineVariable(Variable):
  VAR_REFERENCE = re.compile(r'\$([a-zA-Z0-9_]+)\$')

  def __init__(self, variables, name):
    Variable.__init__(self, variables, name)

  def __var_rep(self, match):
    return self.variables.lookup(match.group(1))

  def value(self):
    susbtituted_content = []
    for raw_line in self.content:
      var_ref_match = self.VAR_REFERENCE.match(raw_line)
      consolidated_line = self.VAR_REFERENCE.sub(self.__var_rep, raw_line)
      susbtituted_content.append(consolidated_line)
    return susbtituted_content

class StringVariable(Variable):
  def __init__(self, variables, name):
    Variable.__init__(self, variables, name)

  def add_content(self, content):
    if len(self.content) > 0:
      raise Exception('Single line var with multiple lines')
    else:
      Variable.add_content(self, content)

  def value(self):
    return self.content[0]

class Variables:
  def __init__(self):
    self.variables = {}

  def lookup(self, name):
    return self.variables[name].value()

  def add(self, variable):
    self.variables[variable.name] = variable
