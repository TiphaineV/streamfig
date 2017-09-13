from Drawing import *

s = Drawing()

s.addColor("grey", "#BBBBBB")
s.addColor("white", "#FFFFFF")
s.addColor("red", "#ff0000")

s.addNode("a",[(2,5)])
s.addNode("b",[(1,8)])
s.addNode("c",[(0,0)])
s.addNode("d",[(6,9)])

s.addLink("a", "b", 2, 4)
s.addLink("b", "d", 7, 8, height=0.4)

s.addTimeLine(ticks=2)

