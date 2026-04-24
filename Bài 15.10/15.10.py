import osmnx as ox
import networkx as nx
import random
import folium
import numpy as np
from shapely.geometry import LineString


G = ox.graph_from_place("District 3, Ho Chi Minh City, Vietnam", network_type="drive", simplify=True)

G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)


def simulate_traffic_data(G):
    for u, v, k, data in G.edges(keys=True, data=True):
        road_length = data.get("length", 100)

        data["vehicle_count"] = random.randint(20, 300)
        data["avg_speed"] = random.uniform(5, 50)
        data["accident_rate"] = random.uniform(0, 1)
        data["peak_hour"] = random.choice([0, 1])

        density = data["vehicle_count"] / max(road_length, 1)

        data["traffic_density"] = density

    return G


G = simulate_traffic_data(G)

def fuzzy_congestion_score(vehicle_count, avg_speed, accident_rate, peak_hour):


    # Mức độ đông xe
    if vehicle_count < 80:
        density_score = 20
    elif vehicle_count < 180:
        density_score = 60
    else:
        density_score = 90

    if avg_speed > 35:
        speed_score = 20
    elif avg_speed > 20:
        speed_score = 55
    else:
        speed_score = 90

    accident_score = accident_rate * 100

    peak_score = 80 if peak_hour == 1 else 20

    risk_score = density_score * 0.35 + speed_score * 0.35 + accident_score * 0.20 + peak_score * 0.10

    return risk_score


def classify_risk(score):
    if score < 40:
        return "low"
    elif score < 70:
        return "medium"
    else:
        return "high"


for u, v, k, data in G.edges(keys=True, data=True):
    score = fuzzy_congestion_score(
        data["vehicle_count"],
        data["avg_speed"],
        data["accident_rate"],
        data["peak_hour"]
    )

    data["risk_score"] = score
    data["risk_level"] = classify_risk(score)
    data["risk_cost"] = data["length"] * (1 + score / 50)


origin_point = (10.7829, 106.6846)    
destination_point = (10.7757, 106.7004) 

origin_node = ox.distance.nearest_nodes(G, origin_point[1], origin_point[0])

destination_node = ox.distance.nearest_nodes(G,destination_point[1],destination_point[0])



route_shortest = ox.shortest_path(
    G,
    origin_node,
    destination_node,
    weight="length"
)

route_safe = ox.shortest_path(
    G,
    origin_node,
    destination_node,
    weight="risk_cost"
)


def get_route_coords(G, route):
    coords = []

    for u, v in zip(route[:-1], route[1:]):
        edge_data = G.get_edge_data(u, v)

        if edge_data is None:
            continue

        first_edge = list(edge_data.values())[0]

        if "geometry" in first_edge:
            xs, ys = first_edge["geometry"].xy
            coords.extend(list(zip(ys, xs)))
        else:
            y1 = G.nodes[u]["y"]
            x1 = G.nodes[u]["x"]
            y2 = G.nodes[v]["y"]
            x2 = G.nodes[v]["x"]
            coords.extend([(y1, x1), (y2, x2)])

    return coords


center_lat = (origin_point[0] + destination_point[0]) / 2
center_lon = (origin_point[1] + destination_point[1]) / 2

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=15,
    tiles="cartodbpositron"
)


def get_edge_color(risk_level):
    if risk_level == "low":
        return "green"
    elif risk_level == "medium":
        return "orange"
    else:
        return "red"


for u, v, k, data in G.edges(keys=True, data=True):
    risk_level = data["risk_level"]
    color = get_edge_color(risk_level)

    if "geometry" in data:
        xs, ys = data["geometry"].xy
        locations = list(zip(ys, xs))
    else:
        locations = [
            [G.nodes[u]["y"], G.nodes[u]["x"]],
            [G.nodes[v]["y"], G.nodes[v]["x"]]
        ]

    folium.PolyLine(
        locations=locations,
        color=color,
        weight=3 if risk_level == "high" else 2,
        opacity=0.55
    ).add_to(m)



shortest_coords = get_route_coords(G, route_shortest)
safe_coords = get_route_coords(G, route_safe)

folium.PolyLine(
    locations=shortest_coords,
    color="blue",
    weight=6,
    opacity=0.8,
    tooltip="Tuyến ngắn nhất"
).add_to(m)

folium.PolyLine(
    locations=safe_coords,
    color="purple",
    weight=6,
    opacity=0.9,
    tooltip="Tuyến đề xuất tránh tắc nghẽn"
).add_to(m)



folium.Marker(
    location=origin_point,
    popup="Điểm xuất phát",
    icon=folium.Icon(color="green", icon="play")
).add_to(m)

folium.Marker(
    location=destination_point,
    popup="Điểm đến",
    icon=folium.Icon(color="red", icon="flag")
).add_to(m)

m

