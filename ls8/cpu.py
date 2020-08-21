"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.ir = 0
        self.SP = 7
        self.reg[7] = 244
        self.fl = [False] * 8
        self.E = 0
        self.LDI = 0b10000010
        self.PRN = 0b01000111
        self.HLT = 0b00000001
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110
        self.CALL = 0b01010000
        self.RET = 0b00010001
        self.ADD = 0b10100000
        self.CMP = 0b10100111
        self.JMP = 0b01010100
        self.JEQ = 0b01010101
        self.JNE = 0b01010110

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""
        address = 0
        try:
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    n = comment_split[0].strip()

                    if n == '':
                        continue

                    val = int(n, 2)
                    # store val in memory
                    self.ram[address] = val

                    address += 1

                    # print(f"{x:08b}: {x:d}")

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {filename} not found")
            sys.exit(2)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            print("adding", reg_a)
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "CMP":
            equal = self.fl[7]
            greater_than = self.fl[6]
            less_than = self.fl[5]
            if self.reg[reg_a] == self.reg[reg_b]:
                equal = True
                greater_than = False
                less_than = False
            elif self.reg[reg_a] > self.reg[reg_b]:
                equal = False
                greater_than = True
                less_than = False
            else:
                equal = False
                greater_than = False
                less_than = True

            self.fl[5:] = [less_than, greater_than, equal]
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

    def run(self):
        """Run the CPU."""
        self.pc = 0
        running = True

        while running:
            self.ir = self.ram_read(self.pc)

            if self.ir == self.LDI:
                reg_addr = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)
                self.reg[reg_addr] = value
                self.pc += 3

            elif self.ir == self.PRN:
                reg_addr = self.ram_read(self.pc + 1)
                value = self.reg[reg_addr]
                print(value)
                self.pc += 2

            elif self.ir == self.MUL:
                reg_addr_a = self.ram_read(self.pc + 1)
                reg_addr_b = self.ram_read(self.pc + 2)
                val1 = self.reg[reg_addr_a]
                val2 = self.reg[reg_addr_b]
                value = val1 * val2
                print(value)
                self.pc += 2

            elif self.ir == self.PUSH:
                reg_addr = self.ram_read(self.pc + 1)
                val = self.reg[reg_addr]
                self.SP -= 1
                self.ram[self.SP] = val
                self.pc += 2

            elif self.ir == self.POP:
                reg_addr = self.ram_read(self.pc + 1)
                val = self.ram_read(self.SP)
                self.reg[reg_addr] = val
                self.ram[self.SP] = 0
                self.SP += 1
                self.pc += 2

            elif self.ir == self.CALL:
                self.reg[self.SP] -= 1
                self.ram[self.reg[self.SP]] = self.pc + 2
                reg = self.ram[self.pc + 1]
                self.pc = self.reg[reg]
                

            elif self.ir == self.RET:
                self.pc = self.ram[self.reg[self.SP]]
                self.reg[self.SP] += 1

            elif self.ir == self.ADD:
                val = self.reg[self.ram[self.pc + 1]] + self.reg[self.ram[self.pc + 2]]
                self.reg[self.ram[self.pc + 1]] = val
                self.pc += 3

            elif self.ir == self.CMP:
                first_reg = self.ram[self.pc + 1]
                sec_reg = self.ram[self.pc + 2]
                self.alu('CMP', first_reg, sec_reg)
                self.pc += 3

            elif self.ir == self.JMP:
                reg_num = self.ram[self.pc + 1]
                self.pc = self.reg[reg_num]

            elif self.ir == self.JEQ:
                reg_to_jump = self.ram[self.pc + 1]
                addr_to_jump = self.reg[reg_to_jump]
                if self.fl[7] is True:
                    self.pc = addr_to_jump
                else:
                    self.pc += 2

            elif self.ir == self.JNE:
                reg_to_jump = self.ram[self.pc + 1]
                addr_to_jump = self.reg[reg_to_jump]
                if self.fl[7] is False:
                    self.pc = addr_to_jump
                else:
                    self.pc += 2

            elif self.ir == self.HLT:
                running = False

            else:
                running = False
