import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import community
import time

def get_clusters(graph, C):
  if nx.get_edge_attributes(graph,'weight') == {}:
    for u,v in graph.edges():
      graph[u][v]['weight'] = 1
  node_weight = {u: 0 for u in graph.nodes()}
  for u,v in graph.edges():
    node_weight[u] += graph[u][v]['weight']
    node_weight[v] += graph[u][v]['weight']
  clusters = list(set(C.values()))
  cluster_nodes = {k:{} for k in clusters}
  for u in graph.nodes():
    cluster_nodes[C[u]][u] = node_weight[u]
  cluster_nodes = {k: sorted(cluster_nodes[k], key = cluster_nodes[k].get, reverse = True) for k in clusters}
  return cluster_nodes


def maximize_modularity(graph, resolution):
  node_weight = {u: 0. for u in graph.nodes()}
  w = 0
  for u,v in graph.edges():
    node_weight[u] += graph[u][v]['weight']
    node_weight[v] += graph[u][v]['weight']
    w += graph[u][v]['weight']
  # init the clustering
  C = {u:u for u in graph.nodes()}
  # cluster weights
  cluster_weight = {u: node_weight[u] for u in graph.nodes()}
  # node-cluster weights (between each node and the clusters)
  node_cluster_weight = {u:{v: 1. * graph[u][v]['weight'] for v in graph.neighbors(u) if v != u} for u in graph.nodes()}
  increase = True
  while increase:
    increase = False
    for u in graph.nodes():
      k = C[u]            
      if k not in node_cluster_weight[u]:
        node_cluster_weight[u][k] = 0
      variation = {k: 0}  
      # update  𝐶  by moving one node from its cluster to one of its neighbors
      for l in node_cluster_weight[u].keys():
        if l!=k:
          c_k=node_cluster_weight[u][k]
          c_l=node_cluster_weight[u][l]  
          v_k=cluster_weight[k]
          v_l=cluster_weight[l]
          v=sum(list(cluster_weight.values()))
          delta_Q=(c_l-c_k)/w-(resolution/(v**2))*(2*node_weight[u]*(cluster_weight[l]-cluster_weight[k]+node_weight[u]))  
          variation[l]=delta_Q  
      l = max(variation, key = variation.get)
      if variation[l] > 0:
        increase = True
        # move node u from cluster k to cluster l
        C[u] = l
        cluster_weight[k] -= node_weight[u]
        cluster_weight[l] += node_weight[u]
        for v in graph.neighbors(u):
          if v != u:
            node_cluster_weight[v][k] -= graph[u][v]['weight']
            if node_cluster_weight[v][k] <= 0:
              node_cluster_weight[v].pop(k)
            if l not in node_cluster_weight[v]:
              node_cluster_weight[v][l] = 0
            node_cluster_weight[v][l] += graph[u][v]['weight']
  return C


def aggregate_graph(graph,C):
  aggregate_graph_ = nx.Graph()
  aggregate_graph_.add_nodes_from(set(C.values()))
  for u,v in graph.edges():
    if aggregate_graph_.has_edge(C[u],C[v]):
      aggregate_graph_[C[u]][C[v]]['weight'] += graph[u][v]['weight']
    else:
      aggregate_graph_.add_edge(C[u],C[v])
      aggregate_graph_[C[u]][C[v]]['weight'] = graph[u][v]['weight']
  return aggregate_graph_

 
def louvain(graph,resolution = 1):
  if nx.get_edge_attributes(graph,'weight') == {}:
    for u,v in graph.edges():
      graph[u][v]['weight'] = 1
  C = maximize_modularity(graph, resolution)
  n = len(C)
  k = len(set(C.values()))
  while k < n:
    aggregate_graph_ = aggregate_graph(graph,C) 
    C_new = maximize_modularity(aggregate_graph_, resolution)
    C = {u: C_new[C[u]] for u in graph.nodes()}
    n = k
    k = len(set(C_new.values()))
  # reindex clusters in decreasing order of size
  clusters = list(set(C.values()))
  cluster_size = {k: 0 for k in clusters}
  for u in C:
    cluster_size[C[u]] += 1
  cluster_index = sorted(cluster_size, key = cluster_size.get, reverse = True)
  reindex = {k:i for i,k in enumerate(cluster_index)}
  C = {u:reindex[C[u]] for u in C}
  return C


