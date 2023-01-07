# Water-Network-Tool-for-Resilience-WNTR-

<img src="water network.jpg" alt="water network" style="max-width: 100%">

## Overview
Drinking water systems face multiple challenges, including aging infrastructure, water quality concerns,
uncertainty in supply and demand, natural disasters, environmental emergencies, and cyber and terrorist attacks.
All of these have the potential to disrupt a large portion of a water system causing damage to infrastructure and
outages to customers. Increasing resilience to these types of hazards is essential to improving water security. The EPANET package is the da facto industry standard used for modeling water distribution systems. However, it is not capable of modelling energy utilisation, disruptive events and running probabilistic simulations. WNTR extends the capabilities of the EPANET by incorporating the aforementioned limitations however, the package needs to be explored to see whether it is a viable alternative to the EPANET in modelling and simulating real-world water systems.

The Water Network Tool for Resilience (WNTR, pronounced winter) is a Python package designed to simulate and
analyze resilience of water distribution networks. This project explored the capabilities of the package and built them into a Streamlit app for ease of access to the users.


## Contents 
- The resource folder contains the presentations, white paper, meeting minutes and a link to the team's Trello board.
- The project is in `notebook_main.ipynb` file.
- The Streamlit folder houses the app `water_network_analyser.py`

## Dependencies
To run this project, one needs to install the following dependencies using `!pip` command:
- numpy
- pandas
- networkx
- wntr
- matplotlib
- plotly
- folium
- utm


## Credits
- [Water netwok picture](https://scx2.b-cdn.net/gfx/news/2018/aitechnology.jpg)
- [Water network elements](http://wateranalytics.org/EPANET/_data_model.html)
