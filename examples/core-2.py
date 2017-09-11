from Drawing import *

sg = Drawing(alpha=0, omega=10)

sg.addNode("a",[(4,5)])
sg.addNode("b",[(4,5),(7,9)])
sg.addNode("c",[(4,5),(7,9)])
sg.addNode("d",[(4,5),(7,9)])

sg.addLink("a", "c", 4, 5, height=0.40, curving=0.3)
sg.addLink("c", "d", 4, 5)
sg.addLink("c", "d", 7, 9)
sg.addLink("b", "d", 4, 5, height=0.40, curving=0.3)
sg.addLink("b", "d", 7, 9, height=0.40, curving=0.3)
sg.addLink("a", "b", 4, 5)
sg.addLink("b", "c", 7, 9)

sg.addTimeLine(ticks=2)

