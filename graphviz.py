# -*- coding: utf-8 -*-
"""
=============================================================================================
1.graphviz
    Weight obtained by the graph from the kernel, and the adjacency matrix, create a graph.
    This is a measure for pydot does not work on python(x,y).
=============================================================================================
Operating conditions necessary {UTF-8/CrLf/Python2.7/numpy/matlot/Scipy}
@author: Hisashi Ikari
"""
from numpy import *
import colorsys

# ===========================================================================================
# graphviz
#   Weight obtained by the graph from the kernel, and the adjacency matrix, create a graph.
# ===========================================================================================
# *** Arguments ***
#   A:"adjacency matrix" AND "weight for the vertex (dot product)"
#       value is 0..........Node is not connected
#       value is non-zero...Nodes are connected, with a weight of positive or negative
#   B:Number of clusters assigned
# ===========================================================================================
def graphviz(A,B):
    """
    For example,
    the description of DOT language to display the graph in graphviz is the following description.
    *** Using the data output in graph.py, to create this format. ***
    -----------------------------------------------------------------------------------------    
    digraph Adjacency-Matrix {
        1 -> 2  [label = "1"];
        1 -> 3 [label = "2"];
        2 -> 4 [label = "3"];
    }
    -----------------------------------------------------------------------------------------    
    """
    N = len(A)    
    sc = 1.0 / len(B)
    
    print "digraph AdjacencyMatrix {"
    print "\tgraph[label=\"Graph representing the weight of the edge and adjacent\",labelloc =t];"
    for i in range(N):
        #p = colorsys.hsv_to_rgb(sc*i,1.0,1.0)
        p = colorsys.hsv_to_rgb(sc*B[i],1.0,1.0)
        print "\t%s [style = filled, color=\"#000000\" fillcolor = \"#%s%s%s\"];" \
              % (i+1, "00" if p[0] == 0.0 else hex(int(p[0]*255)).replace("0x",""), \
                      "00" if p[1] == 0.0 else hex(int(p[1]*255)).replace("0x",""), \
                      "00" if p[2] == 0.0 else hex(int(p[2]*255)).replace("0x","") )
        for j in range(N):    
            if i != j and A[i,j] != 0.0:
                print "\t%s->%s\t[label=\"%s\",color=\"%s\"];" \
                      % (j+1, i+1, A[i,j], "red" if A[i,j] < 0.0 else "blue")
    print "}"
    
# ===========================================================================================
# Reads the data file
# ===========================================================================================
# -------------------------------------------------------------------------------------------
# Initial processing
# -------------------------------------------------------------------------------------------
A = loadtxt("graph_A.txt")
B = loadtxt("result_spectral_clustering.txt")
print "A\n", A
print "B\n", B

graphviz(A,B)
