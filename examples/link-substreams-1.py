from streamfig import *

sg = StreamFig(alpha=0, omega=11)
sg.addNode("a")
sg.addNode("b")
sg.addNode("c")
sg.addNode("d")

sg.addLink("a", "b", 0, 4)
sg.addLink("a", "b", 7, 10)
sg.addLink("a", "c", 2, 6, height=0.4)
sg.addLink("b", "c", 1, 9)
sg.addLink("b", "d", 8, 11, height=0.4)
sg.addLink("c", "d", 7, 10)

sg.addLink("a","b",1,4,width=5,color=11)
sg.addLink("b","c",2,5,width=5,color=11)
sg.addLink("b","c",6,8,width=5,color=11)
sg.addLink("c","d",7,9,width=5,color=11)

sg.addTimeLine(ticks=2)

sg.save("link-substreams-1.fig")
