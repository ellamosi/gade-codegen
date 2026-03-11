#!/usr/bin/env python
from instruction_set import InstructionSet
from tokenizer import Tokenizer
from body_generator import BodyGenerator
from spec_generator import SpecGenerator
from table_generator import TableGenerator

def codegen():
  instructions = InstructionSet.load('opcodes.lst')
  variables, substitutions = Tokenizer.load('mktables.spec')

  BodyGenerator(instructions, substitutions, variables).generate('gade-dev-cpu-instructions.adb')
  SpecGenerator(instructions, variables).generate('gade-dev-cpu-instructions.ads')
  TableGenerator(instructions, variables).generate('gade-dev-cpu-instructions-table.ads')

if __name__ == '__main__':
  codegen()
