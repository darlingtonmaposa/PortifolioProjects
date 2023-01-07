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


# building the network
inp_file = 'Net3.inp'
wn = wntr.network.WaterNetworkModel(inp_file)

######################
# Water age simulation
######################

def water_age(duration):
    '''Evaluates average water age
    	
    	parameter
		----------
		duration: int
		age of water in hours

		returns
		-------
		streamlit image object
		the graphical representation of the average water age
    '''
    
    wn.options.quality.parameter = 'AGE'
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()
    
    age = results.node['quality']
    age_last_nh = age.loc[age.index[-1]-duration*3600:age.index[-1]]
    average_age = age_last_nh.mean()/3600 # convert to hours
    
    wntr.graphics.plot_network(wn, node_attribute=average_age,
                          title='Average water age (last {} hours)'.format(duration), 
                          node_colorbar_label= 'Average age (hours)',
                          filename='water_age')

    image = Image.open('water_age.png')
    return st.image(image, caption='Average Water Age')


def population_impacted(duration, threshold):
	"""
	Evaluates the population impacted by water above the duration
		parameter
		----------
		duration: int
		age of water in hours

		threshold: int
		the time limit above which the population impacted is required

		returns
		-------
		streamlit image object
		the graphical representation of the population impacted by water above the duration
	"""
	# simulation
	wn.options.quality.parameter = 'AGE'
	sim = wntr.sim.EpanetSimulator(wn)
	results = sim.run_sim()

	age = results.node['quality']
	age_last_nh = age.loc[age.index[-1]-duration*3600:age.index[-1]]
	average_age = age_last_nh.mean()/3600 # convert to hours
	pop = wntr.metrics.population(wn)
    
	pop_impacted = wntr.metrics.population_impacted(pop, average_age, np.greater, threshold)


	wntr.graphics.plot_network(wn, node_attribute=pop_impacted,
                               title='Population affected by water age older than {} hours'.format(threshold),
                               node_colorbar_label= 'Population impacted',
                               filename='pop_impacted')

	image = Image.open('pop_impacted.png')
	return st.image(image, caption='Population impacted by water age')



def chem_concen(source1, source2, end_time, duration, threshold):
    '''
    Evaluates chemical concentration at diffrent nework locations
    
        parameters
        ----------
        source1, source2 : str
        name of the part of the network where chemical is injected.

        end_time : int
        end of simulation time in hours
        
        duration : int
        duration of the simulation in days
        
        threshold : int, float
        allowable chemical concentration limit
        
        returns
        -------
        streamlit image object
        the graphical representation of chemical concentrations above regulated
    '''

    inp_file = 'Net3.inp'
    wn = wntr.network.WaterNetworkModel(inp_file)
    wn.options.quality.parameter = 'CHEMICAL'
    source_pattern = wntr.network.elements.Pattern.binary_pattern('SourcePattern',
                                                                  step_size=3600, start_time=3600, end_time=end_time*3600, duration=7*24*3600)
    wn.add_pattern('SourcePattern', source_pattern)
    wn.add_source('Source1', source1, 'SETPOINT', 1000, 'SourcePattern')
    wn.add_source('Source2', source2, 'SETPOINT', 1000, 'SourcePattern')
    sim = wntr.sim.EpanetSimulator(wn)
    results = sim.run_sim()
    chem = results.node['quality']
    
    # check compliance
    mask = wntr.metrics.query(chem, np.greater, threshold)
    chem_above_regulation = mask.any(axis=0) # True/False for each node
    
    # plot the graph
    wntr.graphics.plot_network(wn, node_attribute=chem_above_regulation, 
                               title='Chemical levels above limit',
                               node_colorbar_label= 'Chemical levels', 
                               filename='chemical')
    image = Image.open('chemical.png')
    return st.image(image, caption='Chemical levels')