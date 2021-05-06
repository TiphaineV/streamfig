from streamfig import *

s = StreamFig(alpha=0, omega=4)

s.addNode("a",[(0,0)])
s.addNode("b")
s.addNode("c")

s.addLink("b","c",0,4)

s.addTimeLine(ticks=1)

s.save("density-degree-cluster-2.fig")
