import osmnx as ox
import networkx as nx
import time
#lưu ý: đây chỉ là giả lập, chưa tính tới đường một chiều hoặc lưu lượng giao thông
G = ox.graph_from_place("District 3, Ho Chi Minh City, Vietnam", network_type='drive')
G_projected = ox.project_graph(G)

start_lat_lon = (10.7827, 106.6958) # Hồ Con Rùa
end_lat_lon = (10.7821, 106.6778)   # Ga Sài Gòn

#đoạn này để tìm được node gần nhất với toạ độ cho trước
orig_node = ox.distance.nearest_nodes(G, start_lat_lon[1], start_lat_lon[0])  #hàm này sử dụng toạ độ Oxy nên phải đảo kinh độ và vĩ độ
dest_node = ox.distance.nearest_nodes(G, end_lat_lon[1], end_lat_lon[0])


#mặc định thì hàm này sử dụng thuật toán djikstra
start_time = time.time()
dji_route = nx.shortest_path(G_projected, orig_node, dest_node, weight='length')
dijkstra_time = time.time() - start_time
#bfs
bfs_route = nx.shortest_path(G_projected, orig_node, dest_node)

#nếu không có truyền vào hàm heuristic cho astar thì nó sẽ sử dụng dijkstra
def heuristic(u, v):
    node_u = G_projected.nodes[u]
    node_v = G_projected.nodes[v]
    return ((node_u['x'] - node_v['x'])**2 + (node_u['y'] - node_v['y'])**2)**0.5

#em sử dụng time để tính thời gian xử lí của 2 thuật toán tìm đường ngắn nhất
start_time = time.time()
a_star_route = nx.astar_path(G_projected, orig_node, dest_node, weight = 'length', heuristic = heuristic)
astar_time = time.time() - start_time

fig, ax = ox.plot_graph_route(G_projected, dji_route, node_size=5)
fig, ax = ox.plot_graph_route(G_projected, bfs_route, node_size=5)
fig, ax = ox.plot_graph_route(G_projected, a_star_route, node_size=5)

print(f"{dijkstra_time:.6f}")
print(f"{astar_time:.6f}")

#kết quả cho thấy 2 thuật toán tìm đường đi ngắn nhất có kèm trọng số là a* và dijkstra cho 2 kết quả giống nhau
#còn thuật toán bfs search cho kết quả khác vì nó chỉ cho ra đường đi có số lượng cạnh ít nhất 
#nhìn về tốc độ xử lí thì a* vượt trội hơn so với dijkstra
