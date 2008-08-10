import sys

from compiler import Compiler

def main():

    if len(sys.argv) != 2:
        print "Usage:"
        print "    main.py input output"
        print "input is the file to be compiled"
        print "output is the file where the generated code will be stored"
        sys.exit(1)
    try:
        fp = open(sys.argv[1], "r")
    except IOError:
        print "Either the file", sys.argv[1], "does not exist or it cannot be read"
        sys.exit(1)
    inp = fp.read() + '\0'
    fp.close()

    comp = Compiler()
    try:
        output = open(sys.argv[2], "w")
    except IOError:
        print "File", sys.args[2], "could not be opened"
        sys.exit(1)
    printWriter = PrintWriter(output)

    try:
        program = comp.compile(inp, printWriter)
    except Exception, e:
        print e

    if program:
        pw = new PW()
        pw.set(printWriter)
        program.genC(pw)
        if ( printWriter.checkError() )
            print "There was an error in the output"

main()
