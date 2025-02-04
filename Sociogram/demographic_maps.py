import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
from Sociogram import main_sociogram

def draw_social_map(graph, identifier_to_name, identifier_to_features, attribute='נקבה'):
    """
    Draw the social map of the cadets that includes the specified attribute in their features.

    Parameters:
    - graph (nx.DiGraph): The directed graph of social connections.
    - identifier_to_name (dict): Dictionary mapping identifiers to cadet names.
    - identifier_to_features (dict): Dictionary mapping identifiers to their features (list).
    - attribute (str): The attribute based on which to color nodes.

    Returns:
    - None. Displays the graph.
    """
    arrow_size = 10

    # Reverse Hebrew names for display
    flipped_node_names = {k: v[::-1] for k, v in identifier_to_name.items()}
    plt.figure(figsize=(20, 20))

    # Modify the graph to add weights
    for u, v in graph.edges():
        if attribute in identifier_to_features[u] and attribute in identifier_to_features[v]:
            # Increase weight for edges where both nodes have the attribute
            graph[u][v]['weight'] = 10
        elif attribute in identifier_to_features[u] or attribute in identifier_to_features[v]:
            graph[u][v]['weight'] = 5
        else:
            graph[u][v]['weight'] = 1  # Normal weight for other edges

    # Compute the position of nodes using the spring layout with weighted edges
    pos = nx.spring_layout(graph, weight='weight', iterations=200, k=3, seed=10)  # The layout uses the edge weights


    # Determine the color of nodes based on the attribute
    colors = ['red' if attribute in identifier_to_features[identifier] else 'gray' for identifier in graph.nodes()]

    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_color=colors, node_size=2000)
    # Draw labels
    nx.draw_networkx_labels(graph, pos, labels=flipped_node_names, font_size=10, font_weight='bold')

    # Draw edges differently based on attribute presence
    edges_with_both_attributes = [(u, v) for u, v in graph.edges() if
                                  attribute in identifier_to_features[u] and attribute in identifier_to_features[v]]
    edges_with_attribute = [(u, v) for u, v in graph.edges() if
                            attribute in identifier_to_features[u] or attribute in identifier_to_features[v]]
    edges_with_attribute = list(set(edges_with_attribute) - set(edges_with_both_attributes))


    nx.draw_networkx_edges(graph, pos, edgelist=edges_with_attribute, width=3, alpha=0.2, edge_color='black',
                           arrowsize=arrow_size, arrowstyle='->')
    nx.draw_networkx_edges(graph, pos, edgelist=edges_with_both_attributes, width=5, alpha=0.5, edge_color='red',
                           arrowsize=arrow_size, arrowstyle='->')

    plt.title('Social Map Highlighting ' + attribute[::-1], fontsize=20)
    plt.axis('off')  # Turn off the axis

    output = main_sociogram.FILE_OUT + "/demographic"
    if not os.path.exists(output):
        os.makedirs(output)
    file_path = os.path.join(output, f'group_{attribute}.png')
    plt.savefig(file_path)

    # show only the nodes with the attribute
    plt.figure(figsize=(10, 10))
    nx.draw_networkx_nodes(graph, pos, nodelist=[node for node in graph.nodes() if attribute in identifier_to_features[node]],
                           node_color='red', node_size=3000)
    # add labels for the nodes with the attribute
    nx.draw_networkx_labels(graph, pos, labels={k: v[::-1] for k, v in identifier_to_name.items() if k in [node for node in graph.nodes() if attribute in identifier_to_features[node]]},
                            font_size=10, font_weight='bold')
    nx.draw_networkx_edges(graph, pos, edgelist=edges_with_both_attributes, width=5, alpha=0.5, edge_color='red',
                           arrowsize=arrow_size, arrowstyle='->')
    plt.title('Social Map Highlighting ' + attribute[::-1], fontsize=20)
    plt.axis('off')  # Turn off the axis
    file_path = os.path.join(output, f'zoomin_group_{attribute}.png')
    plt.savefig(file_path)


def draw_demographic_groups(graph, identifier_to_name, identifier_to_features, attributes: list):
    for attr in attributes:
        draw_social_map(graph, identifier_to_name, identifier_to_features, attr)


