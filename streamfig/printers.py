
# class Printer(abc):
    # def __init__(self):
        # pass

    # def printColors(self):
        # pass

    # def printContinuousNode(self):
        # pass

    # def printDiscreteNode(self):
        # pass

class FigPrinter:

    def __init__(self, stream):
        self.stream = stream


    def printColors(self):
        s = self.stream
        for c in s._colors:
            print("0 " + str(s._colors[c]["id"]) + " " + str(s._colors[c]["hex"]), file=s._out_fp)

    def printContinuousNode(self, u):
        s = self.stream
        color = s._nodes[u]["color"]
        times = s._nodes[u]["times"]
        linetype = s._nodes[u]["linetype"]
        nodeid = s._nodes[u]["id"]
        
        # print node id
        print("4 0 " + str(color) + " 50 -1 0 30 0.0000 4 135 120 " + str(s._offset_x + int(s._alpha * s._time_unit) - 400) + " " + str(s._offset_y + 125 + int(nodeid * s._node_unit)) + " " + str(u) + "\\001", file=s._out_fp)

        # print node timelines
        if len(times) == 0:
            print("""2 1 """ + str(linetype) + """ 2 """ + str(color) + """ 7 50 -1 -1 6.000 0 0 7 0 0 2\n \
          """ + str(s._offset_x + int(s._alpha * s._time_unit)) + """ """ + str(s._offset_y + int(nodeid * s._node_unit)) + """ """ + str(s._offset_x + int(s._omega * s._time_unit)) + """ """ + str(s._offset_y + int(nodeid * s._node_unit)), file=s._out_fp)
        else:
            for (i,j) in times:
                print("""2 1 """ + str(linetype) + """ 2 """ + str(color) + """ 7 50 -1 -1 6.000 0 0 7 0 0 2\n \
          """ + str(s._offset_x + int(i* s._time_unit)) + """ """ + str(s._offset_y + int(nodeid * s._node_unit)) + """ """ + str(s._offset_x + int(j * s._time_unit)) + """ """ + str(s._offset_y + int(nodeid * s._node_unit)), file=s._out_fp)

    def printDiscreteNode(self, u):
        s = self._stream
        color = s._nodes[u]["color"]
        times = s._nodes[u]["times"]
        nodeid = s._nodes[u]["id"]
        width = s._nodes[u]["width"]

        print("4 0 " + str(color) + " 50 -1 0 30 0.0000 4 135 120 " + str(s._offset_x + int(s._alpha * s._time_unit) - 400) + " " + str(s._offset_y + 125 + int(nodeid * s._node_unit)) + " " + str(u) + "\\001", file=s._out_fp)

        if len(times) == 0:
            for i in drange(s._alpha, s._omega, s._discrete):
                print("1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(s._offset_x + int(i * s._time_unit)) + " " + str(s._offset_y + nodeid * s._node_unit) + " 45 45 -6525 -2025 -6480 -2025", file=s._out_fp)
        else:
            for (i,j) in times:
                for x in drange(i, j, s._discrete):
                    print("1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(s._offset_x + int(x * s._time_unit)) + " " + str(s._offset_y + nodeid * s._node_unit) + " 45 45 -6525 -2025 -6480 -2025", file=s._out_fp)

    
    def printLink(self, link):
        s = self.stream

        if s._discrete > 0:
            self.__printDiscreteLink(link)
        else:
            self.__printContinuousLink(link)

    def __printContinuousLink(self, link):
        """
            Prints link (continuous case)
        """
        s = self.stream
        u = link["u"]
        v = link["v"]
        b = link["b"]
        e = link["e"]
        color = link["color"]
        curving = link["curving"]
        height = link["height"]
        width = link["width"]


        if color in s._colors:
            color = s._colors[color]["id"]

        if s._directed:
            if s._nodes[u]["id"] > s._nodes[v]["id"]:
                (u,v) = (v,u)
                arrow_type = "0 1"
            else:
                arrow_type = "1 0"
        else:
            if s._nodes[u]["id"] > s._nodes[v]["id"]:
                (u,v) = (v,u)
            arrow_type = "0 0"

        # Draw circles for u and v
        print("1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(s._offset_x + int(b * s._time_unit)) + " " + str(s._offset_y + s._nodes[u]["id"]*s._node_unit) + " 45 45 -6525 -2025 -6480 -2025", file=s._out_fp)
        print("1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(s._offset_x + int(b * s._time_unit)) + " " + str(s._offset_y + s._nodes[v]["id"]*s._node_unit) + " 45 45 -6525 -2025 -6480 -2025", file=s._out_fp)
        
        # Link them
        spline_coords = []

        if s._nodes[u]["id"] != s._nodes[v]["id"]:

            x1, y1 = s._offset_x + int(b * s._time_unit), s._offset_y + s._nodes[u]["id"]*s._node_unit
            x2 = s._offset_x + int((b + curving) * s._time_unit)
            y2 = int((s._offset_y + s._nodes[v]["id"]*s._node_unit) - 0.5 * (s._nodes[v]["id"]-s._nodes[u]["id"]) * s._node_unit) 
            x3 = s._offset_x + int(b * s._time_unit)
            y3 = s._offset_y + s._nodes[v]["id"]*s._node_unit
            spline_coords.append((x1, y1))
            spline_coords.append((x2, y2))
            spline_coords.append((x3, y3))
        else:
            # self loop case
            base_x, base_y = s._offset_x + int(b * s._time_unit), s._offset_y + s._nodes[u]["id"]*s._node_unit 
            spline_coords.append((base_x, base_y))            

            x, y = base_x + ( 0.5 * s._time_unit ), base_y - 0.25 * s._node_unit
            spline_coords.append((int(x), int(y)))    

            x, y = base_x, base_y - 0.5 * s._node_unit 
            spline_coords.append((int(x), int(y)))

            x, y = base_x - (0.5 * s._time_unit ), base_y - 0.25 * s._node_unit
            spline_coords.append((int(x), int(y)))

            x, y = base_x, base_y 
            spline_coords.append((x, y))     


        if s._directed:
            dir_arg1 = "1"
            dir_arg2 = "1.000"
        else:
            dir_arg1 = "0"
            dir_arg2 = "-1.000"
        
        print(f"3 2 0 {width} {color} 7 50 -1 -1 0.000 0 {arrow_type} {len(spline_coords)}", file=s._out_fp)

        # arrow type
        if s._directed:
            print("1 1 3.00 90.00 150.00", file=s._out_fp)
        
        # Print spline coordinates
        print(" ".join([ f"{x} {y}" for x,y in spline_coords ]), file=s._out_fp)

        # more arrow properties 
        print("0.000 " + str(dir_arg2) +" 0.000 1.000 0.000", file=s._out_fp)
        print("# end edge", file=s._out_fp)

        numnodes = abs(s._nodes[u]["id"] - s._nodes[v]["id"])

        # Add duration
        print("2 1 0 " + str(width) + " " + str(color) + " 7 50 -1 -1 0.000 0 0 -1 0 0 2", file=s._out_fp)
        print(str(s._offset_x + int((b + curving) * s._time_unit)) + " " + str(s._offset_y + int(s._nodes[u]["id"]*s._node_unit + (numnodes*s._node_unit*height))) + " " + str(s._offset_x + int(e * s._time_unit)) + " " + str(s._offset_y + s._nodes[v]["id"]*s._node_unit - (numnodes*s._node_unit*(1-height))), file=s._out_fp)

    def __printDiscreteLink(self, link): # u, v, b, e, curving=0.0, color=0, height=0.5, width=3):
        s = self.stream
        u = link["u"]
        v = link["v"]
        b = link["b"]
        e = link["e"]
        color = link["color"]
        curving = link["curving"]
        height = link["height"]
        width = link["width"]

        if color in s._colors:
            color = s._colors[color]["id"]
        if s._directed:
            if s._nodes[u] > s._nodes[v]:
                (u,v) = (v,u)
                arrow_type = "0 1"
            else:
                arrow_type = "1 0"
        else:
            if s._nodes[u]["id"] > s._nodes[v]["id"]:
                (u,v) = (v,u)
            arrow_type = "0 0"

        for i in drange(b,e, s._discrete):
            # Draw circles for u and v
            print("1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(s._offset_x + int(i * s._time_unit)) + " " + str(s._offset_y + s._nodes[u]["id"]*s._node_unit) + " 45 45 -6525 -2025 -6480 -2025", file=s._out_fp)
            print("1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(s._offset_x + int(i * s._time_unit)) + " " + str(s._offset_y + s._nodes[v]["id"]*s._node_unit) + " 45 45 -6525 -2025 -6480 -2025", file=s._out_fp)
            
            # Link them
            x1, y1 = s._offset_x + int(i * s._time_unit), s._offset_y + s._nodes[u]["id"]*s._node_unit
            x2 = s._offset_x + int((i + curving) * s._time_unit)
            y2 = int((s._offset_y + s._nodes[v]["id"]*s._node_unit) - 0.5 * (s._nodes[v]["id"]-s._nodes[u]["id"]) * s._node_unit) 
            x3 = s._offset_x + int(i * s._time_unit)
            y3 = s._offset_y + s._nodes[v]["id"]*s._node_unit

            if s._directed:
                dir_arg1 = "2"
                dir_arg2 = "1.000"
            else:
                dir_arg1 = "0"
                dir_arg2 = "-1.000"

            print("3 2 0 " + str(width) + " " + str(color) + " 7 50 -1 -1 0.000 0 " + str(arrow_type) + " 3\n", file=s._out_fp)
            # arrow type
            if s._directed:
                print("1 1 3.00 90.00 150.00\n", file=s._out_fp)
            print("%s %s %s %s %s %s\n" % (x1, y1, x2, y2, x3, y3), file=s._out_fp)
            print("0.000 " + str(dir_arg2) + " 0.000\n", file=s._out_fp)

            numnodes = abs(s._nodes[u]["id"] - s._nodes[v]["id"])


    def printNodeCluster(self, nc):

        s = self.stream
        u = nc["u"]
        times = nc["times"]
        color = nc["color"]
        width = nc["width"]

        margin = int(width / 2)

        if color in s._colors:
            color = s._colors[color]["id"]  

        if len(times) == 0:
            times = [(s._alpha, s._omega)]

        for (i,j) in times:
            (x1, y1) = ( s._offset_x + int(i * s._time_unit), s._offset_y + int(s._nodes[u]["id"]*s._node_unit) - margin )
            (x2, y2) = ( s._offset_x + int(j * s._time_unit), s._offset_y + int(s._nodes[u]["id"]*s._node_unit) - margin ) 
            (x3, y3) = ( s._offset_x + int(j * s._time_unit), s._offset_y + int(s._nodes[u]["id"]*s._node_unit) + margin ) 
            (x4, y4) = ( s._offset_x + int(i*s._time_unit), s._offset_y + int(s._nodes[u]["id"]*s._node_unit) + margin ) 

            print("2 2 0 0 0 " + str(color) + " 51 -1 20 0.000 0 0 -1 0 0 5", file=s._out_fp)
            print(str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + " " + str(x3) + " " + str(y3) + " " + str(x4) + " " + str(y4) + " " + str(x1) + " " + str(y1), file=s._out_fp)


    def printPath(self, path):
        s = self.stream
        width, color, depth, coords = path["width"], path["color"], path["depth"], path["coords"]
        print(f"2 1 0 {width} {color} 7 {depth} -1 -1 0.000 0 0 -1 0 0 " + str(len(coords)), file=s._out_fp)
        print(" ".join([ " ".join(map(str, i)) for i in coords ] ), file=s._out_fp)


    def printRectangle(self, r):
        s = self.stream
        u = r["u"]
        v = r["v"]
        b = r["b"]
        e = r["e"]
        width = r["width"]
        depth = r["depth"]
        color = r["color"]
        border = r["border"]
        bordercolor = r["bordercolor"]
        borderwidth = r["borderwidth"]

        margin = int(width/2)

        if color in s._colors:
            color = s._colors[color]["id"]
        if bordercolor in s._colors:
            bordercolor = s._colors[bordercolor]["id"]

        # Print border lrtb (if any)
        if "l" in border:
            print("2 1 0 " + str(borderwidth) + " " + str(bordercolor) + " 7 48 -1 -1 0.000 0 0 -1 0 0 2", file=s._out_fp)
            print(str(s._offset_x + int(b * s._time_unit)) + " " + str(s._offset_y + s._nodes[u]["id"] * s._node_unit - margin) + " " + str(s._offset_x + int(b * s._time_unit)) + " " + str(s._offset_y + s._nodes[v]["id"] * s._node_unit + margin) + "\n", file=s._out_fp)
        if "r" in border:
            print("2 1 0 " + str(borderwidth) + " " + str(bordercolor) + " 7 48 -1 -1 0.000 0 0 -1 0 0 2", file=s._out_fp)
            print(str(s._offset_x + int(e * s._time_unit)) + " " + str(s._offset_y + s._nodes[u]["id"] * s._node_unit - margin) + " " + str(s._offset_x + int(e * s._time_unit)) + " " + str(s._offset_y + s._nodes[v]["id"] * s._node_unit + margin) + "\n", file=s._out_fp)
        if "t" in border:
            print("2 1 0 " + str(borderwidth) + " " + str(bordercolor) + " 7 48 -1 -1 0.000 0 0 -1 0 0 2", file=s._out_fp)
            print(str(s._offset_x + int(b * s._time_unit)) + " " + str(s._offset_y + s._nodes[u]["id"] * s._node_unit - margin) + " " + str(s._offset_x + int(e * s._time_unit)) + " " + str(s._offset_y + s._nodes[u]["id"] * s._node_unit - margin), file=s._out_fp)
        if "b" in border:
            print("2 1 0 " + str(borderwidth) + " " + str(bordercolor) + " 7 48 -1 -1 0.000 0 0 -1 0 0 2", file=s._out_fp)
            print(str(s._offset_x + int(b * s._time_unit)) + " " + str(s._offset_y + s._nodes[v]["id"] * s._node_unit + margin) + " " + str(s._offset_x + int(e * s._time_unit)) + " " + str(s._offset_y + s._nodes[v]["id"] * s._node_unit + margin), file=s._out_fp)

        if color > -1:
            # Print rectangle
            print("2 2 0 0 0 " + str(color) + " " + str(depth) + " -1 20 0.000 0 0 -1 0 0 5", file=s._out_fp)
            print(str(s._offset_x + int(b * s._time_unit)) + " " + str(s._offset_y + int(s._nodes[u]["id"]*s._node_unit) - margin) + " " + str(s._offset_x + int(e * s._time_unit)) + " " + str(s._offset_y + int(s._nodes[u]["id"]*s._node_unit) - margin) + " " + str(s._offset_x + int(e * s._time_unit)) + " " + str(s._offset_y + int(s._nodes[v]["id"]*s._node_unit) + margin) + " " + str(s._offset_x + int(b*s._time_unit)) + " " + str(s._offset_y + int(s._nodes[v]["id"]*s._node_unit) + margin) + " " + str(s._offset_x + int(b*s._time_unit)) + " " + str(s._offset_y + int(s._nodes[u]["id"]*s._node_unit) - margin), file=s._out_fp )
        
        # s._out_fp.close()

    def printTimeNodeMark(self, tnm):
        s = self.stream
        t = tnm["t"]
        v = tnm["v"]
        color = tnm["color"]
        width = tnm["width"]
        depth = tnm["depth"]

        print("2 1 0 "+ str(width) + " " + str(color) + " 7 " + str(depth) + " -1 -1 0.000 0 0 -1 0 0 2", file=s._out_fp)
        print(str(s._offset_x + int(t * s._time_unit) - 50 ) + " " + str(s._offset_y + s._nodes[v]["id"] * s._node_unit - 50) + " " + str(s._offset_x + int(t * s._time_unit) + 50 ) + " " + str(s._offset_y + s._nodes[v]["id"] * s._node_unit + 50), file=s._out_fp)

        print("2 1 0 "+ str(width) + " " + str(color) + " 7 " + str(depth) + " -1 -1 0.000 0 0 -1 0 0 2", file=s._out_fp)
        print(str(s._offset_x + int(t * s._time_unit) - 50 ) + " " + str(s._offset_y + s._nodes[v]["id"] * s._node_unit + 50) + " " + str(s._offset_x + int(t * s._time_unit) + 50 ) + " " + str(s._offset_y + s._nodes[v]["id"] * s._node_unit - 50), file=s._out_fp)

    def printTimeIntervalMark(self, tim):
        s = self.stream
        b = tim["b"]
        e = tim["e"]
        color = tim["color"]
        width = tim["width"]

        pos_segment_y = s._offset_y + (s._nodes[s._first_node]["id"] * s._node_unit) - (100 * s._num_time_intervals) - 200

        print("2 1 0 1 0 7 50 -1 -1 0.000 0 0 -1 1 1 2", file=s._out_fp)
        print("13 1 1.00 60.00 120.00", file=s._out_fp)
        print("13 1 1.00 60.00 120.00", file=s._out_fp)
        print(str(s._offset_x + b * s._time_unit) + " " + str(pos_segment_y) + " " + str(s._offset_x + (e * s._time_unit)) + " " + str(pos_segment_y), file=s._out_fp)
        s._num_time_intervals += 1

    def printTimeLine(self):
        """
            Adds a time line at the bottom of the stream graph.

            /!\ Should be called last /!\

            :param ticks: Granularity a which ticks should be outputted (every 2, every 1, etc.)
            :param marks: Custom ticks in the form (t, l)

            :type ticks: float
            :type marks: list

            :Example:
            
            >>> # Most common usage
            >>> d.addTimeLine(ticks=2)
            >>> # With one custom tick labeled "a" at time 2.5
            >>> d.addTimeLine(ticks=2, marks=[(2.5, "a")])
        """

        s = self.stream

        ticks = s._timeline["ticks"]
        label = s._timeline["label"]
        marks = s._timeline["marks"]
        
        timeline_y = s._node_cpt * s._node_unit + int(s._node_unit / 2)
        
        vals = []
        i = s._alpha
        while i < s._omega:
            if (i).is_integer():
                vals.append((int(i),int(i)))
            else:
                vals.append((i,i))
            i = i+ticks
        
        if len(marks) > 0:
            # Ajouter/remplacer les valeurs (t, v)
            for (t,v) in marks:
                found = False
                for x in range(0, len(vals)):
                    if vals[x][0] == t:
                        vals[x] = (t,v)
                        found = True
                if not found:
                    vals.append((t,v))

        # Time arrow
        if s._discrete > 0:
            start, end = s._omega - 0.5, s._omega
        else:
            start, end = s._alpha, s._omega     

        print("2 1 0 1 0 7 50 -1 -1 0.000 0 0 -1 1 0 2", file=s._out_fp)
        print("1 1 1.00 60.00 120.00", file=s._out_fp)
        print(str(s._offset_x + int(start * s._time_unit)) + " " + str(s._offset_y + timeline_y) + " " + str(s._offset_x + int(end * s._time_unit)) + " " + str(s._offset_y + timeline_y), file=s._out_fp)

        # Time ticks
        for (i,j) in vals:
            print("2 1 0 1 0 7 50 -1 -1 0.000 0 0 -1 0 0 2", file=s._out_fp)
            print(str(s._offset_x + int(i * s._time_unit)) + " " + str(s._offset_y + timeline_y) + " " + str(s._offset_x + int(i * s._time_unit)) + " " + str(s._offset_y + timeline_y + 30), file=s._out_fp)
            if i < s._omega - 1:
                print("4 1 0 50 -1 0 20 0.0000 4 135 120 " + str(s._offset_x + int(i * s._time_unit)) + " " + str(s._offset_y + timeline_y + 250) + " " + str(j) + "\\001", file=s._out_fp)

        # Write "time"
        print("4 2 0 50 -1 0 20 0.0000 4 135 120 " + str(s._offset_x + int(s._omega * s._time_unit)) + " " + str(s._offset_y + timeline_y + 250) + " " + label + "\\001", file=s._out_fp)

    def printNodeIntervalMark(self, nim):
        s = self.stream
        u = nim["u"]
        v = nim["v"]
        color = nim["color"]
        width = nim["width"]

        if color in s._colors:
            color = s._colors[color]["id"]

        pos_segment_x = s._offset_x - (150 * s._num_node_intervals) - 600

        print(f"2 1 {color} {width} 0 7 50 -1 -1 0.000 0 0 -1 1 1 2", file=s._out_fp)
        print("13 1 1.00 60.00 120.00", file=s._out_fp)
        print("13 1 1.00 60.00 120.00", file=s._out_fp)
        print(f"{pos_segment_x} {s._offset_y + s._nodes[u]['id'] * s._node_unit}  {pos_segment_x} {s._offset_y + s._nodes[v]['id'] * s._node_unit}", file=s._out_fp)
        s._num_node_intervals += 1

    def printParameter(self, p):
        s = self.stream
        letter = p["letter"]
        value = p["value"]
        color = p["color"]
        width = p["width"]

        if color in s._colors:
            color = s._colors[color]["id"]

        #?Place at top? Confusing with time intervals...
        pos_segment_y = s._offset_y + (s._nodes[s._first_node]["id"] * s._node_unit) - (150 * s._num_time_intervals) - 400
        # Place at bottom instead? Then needs to be written last.
        # pos_segment_y = s._offset_y + s._node_cpt * s._node_unit + 2*s._node_unit

        if s._num_parameters == 0:
            paramoffset = 0
        else:
            paramoffset = 200

        print("2 1 " + str(color) + " " + str(width) + " 0 7 50 -1 -1 0.000 0 0 -1 1 1 2", file=s._out_fp)
        print("13 1 1.00 60.00 120.00", file=s._out_fp)
        print("13 1 1.00 60.00 120.00", file=s._out_fp)
        print(str(s._offset_x + (s._totalval_parameters * s._time_unit  + (s._num_parameters * paramoffset))) + " " + str(pos_segment_y) + " " + str(s._offset_x + int(value * s._time_unit) + (s._totalval_parameters * s._time_unit + (s._num_parameters * paramoffset))) + " " + str(pos_segment_y), file=s._out_fp)

        valtocenter = int(value * s._time_unit / 2) - (200 + (50 * max(int(value) - 2, 0))) 

        print("4 0 0 50 -1 32 14 0.0000 4 180 375 " + str(s._offset_x + (s._totalval_parameters * s._time_unit + int(s._num_parameters * paramoffset)) + valtocenter)  + " " + str(pos_segment_y - 150)  + " " + str(letter) + " = " + str(value) + "\\001")
        s._totalval_parameters += value
        s._num_parameters += 1
