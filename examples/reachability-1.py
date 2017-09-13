from Drawing import *

sg = Drawing()

sg.addNode("u")
sg.addNode("v")
sg.addNode("w")

sg.addLink("u", "v", 2,6)
sg.addLink("v", "w", 4,8)

sg.addNodeCluster("u", [(0,6)], color=13)
sg.addNodeCluster("v", [(0,6)], color=28)
sg.addNodeCluster("w", [(0,6)], color=11)

sg.addTimeLine(ticks=2)
