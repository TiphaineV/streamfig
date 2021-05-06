from streamfig import *

s = StreamFig()

s.addColor("tPink", "#FF9896") # 255, 152,150

s.addNode("a")
s.addNode("b", [(0,4), (5,10)])
s.addNode("c", [(4,9)])
s.addNode("d", [(1,3)])

s.addLink("a", "b", 1, 3)
s.addLink("b", "d", 2, 3)
s.addLink("a", "c", 4.5, 7.5, height=0.40)
s.addLink("a", "b", 7, 8)
s.addLink("b", "c", 6, 9)

s.addTimeNodeMark(1, "d",color="tPink",width=4)
s.addTimeNodeMark(9, "c",color="tPink",width=4)
s.addPath([(2,"d","b"), (3,"b","a"), (7.5, "a", "b"), (8, "b", "c")], 2, 8, color=11, width=6)

s.addTimeLine(ticks=2)

s.save("paths-2.fig")
