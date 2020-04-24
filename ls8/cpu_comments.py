"""CPU functionality."""

import sys

program_file = sys.argv[1]
program = []

LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
SUB = 0b10100001
DIV = 0b10100011
POP = 0b01000110
RET = 0b00010001
PUSH = 0b01000101
CALL = 0b01010000


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # create ram with 256 bytes of memory
        self.ram = [0] * 256
        # and 8 general purpose registers
        self.reg = [0] * 8
        # create a program counter to keep track of the address of current instruction
        self.pc = 0
        self.ir = 0
        self.SP = 7
        # self.reg[7] = 0xF4
        # create instructions (opcode)

        self.instructions = {
            "LDI": 0b10000010,
            "HLT": 0b00000001,
            "PRN": 0b01000111,
            "MUL": 0b10100010,
            "ADD": 0b10100000,
            "SUB": 0b10100001,
            "DIV": 0b10100011,
            "POP": 0b01000110,
            "RET": 0b00010001,
            "PUSH": 0b01000101,
            "CALL": 0b01010000
        }
        self.instructions[LDI] = self.handle_ldi
        # self.instructions[HLT] = self.handle_hlt
        self.instructions[PRN] = self.handle_prn
        self.instructions[MUL] = self.handle_mul
        self.instructions[ADD] = self.handle_add
        self.instructions[SUB] = self.handle_sub
        self.instructions[DIV] = self.handle_div
        self.instructions[POP] = self.handle_pop
        self.instructions[PUSH] = self.handle_push
        self.instructions[CALL] = self.handle_call
        self.instructions[RET] = self.handle_ret

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        with open(program_file) as f:
            for line in f:
                line = line.split('#')
                # print(line)
                line = line[0].strip()
                # print(line)
                if line == '':
                    continue
                line = int(line, 2)
                program.append(line)
        for instruction in program:
            # print(instruction)
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
            self.pc += 3
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
            self.pc += 3
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, mar):  # mar = Memory Address Register
        # should accept the address and return the value stored
        return self.ram[mar]

    def ram_write(self, mdr, mar):  # mdr = Memory Data Register
        # should accept a value to write and the address to write it to
        self.ram[mar] = mdr

    def handle_ldi(self, operand_a=None, operand_b=None):
        self.reg[operand_a] = operand_b
        self.pc += 3

    # def handle_hlt(self, operand_a=None, operand_b=None):
    #     running = False
    #     self.pc += 1

    def handle_prn(self, operand_a=None, operand_b=None):
        print(self.reg[operand_a])
        self.pc += 2

    def handle_mul(self, operand_a=None, operand_b=None):
        self.alu("MUL", operand_a, operand_b)

    def handle_add(self, operand_a=None, operand_b=None):
        self.alu("ADD", operand_a, operand_b)

    def handle_sub(self, operand_a=None, operand_b=None):
        self.alu("SUB", operand_a, operand_b)

    def handle_div(self, operand_a=None, operand_b=None):
        self.alu("DIV", operand_a, operand_b)

    def handle_push(self, operand_a=None, operand_b=None):
        self.reg[self.SP] -= 1
        reg_num = operand_a
        value = self.reg[reg_num]
        address = self.reg[self.SP]
        self.ram[address] = value
        self.pc += 2

    def handle_pop(self, operand_a=None, operand_b=None):
        value = self.ram_read(self.reg[self.SP])
        self.reg[operand_a] = value
        self.reg[self.SP] += 1
        self.pc += 2

    def handle_call(self, operand_a=None, operand_b=None):
        ret_add = self.pc + 2
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = ret_add
        reg_num = self.ram[self.pc+1]
        dest_add = self.reg[reg_num]
        self.pc = dest_add

    def handle_ret(self, operand_a=None, operand_b=None):
        ret_add = self.ram[self.reg[self.SP]]
        self.reg[self.SP] += 1
        self.pc = ret_add

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            # read the memory address thats stored in register ("pc") and store it in 'IR' ("_Instruction Register_")
            ir = self.ram_read(self.pc)
            # using ram_read(), read the bytes at PC+1 and PC+2 from RAM and store them in variables operand_a and operand_b
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # depending on the value of the opcode(instruction), perform the actions needed for the instruction and update the PC accordingly
            # self.trace()

            # self.instructions[ir](operand_a, operand_b)

            if ir == self.instructions["HLT"]:
                running = False
                self.pc += 1

            elif ir == self.instructions["LDI"]:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif ir == self.instructions["PRN"]:
                print(self.reg[operand_a])
                self.pc += 2

            elif ir == self.instructions["MUL"]:
                self.alu("MUL", operand_a, operand_b)
            elif ir == self.instructions["ADD"]:
                self.alu("ADD", operand_a, operand_b)
            elif ir == self.instructions["SUB"]:
                self.alu("SUB", operand_a, operand_b)

            elif ir == self.instructions["PUSH"]:
                # decrement the stack pointer
                self.reg[self.SP] -= 1
                # copy the value from register into memory
                reg_num = self.ram[self.pc+1]
                value = self.reg[reg_num]  # this is what we want to push
                address = self.reg[self.SP]
                # store the value on the stack
                self.ram[address] = value
                self.pc += 2
            elif ir == self.instructions["POP"]:
                # copy the value from the address pointed to by 'SP', to the given register
                value = self.ram_read(self.reg[self.SP])
                self.reg[operand_a] = value
                # increment the stack pointer
                self.reg[self.SP] += 1
                self.pc += 2
            elif ir == self.instructions["CALL"]:
                # set the return address
                ret_add = self.pc + 2
                # decrement the stack pointer
                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = ret_add
                # set the pc to the value in the given register
                reg_num = self.ram[self.pc + 1]
                dest_add = self.reg[reg_num]

                self.pc = dest_add
            elif ir == self.instructions["RET"]:
                # pop the return address from the top of the stack
                ret_add = self.ram[self.reg[self.SP]]
                self.reg[self.SP] += 1
                # set the pc
                self.pc = ret_add
            else:
                print("unknown instruction")
                running = False
