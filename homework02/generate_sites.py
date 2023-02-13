import json
import random


sites_dict = {"sites":[]}

for i in range(5):
    latitude = 16 + 2*random.random()
    longitude = 82 + 2*random.random()
    composition = random.choice(["stony","iron","stony-iron"])
    id = i + 1
    sites_dict["sites"].append({"site_id": id,
                                "latitude": latitude, 
                                "longitude": longitude,
                                "composition": composition})

print(sites_dict)

with open('meteorite_sites.json', 'w') as out:
   json.dump(sites_dict, out, indent=2)

# with open("/home/mihiro10/coe-332/homework02/meteorite_sites.json", "w") as out:
#     json.dump(sites_dict, out, indent=2)


