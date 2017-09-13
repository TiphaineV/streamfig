from Drawing import *

s = Drawing()
s.addColor("tBlue", "#AEC7E8") # 174,199,232
s.addColor("tOrange", "#FFBB78") # 255,187,120
s.addColor("tGreen", "#98DF8A") # 152,223,138
s.addColor("tPink", "#FF9896") # 255, 152,150

s.addNode("a")
s.addNode("b")
s.addNode("c")
s.addNode("d")

#s.addLink("a", "c", 1, 6, height=0.40)
#s.addLink("c", "d", 2, 9)
#s.addLink("b", "d", 3, 10, height=0.40)
#s.addLink("a", "b", 4, 5)
#s.addLink("b", "c", 7, 9)

s.addNodeCluster("a",[(0,1),(6,10)], color="tBlue", width=100)
s.addNodeCluster("b",[(0,3)], color="tBlue", width=100)
s.addNodeCluster("c",[(0,1),(9,10)], color="tBlue", width=100)
s.addNodeCluster("d",[(0,2)], color="tBlue", width=100)

s.addNodeCluster("a",[(1,4),(5,6)], color="tGreen", width=100)
s.addNodeCluster("b",[(3,4),(5,7),(9,10)], color="tGreen", width=100)
s.addNodeCluster("c",[(1,4),(5,7)], color="tGreen", width=100)
s.addNodeCluster("d",[(2,4),(5,7),(9,10)], color="tGreen", width=100)

s.addNodeCluster("a",[(4,5)], color="tPink", width=100)
s.addNodeCluster("b",[(4,5),(7,9)], color="tPink", width=100)
s.addNodeCluster("c",[(4,5),(7,9)], color="tPink", width=100)
s.addNodeCluster("d",[(4,5),(7,9)], color="tPink", width=100)

#s.addNodeCluster("a",[(5,7)], color="tBlue", width=100)
#s.addNodeCluster("b",[(5,7)], color="tBlue", width=100)
## wcc 2
#s.addNodeCluster("b",[(0,3), (8,10)], color="tPink", width=100)
#s.addNodeCluster("c",[(0,10)], color="tPink", width=100)
#s.addNodeCluster("d",[(3,7)], color="tPink", width=100)
## wcc 3
#s.addNodeCluster("d",[(0,2), (8,10)], color="tGreen", width=100)
#s.addNodeCluster("e",[(0,10)], color="tGreen", width=100)
#s.addNodeCluster("f",[(0,4)], color="tGreen", width=100)
#s.addNodeCluster("g",[(0,4)], color="tGreen", width=100)
## wcc 4
#s.addNodeCluster("f",[(7,10)], color="tOrange", width=100)
#s.addNodeCluster("g",[(5,10)], color="tOrange", width=100)



s.addTimeLine(ticks=2)

