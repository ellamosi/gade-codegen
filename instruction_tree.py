class InstructionTree:
  INSTRUCTION_TABLE_SIZE = 256

  def __init__(self):
    self.opcode_nodes = [None] * self.INSTRUCTION_TABLE_SIZE

  def __getitem__(self, key):
    return self.opcode_nodes[key]

  def __len__(self):
    return self.opcode_nodes.len

  def insert_instruction(self, instruction):
    node = self
    for opcode in instruction.opcode_bytes[0:-1]:
      node = node.next_node(opcode)
    node.set_opcode(instruction.opcode_bytes[-1], instruction)

  def next_node(self, opcode):
    next_node = self.opcode_nodes[opcode]
    if next_node is None:
      next_node = InstructionTree()
      self.opcode_nodes[opcode] = next_node
    return next_node

  def set_opcode(self, opcode, instruction):
    self.opcode_nodes[opcode] = instruction

  def subtree(self, prefix):
    node = self
    for opcode in prefix:
      node = node.opcode_nodes[opcode]
    return node

  def is_instruction_node(self):
    return False

  def opcode_prefixes(self):
    prefixes = []
    self.opcode_prefixes_rec(prefixes, [])
    return prefixes

  def opcode_prefixes_rec(self, prefixes, current_prefix):
    prefixes.append(list(current_prefix))
    for opcode, node in enumerate(self.opcode_nodes):
      if not node is None and not node.is_instruction_node():
        current_prefix.append(opcode)
        node.opcode_prefixes_rec(prefixes, current_prefix)
        current_prefix.pop()
