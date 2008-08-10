import sys

from compiler import Compiler

def main():

    if len(sys.argv) != 2:
        print "Use only one parameter, the file to be compiled"
        sys.exit(1)
    try:
        fp = open(sys.argv[1])
    except IOError:
        print "Either the file", sys.argv[1], "does not exist or it cannot be read"
        sys.exit(1)
    inp = fp.read() + '\0'
    fp.close()

    comp = Compiler()

    program = comp.compile(inp)
    program.genC()

main()
