from compiler import Compiler

def main():
    inp = "(-  (+ 5 4) 1)"

    comp = Compiler()
    comp.compile(inp)

main()
