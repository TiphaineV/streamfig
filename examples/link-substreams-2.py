from Drawing import *

sg = Drawing(alpha=0, omega=11)
sg.addNode("a",[(1,4)])
sg.addNode("b",[(1,5),(6,8)])
sg.addNode("c",[(2,5),(6,9)])
sg.addNode("d",[(7,9)])

sg.addLink("a","b",1,4)
sg.addLink("b","c",2,5)
sg.addLink("b","c",6,8)
sg.addLink("c","d",7,9)

sg.addTimeLine(ticks=2)

