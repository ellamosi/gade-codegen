from generator import Generator
from instruction_set import InstructionSet

class TableGenerator(Generator):
  HEADER_VAR = 'TABLE_MODULE_HEADER'
  FOOTER_VAR = 'TABLE_MODULE_FOOTER'

  def __init__(self, instructions, variables):
    Generator.__init__(self, variables)
    self.instructions = instructions

  def generate_content(self, f):
    self.ExtendedTableGenerator(
      self.instructions.cb_instructions, 'CB'
    ).generate_table(f)
    self.RootTableGenerator(
      self.instructions.main_instructions, 'Main'
    ).generate_table(f)

  class RootTableGenerator:
    def __init__(self, instructions, table_name):
      self.instructions = instructions
      self.table_name = table_name

    def generate_table(self, f):
      self.generate_table_header(f)
      self.generate_table_entries(f)
      self.generate_table_footer(f)

    def generate_table_header(self, f):
      f.write(
        '  Opcodes_' + self.table_name +
        ' : aliased constant Instruction_Table_Type :=\n' +
        '     ( 0, (\n'
      )

    def generate_table_entries(self, f):
      for idx, instruction in enumerate(self.instructions):
        self.generate_table_entry(f, instruction, idx)

    def generate_table_entry(self, f, instruction, idx):
      method_access = 'Null'
      operand_type = 'OP_None'
      name_access = 'Null'
      separator = ','
      cycles = '0'
      branch_cycles = '0'
      if instruction is not None:
        method_access = instruction.method_name + "'Access"
        operand_type = instruction.operand_type
        name_access = instruction.method_name + "_Name'Access"
        cycles = str(instruction.cycles)
        if instruction.branch_cycles is not None:
          branch_cycles = str(instruction.branch_cycles)
      if idx == InstructionSet.INSTRUCTION_TABLE_SIZE - 1:
        separator = ''
      extended_access = self.extended_table_access(instruction)
      f.write(
        '      (' +
        method_access + ', ' + operand_type + ', ' + name_access + ', ' +
        extended_access + ', ' + cycles + ', ' + branch_cycles + ')' +
        separator + '\n'
      )

    def extended_table_access(self, instruction):
      if instruction is not None and instruction.extended_opcode():
        opcode_str = format(instruction.opcode1, 'x').upper()
        return "Opcodes_" + opcode_str + "'Access"
      else:
        return 'Null'

    def generate_table_footer(self, f):
      f.write(
        '     ) );\n'
      )

  class ExtendedTableGenerator(RootTableGenerator):
    def extended_table_access(self, instruction):
      return 'Null'
