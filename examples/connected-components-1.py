from streamfig import *

s = StreamFig()

s.addColor("tBlue", "#AEC7E8") # 174,199,232
s.addColor("tOrange", "#FFBB78") # 255,187,120
s.addColor("tGreen", "#98DF8A") # 152,223,138
s.addColor("tPink", "#FF9896") # 255, 152,150
s.addColor("tRed", "#DD0000") # 255, 152,150

s.addNode("a")
s.addNode("b")
s.addNode("c")
s.addNode("d")
s.addNode("e")

s.addLink("a", "b", 0, 10)
s.addLink("b", "c", 0, 3)
s.addLink("a", "c", 2, 10, height=0.4)
s.addLink("c", "d", 5, 10)
s.addLink("d", "e", 0, 10)

s.addRectangle("a", "c", -0.1, 4.95, color=-1, bordercolor="tBlue", border="lrtb")
s.addRectangle("d", "e", -0.1, 4.95, color=-1, bordercolor="tBlue", border="lrtb")
s.addRectangle("a", "e", 5, 10.1, color=-1, bordercolor="tBlue", border="lrtb")

s.addTimeLine(ticks=2)
s.save("connected-components-1.fig")
