from Drawing import *

sg = Drawing(alpha=0, omega=10)
sg.addNode("a")
sg.addNode("b")
sg.addNode("c")
sg.addNode("d")

sg.addLink("a", "b", 0, 4)
sg.addLink("a", "b", 6, 9)
sg.addLink("a", "c", 2, 5, height=0.4)
sg.addLink("b", "c", 1, 8)
sg.addLink("b", "d", 7, 10, height=0.4)
sg.addLink("c", "d", 6, 9)

sg.addNodeCluster("a",[(1,4),(5,8)],color=11,width=100)
sg.addNodeCluster("b",[(5,9)],color=11,width=100)
sg.addNodeCluster("c",[(3,8)],color=11,width=100)

sg.addTimeLine(ticks=2)

