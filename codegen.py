#!/usr/bin/env python
from instruction_set import InstructionSet
from tokenizer import Tokenizer
from body_generator import BodyGenerator
from spec_generator import SpecGenerator
from table_generator import TableGenerator

def codegen():
  instructions = InstructionSet.load('opcodes.lst')
  variables, substitutions = Tokenizer.load('mktables.spec')

  BodyGenerator(instructions, substitutions, variables).generate('Gade-Dev-CPU-Instructions.adb')
  SpecGenerator(instructions, variables).generate('Gade-Dev-CPU-Instructions.ads')
  TableGenerator(instructions, variables).generate('Gade-Dev-CPU-Instructions-Table.ads')

if __name__ == '__main__':
  codegen()
