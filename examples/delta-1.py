from streamfig import *

s = StreamFig(alpha=0, omega=10)

s.addNode("a", [(0,4),(6,10)])
s.addNode("b", [(0,2),(3,3),(4,10)])
s.addNode("c", [(4,8)])

s.addLink("a","b",0,0)
s.addLink("a","b",2,2)
s.addLink("a","b",3,3)
s.addLink("a","b",6,6)
s.addLink("a","b",7,8)
s.addLink("b","c",4,8)

s.addTimeLine(ticks=2)
s.addParameter("D", 2)
s.save("delta-1.fig")
