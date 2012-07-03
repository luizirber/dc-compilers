import sys
from os.path import dirname, abspath, join
sys.path.append(dirname(dirname(abspath(__file__))))
print sys.path

from comp01.compiler import Compiler

def testComp01():
    inp = "(-  (+ 5 4) 1)"
    comp = Compiler()
    comp.compile(inp)
