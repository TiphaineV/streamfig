from streamfig import *

sg = StreamFig()

sg.addNode("a")
sg.addNode("b")
sg.addNode("c")
sg.addNode("d")

sg.addLink("a", "b", 1,2)
sg.addLink("b", "c", 3,4)
sg.addLink("c", "d", 5,6)
sg.addLink("a", "d", 7,8)
sg.addLink("b", "d", 9,10)

sg.addNodeIntervalMark("a", "d")
sg.addTimeIntervalMark(3,8)

sg.addNodeCluster("a", [(1.9,2.1), (6.9, 7.1)], color=11)
sg.addNodeCluster("b", [(2,3), (8.9, 9.1)], color=11)
sg.addNodeCluster("c", [(2.9, 3.1), (4.9,5.1)], color=11)
sg.addNodeCluster("d", [(5,7), (8.9, 9.1)], color=11)

sg.addTimeLine(ticks=2)
sg.save("components.fig")
