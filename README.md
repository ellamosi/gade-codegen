# libgade-codegen

This is code generation helper tool for my [libgade](https://github.com/ellamosi/libgade) emulator side project.

It takes a list of instructions for a Sharp LR35902 CPU `opcodes.lst` and generates an Ada method for each of them based on the patterns defined in `mktables.spec`.

#### How to run:

Assuming you have Python 2.7 or later installed simply:

`python codegen.py`

The generated files are the following:
- `Gade-Instructions.ads`
  Instruction definitions, one procedure per opcode.
- `Gade-Instructions.adb`
  Instruction implementations, one procedure per opcode.
- `Gade-Instruction_Table.ads`
  Tables of pointers to the generated methods, for instruction decoding/lookup.

#### TODO:
- Explain the simple pattern replacement syntax in here
- Generate replaceable operand labels
