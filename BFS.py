import queue
from random import random
from itertools import product
import networkx as nx
import matplotlib.pyplot as plt

# Function to add an edge to the adjacency list
def add_edge(adj_list, u, v):
    adj_list[u].append(v)

# Function for breadth-first search traversal
def bfs_util(u, adj_list, visited):
    answer = []
    q = queue.Queue()

    visited[u] = True
    q.put(u)

    while not q.empty():
        u = q.queue[0]
        answer.append(str(u))

        q.get()

        i = 0
        while i != len(adj_list[u]):
            if not visited[adj_list[u][i]]:
                visited[adj_list[u][i]] = True
                q.put(adj_list[u][i])

            i += 1

    return answer

# Function to perform breadth-first search on the graph
def bfs(adj_list, V):
    answer = []
    visited = [False] * V

    for u in range(V):
        if not visited[u]:
            answer.append(bfs_util(u, adj_list, visited))
    return answer

# Function to generate a random graph
def random_graph(n, p):
    nodes = range(n)
    adj_list = [[] for i in nodes]
    possible_edges = product(nodes, repeat=2)
    for u, v in possible_edges:
        if random() < p:
            adj_list[u].append(v)
    return adj_list

# Function to convert adjacency list to edge list
def edge_list(adj_list):
    nodes_list = []
    dist_list = []
    for i in range(len(adj_list)):
        if len(adj_list[i]) == 0:
            nodes_list.append(str(i))
            dist_list.append('-')
        for j in range(len(adj_list[i])):
            nodes_list.append(str(i))
            dist_list.append(str(adj_list[i][j]))

    edges_list = list(zip(nodes_list, dist_list))

    remove_index = [i for i in range(len(edges_list)) if edges_list[i][1] == '-']

    elements_to_be_removed = [edges_list[i] for i in remove_index]

    for element in elements_to_be_removed:
        edges_list.remove(element)

    return edges_list, nodes_list

# Function to convert BFS traversal to edge tuples
def bfs_tuple(bfs):
    new_edges = []
    for r in bfs:
        for n in range(len(r) - 1):
            new_edges.append((r[n], r[n + 1]))
    return new_edges


V = int(input("Enter the number of vertices: "))

c = input("Do you want the graph to be manually/randomly added? (m/r): ")

if c == "r":

    adj_list = random_graph(V, 0.25)

elif c == "m":

    adj_list = [[] for i in range(V)]
    for vector in range(V):
        adj_N = int(input(f'How many adjacents does vector {vector} have? '))
        for j in range(adj_N):
            n = int(input("Add the adjacent: "))
            add_edge(adj_list, vector, n)

# Perform BFS traversal on the graph
main_list = bfs(adj_list, V)

# Construct path string for visualization
path = ""
for i in range(len(main_list)):
    path += "("
    for j in range(len(main_list[i])):
        if j == len(main_list[i]) - 1:
            path += f"{main_list[i][j]}"
        else:
            path += f"{main_list[i][j]} --> "
    if i == len(main_list) - 1:
        path += ")"
    else:
        path += ") --> "

# Convert BFS traversal to edge tuples for plotting
new_edges = bfs_tuple(bfs(adj_list, V))

# Create a directed graph using NetworkX
G = nx.DiGraph()
G.add_edges_from(edge_list(adj_list)[0])
G.add_nodes_from(edge_list(adj_list)[1])
pos = nx.spring_layout(G)

# Plot the graph
nx.draw_networkx_nodes(G, pos, node_color='r')
nx.draw_networkx_labels(G, pos)
nx.draw_networkx_edges(G, pos, connectionstyle="arc3,rad=0.1", arrows=True)
plt.suptitle(f'{path}', fontsize=14, fontweight='bold')

# Print adjacency list and BFS traversal path
print(adj_list)
print(path)

plt.show()
