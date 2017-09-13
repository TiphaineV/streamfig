from Drawing import *

sg = Drawing(alpha=0, omega=10)
sg.addNode("a",[(1,4),(5,8)])
sg.addNode("b",[(5,9)])
sg.addNode("c",[(3,8)])
sg.addNode("d",[(0,0)])

sg.addLink("a", "b", 6, 8)
sg.addLink("a", "c", 3, 4, height=0.4)
sg.addLink("b", "c", 5, 8)

sg.addTimeLine(ticks=2)

