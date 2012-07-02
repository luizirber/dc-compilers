from compiler import Compiler

def main():
    import sys
    filename = sys.argv[1]
    f = open(filename)

    comp = Compiler()
    program = comp.compile(f.read())
    program.genC()

main()
