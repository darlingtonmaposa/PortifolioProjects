# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 15:51:53 2022

@author: Administrator

"""
import numpy as np
import wntr
import matplotlib as plt
import networkx as nx
inp_file = 'Net3.inp'
wn_res = wntr.network.WaterNetworkModel(inp_file)


G = wn_res.get_graph() # directed multigraph
uG = G.to_undirected() # undirected multigraph
sG = nx.Graph(uG) # undirected simple graph (single edge between two nodes)

def topographic_metrics(wn):
    # Get the WaterNetworkModel graph
    G = wn.get_graph()

    # Print general topographic information
    print(nx.info(G))

    # Plot node and edge attributes.
    junction_attr = wn.query_node_attribute('elevation',
                                          node_type=wntr.network.Junction)
    pipe_attr = wn.query_link_attribute('length', link_type=wntr.network.Pipe)
    wntr.graphics.plot_network(wn, node_attribute=junction_attr,
                               link_attribute=pipe_attr,
                               title='Node elevation and pipe length',
                               node_size=40, link_width=2)

    # Compute link density
    print("Link density: " + str(nx.density(G)))

    # Compute node degree
    node_degree = dict(G.degree())
    wntr.graphics.plot_network(wn, node_attribute=node_degree,
                          title='Node Degree', node_size=40, node_range=[1,5])

    # Compute number of terminal nodes
    terminal_nodes = wntr.metrics.terminal_nodes(G)
    wntr.graphics.plot_network(wn, node_attribute=terminal_nodes,
                          title='Terminal nodes', node_size=40, node_range=[0,1])
    print("Number of terminal nodes: " + str(len(terminal_nodes)))
    print("   " + str(terminal_nodes))

    # Compute pipes with diameter > threshold
    diameter = 0.508 # m (20 inches)
    pipes = wn.query_link_attribute('diameter', np.greater, diameter)
    wntr.graphics.plot_network(wn, link_attribute=list(pipes.keys()),
                          title='Pipes > 20 inches', link_width=2,
                          link_range=[0,1])
    print("Number of pipes > 20 inches: " + str(len(pipes)))
    print("   " + str(pipes))

    # Compute eccentricity, diameter, and average shortest path length
    # These all use an undirected graph
    uG = G.to_undirected() # undirected graph
    if nx.is_connected(uG):
        ecc = nx.eccentricity(uG)
        wntr.graphics.plot_network(wn, node_attribute=ecc, title='Eccentricity',
                              node_size=40, node_range=[15, 30])

        print("Diameter: " + str(nx.diameter(uG)))

        ASPL = nx.average_shortest_path_length(uG)
        print("Average shortest path length: " + str(ASPL))

    # Compute cluster coefficient
    clust_coefficients = nx.clustering(nx.Graph(G))
    wntr.graphics.plot_network(wn, node_attribute=clust_coefficients,
                          title='Clustering Coefficient', node_size=40)

    # Compute betweenness centrality
    bet_cen = nx.betweenness_centrality(G)
    wntr.graphics.plot_network(wn, node_attribute=bet_cen,
                          title='Betweenness Centrality', node_size=40,
                          node_range=[0, 0.4])
    central_pt_dom = wntr.metrics.central_point_dominance(G)
    print("Central point dominance: " + str(central_pt_dom))

    # Compute articulation points
    Nap = list(nx.articulation_points(uG))
    Nap = list(set(Nap)) # get the unique nodes in Nap
    Nap_density = float(len(Nap))/uG.number_of_nodes()
    print("Density of articulation points: " + str(Nap_density))
    wntr.graphics.plot_network(wn, node_attribute=Nap, title='Articulation Point',
                          node_size=40, node_range=[0,1])

    # Compute bridges
    bridges = wntr.metrics.bridges(G)
    wntr.graphics.plot_network(wn, link_attribute=bridges, title='Bridges',
                          link_width=2, link_range=[0,1])
    Nbr_density = float(len(bridges))/G.number_of_edges()
    print("Density of bridges: " + str(Nbr_density))


topographic_metrics(wn_res)