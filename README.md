# gade-codegen

This is code generation helper tool for my [Gade](https://github.com/ellamosi/gade) emulator side project.

It takes a list of instructions for a Sharp LR35902 CPU `opcodes.lst` and generates an Ada method for each of them based on the patterns defined in `mktables.spec`. It should be easy to adapt to generate code for other languages and/or architecture, the similar Zilog Z80 comes to mind.

#### How to run:

Assuming you have Python 3 installed simply:

`python3 codegen.py`

The generated files are the following:
- `gade-dev-cpu-instructions.ads`
  Instruction definitions, one procedure per opcode.
- `gade-dev-cpu-instructions.adb`
  Instruction implementations, one procedure per opcode.
- `gade-dev-cpu-instructions-table.ads`
  Tables of pointers to the generated methods, for instruction decoding/lookup.

## Pattern replacement syntax (`mktables.spec`)

The spec file is tokenized line-by-line with a few simple rules:

- Blank lines and lines starting with `#` are ignored.
- Lines starting with `$` define variables.
- Non-empty lines that do not start with `$` or tab (`\t`) are substitution match expressions.
- Lines starting with a tab belong to the most recent variable or substitution as its content.

### Variable definitions

Single-line variable:

```text
$INSTRUCTION_MODULE_NAME
	Gade.Dev.CPU.Instructions
```

Multi-line variable:

```text
$$SPEC_HEADER
	package $INSTRUCTION_MODULE_NAME$ is
```

Notes:
- `$$NAME` is a multi-line variable.
- `$NAME` is a single-line variable.
- Inside multi-line variable content, `$OTHER_NAME$` references are expanded.

### Substitution definitions

A substitution starts with a regular expression, followed by one or more tab-indented template lines:

```text
(AND|XOR|OR) (A|B|C|D|E|H|L)
	Do_%1 (GB.CPU, GB.CPU.Regs.%2);
```

How matching works:
- The expression is matched against the full instruction mnemonic (`^...$` behavior).
- Parenthesized groups are capture groups.
- `%1`, `%2`, ... in template lines are replaced with captured values.

### Method reference lines

Inside a substitution body, a line that is just `%<mnemonic>` is treated as a call to another generated instruction method:

```text
JP \(HL\)
	%RET
```

This becomes a call to the generated method name for `RET`, with indentation preserved.

### Declarations vs simple body

If a substitution body contains a line equal to `begin` (ignoring leading/trailing spaces), the generator assumes you are writing a full Ada declaration/body block yourself.
If not, it auto-inserts `begin` and indents each body line as statements.
