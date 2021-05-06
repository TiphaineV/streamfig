from streamfig import *

sg = StreamFig()

sg.addNode("a")
sg.addNode("b")
sg.addNode("c")

sg.addLink("a", "b", 1, 6)
sg.addLink("a", "c", 2, 5, height=0.40)
sg.addLink("a", "c", 8, 10, height=0.40)
sg.addLink("b", "c", 3, 9)

sg.addTimeLine(ticks=2)

sg.save("line-stream-1.fig")
