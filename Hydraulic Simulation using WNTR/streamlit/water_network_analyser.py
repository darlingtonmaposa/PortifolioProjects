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

# import simulators
#from simulators import criticality
from simulators import water_quality
from simulators import network_graph

#############
# Color codes
#background: FDFFF5, ee964b
#2nd bg #EE8933, #EF7674 or #D8E831
# OTHERS BLACK
####################################
#Sidebar
with st.sidebar:
    with st.expander("About Us"):
        st.write("""
                T-Flow AI is a team (Team 17) of five data scientists, namely: 
                Buhari Shehu, Kennedy Ombedho, John Lawal, Sandile Ngubane, Joseph Wahome and a data engineer: Darlington Maposa.
                The team collaborated and explored the capabilities of WNTR in modelling the resilience of water networks and developed a web app called Water Analyser.
            """)
with st.sidebar:
    with st.expander("Contact Us"):
        st.markdown("""
                - Kennedy Ombedho `kencarsonbonyo@gmail.com`
                - Buhari Shehu `shehubuhari1@gmail.com`
                - John Lawal `lawjohn4real@yahoo.com`
                - Darlington Maposa `maposad04@gmail.com`
                - Sandile Ngubane `sandilengubane95@gmail.com`
                - Joseph Wahome `joehwahome@gmail.com`
            """)

with st.sidebar:
    with st.expander("Documentation"):
        st.subheader('Network Graph')
        st.write(""" To visualise the water network click on the Network Graph tab and select either
            elevation or pressure and click view network.                
            """)
        st.subheader('Charts')
        st.write('''
            The pressure and demand variations in a pipe can be visualise by clicking the Charts tab and selecting the pipe of interest.

            ''')
        st.subheader('Analyses')
        st.write(''' Pressure and demand analyses can be carried out in the Analyses tab.
            To know how many times pipe pressure goes beyond a threshold, click the Analyses tab. Navigate to the Hydraulic Metrics Section.
            Select the pipe of interest and the threshold.

            ''')
        st.subheader('Simulations')
        st.write(''' In simulation section one can run leak, burst, water quality, fire and earthquake simulations.
            To run any simulations, click the Simulations tab and select the appropriate simulator and enter the parameters of interest.

            ''')
####################################

####################################
# Network

wn = wntr.network.WaterNetworkModel('Net3.inp') 
sim = wntr.sim.EpanetSimulator(wn)
results = sim.run_sim()
####################################
# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(['Home',"Network Graph", "Charts", "Analyses", 'Simulations'])

with tab1: 
   # Home tab
   st.markdown("<h1 style='text-align: center; color: black;'>Water Network Analyser</h1>", unsafe_allow_html=True)
   
   image = Image.open('water.jpg')
   st.image(image, caption='Water Network')

   st.markdown("<b>Water Network Analyser is an application that can be used to visualise, simulate and analyse water networks. The app was built by a team of five (5) data scientists and a data engineer during their internship at ExploreAI Academy in August-October, 2022.</b>", unsafe_allow_html=True)
   st.markdown('<b>The app can visualise a water network by elevation or pressure. Important water network metrics like pressure and demand can also be analysed in the app. Water Network Analyser can also simulate disruptive events, like leaks and bursts, and water quality issues like water age. These are important in making the network more resilient and ensuring water safety.</b>', unsafe_allow_html=True)


with tab2: 
# Network Graph tab
    col1, col2 = st.columns(2)
    option1 = col1.selectbox(
        "Select node attribute",
        ('elevation', 'pressure'),
        )
    if st.button('View network'):
        network_graph.net_graph(option1)

#########################################

with tab3: 
# Charts tab  
   st.header("Demand and Pressure Charts")
   option2 = st.selectbox(
        "Select your link",
        ('2', '35', '40', '50', "123", "125"),
        )
pressure = results.node['pressure'].loc[:,option2]
demand = results.node['demand'].loc[:, option2]
############################################

tab3.header("Pressure chart")
custom_title = 'Pressure variation in pipe {}.'.format(option2)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(pressure.index, pressure)
plt.title(custom_title)
plt.xlabel('Duration (seconds)')
plt.ylabel('Pressure (meters)')
tab3.pyplot(fig)

tab3.header("Demand chart")
custom_title = 'Demand variation in pipe {}.'.format(option2)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(demand.index, demand)
plt.title(custom_title)
plt.xlabel('Duration (seconds)')
plt.ylabel('Demand (in cubic meter)')
tab3.pyplot(fig) 
###############################################
with tab4:
# Analyses tab
    ## Resilience metrics
    #inp_file = st.file_uploader("Choose a file") #future consideration
    wn = wntr.network.WaterNetworkModel('Net3.inp') 
    G = wn.get_graph() # directed multigraph
    #link_density = round(nx.density(G),3)

    ### pressure metrics
    wn2 = wntr.network.WaterNetworkModel('Net3.inp') 
    wn2.options.hydraulic.demand_model = 'PDD'
    sim = wntr.sim.WNTRSimulator(wn2)
    results2 = sim.run_sim()

    pressure2 = results2.node['pressure']
    #threshold = 21.09 # 30 psi
    #threshold = st.slider("Select pressure(m) threshold", min_value=0.00, max_value=80.00, value=21.09, step=0.01)
    #pressure_above_threshold = wntr.metrics.query(pressure2, np.greater, threshold)
    #count_above_threshold = len(pressure_above_threshold[pressure_above_threshold['123']==True])

    ##Number of elements
    node_names = wn.node_name_list
    num_nodes = wn.num_nodes
    elements_dict = wn.describe(level=0)

    # annual network cost
    network_cost = wntr.metrics.annual_network_cost(wn2)
    network_cost = str(round((network_cost/1000000),2))
    network_cost = '$' + network_cost + "" + "M"

    # annual grenhouse gas emission
    network_ghg = wntr.metrics.annual_ghg_emissions(wn2)
    network_ghg = str(round((network_ghg/1000000),2))
    network_ghg = network_ghg + "(kg/m/yr)"

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        link_length = wn.query_link_attribute('length', link_type=wntr.network.model.Pipe)
        total_length = int(link_length.sum())
        st.metric('Total Pipe Length (km) ', total_length, delta=None, delta_color="normal")

    with col2:
        st.metric('No. of Pipes', elements_dict['Links'], delta=None, delta_color="normal")

    with col3:
        st.metric('Annual Network Cost', network_cost, delta=None, delta_color="normal")

    with col4:
        st.metric('Annual GHG Emissions', network_ghg, delta=None, delta_color="normal")

    #with col4:
    #  col4.metric('Times Link123 > Press. threshold', count_above_threshold, delta=None, delta_color="normal")
##########################################################

    st.header('Hydraulic Metrics')
    st.subheader('Pressure Analysis')
    #network simulation
    wn2 = wntr.network.WaterNetworkModel('Net3.inp') 
    wn2.options.hydraulic.demand_model = 'PDD'
    sim = wntr.sim.WNTRSimulator(wn2)
    results2 = sim.run_sim()

    # adhoc network elements list
    net_ele = list(wntr.metrics.query(pressure2, np.greater, 0).columns) # for chemical simulation in water quality

    # querying the links
    col1, col2, col3 = st.columns(3)
    pipe = col1.selectbox("Selct pipe", list(wntr.metrics.query(pressure2, np.greater, threshold).columns)) #tentative df
    threshold = col2.slider("Select pressure threshold", min_value=0.00, max_value=80.00, value=21.09, step=0.01)

    pressure2 = results2.node['pressure']
    pressure_above_threshold = wntr.metrics.query(pressure2, np.greater, threshold)
    count_above_threshold = len(pressure_above_threshold[pressure_above_threshold[pipe]==True])

    col3.metric('Number of times pipe above threshold', count_above_threshold, delta=None, delta_color="normal")
    # graphics
    lists=[]

    for i in pressure_above_threshold[pipe].index:
        if pressure_above_threshold[pipe][i] == True:
            lists.append(1)
        else:
            lists.append(0)


    pressure_above_threshold['chart'] = lists
    

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(pressure_above_threshold['chart'].index, pressure_above_threshold['chart'])
    plt.title('Pressure variation above threshold')
    plt.xlabel('Duration (seconds)')
    plt.ylabel('Count')
    tab4.pyplot(fig)


    #######################################
    #demand | water service availability
    st.subheader('Demand Analysis')
    col5, col6 = st.columns(2)
    pipe_d = col5.selectbox("Select pipe", list(wntr.metrics.query(pressure2, np.greater, threshold).columns)) #tentative df
    expected_demand = wntr.metrics.expected_demand(wn)
    demand = results2.node['demand']                              # results2 because it is pdd dependent, this from pressure met abv.
    wsa = wntr.metrics.water_service_availability(expected_demand, demand)
    wsa.fillna(0, inplace=True)                         # fill null values
    avail = round(int(sum(wsa[pipe_d]))/len(wsa[pipe_d]) * 100 ,2)
    avail_u = '{} %'.format(avail)
    col6.metric('Pipe Water Service Availability', avail_u)

    
######################################################

with tab5:
# Simulations tab
    option = st.selectbox(
        "Select simulation type",
        ('Leak', 'Burst', 'Earthquake', 'Fire' , "Power Outage", 'Water Quality', 'Criticality'),
        )

    if option == 'Water Quality':
        # selections
        col7, col8, col9 = st.columns(3)
        quality_type = col7.selectbox(
        "Select quality type",
        ('Age', 'Population impacted', 'Chemical'),
        )

        duration_h = col8.number_input("Enter simulation duration", min_value=1)
        if quality_type == 'Population impacted':
            thresh = col9.number_input("Enter water age threshold", min_value=1)
        if quality_type == 'Chemical':
            col10, col11, col12, col13, col14 = st.columns(5)
            source1 = col10.selectbox('Select first chem. source', net_ele)
            source2 = col11.selectbox('Select second chem. source', net_ele)
            end_time = col12.number_input('Enter sim end time (hr)', min_value=1)
            duration = col13.number_input('Enter sim duration (days)', min_value=1)
            threshold = col14.number_input('Enter chem. concen. limit', min_value=1)

        # simulations
        if st.button('Simulate'):
            if quality_type == 'Age':
                water_quality.water_age(duration_h)
            elif quality_type == 'Population impacted':
                water_quality.population_impacted(duration_h, thresh)
            elif quality_type == 'Chemical':
                water_quality.chem_concen(source1, source2, end_time, duration, threshold)

    

 

    

    