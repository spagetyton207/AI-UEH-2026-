import folium
from folium.plugins import HeatMap
import numpy as np
import pandas as pd

center = geolocator.geocode("Đại học Kinh tế TP.HCM, Hồ Chí Minh")
center_lat, center_lon = center.latitude, center.longitude


#tạo data giả định
lats = center_lat + np.random.normal(0, 0.005, 100)
lons = center_lon + np.random.normal(0, 0.005, 100)
df_orders = pd.DataFrame({'lat': lats, 'lon': lons})
heat_data = [[row['lat'], row['lon']] for index, row in df_orders.iterrows()]


m = folium.Map([center_lat, center_lon], tiles='CartoDB positron')

HeatMap(data=heat_data).add_to(m)
m
