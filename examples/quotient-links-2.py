# Dark blue = 10
# Dark green = 12
# Purple = 21
# Pink = 27
from Drawing import *

s = Drawing()

s.addNode("A", color=12)
s.addNode("B", color=10)
s.addNode("C", color=27)
s.addNode("D", color=21)

s.addLink("A", "B", 2, 4)
s.addLink("A", "C", 3, 4, height=0.4)
s.addLink("B", "C", 3, 4)
s.addLink("A", "C", 6, 7)
s.addLink("C", "D", 9, 10)

s.addTimeLine(ticks=2)
