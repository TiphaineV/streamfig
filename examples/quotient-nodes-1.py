from streamfig import *

sg = StreamFig()

sg.addNode("a")
sg.addNode("b")
sg.addNode("c")
sg.addNode("d")

sg.addLink("a", "b", 0, 7)
sg.addLink("b", "c", 1, 2)
sg.addLink("b", "c", 4, 8)
sg.addLink("b", "d", 9, 10)
sg.addLink("c", "d", 0, 5)

# Cluster A
sg.addNodeCluster("a", [(0,3)], color=27, width=100)
sg.addNodeCluster("b", [(7,10)], color=27, width=100)

# Cluster B
sg.addNodeCluster("b", [(2,6)], color=11, width=100)
sg.addNodeCluster("d", [(8,10)], color=11, width=100)

# Cluster C
sg.addNodeCluster("c", [(3,8)], color=14, width=100)
sg.addNodeCluster("d", [(0,5)], color=14, width=100)

sg.addTimeLine(ticks=2)

sg.save("quotient-nodes-1.fig")
