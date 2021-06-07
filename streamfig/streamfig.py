# -*- coding: utf-8 -*-
# TODO
# Nettoyage vieux code / Commentaires code
# Documentation
# Remplacer les print(...\n)
# Gestion des erreurs (noeud non ajoute...)

import sys
import streamfig.printers as printers

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

    _node_unit = 600
    _offset_x = 3450
    _offset_y = 2250
    
    _num_node_intervals = 0
    #?Is incremented by one if time marks are used too
    _num_time_intervals = 0
    _num_parameters = 0
    _totalval_parameters = 0

    _first_node = ""


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



    def __init__(self, alpha=0.0, omega=10.0, time_width=500, discrete=0, directed=False, streaming=False, printer=printers.FigPrinter):

        self._streaming = streaming
        self._printer = printer(self)

        self._alpha = float(alpha)
        self._omega = float(omega)
        self._time_unit = time_width
        self._discrete = discrete
        self._directed = directed

        self._nodes = {}
        self._nodes_ordered = []
        self._node_cpt = 1

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

        self.node_ordering = []
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
        self._nodes_ordered.append(u)


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
        self._nodes_ordered.append(u)
        
        if linetype is None:
            linetype = self.linetype
        self._nodes[u]["linetype"] = linetype


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



    def addNodeIntervalMark(self, u, v, color=0, width=1):
        self._node_intervals.append({
            "u": u,
            "v": v,
            "color": color,
            "width": width
        })
        
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

    def addTimeIntervalMark(self, b, e, color=0, width=1):
        self._time_intervals.append({
            "b": b,
            "e": e,
            "color": color,
            "width": width
        })


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


    def addTimeLine(self, ticks=2, label="time", marks=[]):
        self._timeline = {
            "display": True,
            "ticks": ticks,
            "label": label,
            "marks": marks
        }
        

    def save(self, out_file):
        """
            Save stream to fig representation
        """
        if not self._streaming:
            out_fp = open(out_file, "w+")
            self._out_fp = out_fp

            # Assign node IDs following node ordering (if any)
            if len(self.node_ordering) > 0:
                for i, u in enumerate(self.node_ordering): 
                    self._nodes[u]["id"] = i

            print(self._header, file=self._out_fp)
            
            self._printer.printColors()

            if self._discrete:
                printNode = self._printer.printDiscreteNode
            else:
                printNode = self._printer.printContinuousNode

            for u in self._nodes:
                printNode(u)

            for link in self._links:
                self._printer.printLink(link)

            for nc in self._node_clusters:
                self._printer.printNodeCluster(nc)

            for p in self._paths:
                self._printer.printPath(p)

            for tnm in self._timenodemarks:
                self._printer.printTimeNodeMark(tnm)

            # Adds white rectangle in background around first node (for bounding box)
            self.addRectangle(self._first_node, self._first_node, self._alpha, self._omega, width=300,depth=60, color=7)
            for r in self._rectangles:
                self._printer.printRectangle(r)

            for nim in self._node_intervals:
                self._printer.printNodeIntervalMark(nim)

            for tim in self._time_intervals:
                self._printer.printTimeIntervalMark(tim)

            for p in self._parameters:
                self._printer.printParameter(p)

            if self._timeline["display"]:
                self._printer.printTimeLine()



    def optimize(self):
        self.node_ordering = list(self._nodes.keys()).copy() # Take source file order as basis
        # Find better node order !
        NUM_ITER = 100000
        # Add some early stopping

        distance_sum = lambda x: sum(( abs(self.node_ordering.index(l["u"]) - self.node_ordering.index(l["v"])) for l in x))

        old_distance_sum = distance_sum(self._links)
        orig_distance_sum = old_distance_sum
        import random

        for i in range(0, NUM_ITER):
            ix_u, ix_v = random.sample(range(0, len(self.node_ordering)), k=2)
            self.node_ordering[ix_u], self.node_ordering[ix_v] = self.node_ordering[ix_v], self.node_ordering[ix_u]
            new_arrangement_sum = distance_sum(self._links)

            if not new_arrangement_sum < old_distance_sum:
                # Revert permutation
                self.node_ordering[ix_v], self.node_ordering[ix_u] = self.node_ordering[ix_u], self.node_ordering[ix_v]
            else:
                # Update best score and keep permutation
                old_distance_sum = new_arrangement_sum

        print("%d %d (%d percent improvement) " % (orig_distance_sum, old_distance_sum, orig_distance_sum/old_distance_sum*100))

    def __del__(self):
        self._out_fp.close()
