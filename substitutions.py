import re

from token import Token
from instruction import Instruction

class SubstitutionMatch:
  DECLARATIONS = re.compile(r'^[ \t]*begin[ \t]*$')
  METHOD_REFERENCE = re.compile(r'^([ \t]*)%([a-zA-Z0-9,\(\) ]*)[ \t]*$')
  ARGUMENT_REFERENCE = re.compile(r'\%(\d)')

  def __init__(self, substitutions, match, content):
    self.substitutions = substitutions
    self.match = match
    self.raw_content = content
    self.has_declarations = self.__has_declarations()

  def method_name(self):
    return Instruction.method_name_from_mnemonic(self.match.group())

  def value(self):
    susbtituted_content = []
    for raw_line in self.raw_content:
      method_ref_match = self.METHOD_REFERENCE.match(raw_line)
      consolidated_line = None
      if method_ref_match:
        consolidated_line = self.__replace_method(raw_line, method_ref_match)
      else:
        consolidated_line = self.__replace_arguments(raw_line)
      susbtituted_content.append(consolidated_line)
    return susbtituted_content

  def __has_declarations(self):
    for raw_line in self.raw_content:
      if self.DECLARATIONS.match(raw_line):
        return True
    return False

  def __replace_method(self, line, method_ref_match):
    indentation = method_ref_match.group(1)
    mnemonic = method_ref_match.group(2)
    method_name = self.substitutions.lookup(mnemonic).method_name()
    return indentation + method_name + '(GB);'

  def __replace_arguments(self, line):
    return self.ARGUMENT_REFERENCE.sub(self.__arg_rep, line)

  def __arg_rep(self, match):
    group_index = int(match.group(1))
    return self.match.group(group_index)

class Substitution(Token):
  def __init__(self, substitutions, expression):
    self.substitutions = substitutions
    self.expression = expression
    self.full_expression = re.compile(r'^' + expression + r'$')
    self.content = []

  def match(self, mnemonic):
    match = self.full_expression.match(mnemonic)
    if match:
      return SubstitutionMatch(self.substitutions, match, self.content)

  def token_name(self):
    return 'Substitution ' + expression

class Substitutions:
  def __init__(self):
    self.substitutions = []

  def lookup(self, mnemonic):
    for substitution in self.substitutions:
      match = substitution.match(mnemonic)
      if match:
        return match

  def add(self, substitution):
    self.substitutions.append(substitution)
