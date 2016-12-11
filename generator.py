class Generator:
  def __init__(self, variables):
    self.variables = variables

  def generate_from_variable(self, f, variable):
    header = self.variables.lookup(variable)
    self.__write_lines(f, header)

  def generate(self, file_name):
    f = open(file_name, 'w')
    self.generate_from_variable(f, self.HEADER_VAR)
    self.generate_content(f)
    self.generate_from_variable(f, self.FOOTER_VAR)
    f.close()

  @classmethod
  def __write_lines(klass, f, lines):
    for line in lines:
      f.write(line + '\n')
