from compiler import Compiler

def main():
    inp = "(-  (+ 5 4) 1)"

    comp = Compiler()
    expr = comp.compile(inp)
    expr.genC()
    print

main()
