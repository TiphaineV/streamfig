import streamfig

print(streamfig)

s = StreamFig(alpha=0, omega=10)

s.addColor("red", "#FF8080")

s.addColor("tBlue", "#AEC7E8") # 174,199,232
s.addColor("tOrange", "#FFBB78") # 255,187,120
s.addColor("tGreen", "#98DF8A") # 152,223,138
s.addColor("tPink", "#FF9896") # 255, 152,150

s.addNode("a", color=14)
s.addNode("u", color=27)
s.addNode("b", color=14)
s.addNode("v", color=27)
s.addNode("c", color=14)

s.addLink("a", "u", 0, 2)
s.addLink("a", "u", 3, 9)
s.addLink("b", "u", 4, 5)
s.addLink("b", "u", 8, 10)
s.addLink("b", "v", 2, 7)
s.addLink("c", "u", 1, 5, height=0.55)
s.addLink("c", "v", 0, 8)

s.addTimeLine(ticks=2)
