from compiler import Compiler

def main():
    inp = "a = 1 b = 3 : (- (+ a 4) b)"

    comp = Compiler()
    program = comp.compile(inp)
    program.genC()

main()
