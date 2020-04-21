# coding: utf-8
# TODO
# Nettoyage vieux code / Commentaires code
# Documentation
# Remplacer les print(...\n)
# Gestion des erreurs (noeud non ajouté...)

import sys


def drange(start, stop, step):
    r = start
    while r <= stop:
        yield r
        r += step

class Drawing:

    alpha = 0.0
    omega = 0.0
    discrete = -1

    time_unit = 500
    node_unit = 600
    offset_x = 3450
    offset_y = 2250
    
    num_node_intervals = 0
    # Is incremented by one if time marks are used too
    num_time_intervals = 0
    num_parameters = 0
    totalval_parameters = 0

    first_node = ""

    nodes = {}
    node_cpt = 1

    colors = {}
    color_cpt = 31

    def __init__(self, alpha=0.0, omega=10.0, time_width=500, discrete=0, stdout_print=False):
        self.stdout_print = stdout_print
        self.fig_buffer = ""

        header = """#FIG 3.2  Produced by xfig version 3.2.5b\n\
Landscape\n\
Center\n\
Inches\n\
Letter\n\
100.00\n\
Single\n\
-2\n\
1200 2\n"""
        
        self.fig_buffer += header + '\n'
        if self.stdout_print:
            print(header)

        self.alpha = float(alpha)
        self.omega = float(omega)
        self.time_unit = time_width
        self.discrete = discrete

        self.linetype = 2
        self.bar_min_size = None
        self.bar_min_x0 = None

        # Useful predefined colors
        self.addColor("grey", "#888888")



    def setLineType(def_linetype):
        self.linetype = def_linetype

    def addColor(self, name, hex):
        self.color_cpt += 1
        self.colors[name] = self.color_cpt

        color = "0 " + str(self.color_cpt) + " " + str(hex)
        self.fig_buffer += color + '\n'
        if self.stdout_print:
            print(color)


    def addNode(self, u, times=[], color=0, linetype=None):
        if self.discrete > 0:
            self.addDiscreteNode(u, times, color)
        else:
            self.addContinuousNode(u, times, color, linetype)

    def addDiscreteNode(self, u, times=[], color="grey", width=1):

        if color in self.colors:
            color = self.colors[color]

        if self.node_cpt == 1:
            self.first_node = u

        self.node_cpt += 1
        self.nodes[u] = self.node_cpt

        node = "4 0 " + str(color) + " 50 -1 0 30 0.0000 4 135 120 " + str(self.offset_x + int(self.alpha * self.time_unit) - 400) + " " + str(self.offset_y + 125 + int(self.node_cpt * self.node_unit)) + " " + str(u) + "\\001"
        self.fig_buffer += node + '\n'
        if self.stdout_print:
            print(node)

        
        if len(times) == 0:
            for i in drange(self.alpha, self.omega, self.discrete):
                node = "1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self.offset_x + int(i * self.time_unit)) + " " + str(self.offset_y + self.nodes[u]*self.node_unit) + " 45 45 -6525 -2025 -6480 -2025"
                self.fig_buffer += node + '\n'
                if self.stdout_print:
                    print(node)
        else:
            for (i,j) in times:
                for x in drange(i, j, self.discrete):
                    node = "1 3 0 " + str(width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self.offset_x + int(x * self.time_unit)) + " " + str(self.offset_y + self.nodes[u]*self.node_unit) + " 45 45 -6525 -2025 -6480 -2025"
                    self.fig_buffer += node + '\n'
                    if self.stdout_print:
                        print(node)



    def addContinuousNode(self, u, times=[], color=0, linetype=None):
        """ nodeId : identifiant du noeud
            times : suite d'intervalles de temps ou le noeud est actif
        """

        if linetype is None:
            linetype = self.linetype

        if color in self.colors:
            color = self.colors[color]

        if self.node_cpt == 1:
            self.first_node = u

        self.node_cpt += 1
        self.nodes[u] = self.node_cpt

        node = "4 0 " + str(color) + " 50 -1 0 30 0.0000 4 135 120 " + str(self.offset_x + int(self.alpha * self.time_unit) - 400) + " " + str(self.offset_y + 125 + int(self.node_cpt * self.node_unit)) + " " + str(u) + "\\001"
        self.fig_buffer += node + '\n'
        if self.stdout_print:
            print(node)

        if len(times) == 0:
            node = """2 1 """ + str(linetype) + """ 2 """ + str(color) + """ 7 50 -1 -1 6.000 0 0 7 0 0 2\n \
          """ + str(self.offset_x + int(self.alpha * self.time_unit)) + """ """ + str(self.offset_y + int(self.node_cpt * self.node_unit)) + """ """ + str(self.offset_x + int(self.omega * self.time_unit)) + """ """ + str(self.offset_y + int(self.node_cpt * self.node_unit))
            self.fig_buffer += node + '\n'
            if self.stdout_print:
                print(node)

        else:
            for (i,j) in times:
                node = """2 1 """ + str(linetype) + """ 2 """ + str(color) + """ 7 50 -1 -1 6.000 0 0 7 0 0 2\n \
          """ + str(self.offset_x + int(i* self.time_unit)) + """ """ + str(self.offset_y + int(self.node_cpt * self.node_unit)) + """ """ + str(self.offset_x + int(j * self.time_unit)) + """ """ + str(self.offset_y + int(self.node_cpt * self.node_unit))
                self.fig_buffer += node + '\n'
                if self.stdout_print:
                    print(node)

    def addLink(self, u, v, b, e, curving=0.0, color=0, height=0.5, width=None, anchor_width=3, link_width=3, loop_size=3):
        if self.discrete > 0:
            self.addDiscreteLink(u, v, b, e, curving=curving, color=color, height=height, width=width, anchor_width=anchor_width, link_width=link_width, loop_size=loop_size)
        else:
            self.addContinuousLink(u, v, b, e, curving=curving, color=color, height=height, width=width, anchor_width=anchor_width, link_width=link_width, loop_size=loop_size)

    def addNodeValue(self, u, t=-1.5, color=0, size=3, glyph="rectangle", bar_width=10, depth=49):
        if color in self.colors:
            color = self.colors[color]

        if glyph == "circle":
            # Draw circle
            anchor = "1 3 0 " + str(size) + " " + str(color) + " " + str(color) + " " + str(depth) + " -1 20 0.000 1 0.0000 " + str(self.offset_x + int(t * self.time_unit)) + " " + str(self.offset_y + self.nodes[u]*self.node_unit) + " 45 45 -6525 -2025 -6480 -2025"
            self.fig_buffer += anchor + '\n'
            if self.stdout_print:
                print(anchor)

        if glyph == "rectangle":
            margin = int(30*size/2)

            if color in self.colors:
                color = self.colors[color]

            if color > -1:
                #x = 1
                # Print rectangle
                rectangle = "2 2 0 0 0 " + str(color) + " " + str(depth) + " -1 20 0.000 0 0 -1 0 0 5"


                self.fig_buffer += rectangle + '\n'
                if self.stdout_print:
                    print(rectangle)

                x_center = self.offset_x + int(t * self.time_unit)
                y_center = self.offset_y + int(self.nodes[u]*self.node_unit)

                rectangle =  str(x_center - margin) + " " + str(y_center - margin) + " " 
                rectangle += str(x_center + margin) + " " + str(y_center - margin) + " " 
                rectangle += str(x_center + margin) + " " + str(y_center + margin) + " " 
                rectangle += str(x_center - margin) + " " + str(y_center + margin) + " " 
                rectangle += str(x_center - margin) + " " + str(y_center - margin) + " "
                
                self.fig_buffer += rectangle + '\n'
                if self.stdout_print:
                   print(rectangle)

        if glyph == "bar":
            size = int(10*size)
            bar_width = int(10*bar_width)

            if color in self.colors:
                color = self.colors[color]

            if color > -1:
                #x = 1
                # Print rectangle
                rectangle = "2 2 0 0 0 " + str(color) + " " + str(depth) + " -1 20 0.000 0 0 -1 0 0 5"


                self.fig_buffer += rectangle + '\n'
                if self.stdout_print:
                    print(rectangle)

                x_0 = self.offset_x + int(t * self.time_unit)
                y_0 = self.offset_y + int(self.nodes[u]*self.node_unit)

                if t < 0:
                    if not self.bar_min_size or x_0 - size < self.bar_min_size:
                        self.bar_min_size = x_0 - size 
                        self.bar_min_x0 = x_0

                    rectangle =  str(x_0) + " " + str(y_0 - bar_width) + " " 
                    rectangle += str(x_0 - size) + " " + str(y_0 - bar_width) + " " 
                    rectangle += str(x_0 - size) + " " + str(y_0 + bar_width) + " " 
                    rectangle += str(x_0) + " " + str(y_0 + bar_width) + " " 
                    rectangle += str(x_0) + " " + str(y_0 - bar_width) + " "
                else:
                    rectangle =  str(x_0 - int(bar_width/2)) + " " + str(y_0) + " " 
                    rectangle += str(x_0 + int(bar_width/2)) + " " + str(y_0) + " " 
                    rectangle += str(x_0 + int(bar_width/2)) + " " + str(y_0 - size) + " " 
                    rectangle += str(x_0 - int(bar_width/2)) + " " + str(y_0 - size) + " " 
                    rectangle += str(x_0 - int(bar_width/2)) + " " + str(y_0) + " "

                self.fig_buffer += rectangle + '\n'
                if self.stdout_print:
                   print(rectangle)


    def addDiscreteLink(self, u, v, b, e, curving=0.0, color=0, height=0.5, width=None, link_width=3, anchor_width=3):
        if width:
            # deprecated usage of width, maybe signal
            link_width = width
            anchor_width = width

        if color in self.colors:
            color = self.colors[color]
        if self.nodes[u] > self.nodes[v]:
            (u,v) = (v,u)
        for i in drange(b,e, self.discrete):
            # Draw circles for u and v
            anchor = "1 3 0 " + str(anchor_width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self.offset_x + int(i * self.time_unit)) + " " + str(self.offset_y + self.nodes[u]*self.node_unit) + " 45 45 -6525 -2025 -6480 -2025"
            self.fig_buffer += anchor + '\n'
            if self.stdout_print:
                print(anchor)

            anchor = "1 3 0 " + str(anchor_width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self.offset_x + int(i * self.time_unit)) + " " + str(self.offset_y + self.nodes[v]*self.node_unit) + " 45 45 -6525 -2025 -6480 -2025"
            self.fig_buffer += anchor + '\n'
            if self.stdout_print:
                print(anchor)
                      

            # Link them
            x1, y1 = self.offset_x + int(i * self.time_unit), self.offset_y + self.nodes[u]*self.node_unit
            x2 = self.offset_x + int((i + curving) * self.time_unit)
            y2 = int((self.offset_y + self.nodes[v]*self.node_unit) - 0.5 * (self.nodes[v]-self.nodes[u]) * self.node_unit) 
            x3 = self.offset_x + int(i * self.time_unit)
            y3 = self.offset_y + self.nodes[v]*self.node_unit

            link = "3 2 0 " + str(link_width) + " " + str(color) + " 7 50 -1 -1 0.000 0 0 0 3\n"
            self.fig_buffer += link
            if self.stdout_print:
                sys.stdout.write(link)

            link = "%s %s %s %s %s %s\n" % (x1, y1, x2, y2, x3, y3)
            self.fig_buffer += link
            if self.stdout_print:
                sys.stdout.write(link)

            link = "0.000 -1.000 0.000\n"
            self.fig_buffer += link
            if self.stdout_print:
                sys.stdout.write(link)

            numnodes = abs(self.nodes[u] - self.nodes[v])


    def addContinuousLink(self, u, v, b, e, curving=0.0, color=0, height=0.5, width=None, link_width=3, anchor_width=3, loop_size=3):
        if width:
            # deprecated usage of width, maybe signal
            link_width = width
            anchor_width = width

        if color in self.colors:
            color = self.colors[color]
        if self.nodes[u] > self.nodes[v]:
            (u,v) = (v,u)

        # Draw circles for u and v
        anchor = "1 3 0 " + str(anchor_width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self.offset_x + int(b * self.time_unit)) + " " + str(self.offset_y + self.nodes[u]*self.node_unit) + " 45 45 -6525 -2025 -6480 -2025"
        self.fig_buffer += anchor + '\n'
        if self.stdout_print:
            print(anchor)

        anchor = "1 3 0 " + str(anchor_width) + " " + str(color) + " " + str(color) + " 49 -1 20 0.000 1 0.0000 " + str(self.offset_x + int(b * self.time_unit)) + " " + str(self.offset_y + self.nodes[v]*self.node_unit) + " 45 45 -6525 -2025 -6480 -2025"
        self.fig_buffer += anchor + '\n'
        if self.stdout_print:
            print(anchor)


        if v == u:
            node_x = self.offset_x + int(b * self.time_unit)
            node_y = self.offset_y + self.nodes[v] * self.node_unit
            #print ("loop ",node_x,node_y)

            loop ='3 0 2 '+str(link_width)+' '+str(color)+' 0 10 0 -1 0 0 0 0 '+str(4)+'\n'
            loop_size *= 100
            loop += str(node_x)+" "+str(node_y)+" "
            loop += str(node_x+int(loop_size/2))+" "+str(node_y+int(loop_size/3))+" "
            loop += str(node_x+int(loop_size/2))+" "+str(node_y-int(loop_size/3))+" "
            loop += str(node_x)+" "+str(node_y)
            loop += "\n"
            loop += "1 -1 -1 -1 -1 1\n"

            self.fig_buffer += loop + "\n"
            #print(loop)
            if self.stdout_print:
                print(loop)
        
        # Link them
        x1, y1 = self.offset_x + int(b * self.time_unit), self.offset_y + self.nodes[u]*self.node_unit
        x2 = self.offset_x + int((b + curving) * self.time_unit)
        y2 = int((self.offset_y + self.nodes[v]*self.node_unit) - 0.5 * (self.nodes[v]-self.nodes[u]) * self.node_unit) 
        x3 = self.offset_x + int(b * self.time_unit)
        y3 = self.offset_y + self.nodes[v]*self.node_unit

        link = "3 2 0 " + str(link_width) + " " + str(color) + " 7 50 -1 -1 0.000 0 0 0 3\n"
        self.fig_buffer += link
        if self.stdout_print:
            sys.stdout.write(link)
        link = "%s %s %s %s %s %s\n" % (x1, y1, x2, y2, x3, y3)
        self.fig_buffer += link
        if self.stdout_print:
            sys.stdout.write(link)
        link = "0.000 -1.000 0.000\n"
        self.fig_buffer += link
        if self.stdout_print:
            sys.stdout.write(link)

        numnodes = abs(self.nodes[u] - self.nodes[v])

        # Add duration
        duration = "2 1 0 " + str(link_width) + " " + str(color) + " 7 50 -1 -1 0.000 0 0 -1 0 0 2"
        self.fig_buffer += duration + '\n'
        if self.stdout_print:
            print(duration)

        dx0 = self.offset_x + int((b + curving) * self.time_unit)
        dy = self.offset_y + int(self.nodes[u]*self.node_unit + (numnodes*self.node_unit*height))

        if u == v:
            dx0 += int(loop_size/2)
            dy += int(2*(height-0.5) * loop_size/3)

        duration = str(dx0) + " " + str(dy) + " " + str(self.offset_x + int(e * self.time_unit)) + " " + str(dy)
        self.fig_buffer += duration + '\n'
        if self.stdout_print:
            print(duration)

    def addNodeCluster(self, u, times=[], color=0, width=200):

        margin = int(width / 2)

        if color in self.colors:
            color = self.colors[color]        

        if len(times) == 0:
            times = [(self.alpha, self.omega)]

        for (i,j) in times:
            (x1, y1) = ( self.offset_x + int(i * self.time_unit), self.offset_y + int(self.nodes[u]*self.node_unit) - margin )
            (x2, y2) = ( self.offset_x + int(j * self.time_unit), self.offset_y + int(self.nodes[u]*self.node_unit) - margin ) 
            (x3, y3) = ( self.offset_x + int(j * self.time_unit), self.offset_y + int(self.nodes[u]*self.node_unit) + margin ) 
            (x4, y4) = ( self.offset_x + int(i*self.time_unit), self.offset_y + int(self.nodes[u]*self.node_unit) + margin ) 

            cluster = "2 2 0 0 0 " + str(color) + " 51 -1 20 0.000 0 0 -1 0 0 5"
            self.fig_buffer += cluster + '\n'
            if self.stdout_print:
                print(cluster)

            cluster = str(x1) + " " + str(y1) + " " + str(x2) + " " + str(y2) + " " + str(x3) + " " + str(y3) + " " + str(x4) + " " + str(y4) + " " + str(x1) + " " + str(y1)
            self.fig_buffer += cluster + '\n'
            if self.stdout_print:
                print(cluster)

    def addParameter(self, letter, value, color=0, width=1):
        if color in self.colors:
            color = self.colors[color]

        # Place at top? Confusing with time intervals...
        pos_segment_y = self.offset_y + (self.nodes[self.first_node] * self.node_unit) - (150 * self.num_time_intervals) - 400
        # Place at bottom instead? Then needs to be written last.
        # pos_segment_y = self.offset_y + self.node_cpt * self.node_unit + 2*self.node_unit

        if self.num_parameters == 0:
            paramoffset = 0
        else:
            paramoffset = 200

        parameter = "2 1 " + str(color) + " " + str(width) + " 0 7 50 -1 -1 0.000 0 0 -1 1 1 2"
        self.fig_buffer += parameter + '\n'
        if self.stdout_print:
            print(parameter)
        parameter = "13 1 1.00 60.00 120.00"
        self.fig_buffer += parameter + '\n'
        if self.stdout_print:
            print(parameter)
        parameter = "13 1 1.00 60.00 120.00"
        self.fig_buffer += parameter + '\n'
        if self.stdout_print:
            print(parameter)
        parameter = str(self.offset_x + (self.totalval_parameters * self.time_unit  + (self.num_parameters * paramoffset))) + " " + str(pos_segment_y) + " " + str(self.offset_x + int(value * self.time_unit) + (self.totalval_parameters * self.time_unit + (self.num_parameters * paramoffset))) + " " + str(pos_segment_y)
        self.fig_buffer += parameter + '\n'
        if self.stdout_print:
            print(parameter)

        valtocenter = int(value * self.time_unit / 2) - (200 + (50 * max(int(value) - 2, 0))) 

        parameter = "4 0 0 50 -1 32 14 0.0000 4 180 375 " + str(self.offset_x + (self.totalval_parameters * self.time_unit + int(self.num_parameters * paramoffset)) + valtocenter)  + " " + str(pos_segment_y - 150)  + " " + str(letter) + " = " + str(value) + "\\001"
        self.fig_buffer += parameter + '\n'
        if self.stdout_print:
            print(parameter)

        self.totalval_parameters += value
        self.num_parameters += 1

    def addNodeIntervalMark(self, u, v, color=0, width=1):
        if color in self.colors:
            color = self.colors[color]

        pos_segment_x = self.offset_x - (150 * self.num_node_intervals) - 600

        node_interval_mark = "2 1 " + str(color) + " " + str(width) + " 0 7 50 -1 -1 0.000 0 0 -1 1 1 2"
        self.fig_buffer += node_interval_mark + '\n'
        if self.stdout_print:
            print(node_interval_mark)

        node_interval_mark = "13 1 1.00 60.00 120.00"
        self.fig_buffer += node_interval_mark + '\n'
        if self.stdout_print:
            print(node_interval_mark)

        node_interval_mark = "13 1 1.00 60.00 120.00"
        self.fig_buffer += node_interval_mark + '\n'
        if self.stdout_print:
            print(node_interval_mark)

        node_interval_mark = str(pos_segment_x) + " " + str(self.offset_y + self.nodes[u] * self.node_unit) + " " + str(pos_segment_x) + " " + str(self.offset_y + self.nodes[v] * self.node_unit)
        self.fig_buffer += node_interval_mark + '\n'
        if self.stdout_print:
            print(node_interval_mark)

        self.num_node_intervals += 1


    def addTimeNodeMark(self, t, v, color=0, width=2, depth=49):
        if color in self.colors:
            color = self.colors[color]

        time_node_mark = "2 1 0 "+ str(width) + " " + str(color) + " 7 " + str(depth) + " -1 -1 0.000 0 0 -1 0 0 2"
        self.fig_buffer += time_node_mark + '\n'
        if self.stdout_print:
            print(time_node_mark)

        time_node_mark = str(self.offset_x + int(t * self.time_unit) - 50 ) + " " + str(self.offset_y + self.nodes[v]*self.node_unit - 50) + " " + str(self.offset_x + int(t * self.time_unit) + 50 ) + " " + str(self.offset_y + self.nodes[v]*self.node_unit + 50)
        self.fig_buffer += time_node_mark + '\n'
        if self.stdout_print:
            print(time_node_mark)

        time_node_mark = "2 1 0 "+ str(width) + " " + str(color) + " 7 " + str(depth) + " -1 -1 0.000 0 0 -1 0 0 2"
        self.fig_buffer += time_node_mark + '\n'
        if self.stdout_print:
            print(time_node_mark)

        time_node_mark = str(self.offset_x + int(t * self.time_unit) - 50 ) + " " + str(self.offset_y + self.nodes[v]*self.node_unit + 50) + " " + str(self.offset_x + int(t * self.time_unit) + 50 ) + " " + str(self.offset_y + self.nodes[v]*self.node_unit - 50)
        self.fig_buffer += time_node_mark + '\n'
        if self.stdout_print:
            print(time_node_mark)

    def addTimeIntervalMark(self, b, e, color=0, width=1):
        pos_segment_y = self.offset_y + (self.nodes[self.first_node] * self.node_unit) - (100 * self.num_time_intervals) - 200

        time_interval_mark = "2 1 0 1 0 7 50 -1 -1 0.000 0 0 -1 1 1 2"
        self.fig_buffer += time_interval_mark + '\n'
        if self.stdout_print:
            print(time_interval_mark)

        time_interval_mark = "13 1 1.00 60.00 120.00"
        self.fig_buffer += time_interval_mark + '\n'
        if self.stdout_print:
            print(time_interval_mark)

        time_interval_mark = "13 1 1.00 60.00 120.00"
        self.fig_buffer += time_interval_mark + '\n'
        if self.stdout_print:
            print(time_interval_mark)

        time_interval_mark = str(self.offset_x + b * self.time_unit) + " " + str(pos_segment_y) + " " + str(self.offset_x + (e * self.time_unit)) + " " + str(pos_segment_y)
        self.fig_buffer += time_interval_mark + '\n'
        if self.stdout_print:
            print(time_interval_mark)

        self.num_time_intervals += 1

    def addPath(self, path, start, end, gamma=0, color=0, width=1, depth=51):

        if color in self.colors:
            color = self.colors[color]
        
        t0 = path[0][0]
        u0 = path[0][1]
        xi = self.offset_x + int(start * self.time_unit)
        yi = self.offset_y + self.nodes[u0] * self.node_unit
            
        xj = self.offset_x + int((t0) * self.time_unit) 
        yj = self.offset_y + self.nodes[u0] * self.node_unit


        coords = [(xi,yi), (xj,yj)]

        for (t,u,v) in path:
            xi = self.offset_x + int(t * self.time_unit)
            yi = self.offset_y + self.nodes[u] * self.node_unit
            
            xj = self.offset_x + int((t + gamma) * self.time_unit) 
            yj = self.offset_y + self.nodes[v] * self.node_unit
            
            coords.append((xi,yi))
            coords.append((xj,yj))

        tk = path[-1][0]
        vk = path[-1][2]
        xi = self.offset_x + int(tk * self.time_unit)
        yi = self.offset_y + self.nodes[vk] * self.node_unit
            
        xj = self.offset_x + int((end) * self.time_unit) 
        yj = self.offset_y + self.nodes[vk] * self.node_unit
        coords.append((xi,yi))
        coords.append((xj,yj))

        path = "2 1 0 " + str(width) + " " + str(color) + " 7 " + str(depth) + " -1 -1 0.000 0 0 -1 0 0 " + str(len(coords))
        self.fig_buffer += path + '\n'
        if self.stdout_print:
            print(path)

        path = " ".join([ " ".join(map(str, i)) for i in coords ] )
        self.fig_buffer += path + '\n'
        if self.stdout_print:
            print(path)

    def addRectangle(self, u, v, b, e, width=100, depth=51, color=0, border="", bordercolor=0, borderwidth=2):
        
        margin = int(width/2)

        if color in self.colors:
            color = self.colors[color]
        if bordercolor in self.colors:
            bordercolor = self.colors[bordercolor]

        # Print border lrtb (if any)
        if "l" in border:
            rectangle = "2 1 0 " + str(borderwidth) + " " + str(bordercolor) + " 7 48 -1 -1 0.000 0 0 -1 0 0 2"
            self.fig_buffer += rectangle + '\n'
            if self.stdout_print:
                print(rectangle)

            rectangle = str(self.offset_x + int(b * self.time_unit)) + " " + str(self.offset_y + self.nodes[u] * self.node_unit - margin) + " " + str(self.offset_x + int(b * self.time_unit)) + " " + str(self.offset_y + self.nodes[v] * self.node_unit + margin) + "\n"
            self.fig_buffer += rectangle + '\n'
            if self.stdout_print:
                print(rectangle)

        if "r" in border:
            rectangle = "2 1 0 " + str(borderwidth) + " " + str(bordercolor) + " 7 48 -1 -1 0.000 0 0 -1 0 0 2"
            self.fig_buffer += rectangle + '\n'
            if self.stdout_print:
                print(rectangle)

            rectangle = str(self.offset_x + int(e * self.time_unit)) + " " + str(self.offset_y + self.nodes[u] * self.node_unit - margin) + " " + str(self.offset_x + int(e * self.time_unit)) + " " + str(self.offset_y + self.nodes[v] * self.node_unit + margin) + "\n"
            self.fig_buffer += rectangle + '\n'
            if self.stdout_print:
                print(rectangle)

        if "t" in border:
            rectangle = "2 1 0 " + str(borderwidth) + " " + str(bordercolor) + " 7 48 -1 -1 0.000 0 0 -1 0 0 2"
            self.fig_buffer += rectangle + '\n'
            if self.stdout_print:
                print(rectangle)

            rectangle = str(self.offset_x + int(b * self.time_unit)) + " " + str(self.offset_y + self.nodes[u] * self.node_unit - margin) + " " + str(self.offset_x + int(e * self.time_unit)) + " " + str(self.offset_y + self.nodes[u] * self.node_unit - margin)
            self.fig_buffer += rectangle + '\n'
            if self.stdout_print:
                print(rectangle)

        if "b" in border:
            rectangle = "2 1 0 " + str(borderwidth) + " " + str(bordercolor) + " 7 48 -1 -1 0.000 0 0 -1 0 0 2"
            self.fig_buffer += rectangle + '\n'
            if self.stdout_print:
                print(rectangle)

            rectangle = str(self.offset_x + int(b * self.time_unit)) + " " + str(self.offset_y + self.nodes[v] * self.node_unit + margin) + " " + str(self.offset_x + int(e * self.time_unit)) + " " + str(self.offset_y + self.nodes[v] * self.node_unit + margin)
            self.fig_buffer += rectangle + '\n'
            if self.stdout_print:
                print(rectangle)

        if color > -1:
            # Print rectangle
            rectangle = "2 2 0 0 0 " + str(color) + " " + str(depth) + " -1 20 0.000 0 0 -1 0 0 5"
            self.fig_buffer += rectangle + '\n'
            if self.stdout_print:
                print(rectangle)

            rectangle = str(self.offset_x + int(b * self.time_unit)) + " " + str(self.offset_y + int(self.nodes[u]*self.node_unit) - margin) + " " + str(self.offset_x + int(e * self.time_unit)) + " " + str(self.offset_y + int(self.nodes[u]*self.node_unit) - margin) + " " + str(self.offset_x + int(e * self.time_unit)) + " " + str(self.offset_y + int(self.nodes[v]*self.node_unit) + margin) + " " + str(self.offset_x + int(b*self.time_unit)) + " " + str(self.offset_y + int(self.nodes[v]*self.node_unit) + margin) + " " + str(self.offset_x + int(b*self.time_unit)) + " " + str(self.offset_y + int(self.nodes[u]*self.node_unit) - margin)
            self.fig_buffer += rectangle + '\n'
            if self.stdout_print:
                print(rectangle)

    def addTime(self, t, label="", width=1, font=12, color=0):
        # Possibilite de changer le type de ligne, la couleur, etc.
        if self.num_time_intervals == 0:
            self.num_time_intervals = 1

        if color in self.colors:
            color = self.colors[color]

        linetype = 1

        time = """2 1 """ + str(linetype) + """ """ + str(width) + """  """ + str(color) + """ 7 50 -1 -1 2.000 0 0 7 0 0 2\n \
          """ + str(self.offset_x + int(t * self.time_unit)) + """ """ + str(self.offset_y + int(2 * self.node_unit - 150)) + """ """ + str(self.offset_x + int(t * self.time_unit)) + """ """ + str(self.offset_y + int(self.node_cpt * self.node_unit + 300))
        self.fig_buffer += time + '\n'
        if self.stdout_print:
            print(time)

        # Add label if any
        time = "4 0 " + str(color) + " 50 -1 0 " + str(font) + " 0.0000 4 135 120 " + str(self.offset_x + int(t * self.time_unit) - (2 * font * len(label))) + " " + str(self.offset_y - 175 + int(2 * self.node_unit)) + " " + str(label) + "\\001"
        self.fig_buffer += time + '\n'
        if self.stdout_print:
            print(time)

    def addTimeLine(self, ticks=1, marks=None, histogram=None, histogram_label=None, font_size=15):
        timeline_y = self.node_cpt * self.node_unit + int(self.node_unit / 2)
        
        vals = []
        i = self.alpha
        while i < self.omega:
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
        if self.discrete > 0:
            start, end = self.omega - 0.5, self.omega
        else:
            start, end = self.alpha, self.omega     

        timeline = "2 1 0 1 0 7 50 -1 -1 0.000 0 0 -1 1 0 2"
        self.fig_buffer += timeline + '\n'
        if self.stdout_print:
            print(timeline)

        timeline = "1 1 1.00 60.00 120.00"
        self.fig_buffer += timeline + '\n'
        if self.stdout_print:
            print(timeline)

        timeline = str(self.offset_x + int(start * self.time_unit)) + " " + str(self.offset_y + timeline_y) + " " + str(self.offset_x + int(end * self.time_unit)) + " " + str(self.offset_y + timeline_y)
        self.fig_buffer += timeline + '\n'
        if self.stdout_print:
            print(timeline)

        # Time ticks
        for (i,j) in vals:
            timeline = "2 1 0 1 0 7 50 -1 -1 0.000 0 0 -1 0 0 2"
            self.fig_buffer += timeline + '\n'
            if self.stdout_print:
                print(timeline)

            timeline = str(self.offset_x + int(i * self.time_unit)) + " " + str(self.offset_y + timeline_y) + " " + str(self.offset_x + int(i * self.time_unit)) + " " + str(self.offset_y + timeline_y + 30)
            self.fig_buffer += timeline + '\n'
            if self.stdout_print:
                print(timeline)

            if i < self.omega - 1:
                timeline = "4 1 0 50 -1 0 " + str(font_size) + " 0.0000 4 135 120 " + str(self.offset_x + int(i * self.time_unit)) + " " + str(self.offset_y + timeline_y + 250) + " " + str(j) + "\\001"
                self.fig_buffer += timeline + '\n'
                if self.stdout_print:
                    print(timeline)

        # Write "time"
        timeline = "4 2 0 50 -1 0 " + str(font_size) + " 0.0000 4 135 120 " + str(self.offset_x + int(self.omega * self.time_unit)) + " " + str(self.offset_y + timeline_y + 250) + " time\\001"
        self.fig_buffer += timeline + '\n'
        if self.stdout_print:
            print(timeline)


        
        if histogram:
            # eventually sets the histogram axis
            y_0 = self.offset_y + timeline_y
            x_0 = self.bar_min_x0

            axis = "2 1 0 1 0 7 20 -1 -1 0.000 0 0 -1 1 0 2"
            self.fig_buffer += axis + '\n'
            if self.stdout_print:
                print(axis)

            axis = "1 1 1.00 60.00 120.00"
            self.fig_buffer += axis + '\n'
            if self.stdout_print:
                print(axis)

            #y_0 = self.offset_y
            axis = str(x_0) + " " + str(y_0) + " " + str(self.bar_min_size) + " " + str(y_0)

                
            self.fig_buffer += axis + '\n'
            if self.stdout_print:
                print(axis)

            if histogram_label:
                label = "4 0 0 50 -1 0 " + str(font_size) + " 0.0000 4 135 120 " + str(self.bar_min_size) + " " + str(y_0 + 250) + " " + histogram_label + "\\001"
                self.fig_buffer += label + '\n'
                if self.stdout_print:
                    print(label)
        




    def addMeasures(self, point_list, width=1, color=0, height=4, ymin=None, ymax=None, x_ticks=2, y_ticks=3, significant_digit=4, title='Value', tick_angle= 0.6, font_size=15, invert_y_axis=True):

        point_list = sorted(point_list, key=lambda x:x[0])

        if not ymin:
            ymin = min(point_list, key=lambda x:x[1])[1]
        if not ymax:
            ymax = max(point_list, key=lambda x:x[1])[1]
        
        y0 = self.offset_y + int((self.node_cpt+1) * self.node_unit) + 125
        yM = y0 + height * self.node_unit

        if invert_y_axis:
            ytemp = yM
            yM = y0+250
            y0 = ytemp

        # x-axis
        if self.discrete > 0:
            start, end = self.omega - 0.5, self.omega
        else:
            start, end = self.alpha, self.omega     

        axis = "2 1 0 1 0 7 50 -1 -1 0.000 0 0 -1 1 0 2"
        self.fig_buffer += axis + '\n'
        if self.stdout_print:
            print(axis)

        axis = "1 1 1.00 60.00 120.00"
        self.fig_buffer += axis + '\n'
        if self.stdout_print:
            print(axis)

        x0 = self.offset_x + int(start * self.time_unit)
        if invert_y_axis:
            axis = str(x0-50) + " " + str(y0) + " " + str(self.offset_x + int(end * self.time_unit)) + " " + str(y0)
        else:            
            axis = str(x0-50) + " " + str(y0-50) + " " + str(self.offset_x + int(end * self.time_unit)) + " " + str(y0-50)

        self.fig_buffer += axis + '\n'
        if self.stdout_print:
            print(axis)

        
        # x-ticks
        vals = []
        i = self.alpha
        while i < self.omega:
            if (i).is_integer():
                vals.append((int(i),int(i)))
            else:
                vals.append((i,i))
            i = i+x_ticks
            
        for (i,j) in vals:
            timeline = "2 1 0 1 0 7 50 -1 -1 0.000 0 0 -1 0 0 2"
            self.fig_buffer += timeline + '\n'
            if self.stdout_print:
                print(timeline)
            
            ytick = 0
            if invert_y_axis:
                ytick = 50

            timeline = str(self.offset_x + int(i * self.time_unit)) + " " + str(y0+ytick-100) + " " + str(self.offset_x + int(i * self.time_unit)) + " " + str(y0+ytick-50)
            self.fig_buffer += timeline + '\n'
            if self.stdout_print:
                print(timeline)
            
            if invert_y_axis:
                if i < self.omega - 1:
                    timeline = "4 1 0 50 -1 0 "+str(font_size)+" 0.0000 4 135 120 " + str(self.offset_x + int(i * self.time_unit)) + " " + str(y0 + 250) + " " + str(j) + "\\001"
                    self.fig_buffer += timeline + '\n'
                    if self.stdout_print:
                        print(timeline)
                
        if invert_y_axis:
            timeline = "4 2 0 50 -1 0 "+str(font_size)+" 0.0000 4 135 120 " + str(self.offset_x + int(self.omega * self.time_unit)) + " " + str(y0 + 250) + " time\\001"
            self.fig_buffer += timeline + '\n'
            if self.stdout_print:
                print(timeline)

        
        # y-axis 
        axis = "2 1 0 1 0 7 50 -1 -1 0.000 0 0 -1 1 0 2"
        self.fig_buffer += axis + '\n'
        if self.stdout_print:
            print(axis)

        axis = "1 1 1.00 60.00 120.00"
        self.fig_buffer += axis + '\n'
        if self.stdout_print:
            print(axis)

        if invert_y_axis:
            axis = str(x0) + " " + str(y0+50) + " " + str(x0) + " " + str(yM-200)
        else:
            axis = str(x0-50) + " " + str(y0-50) + " " + str(x0-50) + " " + str(yM+200)

            
        self.fig_buffer += axis + '\n'
        if self.stdout_print:
            print(axis)
        

        # the curve per se
        dcurve = '2 1 0 '+str(width)+' '+str(color)+' 0 51 0 -1 0 0 0 0 0 0 '+str(len(point_list))+'\n'
        
        for p in point_list:
            real_x = self.offset_x + int(p[0] * self.time_unit)
            real_y = y0 + int(((p[1]-ymin)/float(ymax-ymin) * (yM-y0)))
            dcurve += str(real_x) + ' ' + str(real_y) + ' '

        self.fig_buffer += dcurve + '\n'
        if self.stdout_print:
            print(dcurve)
    
        # y axis ticks
        if y_ticks > 0:
            if invert_y_axis:
                tick_angle = -tick_angle
            step = (yM - y0)/float(y_ticks)
            # draw the tick
            dticks = ""
            for i in range(y_ticks+1):
                dticks += '2 1 0 1 0 0 51 0 -1 0 0 0 0 0 0 2\n'
                tx = x0 - 150
                if invert_y_axis:
                    tx += 50
                ty = int(y0 + i*step)
                dticks += str(int(tx))+' '+str(int(ty))+' '+str(int(tx+100))+' '+str(int(ty))
                dticks += '\n'

            # draw the value
            for i in range(y_ticks+1):
                tx = x0 - 150
                ty = int(y0 + i*step)
                val = ymin+float((ymax - ymin)/y_ticks)*i
                val_format = '.%d'%significant_digit
                val_str = format(val, val_format)
                dticks += "4 2 0 50 -1 0 "+str(font_size)+" "+str(tick_angle)+" 4 135 120 " + str(int(tx)) + " " + str(int(ty)) + " "+val_str+"\\001\n"
                dticks += '\n'

            self.fig_buffer += dticks
            if self.stdout_print:
                print(dticks)

        # display the axis title
        if title:
            if invert_y_axis:
                title = "4 0 0 50 -1 0 "+str(font_size)+" 0.0000 4 135 120 " + str(x0) + " " + str(yM-150) + " "+title+"\\001"
            else:
                title = "4 0 0 50 -1 0 "+str(font_size)+" 0.0000 4 135 120 " + str(x0-350) + " " + str(yM+450) + " "+title+"\\001"
                
        self.fig_buffer += title + '\n'
        if self.stdout_print:
            print(title)

    def __del__(self):
        # Adds white rectangle in background around first node (for EPS bounding box)
        self.addRectangle(self.first_node, self.first_node, self.alpha, self.omega, width=300,depth=60, color=7)

    def getFigBuffer(self):
        # Adds white rectangle in background around first node (for EPS bounding box)
        self.addRectangle(self.first_node, self.first_node, -3  , self.omega, width=300,depth=60, color=7)
        return self.fig_buffer

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

    print('>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<')
    print(s.fig_buffer)
    print('>>>>>>>>>>>>>>>>>>>> <<<<<<<<<<<<<<<<<<<<')
