from Drawing import *

s = Drawing()

s.addNode("a")
s.addNode("b")
s.addNode("c", [(0,5)])

s.addLink("a","b", 5, 10)
s.addLink("b","c", 0, 5)

s.addTimeLine(ticks=2)
