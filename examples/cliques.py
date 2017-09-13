from Drawing import *

sg = Drawing()
sg.addColor("red", "#FF8080")
sg.addNode("a")
sg.addNode("b")
sg.addNode("c")
sg.addNode("d")

sg.addLink("a", "b", 0, 4)
sg.addLink("a", "b", 6, 9)
sg.addLink("a", "c", 2, 5, height=0.4)
sg.addLink("b", "c", 1, 8)
sg.addLink("b", "d", 7, 10, height=0.4)
sg.addLink("c", "d", 6, 9)

sg.addRectangle("a","c",2,4,color=11)
sg.addRectangle("b","d",7,8,color="red")

sg.addTimeLine(ticks=2)

