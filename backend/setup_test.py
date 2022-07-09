import requests
import random

pcl = [310145, 650145, 650147, 650146, 569933, 310223, 650160, 520147, 521147]
pcd = {}
for n,p in []:#enumerate(pcl):
    r = requests.get("http://127.0.0.1:8000/user/create",params={
        "username":f"testUser{n}",
        "password":"password",
        "postal_code":p,
        "unit_number":f"{p%47}-{p%789}"
        })
    print(r.json())
    pcd[p] = r.json()["id"]

pcd = {310145: '62c9c64af9478e818bba151d', 650145: '62c9c64af9478e818bba151e', 650147: '62c9c64bf9478e818bba151f', 650146: '62c9c64bf9478e818bba1520', 569933: '62c9c64cf9478e818bba1521', 310223: '62c9c64cf9478e818bba1522', 650160: '62c9c64df9478e818bba1523', 520147: '62c9c64df9478e818bba1524', 521147: '62c9c64ef9478e818bba1525'}

items = {}

for n,p in enumerate(pcl):
    items[p] = []
    for i in range(10):
        r = requests.get("http://127.0.0.1:8000/item/add",params={
            "user_id":pcd[p],
            "name":f"item{n}.{i}",
            "expiry":random.randint(1657400000,1660000000),
            "quantity":random.randint(1,100)
            })
        items[p].append(r.json()["item_id"])

for n,p in enumerate(pcl):
    for i in set(items[p][random.randint(0,9)] for _ in range(5)):
        r = requests.get("http://127.0.0.1:8000/item/listingAccept",params={
            "user_id":pcd[pcl[(lambda t:t if t<n else t+1)(random.randint(0,len(pcl)-2))]],
            "item_id":i
            })
