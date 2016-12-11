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
  EXTENDED_OPCODES = [0xCB]

  def __init__(self, opcode1, opcode2, operand_type, mnemonic, cycles):
    self.opcode1 = opcode1
    self.opcode2 = opcode2
    self.operand_type = operand_type
    self.mnemonic = mnemonic
    self.cycles = cycles
    self.method_name = self.method_name_from_mnemonic(mnemonic)

  def extended_opcode(self):
    return self.opcode1 in self.EXTENDED_OPCODES

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

    opcode1, opcode2 = klass.__read_opcode(opcode_str)
    operand_type = klass.__read_operand_type(opcode_str)

    return Instruction(opcode1, opcode2, operand_type, mnemonic_str, cycles_str)

  @classmethod
  def __read_opcode(klass, opcode_str):
    opcode1_str = opcode_str[0:2]
    opcode2_str = opcode_str[2:4]
    opcode1 = int(opcode1_str, 16)
    opcode2 = None
    if opcode2_str != '' and opcode2_str[0] != ' ':
      opcode2 = int(opcode2_str, 16)
    if ((opcode1 not in klass.EXTENDED_OPCODES and opcode2 is not None) or
        (opcode1 in     klass.EXTENDED_OPCODES and opcode2 is     None)):
      raise Exception("Opcode '" + opcode_str + "' is not valid")
    return (opcode1, opcode2)

  @classmethod
  def __read_operand_type(klass, opcode_str):
    content = opcode_str.split()
    operand_type_str = None
    if len(content) > 1:
      operand_type_str = content[1]
    return klass.OPERAND_TYPES[operand_type_str]
