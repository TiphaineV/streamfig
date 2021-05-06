import streamfig

s = streamfig.StreamFig(alpha=0, omega=10, streaming=False)
s.addColor("tBlue", "#AEC7E8") # 174,199,232
s.addColor("tOrange", "#FFBB78") # 255,187,120
s.addColor("tGreen", "#98DF8A") # 152,223,138
s.addColor("tPink", "#FF9896") # 255, 152,150
s.addColor("tRed", "#DD0000") # 255, 152,150

s.addNode("u")
s.addNode("v")
s.addNode("w")

s.addLink("u", "v", 1, 2)
s.addLink("v", "w", 3, 4)
s.addLink("u", "v", 5, 6)
s.addLink("v", "w", 8, 9)

s.addPath(((2,"u","v"), (3, "v", "w")), 2, 3, color="tBlue", width=6)
s.addPath(((6,"u","v"), (8, "v", "w")), 6, 8, color="tGreen", width=6)
s.addPath(((4,"w","v"), (5, "v", "u")), 4, 5, color="tPink", width=6)

#s.addTime(2, label="t", color="red")
#s.addTimeNodeMark(7,"v",color="red",width=4)

#s.addTimeIntervalMark(1,5,width=6,color=11)

s.addTimeLine(ticks=2)

s.save("betweeness-2.fig")
