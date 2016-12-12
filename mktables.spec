#
# libgade opcode code generation for Ada
#

$INSTRUCTION_MODULE_NAME
	Gade.Instructions

$$SPEC_HEADER
	with Gade.CPU; use Gade.CPU;
	with Gade.GB;  use Gade.GB;
	
	package $INSTRUCTION_MODULE_NAME$ is
	

$$SPEC_FOOTER
	end $INSTRUCTION_MODULE_NAME$;

$$BODY_HEADER
	with Gade.CPU.Arithmetic; use Gade.CPU.Arithmetic;
	with Gade.CPU.Logic;      use Gade.CPU.Logic;
	with Gade.CPU.Bitwise;    use Gade.CPU.Bitwise;
	with Gade.Basic_Types;    use Gade.Basic_Types;
	
	package body $INSTRUCTION_MODULE_NAME$ is
	

$$BODY_FOOTER
	end $INSTRUCTION_MODULE_NAME$;

$TABLE_MODULE_NAME
	Gade.Instruction_Table

$$TABLE_MODULE_HEADER
	with Gade.CPU;          use Gade.CPU;
	with Gade.Basic_Types;  use Gade.Basic_Types;
	with Gade.Instructions; use Gade.Instructions;
	with Gade.GB;           use Gade.GB;
	
	package $TABLE_MODULE_NAME$ is
	
	  type Operand_Type is (OP_None, OP_Byte, OP_Word, OP_Offset);
	
	  type Instruction_Access is access procedure
	    (GB : in out GB_Context);
	
	  type Instruction_Table_Type;
	
	  type Instruction_Entry is record
	    Method         : Instruction_Access;
	    Operand        : Operand_Type;
	    Name           : access constant String;
	    Extended_Table : access constant Instruction_Table_Type;
	    Cycles         : Natural;
	    Jump_Cycles    : Natural;
	  end record;
	
	  type Instruction_Array is array
	    (Basic_Types.Byte'Range) of Instruction_Entry;
	
	  type Instruction_Table_Type is record
	    Code_Offset : Natural;
	    Entries     : aliased Instruction_Array;
	  end record;
	
	  Opcodes_Main : aliased constant Instruction_Table_Type;
	  Opcodes_CB   : aliased constant Instruction_Table_Type;
	
	private
	

$$TABLE_MODULE_FOOTER
	end $TABLE_MODULE_NAME$;

#
# Add / Sub / Adc / Sbc
#
(ADD|ADC) A,(A|B|C|D|E|H|L)
	Do_Add(GB.CPU, GB.CPU.Regs.%2, GB.CPU.Regs.A, %1_Carry);

(SUB|SBC) A,(A|B|C|D|E|H|L)
	Do_Sub(GB.CPU, GB.CPU.Regs.%2, GB.CPU.Regs.A, %1_Carry);

(ADD|ADC) A,\(HL\)
	Do_Add(GB.CPU, Read_Byte(GB, GB.CPU.Regs.HL), GB.CPU.Regs.A, %1_Carry);

(SUB|SBC) A,\(HL\)
	Do_Sub(GB.CPU, Read_Byte(GB, GB.CPU.Regs.HL), GB.CPU.Regs.A, %1_Carry);

(ADD|ADC) A,n
	Do_Add(GB.CPU, Read_Byte(GB, GB.CPU.PC), GB.CPU.Regs.A, %1_Carry);
	GB.CPU.PC := GB.CPU.PC + 1;

(SUB|SBC) A,n
	Do_Sub(GB.CPU, Read_Byte(GB, GB.CPU.PC), GB.CPU.Regs.A, %1_Carry);
	GB.CPU.PC := GB.CPU.PC + 1;

ADD SP,n
	  n : Byte;
	begin
	  n := Read_Byte(GB, GB.CPU.PC);
	  GB.CPU.PC := GB.CPU.PC + 1;
	  Do_Add(GB.CPU, GB.CPU.Regs.SP, n);

ADD HL,(SP|BC|DE|HL)
	Do_Add(GB.CPU, GB.CPU.Regs.%1, GB.CPU.Regs.HL);

#
# Logic operations
#
(AND|XOR|OR) \(HL\)
	Do_%1(GB.CPU, Read_Byte(GB, GB.CPU.Regs.HL));

(AND|XOR|OR) (A|B|C|D|E|H|L)
	Do_%1(GB.CPU, GB.CPU.Regs.%2);

(AND|XOR|OR) n
	Do_%1(GB.CPU, Read_Byte(GB, GB.CPU.PC));
	GB.CPU.PC := GB.CPU.PC + 1;

#
# Bit operations
#
BIT ([0-7]),(A|B|C|D|E|H|L)
	Do_Bit(GB.CPU, %1, GB.CPU.Regs.%2);

BIT ([0-7]),\(HL\)
	Do_Bit(GB.CPU, %1, Read_Byte(GB, GB.CPU.Regs.HL));

(SET|RES) ([0-7]),(A|B|C|D|E|H|L)
	Do_Set_Bit(GB.CPU, SR_%1, %2, GB.CPU.Regs.%3, GB.CPU.Regs.%3);

(SET|RES) ([0-7]),\(HL\)
	  Value : Byte;
	begin
	  Value := Read_Byte(GB, GB.CPU.Regs.HL);
	  Do_Set_Bit(GB.CPU, SR_%1, %2, Value, Value);
	  Write_Byte(GB, GB.CPU.Regs.HL, Value);

#
# Jumps and calls
#
CALL (C|NZ|NC|Z),?\(nn\)
	  Addr : constant Word := Read_Word(GB, GB.CPU.PC);
	begin
	  GB.CPU.PC := GB.CPU.PC + 2;
	  if Check_Condition(GB.CPU, C_%1) then
	    Push(GB, GB.CPU.PC);
	    GB.CPU.PC := Addr;
	  end if;

CALL ?\(nn\)
	Push(GB, GB.CPU.PC + 2);
	GB.CPU.PC := Read_Word(GB, GB.CPU.PC);

JP \(HL\)
	GB.CPU.PC := GB.CPU.Regs.HL;

JP \(nn\)
	GB.CPU.PC := Read_Word(GB, GB.CPU.PC);

JP (C|NZ|NC|Z),?\(nn\)
	  Addr : constant Word := Read_Word(GB, GB.CPU.PC);
	begin
	  GB.CPU.PC := GB.CPU.PC + 2;
	  if Check_Condition(GB.CPU, C_%1) then
	  	GB.CPU.PC := Addr;
	  end if;

JR \(PC\+e\)
	  Offset : constant Byte := Read_Byte(GB, GB.CPU.PC);
	begin
	  GB.CPU.PC := GB.CPU.PC + 1;
	  Add_Offset(GB.CPU, GB.CPU.PC, Offset, False);

JR (C|NZ|NC|Z),?\(PC\+e\)
	  Offset : constant Byte := Read_Byte(GB, GB.CPU.PC);
	begin
	  GB.CPU.PC := GB.CPU.PC + 1;
	  if Check_Condition(GB.CPU, C_%1) then
	  	Add_Offset(GB.CPU, GB.CPU.PC, Offset, False);
	  end if;

RETI
	Pop(GB, GB.CPU.PC);
	EI(GB);

RET (C|NZ|NC|Z)
	if Check_Condition(GB.CPU, C_%1) then
	  Pop(GB, GB.CPU.PC);
	end if;

RET
	Pop(GB, GB.CPU.PC);

RST (0|8|10|18|20|28|30|38)H
	Push(GB, GB.CPU.PC);
	GB.CPU.PC := 16#%1#;

#
# Misc
#
CCF
	Reset(GB.CPU.Regs.F.N);
	Reset(GB.CPU.Regs.F.H);
	Set_Value(GB.CPU.Regs.F.C, not Is_Set(GB.CPU.Regs.F.C));

SCF
	Reset(GB.CPU.Regs.F.N);
	Reset(GB.CPU.Regs.F.H);
	Set(GB.CPU.Regs.F.C);

CPL
	GB.CPU.Regs.A := not GB.CPU.Regs.A;
	Set(GB.CPU.Regs.F.H);
	Set(GB.CPU.Regs.F.N);

DAA
	Do_Daa(GB.CPU);

STOP
	GB.CPU.Halted := True;
	raise Program_Error;

HALT
	GB.CPU.Halted := True;
	raise Program_Error;

#
# Compare
#
CP \(HL\)
	  Value, Dummy : Byte;
	begin
	  Value := Read_Byte(GB, GB.CPU.Regs.HL);
	  Do_Sub(GB.CPU, Value, Dummy, SUB_Carry);

CP (A|B|C|D|E|H|L)
	  Dummy : Byte;
	begin
	  Do_Sub(GB.CPU, GB.CPU.Regs.%1, Dummy, SUB_Carry);

CP n
	  Value, Dummy : Byte;
	begin
	  Value := Read_Byte(GB, GB.CPU.PC);
	  GB.CPU.PC := GB.CPU.PC + 1;
	  Do_Sub(GB.CPU, Value, Dummy, SUB_Carry);

#
# INC and DEC
#
(INC|DEC) \(HL\)
	  Value : Byte;
	begin
	  Value := Read_Byte(GB, GB.CPU.Regs.HL);
	  Do_Inc_Dec(GB.CPU, %1, Value, Value);
	  Write_Byte(GB, GB.CPU.Regs.HL, Value);

(INC|DEC) (A|B|C|D|E|H|L)
	Do_Inc_Dec(GB.CPU, %1, GB.CPU.Regs.%2, GB.CPU.Regs.%2);

INC (BC|DE|HL|SP)
	GB.CPU.Regs.%1 := GB.CPU.Regs.%1 + 1;

DEC (BC|DE|HL|SP)
	GB.CPU.Regs.%1 := GB.CPU.Regs.%1 - 1;

#
# Interrupts
#
(EI|DI)
	GB.CPU.IFF := IE_%1;

#
# Loads
#
LD \((BC|DE|HL)\),A
	Write_Byte(GB, GB.CPU.Regs.%1, GB.CPU.Regs.A);

LD \(HL\),(B|C|D|E|H|L)
	Write_Byte(GB, GB.CPU.Regs.HL, GB.CPU.Regs.%1);

LD \(HL\),n
	  Value : Byte;
	begin
	  Value := Read_Byte(GB, GB.CPU.PC);
	  GB.CPU.PC := GB.CPU.PC + 1;
	  Write_Byte(GB, GB.CPU.Regs.HL, Value);

LD \(n\),A
	raise Program_Error;

LD (BC|DE|HL|SP),(BC|DE|HL|SP)
	GB.CPU.Regs.%1 := GB.CPU.Regs.%2;

LD \(nn\),(BC|DE|HL|SP)
	  Addr : Word;
	begin
	  Addr := Read_Word(GB, GB.CPU.PC);
	  GB.CPU.PC := GB.CPU.PC + 2;
	  Write_Word(GB, Addr, GB.CPU.Regs.%1);

LD A,\((BC|DE)\)
	GB.CPU.Regs.A := Read_Byte(GB, GB.CPU.Regs.%1);

LD (A|B|C|D|E|H|L),\(HL\)
	GB.CPU.Regs.%1 := Read_Byte(GB, GB.CPU.Regs.HL);

LD (A|B|C|D|E|H|L),\(nn\)
	  Addr : Word;
	begin
	  Addr := Read_Word(GB, GB.CPU.PC);
	  GB.CPU.PC := GB.CPU.PC + 2;
	  GB.CPU.Regs.%1 := Read_Byte(GB, Addr);

LD (A|B|C|D|E|H|L),(A|B|C|D|E|H|L)
	GB.CPU.Regs.%1 := GB.CPU.Regs.%2;

LD A,(I|R)
	raise Program_Error;

LD (I|R),A
	raise Program_Error;

LD (A|B|C|D|E|H|L),n
	GB.CPU.Regs.%1 := Read_Byte(GB, GB.CPU.PC);
	GB.CPU.PC := GB.CPU.PC + 1;

LD (BC|DE|HL|SP),\(nn\)
	raise Program_Error;

LD (BC|DE|HL|SP),nn
	GB.CPU.Regs.%1 := Read_Word(GB, GB.CPU.PC);
	GB.CPU.PC := GB.CPU.PC + 2;

LD \(nn\),A
	  Addr : Word;
	begin
	  Addr := Read_Word(GB, GB.CPU.PC);
	  GB.CPU.PC := GB.CPU.PC + 2;
	  Write_Byte(GB, Addr, GB.CPU.Regs.A);

LD \(C\),A
	Write_Byte(GB, 16#FF00# + Word(GB.CPU.Regs.C), GB.CPU.Regs.A);

LD A,\(C\)
	GB.CPU.Regs.A := Read_Byte(GB, 16#FF00# + Word(GB.CPU.Regs.C));

LDHL SP,n
	  n    : Byte;
	  Addr : Word;
	begin
	  n := Read_Byte(GB, GB.CPU.PC);
	  GB.CPU.PC := GB.CPU.PC + 1;
	  Addr := GB.CPU.Regs.SP;
	  Do_Add(GB.CPU, Addr, n);
	  GB.CPU.Regs.HL := Addr;

LDH A,\(n\)
	  n    : Byte;
	  Addr : Word;
	begin
	  n := Read_Byte(GB, GB.CPU.PC);
	  GB.CPU.PC := GB.CPU.PC + 1;
	  Addr := 16#FF00# + Word(n);
	  GB.CPU.Regs.A := Read_Byte(GB, Addr);

LDH \(n\),A
	  n    : Byte;
	  Addr : Word;
	begin
	  n := Read_Byte(GB, GB.CPU.PC);
	  GB.CPU.PC := GB.CPU.PC + 1;
	  Addr := 16#FF00# + Word(n);
	  Write_Byte(GB, Addr, GB.CPU.Regs.A);

LDIR
	raise Program_Error;

LDI
	raise Program_Error;

LDI A,\(HL\)
	%LD A,(HL)
	%INC HL

LDI \(HL\),A
	%LD (HL),A
	%INC HL

LDDR
	raise Program_Error;

LDD
	raise Program_Error;

LDD A,\(HL\)
	%LD A,(HL)
	%DEC HL

LDD \(HL\),A
	%LD (HL),A
	%DEC HL

NOP
	null;

POP (BC|DE|HL)
	Pop(GB, GB.CPU.Regs.%1);

POP AF
	Pop(GB, GB.CPU.Regs.AF);
	GB.CPU.Regs.AF := GB.CPU.Regs.AF and 16#FFF0#;

PUSH (AF|BC|DE|HL)
	Push(GB, GB.CPU.Regs.%1);

#
# Rotate & shift
#
(RLC|RRC|RL|RR) \(HL\)
	  Value : Byte;
	begin
	  Value := Read_Byte(GB, GB.CPU.Regs.HL);
	  Do_%1(GB.CPU, True, Value);
	  Write_Byte(GB, GB.CPU.Regs.HL, Value);

(RLC|RRC|RL) (A|B|C|D|E|H|L)
	Do_%1(GB.CPU, True, GB.CPU.Regs.%2);

RR (A|B|C|D|E|H|L)
	Do_RR(GB.CPU, True, GB.CPU.Regs.%1);

RRA
	Do_RR(GB.CPU, False, GB.CPU.Regs.A);

(RL|RLC|RRC)A
	Do_%1(GB.CPU, False, GB.CPU.Regs.A);

(SL|SR)(L|A) \(HL\)
	  Value : Byte;
	begin
	  Value := Read_Byte(GB, GB.CPU.Regs.HL);
	  Do_%1(GB.CPU, S_%2, Value);
	  Write_Byte(GB, GB.CPU.Regs.HL, Value);

(SL|SR)(L|A) (A|B|C|D|E|H|L)
	Do_%1(GB.CPU, S_%2, GB.CPU.Regs.%3);

SWAP (A|B|C|D|E|H|L)
	Do_Swap(GB.CPU, GB.CPU.Regs.%1);

SWAP \(HL\)
	  Value : Byte;
	begin
	  Value := Read_Byte(GB, GB.CPU.Regs.HL);
	  Do_Swap(GB.CPU, Value);
	  Write_Byte(GB, GB.CPU.Regs.HL, Value);
