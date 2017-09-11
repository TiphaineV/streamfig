from Drawing import *

sg = Drawing(alpha=0, omega=5)

sg.addNode("x")
sg.addNode("v")
sg.addNode("y")

sg.addLink("x", "v", 1, 2)
sg.addLink("v", "y", 2, 3)

sg.addRectangle("x", "v", 2, 4, color=-1, border="lrtb")

sg.addTime(1, label="a")
sg.addTime(2, label="b")
sg.addTime(3, label="c")

sg.addPath(((2,"x","v"), (2,"v","y")), 2, 2, color=11, width=3)

sg.addTimeLine()
