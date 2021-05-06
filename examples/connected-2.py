from streamfig import *

s = StreamFig()

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

s.addNodeCluster("a", [(0,10)], color=11,width=80)
s.addNodeCluster("a", [(1,3)], color=11,width=150)
s.addNodeCluster("b", [(7,8)], color=11,width=80)
s.addNodeCluster("b", [(1,3)], color=11,width=150)
s.addNodeCluster("c", [(7,8)], color=11,width=80)
s.addNodeCluster("d", [(2,3)], color=11,width=150)

# $[2,3]\times\{a,b,d\} \cup [1,2]\times\{a,b\} \cup [0,10]\times\{a\} \cup [7,8]\times\{a,b,c\}$
# $[2,3]\times\{a,b,d\} \cup [1,2]\times\{a,b\} \cup [0,4]\times\{b\}$

s.addNodeCluster("a", [(1,3)], color="tPink",width=80)
s.addNodeCluster("b", [(0,4)], color="tPink",width=80)
s.addNodeCluster("d", [(2,3)], color="tPink",width=80)

s.addTimeLine(ticks=2)
s.save("connected-2.fig")
