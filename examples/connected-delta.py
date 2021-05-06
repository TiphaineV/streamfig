from streamfig import *

s = StreamFig()

s.addNode("a")
s.addNode("b")
s.addNode("c")

s.addLink("a", "b", 1, 1)
s.addLink("a", "b", 3, 3)
s.addLink("a", "b", 7, 7)
s.addLink("a", "b", 9, 9)

s.addLink("b", "c", 2, 2)
s.addLink("b", "c", 4, 4)
s.addLink("b", "c", 6, 6)
s.addLink("b", "c", 8, 8)

s.addLink("a", "c", 5, 5)

s.addParameter("D", 2.2)
s.addTimeLine(ticks=2)
s.save("connected-delta.fig")
