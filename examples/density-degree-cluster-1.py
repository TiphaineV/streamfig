from Drawing import *

s = Drawing(alpha=0, omega=4)

s.addNode("a", [(0,2)])
s.addNode("b")
s.addNode("c", [(2,4)])

s.addLink("a","b",0,2)
s.addLink("b","c",2,4)

s.addTimeLine(ticks=1)

