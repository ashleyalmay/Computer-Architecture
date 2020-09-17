"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0]* 8
        self.fl = 0
        self.ie = 0
        self.pc = 0
        self.ops = {}
        self.ops[LDI] = self.LDI
        self.ops[PRN] = self.PRN
        self.ops[HLT] = self.HLT
        self.ops[MUL] = self.MUL
        self.ops[POP] = self.POP
        self.ops[PUSH] = self.PUSH
        self.running = False
        self.sp = len(self.ram)


    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self,value,address):
        self.ram[address] = value

    def MUL(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.reg[reg_a] *= self.reg[reg_b]
        self.pc += 3

    def HLT(self):
        self.running = False
        #stop program
        
    def LDI(self):
        address = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.reg[address] = value
        self.pc += 3

    def PRN(self):
        address = self.ram[self.pc + 1]
        print(self.reg[address])
        self.pc += 2

    def PUSH(self):
        self.sp -= 1
        self.ram_write(self.reg[self.ram[self.pc + 1]], self.sp)
        self.pc += 2

    def POP(self):
        self.reg[self.ram[self.pc + 1]] =self.ram_read(self.sp)
        self.sp += 1
        self.pc += 2

    def load(self):
        """Load a program into memory."""

        address = 0

        # if len(sys.argv) != 2:
        #         print("usage: comp.py progname")
        #         sys.exit(1)
        
        try:
            #with open('examples/' + sys.argv[1]) as f:
            with open('ls8/examples/' + 'stack.ls8') as f:
                for line in f:
                    line = line.strip()
                    temp = line.split()
                    if len(temp) == 0:
                            continue
                    if temp[0][0] == '#':
                            continue
                    try:
                        self.ram[address] = int(temp[0], 2)
                    except ValueError:
                        print(f"Invalid number: {temp[0]}")
                        sys.exit(1)
                    address += 1
        except FileNotFoundError:
                print(f"Couldn't open {sys.argv[1]}")
                sys.exit(1)
        if address == 0:
            print("Program was empty!")
            sys.exit(3)

    def alu(self, op, reg_a, reg_b):
        """ALU operations. NOT USING RIP"""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
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
        self.running = True

        while self.running:
            ir = self.ram_read(self.pc)
            op_handler = self.ops[ir]
            op_handler()




