from instruction import Instruction
from instruction_tree import InstructionTree

class InstructionSet:
  def __init__(self, instructions):
    self.instructions = instructions
    self.instruction_tree = InstructionTree()

    for instruction in instructions:
      self.instruction_tree.insert_instruction(instruction)

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

