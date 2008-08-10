from compiler import Compiler

def main():
    inp = "(-  (+ 5 4) 1)"

    comp = Compiler()
    print "Resultado:", comp.compile(inp)

main()
