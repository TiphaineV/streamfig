# Dark blue = 10
# Dark green = 12
# Purple = 21
# Pink = 27
from Drawing import *

s = Drawing()

s.addNode("a")
s.addNode("b")
s.addNode("c")
s.addNode("d")

s.addLink("a", "b", 0, 4, color=12)
s.addLink("a", "b", 6, 8, color=12)
s.addLink("b", "c", 2, 4, color=10)
s.addLink("b", "c", 5, 7, color=27)
s.addLink("b", "c", 9, 10, color=27)
s.addLink("b", "d", 3, 5, color=27, height=0.6)
s.addLink("c", "d", 7, 10, color=21)

s.addTimeLine(ticks=2)
