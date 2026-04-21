from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import time 
import folium

geolocator = Nominatim(user_agent="my_mapping_app_123",timeout = 10)

dia_chi = [
    "Nhà ga T3 Sân bay Tân Sơn Nhất",
    "Bệnh viện Chợ Rẫy",
    "Vạn Hạnh Mall",
    "Chợ Bến Thành",
    "Toà nhà Bitexco",
    "Nhà thi đấu Phú Thọ",
    "Nhà hát Thành phố",
    "Nhà hát Hoà Bình",
    "Landmark 81"

]
center = geolocator.geocode("Đại học Kinh tế TP.HCM, Hồ Chí Minh")

results = []

for dc in dia_chi:
    location = geolocator.geocode(f"{dc}, Hồ Chí Minh")
    
    if location:
        results.append(location)
    time.sleep(1) #quá nhiều request mỗi giây sẽ gây nên em giới hạn 1 request/ giây

m = folium.Map([center.latitude,center.longitude], tiles="CartoDB positron", zoom_start=14)
folium.Marker([center.latitude, center.longitude], popup = center.address).add_to(m)


for tmp in results:
    distance = geodesic([tmp.latitude,tmp.longitude],[center.latitude,center.longitude])
    folium.Marker([tmp.latitude, tmp.longitude], popup = tmp.address).add_to(m)
    folium.PolyLine([[tmp.latitude,tmp.longitude],[center.latitude,center.longitude]], tooltip = f"{distance.km} km").add_to(m) #hiển thi chiều dài bằng tooltip
m

