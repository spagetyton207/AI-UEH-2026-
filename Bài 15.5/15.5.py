import folium

center_lat, center_lon = 10.7828, 106.6959 

m = folium.Map([center_lat, center_lon], zoom_start=13, tiles='CartoDB positron')

folium.Marker( [center_lat, center_lon], popup="Kho hàng trung tâm",).add_to(m)

service_zones = [
    {"radius": 500, "color": "green", "fill": "#green", "note": "Vùng 1: Ưu tiên (3km)"},
    {"radius": 1000, "color": "#f39c12", "fill": "#f39c12", "note": "Vùng 2: Tiêu chuẩn (5km)"},
    {"radius": 1500, "color": "#e74c3c", "fill": "#e74c3c", "note": "Vùng 3: Mở rộng (10km)"}
]

for zone in reversed(service_zones):
    folium.Circle([center_lat, center_lon],
        radius=zone["radius"],
        color=zone["color"],
        weight=2,
        fill=True,
        fill_color=zone["fill"],
        fill_opacity=0.1,
        popup=zone["note"]
    ).add_to(m)

m
