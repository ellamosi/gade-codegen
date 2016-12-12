from generator import Generator

class SpecGenerator(Generator):
  HEADER_VAR = 'SPEC_HEADER'
  FOOTER_VAR = 'SPEC_FOOTER'

  def __init__(self, instructions, variables):
    Generator.__init__(self, variables)
    self.instructions = instructions

  def generate_content(self, f):
    for instruction in self.instructions:
      self.__generate_method(f, instruction)

  def __generate_method(self, f, instruction):
    self.__generate_method_name_constant(f, instruction)
    self.__generate_method_declaration(f, instruction)

  def __generate_method_name_constant(self, f, instruction):
    f.write(
      '  ' + instruction.method_name + '_Name : aliased constant String := "' +
      instruction.mnemonic + '";\n'
    )

  def __generate_method_declaration(self, f, instruction):
    f.write(
      '  procedure ' + instruction.method_name +
      ' (GB : in out GB_Context);\n\n'
    )
