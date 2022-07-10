from geopy.geocoders import GoogleV3
from geopy import distance
import os
geolocator = GoogleV3(api_key=os.environ['API_KEY'],domain="maps.google.com.sg")
pcs = [546080,308215,238858,48508,48542,570150,521147]
locations = [geolocator.geocode({"country":"Singapore","postalcode":i}) for i in pcs]
for i in range(len(locations)):
    for j in range(i+1,len(locations)):
        print(f"Distance between {locations[i].address} and {locations[j].address}: {distance.distance(locations[i].point,locations[j].point)}")
