from variables import *
from substitutions import *

class Tokenizer:
  def __init__(self):
    self.variables = Variables()
    self.substitutions = Substitutions()

  def read_tokens(self, f):
    token = self.__read_token(f, None)
    while token is not None:
      token = self.__read_token(f, token)

  def __read_token(self, f, last_token):
    token = last_token
    line = self.__skip_blank_lines(f)
    llen = len(line)
    if llen >= 2 and line[0:2] == '$$':
      # Multiline var token
      token = MultilineVariable(self.variables, line[2:-1])
      self.variables.add(token)
    elif llen >= 1 and line[0] == '$':
      # String var token
      token = StringVariable(self.variables, line[1:-1])
      self.variables.add(token)
    elif llen >= 1 and line[0] == '\t':
      # Content line
      last_token.add_content(line[1:-1])
    elif llen > 1:
      # Expression line
      token = Substitution(self.substitutions, line[0:-1])
      self.substitutions.add(token)
    else:
      token = None
    if token != last_token and last_token != None:
      last_token.close()
    return token

  def __skip_blank_lines(self, f):
    line = f.readline()
    while line != '' and line[0] in ['\n', '#']:
      line = f.readline()
    return line

  @classmethod
  def load(klass, file_name):
    f = open(file_name, 'r')
    t = Tokenizer()
    t.read_tokens(f)
    f.close()
    return t.variables, t.substitutions
