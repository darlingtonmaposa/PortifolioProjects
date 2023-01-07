# Streamlit dependencies
import streamlit as st

# Data handling dependencies
import pandas as pd
import numpy as np

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# importing visualization library
#import matplotlib.pyplot as plt
import plotly.graph_objs as go

# import warnings
import warnings 
warnings.filterwarnings('ignore')

#import scipy
import scipy as sc


# import wntr
import wntr
# import networkx
import networkx as nx

# image   
from PIL import Image


def net_graph(option):
	'''
	Plots water network graph by elevation or pressure

	parameter
	---------
		option : str
		elevation or pressure
	returns
	-------
		streamlit image object
		the graphical representation of the water network by the given parameter
	'''

	# graph title
	title = 'The graph of the water network by ' + option
	# color bar label with units
	col_label = option + ' (m)'
	# plot the graph
	wn = wntr.network.WaterNetworkModel('Net3.inp')
	ax = wntr.graphics.plot_network(wn, node_attribute=option, title=title, 
	                                    node_colorbar_label=col_label, filename='network')
	    
	image2 = Image.open('network.png')
	return st.image(image2, caption='Water Network')
