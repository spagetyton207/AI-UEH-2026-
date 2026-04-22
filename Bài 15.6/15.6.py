import osmnx as ox
import matplotlib.pyplot as plt

G = ox.graph_from_place("District 3, Ho Chi Minh city, Vietnam", network_type='drive')

G_projected = ox.project_graph(G)

fig, ax = ox.plot_graph(G_projected, node_size=3, node_color = 'red')
plt.show()
thong_so = ox.basic_stats(G_projected)
print(f"Số lượng nút giao: {thong_so['n']}")
print(f"Số lượng đoạn đường: {thong_so['m']}")
print(f"Tổng chiều dài đường: {thong_so['edge_length_total']}")
print(f"Chiều dài đường trung bình: {thong_so['edge_length_avg']}")
