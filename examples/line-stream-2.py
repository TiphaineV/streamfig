from Drawing import *

sg = Drawing()

sg.addNode("ab", [(1,6)])
sg.addNode("bc", [(3,9)])
sg.addNode("ac", [(2,5),(8,10)])

sg.addLink("ab", "ac", 2, 5, height=0.40)
sg.addLink("ab", "bc", 3, 6)
sg.addLink("ac", "bc", 3, 5)
sg.addLink("ac", "bc", 8, 9)

sg.addTimeLine(ticks=2)

