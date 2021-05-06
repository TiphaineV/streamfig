from streamfig import *

s = StreamFig(alpha=0, omega=10)

s.addNode("a",[(4,5)])
s.addNode("b",[(4,5),(7,9)])
s.addNode("c",[(4,5),(7,9)])
s.addNode("d",[(4,5),(7,9)])

s.addLink("a", "c", 4, 5, height=0.40, curving=0.3)
s.addLink("c", "d", 4, 5)
s.addLink("c", "d", 7, 9)
s.addLink("b", "d", 4, 5, height=0.40, curving=0.3)
s.addLink("b", "d", 7, 9, height=0.40, curving=0.3)
s.addLink("a", "b", 4, 5)
s.addLink("b", "c", 7, 9)

s.addTimeLine(ticks=2)
s.save("core-2.fig")
