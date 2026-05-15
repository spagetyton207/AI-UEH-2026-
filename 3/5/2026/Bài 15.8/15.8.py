import osmnx as ox
import networkx as nx
import random
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
from scipy.optimize import linear_sum_assignment

G = ox.graph_from_place("District 3, Ho Chi Minh City, Vietnam", network_type='walk')
G_projected = ox.project_graph(G)

nx.set_node_attributes(G_projected, 'intersection', 'node_type')


#hàm này em sử dụng AI để có thể tạo được data sample
def generate_entities_on_edges(graph, n, entity_type):
    entities = []
    edges = list(graph.edges(data=True))

    for i in range(n):
        u, v, data = random.choice(edges)


        nodes_data = graph.nodes
        t = random.random()
        point = Point(
            nodes_data[u]['x'] + (nodes_data[v]['x'] - nodes_data[u]['x']) * t,
            nodes_data[u]['y'] + (nodes_data[v]['y'] - nodes_data[u]['y']) * t
        )

        entities.append({
            "id": f"{entity_type}_{i}",
            "x": point.x,
            "y": point.y,
            "type": entity_type
        })

    return entities

customers = generate_entities_on_edges(G_projected, n=10, entity_type='customer')
vehicles = generate_entities_on_edges(G_projected, n=50, entity_type='vehicle')

length_matrix = []

for v in vehicles:
    temp_row = []
    for c in customers:
        try:
            c_node = ox.distance.nearest_nodes(G_projected, c["x"], c["y"])
            v_node = ox.distance.nearest_nodes(G_projected, v["x"], v["y"])

            dist = nx.shortest_path_length(
                G_projected,
                source=v_node,
                target=c_node,
                weight="length"
            )
            temp_row.append(dist)

        except nx.NetworkXNoPath:
            temp_row.append(float("inf"))

    length_matrix.append(temp_row)
row_i, column_i = linear_sum_assignment(length_matrix)
print(row_i)
print(column_i)
df_matrix = pd.DataFrame(
    length_matrix,
    index=[v["id"] for v in vehicles],
    columns=[c["id"] for c in customers]
)
display(df_matrix)
    

fig, ax = ox.plot_graph(
    G_projected,
    node_size=0,
    edge_linewidth=0.5,
    edge_color="green",
    show=False,
    close=False
)

all_route = []

for i in range(len(row_i)):
    v = vehicles[row_i[i]]
    c = customers[column_i[i]]

    v_node = ox.distance.nearest_nodes(G_projected, v["x"], v["y"])
    c_node = ox.distance.nearest_nodes(G_projected, c["x"], c["y"])

    route = ox.shortest_path(G_projected, v_node, c_node, weight="length")

    if route is not None:
        all_route.append(route)

fig, ax = ox.plot_graph_routes(
    G_projected,
    all_route,
    ax=ax,
    node_size=0,
    show=False,
    close=False
)

customer_x = [c["x"] for c in customers]
customer_y = [c["y"] for c in customers]
vehicle_x = [v["x"] for v in vehicles]
vehicle_y = [v["y"] for v in vehicles]

ax.scatter(customer_x, customer_y, c="blue", s=30, label="customers", zorder=5)
ax.scatter(vehicle_x, vehicle_y, c="orange", s=50, label="vehicles", zorder=6)

ax.legend()
plt.show()


