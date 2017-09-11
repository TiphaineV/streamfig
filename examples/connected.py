from Drawing import *

s = Drawing()

s.addColor("tRed", "#FF9896")

s.addNode("a")
s.addNode("b", [(0,4),(5,10)])
s.addNode("c", [(4,9)])
s.addNode("d", [(1,3)])

s.addLink("a", "b", 1, 3)
s.addLink("b", "d", 2, 3)
s.addLink("a", "c", 4.5, 7.5, height=0.60)
s.addLink("a", "b", 7, 8)
s.addLink("a", "b", 6, 9)


s.addRectangle("a", "a", 0, 1, color=-1, bordercolor="tRed", border="lrtb")
s.addRectangle("b", "b", 0, 1, color=-1, bordercolor="tRed", border="lrtb")

s.addRectangle("a", "b", 1, 2, color=-1, bordercolor="tRed", border="lrtb")
s.addRectangle("d", "d", 1, 2, color=-1, bordercolor="tRed", border="lrtb")

s.addRectangle("a", "d", 2, 3, color=-1, bordercolor="tRed", border="lrtb")

s.addRectangle("a", "a", 3, 4.5, color=-1, bordercolor="tRed", border="lrtb")
s.addRectangle("b", "b", 3, 4, color=-1, bordercolor="tRed", border="lrtb")
s.addRectangle("c", "c", 4, 4.5, color=-1, bordercolor="tRed", border="lrtb")

s.addRectangle("a", "c", 4.5, 6, color=-1, bordercolor="tRed", border="lrtb")
s.addRectangle("b", "b", 5, 6, color=-1, bordercolor="tRed", border="lrtb")

s.addRectangle("a", "c", 6, 8, color=-1, bordercolor="tRed", border="lrtb")
s.addRectangle("a", "a", 8, 10, color=-1, bordercolor="tRed", border="lrtb")
s.addRectangle("b", "c", 8, 9, color=-1, bordercolor="tRed", border="lrtb")
s.addRectangle("b", "b", 9, 10, color=-1, bordercolor="tRed", border="lrtb")


s.addTimeLine()
