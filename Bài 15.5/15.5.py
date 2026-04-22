import folium
center_cor = [10.7828, 106.6959]
m = folium.Map(center_cor, zoom_start=13, tiles='CartoDB positron')

folium.Marker(center_cor, popup="Kho hàng trung tâm",).add_to(m)

service_zones = [
    {"radius": 500, "color": "green", "fill": "#green", "note":"3km"},
    {"radius": 1000, "color": "orange", "fill": "orange", "note": "5km"},
    {"radius": 1500, "color": "red", "fill": "red", "note": "10km"}
]

for zone in service_zones:
    folium.Circle(center_cor, radius=zone["radius"], color=zone["color"], fill_color=zone["fill"], popup=zone["note"]).add_to(m)
m
