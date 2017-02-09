import re

class Instruction:
  METHOD_NAME_REPS = {
    '(': 'off_',
    ' ': '_',
    ')': '',
    ',': '_',
    '+': '_'
  }
  METHOD_NAME_REPS_REGEX = re.compile('|'.join(map(re.escape, METHOD_NAME_REPS)))
  OPERAND_TYPES = {
    'nn' : 'OP_Word',
    'n'  : 'OP_Byte',
    'e'  : 'OP_Offset',
    None : 'OP_None'
  }

  def __init__(self, opcode_bytes, operand_type, mnemonic, cycles, branch_cycles):
    self.opcode_bytes = opcode_bytes
    self.operand_type = operand_type
    self.mnemonic = mnemonic
    self.cycles = cycles
    self.branch_cycles = branch_cycles
    self.method_name = self.method_name_from_mnemonic(mnemonic)

  def extended_opcode(self, depth=0):
    len(self.opcode_bytes) - 1 > depth

  def is_instruction_node(self):
    return True

  @classmethod
  def method_name_from_mnemonic(klass, mnemonic):
    return klass.METHOD_NAME_REPS_REGEX.sub(klass.__method_name_rep, mnemonic)

  @classmethod
  def __method_name_rep(klass, match):
    return klass.METHOD_NAME_REPS[match.group()]

  @classmethod
  def load(klass, instruction_str):
    opcode_str = instruction_str[0:10].rstrip()
    mnemonic_str = instruction_str[11:26].rstrip()
    cycles_str = instruction_str[27:-1].rstrip()

    opcode_bytes = klass.__read_opcode(opcode_str)
    operand_type = klass.__read_operand_type(opcode_str)
    cycles, branch_cycles = klass.__read_cycles(cycles_str)

    return Instruction(
      opcode_bytes, operand_type, mnemonic_str, cycles, branch_cycles
    )

  @classmethod
  def __read_opcode(klass, opcode_str):
    opcode_bytes_str = opcode_str.split(' ', 1)[0]
    opcode_bytes = []
    for i in xrange(0, len(opcode_bytes_str), 2):
      byte = int(opcode_bytes_str[i:i+2], 16)
      opcode_bytes.append(byte)
    return opcode_bytes

  @classmethod
  def __read_operand_type(klass, opcode_str):
    content = opcode_str.split()
    operand_type_str = None
    if len(content) > 1:
      operand_type_str = content[1]
    return klass.OPERAND_TYPES[operand_type_str]

  @classmethod
  def __read_cycles(klass, cycles_str):
    content = cycles_str.split('/')
    cycles = int(content[0])
    branch_cycles = None
    if len(content) > 1:
      branch_cycles = int(content[1])
    return cycles, branch_cycles
