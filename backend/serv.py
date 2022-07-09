import httpx

accounts = 

headers = {
    "Host": "haveibeenpwned.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "https://haveibeenpwned.com/",
    "X-Requested-With": "XMLHttpRequest",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Te": "trailers"
}

c = httpx.Client(http2=True)

for acc in accounts:
    url = f"https://haveibeenpwned.com/unifiedsearch/{acc}"
    r = c.get(url,headers=headers)
    if r.status_code == 404:
        print(f"{acc} is safe")
    elif r.status_code == 200:
        print(f"{acc} is in a breach")
        for br in r.json()["Breaches"]:
            print(f"\tBreached in {br['Name']} on {br['BreachDate']}")
    else:
        print("probably blocked rip")
        print(r.status_code)
        print(r.text)

