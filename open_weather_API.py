import json

import requests, os
import requests.cookies
from dotenv import load_dotenv


load_dotenv()
api = os.getenv("api_key")
city = input().capitalize()
lat, lon = 0, 0
url_geo = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api}"
url_weather = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api}"
# &exclude={part}
try:
    response = requests.get(url=url_geo)
    response.raise_for_status()
    lat, lon = response.json()[0]["lat"], response.json()[0]["lon"]
    resp = requests.get(url=url_weather)
    print("Enter the period please: current, daily or hourly\n")
    period = input()
    data = resp.json()[period]
    print(json.dumps(data, indent=2))
except requests.exceptions.RequestException as err:
    print(f"Response error {err}")
except KeyError as er:
    print(f"Key error {er}")