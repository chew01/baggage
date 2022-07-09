from geopy.geocoders import Nominatim
from geopy import distance
geolocator = Nominatim(user_agent="baggage-backend")
pcs = [569933,310145,520147,570150]
locations = [geolocator.geocode({"country":"Singapore","postalcode":i}) for i in pcs]
for i in range(len(locations)):
    for j in range(i+1,len(locations)):
        print(f"Distance between {locations[i].address} and {locations[j].address}: {distance.distance(locations[i].point,locations[j].point)}")
