import sys
# write a python program that runs programs
# parse the command line
program_filename = sys.argv[1]


PRINT_LUIS = 1
HALT = 2
SAVE_REG = 3  # Store a value in a register ( in the LS8 called LDI)
PRINT_REG = 4  # corresponds to PRN in the LS8


# memory = [
#     PRINT_LUIS,
#     SAVE_REG,  # save R0,37 store 37 in R0 the opcode
#     0,  # R0 operand ("argument")
#     37,  # 37 operand
#     PRINT_LUIS,
#     PRINT_REG,  # PRINT_REG R0
#     0,  # R0
#     HALT
# ]
memory = [0] * 256
register = [0] * 8  # like variables R0-R7

# load program into memory
address = 0
with open(program_filename) as f:
    for line in f:
        line = line.split('#')
        line = line[0].strip()
        if line == '':
            continue

        memory[address] = int(line)

        address += 1


pc = 0  # Program Counter, the address of the current instruction
running = True

while running:
    inst = memory[pc]
    inst_len = 1
    if inst == PRINT_LUIS:
        print("Luis")
        pc += 1
    elif inst == SAVE_REG:
        reg_num = memory[pc+1]
        value = memory[pc+2]
        register[reg_num] = value
        pc += 3
    elif inst == PRINT_REG:
        reg_num = memory[pc + 1]
        value = register[reg_num]
        print(value)
        pc += 2
    elif inst == HALT:
        running = False
    else:
        print("unknown instruction")
        running = False
