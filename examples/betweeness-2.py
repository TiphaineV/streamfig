from Drawing import *

sg = Drawing(alpha=0, omega=5)

sg.addNode("x")
sg.addNode("v")
sg.addNode("y")

sg.addLink("x", "v", 1, 3)
sg.addLink("v", "y", 2, 4)

sg.addTime(1, label="a")
sg.addTime(2, label="b")
sg.addTime(3, label="c")
sg.addTime(4, label="d")

sg.addPath(((2.5,"x","v"), (2.5,"v","y")), 2.5, 2.5, color=11, width=3)

sg.addTimeLine()
