from Drawing import *

s = Drawing()

s.addNode("a")
s.addNode("b")
s.addNode("c")
s.addNode("d")

s.addLink("a", "c", 1, 6, height=0.40)
s.addLink("c", "d", 2, 9)
s.addLink("b", "d", 3, 10, height=0.40)
s.addLink("a", "b", 4, 5)
s.addLink("b", "c", 7, 9)

s.addTimeLine(ticks=2)

