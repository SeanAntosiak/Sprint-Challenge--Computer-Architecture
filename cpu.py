"""CPU functionality."""

import sys

MUL = 0b10100010
ADD = 0b10100000
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
PSH = 0b01000101
POP = 0b01000110
CAL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        path = sys.argv[1]

        file = open(path)
        program_file = file.readlines()
        program = []
        for line in program_file:
            if line[0] == '#' or line[0] == '\n':
                pass
            else:
                program.append(int(line[:8], 2))

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, opa, opb):
        """ALU operations."""

        if op == "ADD":
            self.reg[opa] += self.reg[opb]

        elif op == "MUL":
            self.reg[opa] *= self.reg[opb]

        elif op == 'EQ':
            if opa == opb:
                return(0b00000001)
            elif opa < opb:
                return(0b00000100)
            elif opa > opb:
                return(0b00000010)

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(loc):
        return self.ram[loc]

    def ram_write(loc, val):
        self.ram[loc] = val

    def run(self):
        """Run the CPU."""
        pc = self.pc
        SP = 0xF3
        FL = 0b00000000

        while True:
            IR = self.ram[pc]
            if IR == HLT:
                break
            elif IR == LDI:
                opa = self.ram[pc + 1]
                opb = self.ram[pc + 2]
                pc += 3
                self.reg[opa] = opb

            elif IR == PRN:
                reg_loc = self.ram[pc + 1]
                print(self.reg[reg_loc])
                pc += 2

            elif IR == ADD:
                opa = self.ram[pc + 1]
                opb = self.ram[pc + 2]
                self.alu('ADD', opa, opb)
                pc += 3

            elif IR == MUL:
                opa = self.ram[pc + 1]
                opb = self.ram[pc + 2]
                self.alu('MUL', opa, opb)
                pc += 3

            elif IR == PSH:
                opa = self.ram[pc + 1]
                self.ram[SP] = self.reg[opa]
                SP -= 1
                pc += 2

            elif IR == POP:
                opa = self.ram[pc + 1]
                SP += 1
                self.reg[opa] = self.ram[SP]
                pc += 2

            elif IR == CAL:
                opa = self.ram[pc + 1]
                self.ram[SP] = pc + 2
                SP -= 1
                pc = self.reg[opa]

            elif IR == RET:
                SP += 1
                pc = self.ram[SP]

            elif IR == CMP:
                opa = self.ram[pc + 1]
                opb = self.ram[pc + 2]
                rega = self.reg[opa]
                regb = self.reg[opb]
                FL = self.alu('EQ', rega, regb)
                pc += 3

            elif IR == JMP:
                opa = self.ram[pc + 1]
                pc = self.reg[opa]

            elif IR == JEQ:
                opa = self.ram[pc + 1]
                if FL == 1:
                    pc = self.reg[opa]
                else:
                    pc += 2

            elif IR == JNE:
                opa = self.ram[pc + 1]
                if FL != 1:
                    pc = self.reg[opa]
                else:
                    pc += 2
