import folium
import geopandas as gpd
import pandas as pd
file_name = "vietnam.geojson" 
gdf_hcm = gpd.read_file(file_name)
data = {
    'name': ['Hồ Chí Minh city', 'Bình Dương', 'Đồng Nai', 'Bà Rịa - Vũng Tàu', 'Hà Nội', 'Đà Nẵng'],
    'doanh_thu': [956, 700, 800, 600, 580, 620]
}
df_data = pd.DataFrame(data)

merged = gdf_hcm.merge(df_data, on='name', how='left') #join left để không bị mất dữ liệu

m = folium.Map([16, 110], zoom_start=6, tiles='CartoDB positron')

folium.Choropleth(
    geo_data=merged,          
    data=merged,                
    columns=["name", "doanh_thu"], 
    key_on="feature.properties.name",
    legend_name="Doanh thu theo tỷ đồng",
    nan_fill_color="white",
    fill_color="YlOrRd"
).add_to(m)

m
