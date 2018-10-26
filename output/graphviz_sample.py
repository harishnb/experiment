# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 11:39:15 2018

@author: harisbha
"""

# Go to the Graphviz website and download and install to your computer (do NOT need to install for all users).
#
# Download and install Anaconda3.5 from the Continuum website.
#
# Add Graphviz to the environment variable "Path":
#
# Go to Computer > Properties > Advanced system settings > Environment Variables and then find "Path" in the system variables box. Click on Path and click edit.
# Append ;C:\Program Files (x86)\Graphviz2.38\bin to the end of the many paths that are already present in Path. Note, the path to Graphviz may be different for you so make sure to put the correct path. The folder "bin" should have many files including the dot.exe application.
# To check the install go to the command prompt and enter: dot -V this should return the version of Graphviz installed. For example, dot - graphviz version 2.38.0. If this does not work, enter set and look for the Graphviz path.
# Go to the Anaconda command prompt and enter: pip install graphviz
#
# Restart Spyder or launch it if not already open.
#
# Now within your Python script add import graphviz
#


import graphviz
import pygal
import pandas as pd
import os
import sys
import string

var_full_data = pd.read_csv('data.csv')
var_screen_list = []
var_unique_list = []
var_edge_list = []
sys.stdout = open("output_print.txt", "w")
var_dic_screen_entry = {}


def extract_screen_name():
    global var_screen_list
    for idx2 in list(range(0, len(var_full_data))):
        var_screen_list.append(var_full_data.ScreenName[idx2])


def draw_graph():
    dot = graphviz.Digraph(comment='The screen Nodes')
    dot.format = 'svg'
    # Add the screen Names as nodes
    var_unique_list = list(set(var_screen_list))
    print(var_unique_list)
    print("=============================")

    var_len_unique_list = len(var_unique_list)
    var_node_list = list(string.ascii_uppercase)
    #    if var_len_unique_list < 26:
    #        var_node_list = list(string.ascii_uppercase)

    ###ToDo if the total screen size is greater than 26 add lowercase

    for idx2 in list(range(0, len(var_full_data))):
        if idx2 + 1 < len(var_full_data):
            tmp_indx1 = var_node_list[(var_unique_list.index(var_full_data.ScreenName[idx2]))]
            tmp_indx2 = var_node_list[var_unique_list.index(var_full_data.ScreenName[idx2 + 1])]

            if (var_full_data.ScreenName[idx2 + 1]) in var_dic_screen_entry:
                var_dic_screen_entry[var_full_data.ScreenName[idx2 + 1]] += 1
            else:
                var_dic_screen_entry[var_full_data.ScreenName[idx2 + 1]] = 1

            print(str(var_full_data.ScreenName[idx2]) + ":" + tmp_indx1)
            print(str(var_full_data.ScreenName[idx2 + 1]) + ":" + tmp_indx2)
            print("|||||||")
            var_edge_list.append(tmp_indx1 + tmp_indx2)
    print("---------------------------------------")
    print(var_dic_screen_entry)
    for idx1 in range(0, var_len_unique_list):
        tmp_str = str(var_unique_list[idx1]) + ":" + str(var_dic_screen_entry[var_unique_list[idx1]])
        dot.node(var_node_list[idx1], tmp_str)
        print("idx1= " + var_node_list[idx1] + tmp_str)

    print("+++++++++++++Edge list+++++++++++++")
    print(var_edge_list)
    dot.edges(var_edge_list)
    dot.render('templates/static/images/graph', view=True)


extract_screen_name()
draw_graph()

sys.stdout.close()
sys.exit(1)
# Below is an example of how to create a graph from a pre-generated .gv file (at least a starting point for exploration)
#
# from graphviz import Source
# Source.from_file('file.gv')
