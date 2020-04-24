"""CPU functionality."""
import sys

program_file = sys.argv[1]
program = []




class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.ir = 0
        self.SP = 7
        self.reg[7] = 0xF4
                       # LGE
        self.fl = 0b00000000

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
            "JMP": 0b01010100,
            "CMP": 0b10100111,
            "JEQ": 0b01010101,
            "JNE": 0b01010110,
            "PUSH": 0b01000101,
            "CALL": 0b01010000,

        }

    def load(self):
        """Load a program into memory."""
        address = 0
        # program = [
        #     0b10000010, # LDI R0,10
        #     0b00000000,
        #     0b00001010,
        #     0b10000010, # LDI R1,20
        #     0b00000001,
        #     0b00010100,
        #     0b10000010, # LDI R2,TEST1
        #     0b00000010,
        #     0b00010011,
        #     0b10100111, # CMP R0,R1
        #     0b00000000,
        #     0b00000001,
        #     0b01010101, # JEQ R2
        #     0b00000010,
        #     0b10000010, # LDI R3,1
        #     0b00000011,
        #     0b00000001,
        #     0b01000111, # PRN R3
        #     0b00000011,
        #     # TEST1 ,(address 19):
        #     0b10000010, # LDI R2,TEST2
        #     0b00000010,
        #     0b00100000,
        #     0b10100111, # CMP R0,R1
        #     0b00000000,
        #     0b00000001,
        #     0b01010110, # JNE R2
        #     0b00000010,
        #     0b10000010, # LDI R3,2
        #     0b00000011,
        #     0b00000010,
        #     0b01000111, # PRN R3
        #     0b00000011,
        #     # TEST2 ,(address 32):
        #     0b10000010, # LDI R1,10
        #     0b00000001,
        #     0b00001010,
        #     0b10000010, # LDI R2,TEST3
        #     0b00000010,
        #     0b00110000,
        #     0b10100111, # CMP R0,R1
        #     0b00000000,
        #     0b00000001,
        #     0b01010101, # JEQ R2
        #     0b00000010,
        #     0b10000010, # LDI R3,3
        #     0b00000011,
        #     0b00000011,
        #     0b01000111, # PRN R3
        #     0b00000011,
        #     # TEST3 ,(address 48):
        #     0b10000010, # LDI R2,TEST4
        #     0b00000010,
        #     0b00111101,
        #     0b10100111, # CMP R0,R1
        #     0b00000000,
        #     0b00000001,
        #     0b01010110, # JNE R2
        #     0b00000010,
        #     0b10000010, # LDI R3,4
        #     0b00000011,
        #     0b00000100,
        #     0b01000111, # PRN R3
        #     0b00000011,
        #     # TEST4 ,(address 61):
        #     0b10000010, # LDI R3,5
        #     0b00000011,
        #     0b00000101,
        #     0b01000111, # PRN R3
        #     0b00000011,
        #     0b10000010, # LDI R2,TEST5
        #     0b00000010,
        #     0b01001001,
        #     0b01010100, # JMP R2
        #     0b00000010,
        #     0b01000111, # PRN R3
        #     0b00000011,
        #     # TEST5 (address 73):
        #     0b00000001 # HLT
        # ]
        with open(program_file) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()
                if line == '':
                    continue
                line = int(line, 2)
                program.append(line)
        for instruction in program:
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
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
                print("fl",self.fl)
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
                print("fl",self.fl)
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
                print("fl",self.fl)
            else:
                self.fl = 0b00000000
                print("fl",self.fl)
            self.pc += 3
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
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

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def run(self):
        """Run the CPU."""
        running = True
        while running:
            ir = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.trace()
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
                self.reg[self.SP] -= 1
                reg_num = self.ram[self.pc+1]
                value = self.reg[reg_num]
                address = self.reg[self.SP]
                self.ram[address] = value
                self.pc += 2

            elif ir == self.instructions["POP"]:
                value = self.ram_read(self.reg[self.SP])
                self.reg[operand_a] = value
                self.reg[self.SP] += 1
                self.pc += 2

            elif ir == self.instructions["CALL"]:
                ret_add = self.pc + 2
                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = ret_add
                reg_num = self.ram[self.pc + 1]
                dest_add = self.reg[reg_num]
                self.pc = dest_add

            elif ir == self.instructions["RET"]:
                ret_add = self.ram[self.reg[self.SP]]
                self.reg[self.SP] += 1
                self.pc = ret_add
            # ---------------------------------------
            elif ir == self.instructions["CMP"]:
                self.alu("CMP", operand_a, operand_b)

            elif ir == self.instructions["JMP"]:
                self.pc = self.reg[operand_a]

            elif ir == self.instructions["JEQ"]:
                if self.fl == 0b00000001:
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif ir == self.instructions["JNE"]:
                if self.fl != 0b00000001:
                    self.pc == self.reg[operand_a]
                else:
                    self.pc += 2
            else:
                print("unknown instruction")
                running = False
