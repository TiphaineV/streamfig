from streamfig import *

s = StreamFig(alpha=0, omega=13, discrete=1)

s.addNode("a")
s.addNode("b", [(1,5), (7,13)])
s.addNode("c", [(5,12)])
s.addNode("d", [(1,3)])

s.addLink("a", "b", 1, 4)
s.addLink("a", "b", 9, 10)
s.addLink("a", "c", 6, 9, curving=0.3)
s.addLink("b", "d", 2, 3, curving=0.2)
s.addLink("b", "c", 8, 12)

s.addTimeLine(ticks=2)

s.save("discrete.fig")
