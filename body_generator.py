from generator import Generator

class BodyGenerator(Generator):
  HEADER_VAR = 'BODY_HEADER'
  FOOTER_VAR = 'BODY_FOOTER'

  def __init__(self, instructions, substitutions, variables):
    Generator.__init__(self, variables)
    self.instructions = instructions
    self.substitutions = substitutions

  def generate_content(self, f):
    for instruction in self.instructions:
      match = self.substitutions.lookup(instruction.mnemonic)
      if match:
        self.__generate_method(f, match)

  def __generate_method(self, f, match):
    self.__generate_method_header(f, match)
    self.__generate_method_body(f, match)
    self.__generate_method_footer(f, match)

  def __generate_method_header(self, f, match):
    f.write(
      '   procedure ' + match.method_name() + ' (GB : in out Gade.GB.GB_Type) is\n'
    )
    if not match.has_declarations:
      f.write('   begin\n')

  def __generate_method_body(self, f, match):
    for content_line in match.value():
      if not match.has_declarations:
        f.write('   ')
      f.write('   ' + content_line + '\n')

  def __generate_method_footer(self, f, match):
    f.write('   end ' + match.method_name() + ';\n\n')
