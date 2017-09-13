from Drawing import *

sg = Drawing(omega=12)

sg.addNode("a", [(0,4)])
sg.addNode("b", [(2,8), (10,12)])
sg.addNode("c", [(2,11)])

sg.addTime(0, label="a")
sg.addTime(1, label="t")
sg.addTime(6, label="t2")
sg.addTime(9, label="t3")
sg.addTime(10, label="w")

sg.addPath([(3,"a","b"), (6,"b","c"), (9, "c","b")], 1, 11, gamma=2, width=3, color=11)

sg.addTimeLine(ticks=2)
sg.addParameter("g", 2)
