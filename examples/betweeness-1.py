from Drawing import *

sg = Drawing(alpha=0, omega=4)

sg.addNode("u")
sg.addNode("v")
sg.addNode("w")

sg.addLink("u", "v", 1, 2)
sg.addLink("v", "w", 2, 3)

sg.addPath(((2,"u","v"), (2,"v","w")), 2, 2, color=11, width=6)

sg.addTimeLine()
