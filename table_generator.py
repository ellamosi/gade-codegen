from generator import Generator
from instruction_set import InstructionSet
from instruction_tree import InstructionTree

class TableGenerator(Generator):
  HEADER_VAR = 'TABLE_MODULE_HEADER'
  FOOTER_VAR = 'TABLE_MODULE_FOOTER'

  def __init__(self, instructions, variables):
    Generator.__init__(self, variables)
    self.instructions = instructions

  def generate_content(self, f):
    prefixes = self.instructions.instruction_tree.opcode_prefixes()
    # Sort by length, then lexicographically
    # This declares the most deeply nested first, so we can reference
    # them within the less deeply nested
    prefixes.sort(key=lambda item: (-len(item), item))
    for prefix in prefixes:
      subtree = self.instructions.instruction_tree.subtree(prefix)
      PartialTableGenerator(subtree, prefix).generate_table(f)

class NullTableEntry:
  def method_access(self):
    return 'Null'

  def operand_type(self):
    return 'OP_None'

  def name_access(self):
    return 'Null'

  def extended_access(self):
    return 'Null'

  def cycles(self):
    return '0'

  def branch_cycles(self):
    return '0'

class InstructionTableEntry(NullTableEntry):
  def __init__(self, instruction_node):
    self.instruction_node = instruction_node

  def method_access(self):
    return self.instruction_node.method_name + "'Access"

  def operand_type(self):
    return self.instruction_node.operand_type

  def name_access(self):
    return self.instruction_node.method_name + "_Name'Access"

  def cycles(self):
    return str(self.instruction_node.cycles)

  def branch_cycles(self):
    if self.instruction_node.branch_cycles is not None:
      return str(self.instruction_node.branch_cycles)
    else:
      return '0'

class ExtendedTableEntry(NullTableEntry):
  def __init__(self, instruction_node, table_name, opcode_byte):
    self.instruction_node = instruction_node
    self.table_name = table_name
    self.opcode_byte = opcode_byte

  def extended_access(self):
    opcode_prefix = PartialTableGenerator.opcode_byte_str(self.opcode_byte)
    extended_table_prefix = self.table_name + opcode_prefix
    return "Opcodes_" + extended_table_prefix + "'Access"

class PartialTableGenerator:
  def __init__(self, instruction_subtree, table_prefix):
    self.table_nodes = instruction_subtree
    self.table_prefix = table_prefix

  def generate_table(self, f):
    self.generate_table_header(f)
    self.generate_table_entries(f)
    self.generate_table_footer(f)

  def generate_table_header(self, f):
    f.write(
      '  Opcodes_' + self.table_name() +
      ' : aliased constant Instruction_Table_Type :=\n' +
      '     ( 0, (\n'
    )

  def table_name(self):
    if self.table_prefix:
      return PartialTableGenerator.prefix_str(self.table_prefix)
    else:
      return 'Main'

  def generate_table_entries(self, f):
    for opcode_byte, node in enumerate(self.table_nodes):
      self.generate_table_entry(f, node, opcode_byte)

  def generate_table_entry(self, f, node, opcode_byte):
    table_entry = self.get_table_entry_instance(node, opcode_byte)

    separator = ','
    if opcode_byte == InstructionTree.INSTRUCTION_TABLE_SIZE - 1:
      separator = ''

    f.write(
      ''.join([
        '      (',
        table_entry.method_access(), ', ',
        table_entry.operand_type(), ', ' ,
        table_entry.name_access(), ', ',
        table_entry.extended_access(), ', ',
        table_entry.cycles(), ', ',
        table_entry.branch_cycles(), ')',
        separator, '\n'
      ])
    )

  def get_table_entry_instance(self, node, opcode_byte):
    if node is None:
      return NullTableEntry()
    elif node.is_instruction_node():
      return InstructionTableEntry(node)
    else:
      return ExtendedTableEntry(node, self.table_name(), opcode_byte)

  def generate_table_footer(self, f):
    f.write(
      '     ) );\n\n'
    )

  @classmethod
  def prefix_str(klass, prefix):
    prefix_str = ""
    for prefix_byte in prefix:
      prefix_str += PartialTableGenerator.opcode_byte_str(prefix_byte)
    return prefix_str

  @classmethod
  def opcode_byte_str(klass, opcode_byte):
    return format(opcode_byte, '02X')
