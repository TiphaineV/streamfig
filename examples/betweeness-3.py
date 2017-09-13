from Drawing import *

sg = Drawing(alpha=0, omega=5)

sg.addNode("u")
sg.addNode("v")
sg.addNode("w")

sg.addLink("u", "v", 1, 3)
sg.addLink("v", "w", 2, 4)

sg.addPath(((2.5,"u","v"), (2.5,"v","w")), 2.5, 2.5, color=11, width=6)

sg.addTimeLine()
