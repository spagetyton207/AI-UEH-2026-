import osmnx as ox
import networkx as nx
import random
import matplotlib.pyplot as plt
import pandas as pd
from shapely.geometry import Point
from scipy.optimize import linear_sum_assignment
from sklearn.cluster import KMeans
import numpy as np

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

customers = generate_entities_on_edges(G_projected, n=100, entity_type='customer')


k = 5

customer_coords = np.array([[c["x"], c["y"]] for c in customers])

kmeans = KMeans(n_clusters=k)

labels = kmeans.fit_predict(customer_coords)
centroids = kmeans.cluster_centers_

for i, c in enumerate(customers):
    c["cluster"] = labels[i]

representative_points = []

for cluster_id in range(k):
    cluster_customers = [c for c in customers if c["cluster"] == cluster_id]
    centroid = centroids[cluster_id] 
    nearest_customer = min(cluster_customers,key=lambda c: np.linalg.norm(np.array([c["x"], c["y"]]) - centroid))
    representative_points.append(nearest_customer)

fig, ax = ox.plot_graph(
G_projected,
node_size=0,
show=False,
close=False
)


customer_x = [c["x"] for c in customers]
customer_y = [c["y"] for c in customers]

ax.scatter(
    customer_x,
    customer_y,
    c=labels,             
    s=30,
)
rep_x = [p["x"] for p in representative_points]
rep_y = [p["y"] for p in representative_points]

ax.scatter(
    rep_x,
    rep_y,
    c="yellow",
    edgecolors="red",
    s=50,
    label="điểm đặt kho tối ưu",
)

ax.legend()
plt.show()

#lí do em chọn điểm đặt kho tại điểm cùa khách hàng gần trung tâm nhất để đảm bảo chỗ đó có tồn tại đường hoặc vị trí
