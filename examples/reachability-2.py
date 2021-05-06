from streamfig import *

sg = StreamFig()

sg.addNode("u")
sg.addNode("v")
sg.addNode("w")

sg.addLink("u", "v", 1,3)
sg.addLink("v", "w", 4,6)
sg.addLink("u", "v", 7,9)

sg.addNodeCluster("u", [(0,3)], color=13)
sg.addNodeCluster("v", [(0,6)], color=28)
sg.addNodeCluster("w", [(0,6)], color=11)

sg.addTimeLine(ticks=2)
sg.save("reachability-2.fig")
