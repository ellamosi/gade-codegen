from instruction import Instruction

class InstructionSet:
  INSTRUCTION_TABLE_SIZE = 256

  def __init__(self, instructions):
    self.instructions = instructions
    self.main_instructions = [None] * self.INSTRUCTION_TABLE_SIZE
    self.cb_instructions = [None] * self.INSTRUCTION_TABLE_SIZE
    for instruction in instructions:
      if not instruction.extended_opcode():
        self.main_instructions[instruction.opcode1] = instruction
      else:
        self.cb_instructions[instruction.opcode2] = instruction

  def __getitem__(self, key):
    return self.instructions[key]

  def __len__(self):
    return self.instructions.len

  @classmethod
  def load(klass, file_name):
    f = open(file_name, 'r')
    instructions = []
    for line in f:
      instruction = Instruction.load(line)
      instructions.append(instruction)
    f.close()
    return InstructionSet(instructions)
