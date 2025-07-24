def fetch_tat_data():
    import requests
    r = requests.get("https://tatapi.tourismthailand.org/api/tourism/v1/attraction")
    if r.ok:
        print("Data:", r.json())
    else:
        print("Fetch failed")
