# -*- coding: utf-8 -*-
# TODO
# Nettoyage vieux code / Commentaires code
# Documentation
# Remplacer les print(...\n)
# Gestion des erreurs (noeud non ajoute...)

import sys

__version__ = "1.2"
__author__ = "Tiphaine Viard"

def drange(start, stop, step):
    """
        Helper function generating a range of numbers.

        :param start: Range start
        :param end: Range end
        :param step: Range step (the difference between two subsequent elements in the range equals step)
        :type start: float
        :type end: float
        :type step: float
        :return: an iterator over the range
        :rtype: generator

        :Example:

        >>> [i for i in drange(0.0,1.0,0.1)]
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    """
    r = start
    while r <= stop:
        yield r
        r += step

class StreamFig:
    """
        Initializes a stream graph drawing.

        :param alpha: Start time of stream graph.
        :param omega: End time of stream graph.
        :param time_width: Width (in the final fig) of one time unit.
        :param discrete: Duration of the time step if time is discrete. 0 if time is continuous.

        :type alpha: float
        :type omega: float
        :type time_width: positive int
        :type discrete: positive int
        
        :Example:
        
        >>> d = Drawing(alpha=0, omega=5.5)
        >>> d = Drawing(alpha=0, omega=6, discrete=2)
    """

    _alpha = 0.0
    _omega = 0.0
    _discrete = -1

    _time_unit = 500
    _node_unit = 600
    _offset_x = 3450
    _offset_y = 2250
    
    _num_node_intervals = 0
    #?Is incremented by one if time marks are used too
    _num_time_intervals = 0
    _num_parameters = 0
    _totalval_parameters = 0

    _first_node = ""

    _nodes = {}
    _node_cpt = 1

    _links = []

    _node_clusters = []

    # _directed = False

    _streaming = False
    _out_fp = None

    def streaming(func):
        """
            Decorator for streaming mode (for larger datasets, typically)
            If the streaming class argument is True, then every action will be outputted
            straight away. Else, it will be stored for later usage.
        """
        import functools
        @functools.wrap(func)
        def wrapper(self, *args, **kwargs):
            func(*args, **kwargs)
        return wrapper



    def __init__(self, alpha=0.0, omega=10.0, time_width=500, discrete=0, directed=False, streaming=False):

        self._streaming = streaming

        self._alpha = float(alpha)
        self._omega = float(omega)
        self._time_unit = time_width
        self._discrete = discrete
        self._directed = directed

        self._timeline = { "display": False, "ticks": 2, "label": "time", "marks": [] }
        self._paths = []
        self._colors = {}
        self._color_cpt = 31

        self.linetype = 2
        
        self._timenodemarks = []
        self._rectangles = []
        self._node_intervals = []
        self._time_intervals = []
        self._parameters = []

        # Useful predefined colors
        # self.addColor("grey", "#888888")

        
        self._header = """#FIG 3.2  Produced by xfig version 3.2.5b\n\
Landscape\n\
Center\n\
Inches\n\
Letter\n\
100.00\n\
Single\n\
-2\n\
1200 2\n"""
        if self._streaming:
            print(self._header)


    def setLineType(def_linetype):
        """
            Changes the linetype for nodes (i.e. from dashed to dotted). Default is dotted (linetype=2).
            See FIG documentation for all values.

            :param def_linetype: the new linetype
            :type def_linetype: int
        """

        self.linetype = def_linetype

    def addColor(self, name, hex_code):
        """
            Adds a new RGB color for use.

            :param name: Color identifier (must be unique, case sensitive)
            :param hex: Color in hexadecimal format
            :type name: str
            :type hex: str

            :Example:

            >>> d.addColor("red", "#FF0000")
        """

        self._color_cpt += 1
        self._colors[name] = { "id": self._color_cpt, "hex": hex_code }

    
    def printColors(self):
        for c in self._colors:
            print("0 " + str(self._colors[c]["id"]) + " " + str(self._colors[c]["hex"]), file=self._out_fp)

    def addNode(self, u, times=[], color=0, linetype=None):
        """
            Adds a new node to the stream graph.

            :param u: Name of the node (should be unique).
            :param times: List of tuples indicating when the node is present.
            :param color: Color of the node, either a XFIG int or a user-defined color.
            :param linetype: ?

            :type u: str
            :type times: list of 2-tuples
            :type color: int or str
        
            :Example:
            
            >>> # Adds a node "v" from alpha to omega
            >>> d.addNode("v")
            >>> # Adds a node "v" from time 1 to time 2.5 and from time 4 to time 8.
            >>> d.addNode("v", times=[(1,2.5),(4,8)])
        """
        if self._discrete > 0:
            self.__addDiscreteNode(u, times, color)
        else:
            self.__addContinuousNode(u, times, color, linetype)

    def __addDiscreteNode(self, u, times=[], color="grey", width=1):

        if color in self._colors:
            color = self._colors[color]["id"]

        if self._node_cpt == 1:
            self._first_node = u

        self._node_cpt += 1
        self._nodes[u] = {
            "id": self._node_cpt,
            "times": times,
            "color": color,
            "width": width
        }


    def printDiscreteNode(self, u):
        color = self._nodes[u]["color"]
        times = self._nodes[u]["times"]
        nodeid = self._nodes[u]["id"]
        width = self._nodes[u]["width"]

        print("4 0 " + str(color) + " 50 -1 0 30 0.0000 4 135 120 " + str(self._offset_x + int(self._alpha * self._time_unit) - 400) + " " + str(self._offset_y + 125 + int(nodeid * self._node_unit)) + " " + str(u) + "\\001", file=self._out_fp)

        if len(times) == 0:
            for i in drange(self._alpha, self._omega, self._discrete):
                print("1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self._offset_x + int(i * self._time_unit)) + " " + str(self._offset_y + nodeid * self._node_unit) + " 45 45 -6525 -2025 -6480 -2025", file=self._out_fp)
        else:
            for (i,j) in times:
                for x in drange(i, j, self._discrete):
                    print("1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self._offset_x + int(x * self._time_unit)) + " " + str(self._offset_y + nodeid * self._node_unit) + " 45 45 -6525 -2025 -6480 -2025", file=self._out_fp)

    def __addContinuousNode(self, u, times=[], color=0, linetype=None):
        """ nodeId : identifiant du noeud
            times : suite d'intervalles de temps ou le noeud est actif
        """


        if color in self._colors:
            color = self._colors[color]["id"]

        if self._node_cpt == 1:
            self._first_node = u

        self._node_cpt += 1
        self._nodes[u] = {}
        self._nodes[u]["id"] = self._node_cpt
        self._nodes[u]["times"] = times
        self._nodes[u]["color"] = color
        
        if linetype is None:
            linetype = self.linetype
        self._nodes[u]["linetype"] = linetype

    def printContinuousNode(self, u):
        color = self._nodes[u]["color"]
        times = self._nodes[u]["times"]
        linetype = self._nodes[u]["linetype"]
        nodeid = self._nodes[u]["id"]
        
        # print node id
        print("4 0 " + str(color) + " 50 -1 0 30 0.0000 4 135 120 " + str(self._offset_x + int(self._alpha * self._time_unit) - 400) + " " + str(self._offset_y + 125 + int(nodeid * self._node_unit)) + " " + str(u) + "\\001", file=self._out_fp)

        # print node timelines
        if len(times) == 0:
            print("""2 1 """ + str(linetype) + """ 2 """ + str(color) + """ 7 50 -1 -1 6.000 0 0 7 0 0 2\n \
          """ + str(self._offset_x + int(self._alpha * self._time_unit)) + """ """ + str(self._offset_y + int(nodeid * self._node_unit)) + """ """ + str(self._offset_x + int(self._omega * self._time_unit)) + """ """ + str(self._offset_y + int(nodeid * self._node_unit)), file=self._out_fp)
        else:
            for (i,j) in times:
                print("""2 1 """ + str(linetype) + """ 2 """ + str(color) + """ 7 50 -1 -1 6.000 0 0 7 0 0 2\n \
          """ + str(self._offset_x + int(i* self._time_unit)) + """ """ + str(self._offset_y + int(nodeid * self._node_unit)) + """ """ + str(self._offset_x + int(j * self._time_unit)) + """ """ + str(self._offset_y + int(nodeid * self._node_unit)), file=self._out_fp)

    def addLink(self, u, v, b, e, curving=0.0, color=0, height=0.5, width=3):
        """
            Adds a link from time b to time e between nodes u and v.

            :param u: Node to be linked
            :param v: Node to be linked
            :param b: Start time of the link
            :param e: End time of the link
            :param curving: Curving of the link. 0 corresponds to a straight link, 
                            negative values will draw the link bent on the left, 
                            positive values will draw the link bent on the right
            :param color: the link's color (see addColor())
            :param height:  Fixes the position of the duration bar; values are between 0 and 1.
                            0 would draw the duration bar at node u's level, 1 at node's v, 0.5 in between, etc.
            :param width: The link's width

            :type u: str
            :type v: str
            :type b: float
            :type e: float
            :type curving: float
            :type color: str/int
            :type height: float
            :type width: int

            :Example:

            >>> # Add link from time 1 to time 3 between nodes u and v
            >>> d.addLink("u", "v", 1, 3)
            >>> # Add a right curved link from time 1 to time 3 between nodes u and v
            >>> d.addLink("u", "v", 1, 3, curving=0.3)
        """
        link = {
            "u": u,
            "v": v,
            "b": b,
            "e": e,
            "curving": curving,
            "color": color,
            "height": height,
            "width": width
        }

        self._links.append(link)

    def __printDiscreteLink(self, link): # u, v, b, e, curving=0.0, color=0, height=0.5, width=3):
        u = link["u"]
        v = link["v"]
        b = link["b"]
        e = link["e"]
        color = link["color"]
        curving = link["curving"]
        height = link["height"]
        width = link["width"]

        if color in self._colors:
            color = self._colors[color]["id"]
        if self._directed:
            if self._nodes[u] > self._nodes[v]:
                (u,v) = (v,u)
                arrow_type = "0 1"
            else:
                arrow_type = "1 0"
        else:
            if self._nodes[u]["id"] > self._nodes[v]["id"]:
                (u,v) = (v,u)
            arrow_type = "0 0"

        for i in drange(b,e, self._discrete):
            # Draw circles for u and v
            print("1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self._offset_x + int(i * self._time_unit)) + " " + str(self._offset_y + self._nodes[u]["id"]*self._node_unit) + " 45 45 -6525 -2025 -6480 -2025", file=self._out_fp)
            print("1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self._offset_x + int(i * self._time_unit)) + " " + str(self._offset_y + self._nodes[v]["id"]*self._node_unit) + " 45 45 -6525 -2025 -6480 -2025", file=self._out_fp)
            
            # Link them
            x1, y1 = self._offset_x + int(i * self._time_unit), self._offset_y + self._nodes[u]["id"]*self._node_unit
            x2 = self._offset_x + int((i + curving) * self._time_unit)
            y2 = int((self._offset_y + self._nodes[v]["id"]*self._node_unit) - 0.5 * (self._nodes[v]["id"]-self._nodes[u]["id"]) * self._node_unit) 
            x3 = self._offset_x + int(i * self._time_unit)
            y3 = self._offset_y + self._nodes[v]["id"]*self._node_unit

            if self._directed:
                dir_arg1 = "2"
                dir_arg2 = "1.000"
            else:
                dir_arg1 = "0"
                dir_arg2 = "-1.000"

            print("3 2 0 " + str(width) + " " + str(color) + " 7 50 -1 -1 0.000 0 " + str(arrow_type) + " 3\n", file=self._out_fp)
            # arrow type
            if self._directed:
                print("1 1 3.00 90.00 150.00\n", file=self._out_fp)
            print("%s %s %s %s %s %s\n" % (x1, y1, x2, y2, x3, y3), file=self._out_fp)
            print("0.000 " + str(dir_arg2) + " 0.000\n", file=self._out_fp)

            numnodes = abs(self._nodes[u]["id"] - self._nodes[v]["id"])

    def printLink(self, link):

        if self._discrete > 0:
            self.__printDiscreteLink(link)
        else:
            self.__printContinuousLink(link)

    def __printContinuousLink(self, link):
        """
            Prints link (continuous case)
        """
        u = link["u"]
        v = link["v"]
        b = link["b"]
        e = link["e"]
        color = link["color"]
        curving = link["curving"]
        height = link["height"]
        width = link["width"]


        if color in self._colors:
            color = self._colors[color]["id"]

        if self._directed:
            if self._nodes[u]["id"] > self._nodes[v]["id"]:
                (u,v) = (v,u)
                arrow_type = "0 1"
            else:
                arrow_type = "1 0"
        else:
            if self._nodes[u]["id"] > self._nodes[v]["id"]:
                (u,v) = (v,u)
            arrow_type = "0 0"

        # Draw circles for u and v
        print("1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self._offset_x + int(b * self._time_unit)) + " " + str(self._offset_y + self._nodes[u]["id"]*self._node_unit) + " 45 45 -6525 -2025 -6480 -2025", file=self._out_fp)
        print("1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self._offset_x + int(b * self._time_unit)) + " " + str(self._offset_y + self._nodes[v]["id"]*self._node_unit) + " 45 45 -6525 -2025 -6480 -2025", file=self._out_fp)
        
        # Link them
        spline_coords = []

        if self._nodes[u]["id"] != self._nodes[v]["id"]:

            x1, y1 = self._offset_x + int(b * self._time_unit), self._offset_y + self._nodes[u]["id"]*self._node_unit
            x2 = self._offset_x + int((b + curving) * self._time_unit)
            y2 = int((self._offset_y + self._nodes[v]["id"]*self._node_unit) - 0.5 * (self._nodes[v]["id"]-self._nodes[u]["id"]) * self._node_unit) 
            x3 = self._offset_x + int(b * self._time_unit)
            y3 = self._offset_y + self._nodes[v]["id"]*self._node_unit
            spline_coords.append((x1, y1))
            spline_coords.append((x2, y2))
            spline_coords.append((x3, y3))
        else:
            # self loop case
            base_x, base_y = self._offset_x + int(b * self._time_unit), self._offset_y + self._nodes[u]["id"]*self._node_unit 
            spline_coords.append((base_x, base_y))            

            x, y = base_x + ( 0.5 * self._time_unit ), base_y - 0.25 * self._node_unit
            spline_coords.append((int(x), int(y)))    

            x, y = base_x, base_y - 0.5 * self._node_unit 
            spline_coords.append((int(x), int(y)))

            x, y = base_x - (0.5 * self._time_unit ), base_y - 0.25 * self._node_unit
            spline_coords.append((int(x), int(y)))

            x, y = base_x, base_y 
            spline_coords.append((x, y))     


        if self._directed:
            dir_arg1 = "1"
            dir_arg2 = "1.000"
        else:
            dir_arg1 = "0"
            dir_arg2 = "-1.000"
        
        print(f"3 2 0 {width} {color} 7 50 -1 -1 0.000 0 {arrow_type} {len(spline_coords)}", file=self._out_fp)

        # arrow type
        if self._directed:
            print("1 1 3.00 90.00 150.00", file=self._out_fp)
        
        # Print spline coordinates
        print(" ".join([ f"{x} {y}" for x,y in spline_coords ]), file=self._out_fp)

        # more arrow properties 
        print("0.000 " + str(dir_arg2) +" 0.000 1.000 0.000", file=self._out_fp)
        print("# end edge", file=self._out_fp)

        numnodes = abs(self._nodes[u]["id"] - self._nodes[v]["id"])

        # Add duration
        print("2 1 0 " + str(width) + " " + str(color) + " 7 50 -1 -1 0.000 0 0 -1 0 0 2", file=self._out_fp)
        print(str(self._offset_x + int((b + curving) * self._time_unit)) + " " + str(self._offset_y + int(self._nodes[u]["id"]*self._node_unit + (numnodes*self._node_unit*height))) + " " + str(self._offset_x + int(e * self._time_unit)) + " " + str(self._offset_y + self._nodes[v]["id"]*self._node_unit - (numnodes*self._node_unit*(1-height))), file=self._out_fp)


    def addNodeCluster(self, u, times=[], color=0, width=200):
        """
            Adds a node cluster (drawn as a rectangle) for one node over time.

            :param u: The node in the cluster
            :param times: The times at which u is in the cluster
            :param color: The color of the rectangle
            :param width: The width of the rectangle

            :type u: str
            :type times: list of tuples
            :type color: str/int
            :type width: int

            :Example:

            >>> # Create the blue node cluster {u}x[3,4] U {v}x[5,7.5] U {x}x[2,4]
            >>> d.addNodeCluster("u", [(3,4)], color=11)
            >>> d.addNodeCluster("v", [(5,7.5)], color=11)
            >>> d.addNodeCluster("x", [(2,4)], color=11)

        """
        nc = {
            "u": u,
            "times": times,
            "color": color,
            "width": width
        }
        self._node_clusters.append(nc)


    def printNodeCluster(self, nc):

        u = nc["u"]
        times = nc["times"]
        color = nc["color"]
        width = nc["width"]

        margin = int(width / 2)

        if color in self._colors:
            color = self._colors[color]["id"]  

        if len(times) == 0:
            times = [(self._alpha, self._omega)]

        for (i,j) in times:
            (x1, y1) = ( self._offset_x + int(i * self._time_unit), self._offset_y + int(self._nodes[u]["id"]*self._node_unit) - margin )
            (x2, y2) = ( self._offset_x + int(j * self._time_unit), self._offset_y + int(self._nodes[u]["id"]*self._node_unit) - margin ) 
            (x3, y3) = ( self._offset_x + int(j * self._time_unit), self._offset_y + int(self._nodes[u]["id"]*self._node_unit) + margin ) 
            (x4, y4) = ( self._offset_x + int(i*self._time_unit), self._offset_y + int(self._nodes[u]["id"]*self._node_unit) + margin ) 

            print("2 2 0 0 0 " + str(color) + " 51 -1 20 0.000 0 0 -1 0 0 5", file=self._out_fp)
            print(str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + " " + str(x3) + " " + str(y3) + " " + str(x4) + " " + str(y4) + " " + str(x1) + " " + str(y1), file=self._out_fp)

    def addParameter(self, letter, value, color=0, width=1):
        """
            Adds a parameter (like Delta=2). Multiple parameters will be placed at the top of the drawing, on each other's side 

            :param letter: The letter for the parameter, in ascii (will be translated in greek, i.e. d gives delta, m gives mu, etc.)
            :param value: The value for the parameter
            :param color: The color (see addColor())
            :param width: The interval's width

            :type letter: str
            :type value: float
            :type color: int/str
            :type width: int

            :Example:
            
            >>> # Adds a parameter delta with value 3
            >>> d.addParameter("d", 3)
        """

        self._parameters.append({
            "letter": letter,
            "value": value,
            "color": color,
            "width": width
        })


    def printParameter(self, p):
        letter = p["letter"]
        value = p["value"]
        color = p["color"]
        width = p["width"]

        if color in self._colors:
            color = self._colors[color]["id"]

        #?Place at top? Confusing with time intervals...
        pos_segment_y = self._offset_y + (self._nodes[self._first_node]["id"] * self._node_unit) - (150 * self._num_time_intervals) - 400
        # Place at bottom instead? Then needs to be written last.
        # pos_segment_y = self._offset_y + self._node_cpt * self._node_unit + 2*self._node_unit

        if self._num_parameters == 0:
            paramoffset = 0
        else:
            paramoffset = 200

        print("2 1 " + str(color) + " " + str(width) + " 0 7 50 -1 -1 0.000 0 0 -1 1 1 2", file=self._out_fp)
        print("13 1 1.00 60.00 120.00", file=self._out_fp)
        print("13 1 1.00 60.00 120.00", file=self._out_fp)
        print(str(self._offset_x + (self._totalval_parameters * self._time_unit  + (self._num_parameters * paramoffset))) + " " + str(pos_segment_y) + " " + str(self._offset_x + int(value * self._time_unit) + (self._totalval_parameters * self._time_unit + (self._num_parameters * paramoffset))) + " " + str(pos_segment_y), file=self._out_fp)

        valtocenter = int(value * self._time_unit / 2) - (200 + (50 * max(int(value) - 2, 0))) 

        print("4 0 0 50 -1 32 14 0.0000 4 180 375 " + str(self._offset_x + (self._totalval_parameters * self._time_unit + int(self._num_parameters * paramoffset)) + valtocenter)  + " " + str(pos_segment_y - 150)  + " " + str(letter) + " = " + str(value) + "\\001")
        self._totalval_parameters += value
        self._num_parameters += 1

    def addNodeIntervalMark(self, u, v, color=0, width=1):
        self._node_intervals.append({
            "u": u,
            "v": v,
            "color": color,
            "width": width
        })
        

    def printNodeIntervalMark(self, nim):
        u = nim["u"]
        v = nim["v"]
        color = nim["color"]
        width = nim["width"]

        if color in self._colors:
            color = self._colors[color]["id"]

        pos_segment_x = self._offset_x - (150 * self._num_node_intervals) - 600

        print(f"2 1 {color} {width} 0 7 50 -1 -1 0.000 0 0 -1 1 1 2", file=self._out_fp)
        print("13 1 1.00 60.00 120.00", file=self._out_fp)
        print("13 1 1.00 60.00 120.00", file=self._out_fp)
        print(f"{pos_segment_x} {self._offset_y + self._nodes[u]['id'] * self._node_unit}  {pos_segment_x} {self._offset_y + self._nodes[v]['id'] * self._node_unit}", file=self._out_fp)
        self._num_node_intervals += 1


    def addTimeNodeMark(self, t, v, color=0, width=2, depth=49):
        """
            Adds a mark (a cross) at a given node and time.

            :param t: The time at which to add the mark
            :param v: The node at which to add the mark
            :param color: The mark's color (see addColor())
            :param width: The mark's width
            :param depth: Layer for XFIG. Higher values will put the mark in the background, lower in the foreground.

            :type t: float
            :type v: str
            :type color: int/str
            :type width: int
            :type depth: int

            :Example:

            >>> d.addTimeNodeMark(2, "u", color=11, width=3)
        """
        if color in self._colors:
            color = self._colors[color]["id"]

        self._timenodemarks.append({
            "t": t,
            "v": v,
            "color": color,
            "width": width,
            "depth": depth
        })

    def printTimeNodeMark(self, tnm):

        t = tnm["t"]
        v = tnm["v"]
        color = tnm["color"]
        width = tnm["width"]
        depth = tnm["depth"]

        print("2 1 0 "+ str(width) + " " + str(color) + " 7 " + str(depth) + " -1 -1 0.000 0 0 -1 0 0 2", file=self._out_fp)
        print(str(self._offset_x + int(t * self._time_unit) - 50 ) + " " + str(self._offset_y + self._nodes[v]["id"] * self._node_unit - 50) + " " + str(self._offset_x + int(t * self._time_unit) + 50 ) + " " + str(self._offset_y + self._nodes[v]["id"] * self._node_unit + 50), file=self._out_fp)

        print("2 1 0 "+ str(width) + " " + str(color) + " 7 " + str(depth) + " -1 -1 0.000 0 0 -1 0 0 2", file=self._out_fp)
        print(str(self._offset_x + int(t * self._time_unit) - 50 ) + " " + str(self._offset_y + self._nodes[v]["id"] * self._node_unit + 50) + " " + str(self._offset_x + int(t * self._time_unit) + 50 ) + " " + str(self._offset_y + self._nodes[v]["id"] * self._node_unit - 50), file=self._out_fp)

    def addTimeIntervalMark(self, b, e, color=0, width=1):
        self._time_intervals.append({
            "b": b,
            "e": e,
            "color": color,
            "width": width
        })

    def printTimeIntervalMark(self, tim):
        b = tim["b"]
        e = tim["e"]
        color = tim["color"]
        width = tim["width"]

        pos_segment_y = self._offset_y + (self._nodes[self._first_node]["id"] * self._node_unit) - (100 * self._num_time_intervals) - 200

        print("2 1 0 1 0 7 50 -1 -1 0.000 0 0 -1 1 1 2", file=self._out_fp)
        print("13 1 1.00 60.00 120.00", file=self._out_fp)
        print("13 1 1.00 60.00 120.00", file=self._out_fp)
        print(str(self._offset_x + b * self._time_unit) + " " + str(pos_segment_y) + " " + str(self._offset_x + (e * self._time_unit)) + " " + str(pos_segment_y), file=self._out_fp)
        self._num_time_intervals += 1

    def addPath(self, path, start, end, gamma=0, color=0, width=1, depth=51):
        """
            Adds a temporal path from a sequence of (t,u,v) meaning that there was a hop from u to v at time t.

            :param path: A list of (t,u,v) that are the hops in the path
            :param start: The start time of the path
            :param end: The end time of the path
            :param gamma: Useful for gamma-path (if gamma > 0, the hops from u to v will take gamma time units)
            :param color: The path's color (see addColor())
            :param width: The path's width
            :param depth: Layer for XFIG. Higher values will put the mark in the background, lower in the foreground.

            :type path: list
            :type start: float
            :type end: float
            :type gamma: float
            :type color: int/str
            :type width: int
            :type depth: int

            :Example:

            >>> # Path from u to x from time 1 to time 9
            >>> d.addPath([(2,u,v), (5, v, x)], 1, 7)
            >>> # gamma=2-path from u to x from time 1 to time 9
            >>> d.addPath([(2,u,v), (5, v, x)], 1, 9, gamma=2)
        """

        if color in self._colors:
            color = self._colors[color]["id"]
        
        t0 = path[0][0]
        u0 = path[0][1]
        xi = self._offset_x + int(start * self._time_unit)
        yi = self._offset_y + self._nodes[u0]["id"] * self._node_unit
            
        xj = self._offset_x + int((t0) * self._time_unit) 
        yj = self._offset_y + self._nodes[u0]["id"] * self._node_unit


        coords = [(xi,yi), (xj,yj)]

        for (t,u,v) in path:
            xi = self._offset_x + int(t * self._time_unit)
            yi = self._offset_y + self._nodes[u]["id"] * self._node_unit
            
            xj = self._offset_x + int((t + gamma) * self._time_unit) 
            yj = self._offset_y + self._nodes[v]["id"] * self._node_unit
            
            coords.append((xi,yi))
            coords.append((xj,yj))

        tk = path[-1][0]
        vk = path[-1][2]
        xi = self._offset_x + int(tk * self._time_unit)
        yi = self._offset_y + self._nodes[vk]["id"] * self._node_unit
            
        xj = self._offset_x + int((end) * self._time_unit) 
        yj = self._offset_y + self._nodes[vk]["id"] * self._node_unit
        coords.append((xi,yi))
        coords.append((xj,yj))

        self._paths.append({
            "width": width,
            "color": color,
            "depth": depth,
            "coords": coords
            })

    def printPath(self, path):
        width, color, depth, coords = path["width"], path["color"], path["depth"], path["coords"]
        print(f"2 1 0 {width} {color} 7 {depth} -1 -1 0.000 0 0 -1 0 0 " + str(len(coords)), file=self._out_fp)
        print(" ".join([ " ".join(map(str, i)) for i in coords ] ), file=self._out_fp)

    def addRectangle(self, u, v, b, e, width=100, depth=51, color=0, border="", bordercolor=0, borderwidth=2):
        """
            Adds a rectangle from node u to node v and from time b to time e.
            The corners of the rectangle will be (u,b), (u,e), (v,b), (v,e)

            :param u: Start node
            :param v: End node
            :param b: Start time
            :param e: End time
            :param width: The rectangle's width (to add an offset)
            :param depth: Layer for XFIG. Higher values will put the mark in the background, lower in the foreground
            :param color: Background color (see addColor())
            :param border: If borders should be drawn, takes "lrtb" (for left, right, top, bottom) as arguments
            :param bordercolor: The border's color (see addColor())
            :param borderwidth: The border's width

            :type u: str
            :type v: str
            :type b: float
            :type e: float
            :type width: int
            :type depth: int
            :type color: int/str
            :type border: str
            :type bordercolor: int/str
            :type borderwidth: int

            :Example:

            >>> # Rectangle without border
            >>> d.addRectangle("u", "v", 2, 6, color=11) 
            >>> # Rectangle with border all around
            >>> d.addRectangle("u", "v", 2, 6, color=11, border="lrtb")
            >>> # Rectangle with borders except on top
            >>> d.addRectangle("u", "v", 2, 6, color=11, border="lrb")
        """

        self._rectangles.append(
            {
                "u": u,
                "v": v,
                "b": b,
                "e": e,
                "width": width,
                "depth": depth,
                "color": color,
                "border": border,
                "bordercolor": bordercolor,
                "borderwidth": borderwidth
            }        
        )

    def printRectangle(self, r):

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

        if color in self._colors:
            color = self._colors[color]["id"]
        if bordercolor in self._colors:
            bordercolor = self._colors[bordercolor]["id"]

        # Print border lrtb (if any)
        if "l" in border:
            print("2 1 0 " + str(borderwidth) + " " + str(bordercolor) + " 7 48 -1 -1 0.000 0 0 -1 0 0 2", file=self._out_fp)
            print(str(self._offset_x + int(b * self._time_unit)) + " " + str(self._offset_y + self._nodes[u]["id"] * self._node_unit - margin) + " " + str(self._offset_x + int(b * self._time_unit)) + " " + str(self._offset_y + self._nodes[v]["id"] * self._node_unit + margin) + "\n", file=self._out_fp)
        if "r" in border:
            print("2 1 0 " + str(borderwidth) + " " + str(bordercolor) + " 7 48 -1 -1 0.000 0 0 -1 0 0 2", file=self._out_fp)
            print(str(self._offset_x + int(e * self._time_unit)) + " " + str(self._offset_y + self._nodes[u]["id"] * self._node_unit - margin) + " " + str(self._offset_x + int(e * self._time_unit)) + " " + str(self._offset_y + self._nodes[v]["id"] * self._node_unit + margin) + "\n", file=self._out_fp)
        if "t" in border:
            print("2 1 0 " + str(borderwidth) + " " + str(bordercolor) + " 7 48 -1 -1 0.000 0 0 -1 0 0 2", file=self._out_fp)
            print(str(self._offset_x + int(b * self._time_unit)) + " " + str(self._offset_y + self._nodes[u]["id"] * self._node_unit - margin) + " " + str(self._offset_x + int(e * self._time_unit)) + " " + str(self._offset_y + self._nodes[u]["id"] * self._node_unit - margin), file=self._out_fp)
        if "b" in border:
            print("2 1 0 " + str(borderwidth) + " " + str(bordercolor) + " 7 48 -1 -1 0.000 0 0 -1 0 0 2", file=self._out_fp)
            print(str(self._offset_x + int(b * self._time_unit)) + " " + str(self._offset_y + self._nodes[v]["id"] * self._node_unit + margin) + " " + str(self._offset_x + int(e * self._time_unit)) + " " + str(self._offset_y + self._nodes[v]["id"] * self._node_unit + margin), file=self._out_fp)

        if color > -1:
            # Print rectangle
            print("2 2 0 0 0 " + str(color) + " " + str(depth) + " -1 20 0.000 0 0 -1 0 0 5", file=self._out_fp)
            print(str(self._offset_x + int(b * self._time_unit)) + " " + str(self._offset_y + int(self._nodes[u]["id"]*self._node_unit) - margin) + " " + str(self._offset_x + int(e * self._time_unit)) + " " + str(self._offset_y + int(self._nodes[u]["id"]*self._node_unit) - margin) + " " + str(self._offset_x + int(e * self._time_unit)) + " " + str(self._offset_y + int(self._nodes[v]["id"]*self._node_unit) + margin) + " " + str(self._offset_x + int(b*self._time_unit)) + " " + str(self._offset_y + int(self._nodes[v]["id"]*self._node_unit) + margin) + " " + str(self._offset_x + int(b*self._time_unit)) + " " + str(self._offset_y + int(self._nodes[u]["id"]*self._node_unit) - margin), file=self._out_fp )
        
        # self._out_fp.close()

    def addTime(self, t, label="", width=1, font=12, color=0):
        """
            Adds a vertical dotted line at a given time.

            :param t: the time at which the line will be drawn
            :param label: the label that will be displayed on top of the vertical line
            :param width: the line's width
            :param font: the label's font (in pt)
            :param color: the line's color (XFIG defined or user-defined, see addColor() )

            :Example:
        
            >>> # Adds a vertical line labelled "t" at time 2
            >>> d.addTime(2, "t")
        """

        if self._num_time_intervals == 0:
            self._num_time_intervals = 1

        if color in self._colors:
            color = self._colors[color]["id"]

        linetype = 1

        print("""2 1 """ + str(linetype) + """ """ + str(width) + """  """ + str(color) + """ 7 50 -1 -1 2.000 0 0 7 0 0 2\n \
          """ + str(self._offset_x + int(t * self._time_unit)) + """ """ + str(self._offset_y + int(2 * self._node_unit - 150)) + """ """ + str(self._offset_x + int(t * self._time_unit)) + """ """ + str(self._offset_y + int(self._node_cpt * self._node_unit + 300)))

        # Add label if any
        print("4 0 " + str(color) + " 50 -1 0 " + str(font) + " 0.0000 4 135 120 " + str(self._offset_x + int(t * self._time_unit) - (2 * font * len(label))) + " " + str(self._offset_y - 175 + int(2 * self._node_unit)) + " " + str(label) + "\\001")


    def addTimeLine(self, ticks=2, label="time", marks=None):
        self._timeline = {
            "display": True,
            "ticks": ticks,
            "label": label,
            "marks": []
        }
        

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

        ticks = self._timeline["ticks"]
        label = self._timeline["label"]
        marks = self._timeline["marks"]
        
        timeline_y = self._node_cpt * self._node_unit + int(self._node_unit / 2)
        
        vals = []
        i = self._alpha
        while i < self._omega:
            if (i).is_integer():
                vals.append((int(i),int(i)))
            else:
                vals.append((i,i))
            i = i+ticks
        
        if marks is not None:
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
        if self._discrete > 0:
            start, end = self._omega - 0.5, self._omega
        else:
            start, end = self._alpha, self._omega     

        print("2 1 0 1 0 7 50 -1 -1 0.000 0 0 -1 1 0 2", file=self._out_fp)
        print("1 1 1.00 60.00 120.00", file=self._out_fp)
        print(str(self._offset_x + int(start * self._time_unit)) + " " + str(self._offset_y + timeline_y) + " " + str(self._offset_x + int(end * self._time_unit)) + " " + str(self._offset_y + timeline_y), file=self._out_fp)

        # Time ticks
        for (i,j) in vals:
            print("2 1 0 1 0 7 50 -1 -1 0.000 0 0 -1 0 0 2", file=self._out_fp)
            print(str(self._offset_x + int(i * self._time_unit)) + " " + str(self._offset_y + timeline_y) + " " + str(self._offset_x + int(i * self._time_unit)) + " " + str(self._offset_y + timeline_y + 30), file=self._out_fp)
            if i < self._omega - 1:
                print("4 1 0 50 -1 0 20 0.0000 4 135 120 " + str(self._offset_x + int(i * self._time_unit)) + " " + str(self._offset_y + timeline_y + 250) + " " + str(j) + "\\001", file=self._out_fp)

        # Write "time"
        print("4 2 0 50 -1 0 20 0.0000 4 135 120 " + str(self._offset_x + int(self._omega * self._time_unit)) + " " + str(self._offset_y + timeline_y + 250) + " " + label + "\\001", file=self._out_fp)

    def save(self, out_file):
        """
            Save stream to fig representation
        """
        if not self._streaming:
            out_fp = open(out_file, "w+")
            self._out_fp = out_fp

            print(self._header, file=self._out_fp)
            
            self.printColors()

            if self._discrete:
                printNode = self.printDiscreteNode
            else:
                printNode = self.printContinuousNode

            for u in self._nodes:
                printNode(u)

            for link in self._links:
                self.printLink(link)

            for nc in self._node_clusters:
                self.printNodeCluster(nc)

            for p in self._paths:
                self.printPath(p)

            for tnm in self._timenodemarks:
                self.printTimeNodeMark(tnm)

            # Add white rectangle for padding
            self.addRectangle(self._first_node, self._first_node, self._alpha, self._omega, width=300,depth=60, color=7)
            for r in self._rectangles:
                self.printRectangle(r)

            for nim in self._node_intervals:
                self.printNodeIntervalMark(nim)

            for tim in self._time_intervals:
                self.printTimeIntervalMark(tim)

            for p in self._parameters:
                self.printParameter(p)

            if self._timeline["display"]:
                self.printTimeLine()



    def optimize(self):
        # Find better node order !
        NUM_ITER = 10000
        # Add some early stopping

        distance_sum = lambda x: sum(( abs(self._nodes[l["u"]]["id"] - self._nodes[l["v"]]["id"]) for l in x))

        old_distance_sum = distance_sum(self._links)
        orig_distance_sum = old_distance_sum
        import random

        for i in range(0, NUM_ITER):
            u, v = random.sample(self._nodes.keys(), 2)
            self._nodes[u], self._nodes[v] = self._nodes[v], self._nodes[u]
            new_arrangement_sum = distance_sum(self._links)

            if not new_arrangement_sum < old_distance_sum:
                # Revert permutation
                self._nodes[v], self._nodes[u] = self._nodes[u], self._nodes[v]
            else:
                # Update best score and keep permutation
                old_distance_sum = new_arrangement_sum

        print("%d %d (%d percent improvement) " % (orig_distance_sum, old_distance_sum, orig_distance_sum/old_distance_sum*100))

    def __del__(self):
        # Adds white rectangle in background around first node (for EPS bounding box)
        self._out_fp.close()

# main
if __name__ == '__main__':

    # s = Drawing()
    # s = Drawing(alpha=0, omega=10)
    s = Drawing(alpha=0, omega=10)

    s.addColor("grey", "#888888")
    s.addColor("red", "#ff0000")

    s.addNode("u")
    s.addNode("v")
    s.addNode("x")

    # s.addNodeCluster("u", [(0.5,2)], color=11, width=200)
    # s.addNodeCluster("v", color=11)
    s.addRectangle("u", "v", 4, 6, color=12)
    # s.addNodeCluster("u", [(6,7.5)], color="red")

    s.addLink("u", "v", 1.5, 6, curving=0.2)
    s.addLink("v", "x", 3, 5)

    s.addPath([(2, "u", "v"), (4, "v", "x")], 1, 9, width=5, color=11)

    # s.addLink("u", "v", 1, 4, height=0.25)
    # s.addLink("u", "v", 5, 7)
    # s.addLink("v", "x", 3, 4)

    # s.addTimeLine(ticks=2, marks=[(2, "a"), (2.5, "c"), (5, "t"), (6, "b")])
    s.addTimeLine(ticks=2)
