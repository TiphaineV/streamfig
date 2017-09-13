from Drawing import *

s = Drawing(alpha=0, omega=17)
s.addColor("red", "#FF0000")

s.addNode("u")
s.addNode("x")
s.addNode("v")
s.addNode("y")
s.addNode("w")

s.addLink("u", "x", 1, 2)
s.addLink("u", "x", 9, 10)
s.addLink("x", "v", 3, 4)
s.addLink("x", "v", 11, 12)
s.addLink("v", "y", 5, 6)
s.addLink("v", "y", 13, 14)
s.addLink("y", "w", 7, 8)
s.addLink("y", "w", 15, 16)

s.addPath(((2,"u","x"), (3.5,"x","v"), (5.5, "v", "y"), (7, "y", "w")), 2, 7, color=11, width=6)
s.addPath(((10,"u","x"), (11.5,"x","v"), (13.5, "v", "y"), (15, "y", "w")), 10, 15, color=14, width=6)

s.addTimeNodeMark(4.5,"v",color="red",width=4)

s.addTimeLine(ticks=80, marks=[(0,""),(2,2), (7,7), (10,10), (15,15), (3, "a"), (4, "b"), (5, "c"), (6, "d"), (11, "e"), (12, "f"), (13, "g"), (14, "h")])
#s.addTimeLine(ticks=2)
