import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()

nodes = ["A","B","C","D","F","G","H","I"]
G.add_nodes_from(nodes)

# Special sum nodes
G.add_node("SUM2")
G.add_node("SUM3_ADG")
G.add_node("SUM3_CFI")
G.add_node("SUM3_ABC")
G.add_node("SUM3_GHI")

# Pairwise constraints → directed edges to SUM2
for n in nodes:
    G.add_edge(n, "SUM2")

# Triple constraints → directed edges to SUM3 nodes
triangles = {
    "SUM3_ADG": ["A","D","G"],
    "SUM3_CFI": ["C","F","I"],
    "SUM3_ABC": ["A","B","C"],
    "SUM3_GHI": ["G","H","I"]
}

for Znode, members in triangles.items():
    for m in members:
        G.add_edge(m, Znode)

# Draw
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(12,12))

nx.draw(G, pos, with_labels=True, node_size=1500, font_size=14, arrows=True)

plt.title("Directed Graph Encoding All Allowed Relations (2 and 3 Only)")
plt.axis("off")
plt.show()

# import networkx as nx
# import matplotlib.pyplot as plt

# # Original nodes
# nodes = ["A","B","C","D","F","G","H","I"]

# # New Z nodes for triple constraints
# Z_nodes = ["Z_ADG", "Z_CFI", "Z_ABC", "Z_GHI"]

# G = nx.Graph()

# G.add_nodes_from(nodes)
# G.add_nodes_from(Z_nodes)

# # Pairwise edges (complete graph)
# for i in range(len(nodes)):
#     for j in range(i+1, len(nodes)):
#         G.add_edge(nodes[i], nodes[j], label="X+Y=2")

# # Triple constraint stars
# triangles = {
#     "Z_ADG": ["A","D","G"],
#     "Z_CFI": ["C","F","I"],
#     "Z_ABC": ["A","B","C"],
#     "Z_GHI": ["G","H","I"]
# }

# for Znode, members in triangles.items():
#     for m in members:
#         G.add_edge(Znode, m, label="Z=1")

# # Draw
# pos = nx.spring_layout(G, seed=42)
# plt.figure(figsize=(12,12))

# nx.draw(G, pos, with_labels=True, node_size=1500, font_size=14)

# edge_labels = {(u,v): G[u][v]['label'] for u,v in G.edges()}
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

# plt.title("2D Network Graph with Z-Nodes Representing 3D Height")
# plt.axis("off")
# plt.show()

# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# # Base coordinates (X+Y=2, Z=0)
# coords_base = {
#     "A": (0.0, 2.0, 0),
#     "B": (0.5, 1.5, 0),
#     "C": (1.0, 1.0, 0),
#     "D": (1.5, 0.5, 0),
#     "F": (2.0, 0.0, 0),
#     "G": (0.2, 1.8, 0),
#     "H": (1.2, 0.8, 0),
#     "I": (0.8, 1.2, 0)
# }

# # Lifted coordinates (same X,Y, Z=1)
# coords_top = {k: (x, y, 1) for k, (x, y, _) in coords_base.items()}

# nodes = list(coords_base.keys())

# # Triple constraints (pyramids)
# triangles = [
#     ("A","D","G"),
#     ("C","F","I"),
#     ("A","B","C"),
#     ("G","H","I")
# ]

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Draw base nodes
# for n,(x,y,z) in coords_base.items():
#     ax.scatter(x,y,z,color='black')
#     ax.text(x,y,z,n)

# # Draw lifted nodes
# for n,(x,y,z) in coords_top.items():
#     ax.scatter(x,y,z,color='red')
#     ax.text(x,y,z,n)

# # 1) All pairwise relations X+E+Y=3k → X+Y=2
# #    Draw edges on the base plane (Z=0)
# for i in range(len(nodes)):
#     for j in range(i+1, len(nodes)):
#         n1, n2 = nodes[i], nodes[j]
#         x1,y1,z1 = coords_base[n1]
#         x2,y2,z2 = coords_base[n2]
#         ax.plot([x1,x2],[y1,y2],[z1,z2],color='gray',alpha=0.4)

# # 2) Triple constraints → triangles at Z=1 + vertical walls
# for tri in triangles:
#     X,Y,Z = tri

#     # top triangle edges
#     for (u,v) in [(X,Y),(Y,Z),(Z,X)]:
#         x1,y1,z1 = coords_top[u]
#         x2,y2,z2 = coords_top[v]
#         ax.plot([x1,x2],[y1,y2],[z1,z2],color='red',linewidth=2)

#     # vertical edges (pyramid walls)
#     for node in tri:
#         xb,yb,zb = coords_base[node]
#         xt,yt,zt = coords_top[node]
#         ax.plot([xb,xt],[yb,yt],[zb,zt],color='black',linewidth=1)

# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# plt.show()

# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# # Coordinates satisfying X+Y=2
# coords_base = {
#     "A": (0.0, 2.0, 0),
#     "B": (0.5, 1.5, 0),
#     "C": (1.0, 1.0, 0),
#     "D": (1.5, 0.5, 0),
#     "F": (2.0, 0.0, 0),
#     "G": (0.2, 1.8, 0),
#     "H": (1.2, 0.8, 0),
#     "I": (0.8, 1.2, 0)
# }

# coords_top = {k: (x, y, 1) for k, (x, y, _) in coords_base.items()}

# # Triple constraints (pyramids)
# triangles = [
#     ("A","D","G"),
#     ("C","F","I"),
#     ("A","B","C"),
#     ("G","H","I")
# ]

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# # Draw base nodes
# for n,(x,y,z) in coords_base.items():
#     ax.scatter(x,y,z,color='black')
#     ax.text(x,y,z,n)

# # Draw lifted nodes
# for n,(x,y,z) in coords_top.items():
#     ax.scatter(x,y,z,color='red')
#     ax.text(x,y,z,n)

# # Draw pyramid edges
# for tri in triangles:
#     X,Y,Z = tri
#     # top triangle edges
#     ax.plot(
#         [coords_top[X][0], coords_top[Y][0]],
#         [coords_top[X][1], coords_top[Y][1]],
#         [coords_top[X][2], coords_top[Y][2]],
#         color='red'
#     )
#     ax.plot(
#         [coords_top[Y][0], coords_top[Z][0]],
#         [coords_top[Y][1], coords_top[Z][1]],
#         [coords_top[Y][2], coords_top[Z][2]],
#         color='red'
#     )
#     ax.plot(
#         [coords_top[Z][0], coords_top[X][0]],
#         [coords_top[Z][1], coords_top[X][1]],
#         [coords_top[Z][2], coords_top[X][2]],
#         color='red'
#     )

#     # vertical edges (pyramid walls)
#     for node in tri:
#         ax.plot(
#             [coords_base[node][0], coords_top[node][0]],
#             [coords_base[node][1], coords_top[node][1]],
#             [coords_base[node][2], coords_top[node][2]],
#             color='gray'
#         )

# plt.show()

# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# import networkx as nx

# G = nx.Graph()

# coords = {
#     "A": (1.2, 0.8, 1),
#     "B": (0.5, 1.5, 1),
#     "C": (1.4, 0.6, 1),
#     "D": (0.9, 1.1, 1),
#     "F": (1.1, 0.9, 1),
#     "G": (0.7, 1.3, 1),
#     "H": (1.3, 0.7, 1),
#     "I": (0.6, 1.4, 1)
# }

# # Add nodes
# for n, (x,y,z) in coords.items():
#     G.add_node(n, pos=(x,y,z))

# # Add pairwise edges (X+Y=2)
# nodes = list(coords.keys())
# for i in range(len(nodes)):
#     for j in range(i+1, len(nodes)):
#         G.add_edge(nodes[i], nodes[j], color='gray', weight=1)

# # Add triangle edges (X+Y+Z=3)
# triangles = [
#     ("A","D","G"),
#     ("C","F","I"),
#     ("A","B","C"),
#     ("G","H","I")
# ]

# for tri in triangles:
#     X, Y, Z = tri
#     G.add_edge(X, Y, color='red', weight=3)
#     G.add_edge(Y, Z, color='red', weight=3)
#     G.add_edge(Z, X, color='red', weight=3)

# # Draw 3D graph
# fig = plt.figure(figsize=(10,10))
# ax = fig.add_subplot(111, projection='3d')

# for node, (x,y,z) in coords.items():
#     ax.scatter(x, y, z, s=200)
#     ax.text(x, y, z, node, fontsize=12)

# for u, v in G.edges():
#     x = [coords[u][0], coords[v][0]]
#     y = [coords[u][1], coords[v][1]]
#     z = [coords[u][2], coords[v][2]]
#     color = G[u][v]['color']
#     ax.plot(x, y, z, color=color)

# ax.set_title("3D Network Graph: Pairwise (gray) and Triple (red) Constraints")
# plt.show()

# import networkx as nx
# import matplotlib.pyplot as plt

# nodes = ["A","B","C","D","F","G","H","I"]

# G = nx.Graph()
# G.add_nodes_from(nodes)

# # Add all pairwise edges (from X+E+Y=3k)
# for i in range(len(nodes)):
#     for j in range(i+1, len(nodes)):
#         G.add_edge(nodes[i], nodes[j], color='lightgray', weight=1)

# # Triangles (from X+Y+Z=3k)
# triangles = [
#     ("A","D","G"),
#     ("C","F","I"),
#     ("A","B","C"),
#     ("G","H","I")
# ]

# # Add triangle edges with special color
# for tri in triangles:
#     X, Y, Z = tri
#     G.add_edge(X, Y, color='red', weight=3)
#     G.add_edge(Y, Z, color='red', weight=3)
#     G.add_edge(Z, X, color='red', weight=3)

# # Draw
# pos = nx.spring_layout(G, seed=42)
# edges = G.edges()
# colors = [G[u][v]['color'] for u,v in edges]
# weights = [G[u][v]['weight'] for u,v in edges]

# plt.figure(figsize=(10,10))
# nx.draw(G, pos, with_labels=True, edge_color=colors, width=weights,
#         node_size=1500, font_size=20)
# plt.title("Network Graph with Pairwise Constraints and Triangle Constraints")
# plt.show()

# import networkx as nx
# import matplotlib.pyplot as plt

# nodes = ["A","B","C","D","F","G","H","I"]

# G = nx.Graph()
# G.add_nodes_from(nodes)

# # Add edges with correct label X+Y=2
# for i in range(len(nodes)):
#     for j in range(i+1, len(nodes)):
#         X = nodes[i]
#         Y = nodes[j]
#         G.add_edge(X, Y, label="2")

# pos = nx.spring_layout(G, seed=42)

# plt.figure(figsize=(8,8))
# nx.draw(G, pos, with_labels=True, node_size=1500, font_size=16)

# edge_labels = {(u, v): "2" for u, v in G.edges()}
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)

# plt.title("Network Graph for X + E + Y = 3k with E=1, k=1 → X+Y=2")
# plt.axis("off")
# plt.show()

# import networkx as nx
# import matplotlib.pyplot as plt

# # Nodes from your equations
# nodes = ["A","B","C","D","F","G","H","I"]

# G = nx.Graph()
# G.add_nodes_from(nodes)

# # Add an edge between every pair (complete graph)
# for i in range(len(nodes)):
#     for j in range(i+1, len(nodes)):
#         X = nodes[i]
#         Y = nodes[j]
#         G.add_edge(X, Y, label="X+E+Y=3k")

# # Layout and draw
# pos = nx.spring_layout(G, seed=42)

# plt.figure(figsize=(8,8))
# nx.draw(G, pos, with_labels=True, node_size=1500, font_size=16)

# # Optional: show edge labels
# edge_labels = {(u, v): "3k" for u, v in G.edges()}
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)

# plt.title("Network Graph for X + E + Y = 3k")
# plt.axis("off")
# plt.show()



# import networkx as nx
# import matplotlib.pyplot as plt

# # Nodes
# nodes = ["A","B","C","D","F","G","H","I"]

# # Build graph
# G = nx.Graph()
# G.add_nodes_from(nodes)

# # Add edges
# for i in range(len(nodes)):
#     for j in range(i+1, len(nodes)):
#         X = nodes[i]
#         Y = nodes[j]

#         # Special edges: any edge involving B is 3K
#         if X == "B" or Y == "B":
#             G.add_edge(X, Y, color='red', weight=2)
#         else:
#             G.add_edge(X, Y, color='blue', weight=1)

# # Draw graph
# pos = nx.spring_layout(G, seed=42)
# edges = G.edges()
# colors = [G[u][v]['color'] for u,v in edges]
# weights = [G[u][v]['weight'] for u,v in edges]

# plt.figure(figsize=(10,10))
# nx.draw(G, pos, with_labels=True, edge_color=colors, width=weights, node_size=1500, font_size=20)
# plt.title("Network Graph of X + E + Y = 3k / 3K")
# plt.show()
