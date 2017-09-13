from Drawing import *

s = Drawing(alpha=0, omega=10)

s.addColor("tBlue", "#AEC7E8") # 174,199,232
s.addColor("tOrange", "#FFBB78") # 255,187,120
s.addColor("tGreen", "#98DF8A") # 152,223,138
s.addColor("tPink", "#FF9896") # 255, 152,150
s.addColor("tWhite", "#FFFFFF") # 255, 152,150

s.addNode("a", color=14)
s.addNode("u", color="tWhite")
s.addNode("b", color=14)
s.addNode("v", color="tWhite")
s.addNode("c", color=14)

s.addLink("a", "c", 1, 2, height=0.33)
s.addLink("a", "c", 3, 5, height=0.33)
s.addLink("a", "b", 4, 5)
s.addLink("a", "b", 8, 9)
#s.addLink("b", "c", 4, 5)
s.addLink("b", "c", 2, 7)

s.addTimeLine(ticks=2)
