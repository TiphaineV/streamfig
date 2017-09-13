from Drawing import *

#s = Drawing(alpha=0, omega=5)
s = Drawing(alpha=1, omega=9)

s.addNode("a", [(1,9)])
s.addNode("b", [(1,9)])
s.addNode("c", [(3,9)])

s.addLink("a","b",1,4)
s.addLink("a","b",5,9)
s.addLink("b","c",3,9)

#s.addTimeLine(ticks=1)
#s.addTimeLine(ticks=5, marks=[(2,2)])
s.addTimeLine(ticks=2)
#s.addParameter("D", 1)

