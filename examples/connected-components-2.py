from Drawing import *

s = Drawing()

s.addColor("tBlue", "#AEC7E8") # 174,199,232
s.addColor("tOrange", "#FFBB78") # 255,187,120
s.addColor("tGreen", "#98DF8A") # 152,223,138
s.addColor("tPink", "#FF9896") # 255, 152,150
s.addColor("tRed", "#DD0000") # 255, 152,150

s.addNode("a", [(0,10)])
s.addNode("b", [(0,4),(5,10)])
s.addNode("c", [(4,9)])
s.addNode("d", [(1,3)])

s.addLink("a","b",1,3)
s.addLink("a","b",7,8)
s.addLink("b","c",6,9)
s.addLink("b","d",2,3,height=0.4)
s.addLink("a","c",4.5,7.5,height=0.4)


s.addRectangle("a", "a", 0, .95, color=-1, bordercolor="tGreen", border="lrtb")
s.addRectangle("b", "b", 0, .95, color=-1, bordercolor="tGreen", border="lrtb")

s.addRectangle("a", "b", 1, 1.95, color=-1, bordercolor="tGreen", border="lrtb")
s.addRectangle("d", "d", 1, 1.95, color=-1, bordercolor="tGreen", border="lrtb")

s.addRectangle("a", "d", 2, 3, color=-1, bordercolor="tGreen", border="lrtb")

s.addRectangle("a", "a", 3.05, 4.45, color=-1, bordercolor="tGreen", border="lrtb")
s.addRectangle("b", "b", 3.05, 4, color=-1, bordercolor="tGreen", border="lrtb")
s.addRectangle("c", "c", 4, 4.45, color=-1, bordercolor="tGreen", border="lrtb")

s.addRectangle("a", "c", 4.5, 5.95, color=-1, bordercolor="tGreen", border="lrtb")
s.addRectangle("b", "b", 5, 5.95, color=-1, bordercolor="tGreen", border="lrtb")

s.addRectangle("a", "c", 6, 8, color=-1, bordercolor="tGreen", border="lrtb")
s.addRectangle("a", "a", 8.05, 10, color=-1, bordercolor="tGreen", border="lrtb")
s.addRectangle("b", "c", 8.05, 9, color=-1, bordercolor="tGreen", border="lrtb")
s.addRectangle("b", "b", 9.05, 10, color=-1, bordercolor="tGreen", border="lrtb")


s.addTimeLine(ticks=2)

